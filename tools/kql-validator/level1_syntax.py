"""Level 1 KQL syntax validation.

Structural checks on KQL query files: unbalanced delimiters, SQL keyword
contamination, pipe structure violations, header comment conventions.
No external dependencies required.
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from . import kql_tables

# -- Data model --------------------------------------------------------------

@dataclass
class ValidationIssue:
    line: int
    column: int
    severity: str  # "error" or "warning"
    code: str
    message: str
    suggestion: str = ""

@dataclass
class ValidationResult:
    file: str
    level: int
    status: str  # "PASS", "WARN", "FAIL"
    errors: list[ValidationIssue] = field(default_factory=list)
    warnings: list[ValidationIssue] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = {"file": self.file, "level": self.level, "status": self.status,
             "errors": [_issue_dict(i) for i in self.errors],
             "warnings": [_issue_dict(i) for i in self.warnings]}
        return d

def _issue_dict(issue: ValidationIssue) -> dict:
    d = {"line": issue.line, "column": issue.column, "severity": issue.severity,
         "code": issue.code, "message": issue.message}
    if issue.suggestion:
        d["suggestion"] = issue.suggestion
    return d

# -- Constants ----------------------------------------------------------------

KQL_OPERATORS = {
    "where", "project", "project-away", "project-keep", "project-rename",
    "project-reorder", "extend", "summarize", "join", "union", "let",
    "count", "distinct", "sort", "order", "top", "take", "limit",
    "render", "mv-expand", "mv-apply", "parse", "parse-where", "evaluate",
    "make-series", "search", "print", "invoke", "lookup", "as", "consume",
    "fork", "facet", "getschema", "sample", "sample-distinct", "serialize",
    "range",
}
PIPE_OPERATORS = KQL_OPERATORS - {"let", "union"}

SQL_SINGLE_KEYWORDS = {"SELECT": "project", "FROM": "(use table name directly)",
                        "LIKE": "has / contains / matches regex"}
SQL_LOGICAL_OPS = {"AND": "and", "OR": "or", "NOT": "not", "WHERE": "where (with | prefix)"}

TRR_PATTERN = re.compile(r"TRR\d{4}")
DDM_NODE_PATTERN = re.compile(r"\bn\d+\b")
AGO_STRING_PATTERN = re.compile(r"\bago\(\s*([\"'])")

# -- Text utilities -----------------------------------------------------------

def _remove_strings_and_comments(line: str) -> str:
    """Replace string contents and // comments with spaces, keeping positions."""
    out = list(line)
    in_str, sch = False, ""
    i = 0
    while i < len(out):
        c = out[i]
        if in_str:
            if c == "\\" and i + 1 < len(out):
                out[i] = out[i + 1] = " "; i += 2; continue
            if c == sch: in_str = False
            out[i] = " "
        else:
            if c in ('"', "'"):
                in_str, sch = True, c; out[i] = " "
            elif c == "/" and i + 1 < len(out) and out[i + 1] == "/":
                for j in range(i, len(out)): out[j] = " "
                break
        i += 1
    return "".join(out)

def _strip_inline_comment(line: str) -> str:
    """Remove trailing // comment, respecting string literals."""
    in_str, sch = False, ""
    i = 0
    while i < len(line):
        c = line[i]
        if in_str:
            if c == "\\" and i + 1 < len(line): i += 2; continue
            if c == sch: in_str = False
        else:
            if c in ('"', "'"): in_str, sch = True, c
            elif c == "/" and i + 1 < len(line) and line[i + 1] == "/":
                return line[:i]
        i += 1
    return line

def _first_word(line: str) -> str | None:
    m = re.match(r"([A-Za-z_][\w-]*)", line)
    return m.group(1) if m else None

# -- Query block model --------------------------------------------------------

@dataclass
class QueryBlock:
    lines: list[tuple[int, str]]   # (1-based line number, raw text)
    start_line: int
    table_name: str = ""

def _split_query_blocks(text: str) -> list[QueryBlock]:
    """Split KQL text into query blocks at ; boundaries.

    Let bindings ending with ; are grouped with the query that uses them
    when the next meaningful code line is another let or a table name.
    """
    raw_lines = text.split("\n")
    blocks: list[QueryBlock] = []
    cur: list[tuple[int, str]] = []
    in_let = False

    def _flush():
        nonlocal cur, in_let
        if cur:
            blocks.append(_make_block(cur))
            cur, in_let = [], False

    def _peek_code(start: int) -> str | None:
        """Next non-empty line from start."""
        for j in range(start, len(raw_lines)):
            if raw_lines[j].strip(): return raw_lines[j].strip()
        return None

    def _peek_non_comment(start: int) -> str | None:
        """Next non-empty, non-comment line from start."""
        for j in range(start, len(raw_lines)):
            s = raw_lines[j].strip()
            if s and not s.startswith("//"): return s
        return None

    for idx, raw in enumerate(raw_lines):
        ln = idx + 1
        stripped = raw.strip()
        if not stripped and not cur: continue
        if stripped.startswith("//") and not cur: continue
        cur.append((ln, raw))
        if stripped.startswith("let "): in_let = True

        content = _strip_inline_comment(stripped).rstrip()
        if not content.endswith(";"): continue

        if not in_let:
            _flush(); continue

        # Let statement ended with ;. Decide: is the next code a continuation
        # (the query using this let) or a new block?
        nxt = _peek_code(idx + 1)
        if nxt is None:
            _flush(); continue
        if nxt.startswith("let "):
            continue  # another let, keep accumulating
        if nxt.startswith("//"):
            # Check if this comment is a new TRR header
            if TRR_PATTERN.search(nxt):
                _flush(); continue
            # Non-header comment; check what code follows
            code_after = _peek_non_comment(idx + 1)
            if code_after and (code_after.startswith("let ") or _looks_like_table(code_after)):
                continue  # continuation
            _flush(); continue
        if _looks_like_table(nxt):
            continue  # query using the let binding
        _flush()

    _flush()
    return blocks

def _looks_like_table(line: str) -> bool:
    s = line.strip()
    if not s or s.startswith("//") or s.startswith("|"): return False
    w = _first_word(s)
    return bool(w) and w.lower() not in PIPE_OPERATORS

def _make_block(lines: list[tuple[int, str]]) -> QueryBlock:
    block = QueryBlock(lines=lines, start_line=lines[0][0] if lines else 0)
    for _, raw in lines:
        s = raw.strip()
        if not s or s.startswith("//") or s.startswith("let ") or s.startswith("|"):
            continue
        m = re.match(r"([A-Za-z_]\w*)", s)
        if m: block.table_name = m.group(1)
        break
    return block

# -- Checks -------------------------------------------------------------------

def _check_delimiters(lines: list[str]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    paren_stack: list[tuple[int, int]] = []
    bracket_stack: list[tuple[int, int]] = []

    for ln0, raw in enumerate(lines):
        ln = ln0 + 1
        in_str, sch, in_cmt = False, "", False
        str_start = 0
        i = 0
        while i < len(raw):
            c = raw[i]; col = i + 1
            if in_cmt: break
            if in_str:
                if c == "\\" and i + 1 < len(raw): i += 2; continue
                if c == sch: in_str = False
            else:
                if c == "/" and i + 1 < len(raw) and raw[i + 1] == "/": break
                if c in ('"', "'"): in_str, sch, str_start = True, c, col
                elif c == "(": paren_stack.append((ln, col))
                elif c == ")":
                    if paren_stack: paren_stack.pop()
                    else: issues.append(ValidationIssue(ln, col, "error", "L1-DELIM-002",
                        "Unmatched closing parenthesis", "Remove extra ')' or add matching '('"))
                elif c == "[": bracket_stack.append((ln, col))
                elif c == "]":
                    if bracket_stack: bracket_stack.pop()
                    else: issues.append(ValidationIssue(ln, col, "error", "L1-DELIM-004",
                        "Unmatched closing bracket", "Remove extra ']' or add matching '['"))
            i += 1
        if in_str:
            issues.append(ValidationIssue(ln, str_start, "error", "L1-DELIM-005",
                f"Unclosed string literal (opened with {sch})", f"Add closing {sch}"))

    for ln, col in paren_stack:
        issues.append(ValidationIssue(ln, col, "error", "L1-DELIM-001",
            f"Unclosed parenthesis opened at line {ln}, column {col}", "Add closing parenthesis"))
    for ln, col in bracket_stack:
        issues.append(ValidationIssue(ln, col, "error", "L1-DELIM-003",
            f"Unclosed bracket opened at line {ln}, column {col}", "Add closing bracket"))
    return issues


def _check_sql_keywords(lines: list[str]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for ln0, raw in enumerate(lines):
        ln = ln0 + 1
        if raw.strip().startswith("//"): continue
        content = _remove_strings_and_comments(raw)
        for kw, fix in SQL_SINGLE_KEYWORDS.items():
            for m in re.finditer(r"\b" + kw + r"\b", content):
                issues.append(ValidationIssue(ln, m.start() + 1, "error", "L1-KEYWORD-001",
                    f"SQL keyword '{kw}' is not valid KQL", f"Use '{fix}' instead"))
        for op, fix in SQL_LOGICAL_OPS.items():
            for m in re.finditer(r"\b" + op + r"\b", content):
                code = "L1-KEYWORD-001" if op == "WHERE" else "L1-KEYWORD-002"
                msg = (f"SQL keyword '{op}' is not valid KQL" if op == "WHERE"
                       else f"SQL logical operator '{op}' used instead of KQL '{fix}'")
                sug = f"Use '| where' instead" if op == "WHERE" else f"Replace '{op}' with '{fix}'"
                issues.append(ValidationIssue(ln, m.start() + 1, "error", code, msg, sug))
        for pat, kw, fix in [(r"\bGROUP\s+BY\b", "GROUP BY", "summarize"),
                              (r"\bORDER\s+BY\b", "ORDER BY", "sort by")]:
            for m in re.finditer(pat, content):
                issues.append(ValidationIssue(ln, m.start() + 1, "error", "L1-KEYWORD-001",
                    f"SQL keyword '{kw}' is not valid KQL", f"Use '{fix}' instead"))
    return issues


def _check_ago_format(lines: list[str]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for ln0, raw in enumerate(lines):
        if raw.strip().startswith("//"): continue
        for m in AGO_STRING_PATTERN.finditer(raw):
            issues.append(ValidationIssue(ln0 + 1, m.start() + 1, "error", "L1-FUNC-001",
                "ago() takes a timespan literal, not a string",
                'Use ago(24h) instead of ago("24h")'))
    return issues


def _check_trailing_pipe(lines: list[str]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for ln0, raw in enumerate(lines):
        stripped = raw.strip()
        if not stripped or stripped.startswith("//"): continue
        content = _strip_inline_comment(stripped).rstrip()
        if content != "|" and not content.endswith("|"): continue
        # Look ahead for continuation
        has_next = False
        for j in range(ln0 + 1, len(lines)):
            ns = lines[j].strip()
            if ns and not ns.startswith("//"): has_next = True; break
        if not has_next:
            issues.append(ValidationIssue(ln0 + 1, raw.rindex("|") + 1, "error",
                "L1-STRUCT-001", "Trailing pipe with no operator",
                "Add an operator after '|' or remove the trailing pipe"))
    return issues


def _check_table_name(block: QueryBlock) -> list[ValidationIssue]:
    if not block.table_name: return []
    if not any(l.strip() and not l.strip().startswith("//") for _, l in block.lines):
        return []
    if block.table_name in kql_tables.ALL_KNOWN_TABLES: return []
    if block.table_name.lower() in KQL_OPERATORS | {"union"}: return []
    for orig_ln, raw in block.lines:
        s = raw.strip()
        if not s or s.startswith("//") or s.startswith("let ") or s.startswith("|"):
            continue
        col = raw.find(block.table_name) + 1
        return [ValidationIssue(orig_ln, max(col, 1), "warning", "L1-TABLE-001",
            f"Table '{block.table_name}' not in known table list",
            "Verify table exists in your environment. "
            "Level 2 validation will check against the environment profile.")]
    return []


def _check_pipe_structure(block: QueryBlock) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    seen_first = False
    for orig_ln, raw in block.lines:
        stripped = raw.strip()
        if not stripped or stripped.startswith("//"): continue
        content = _strip_inline_comment(stripped).strip()
        if not content: continue
        if content.startswith("let "): seen_first = True; continue
        if not seen_first:
            seen_first = True
            w = _first_word(content)
            if w and w.lower() in PIPE_OPERATORS:
                issues.append(ValidationIssue(orig_ln, 1, "error", "L1-PIPE-001",
                    f"Operator '{w}' without preceding pipe or table name",
                    f"Add '| ' before '{w}' or add a table name"))
            continue
        if content.startswith("|"): continue
        w = _first_word(content)
        if w and w.lower() in PIPE_OPERATORS:
            col = raw.find(w) + 1
            issues.append(ValidationIssue(orig_ln, max(col, 1), "error", "L1-PIPE-001",
                f"Operator '{w}' must be preceded by '|'",
                f"Add '| ' before '{w}'"))
    return issues


def _check_assignment_in_where(block: QueryBlock) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    in_where = False
    for orig_ln, raw in block.lines:
        stripped = raw.strip()
        if not stripped or stripped.startswith("//"): continue
        content = _strip_inline_comment(stripped).strip()
        if not content: continue
        if re.match(r"\|\s*where\b", content): in_where = True
        elif re.match(r"\|\s*\w", content) or content.startswith("let "): in_where = False
        if not in_where: continue
        cleaned = _remove_strings_and_comments(raw)
        i = 0
        while i < len(cleaned):
            if cleaned[i] == "=":
                prev = cleaned[i - 1] if i > 0 else " "
                nxt = cleaned[i + 1] if i + 1 < len(cleaned) else " "
                if nxt == "=" or prev in ("!", ">", "<") or nxt == "~":
                    i += 2; continue
                issues.append(ValidationIssue(orig_ln, i + 1, "error", "L1-EQUAL-001",
                    "Single '=' in where clause (assignment, not comparison)",
                    "Use '==' for equality comparison"))
            i += 1
    return issues


def _check_time_field(block: QueryBlock) -> list[ValidationIssue]:
    if not block.table_name or block.table_name not in kql_tables.ALL_KNOWN_TABLES:
        return []
    expected = kql_tables.expected_time_field(block.table_name)
    if expected is None: return []
    wrong = (kql_tables.DEFENDER_TIME_FIELD if expected == kql_tables.SENTINEL_TIME_FIELD
             else kql_tables.SENTINEL_TIME_FIELD)
    issues: list[ValidationIssue] = []
    for orig_ln, raw in block.lines:
        if raw.strip().startswith("//"): continue
        cleaned = _remove_strings_and_comments(raw)
        for m in re.finditer(r"\b" + wrong + r"\b", cleaned):
            issues.append(ValidationIssue(orig_ln, m.start() + 1, "warning", "L1-TIME-001",
                f"Table '{block.table_name}' typically uses '{expected}', not '{wrong}'",
                f"Use '{expected}' for {block.table_name}"))
    return issues


def _check_headers(lines: list[str]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    first_ln, first_text = 0, ""
    for i, raw in enumerate(lines):
        if raw.strip(): first_ln, first_text = i + 1, raw.strip(); break
    if not first_text: return []
    if not first_text.startswith("//"):
        return [ValidationIssue(first_ln, 1, "warning", "L1-HEADER-001",
            "File does not start with a header comment",
            "Add // comment header with TRR procedure ID and DDM operation reference")]
    header = ""
    for raw in lines:
        s = raw.strip()
        if s.startswith("//"): header += s + "\n"
        elif s: break
    if not TRR_PATTERN.search(header):
        issues.append(ValidationIssue(first_ln, 1, "warning", "L1-HEADER-002",
            "Header comment does not reference a TRR procedure ID",
            "Add TRR procedure ID (e.g., TRR0011.AD.A)"))
    if not DDM_NODE_PATTERN.search(header):
        issues.append(ValidationIssue(first_ln, 1, "warning", "L1-HEADER-003",
            "Header comment does not reference a DDM node",
            'Add DDM operation reference (e.g., n6 "Operation Name")'))
    return issues


def _check_semicolons(lines: list[str]) -> list[ValidationIssue]:
    for i in range(len(lines) - 1, -1, -1):
        s = lines[i].strip()
        if s and not s.startswith("//"):
            content = _strip_inline_comment(s).rstrip()
            if not content.endswith(";"):
                return [ValidationIssue(i + 1, len(lines[i]), "warning", "L1-STRUCT-002",
                    "Query does not end with semicolon", "Add ';' at the end of the query")]
            return []
    return []

# -- Main entry point ---------------------------------------------------------

def validate(text: str, filepath: str = "<stdin>") -> ValidationResult:
    """Run all Level 1 checks against the given KQL text."""
    issues: list[ValidationIssue] = []
    lines = text.split("\n")

    issues.extend(_check_delimiters(lines))
    issues.extend(_check_sql_keywords(lines))
    issues.extend(_check_ago_format(lines))
    issues.extend(_check_trailing_pipe(lines))

    for block in _split_query_blocks(text):
        issues.extend(_check_table_name(block))
        issues.extend(_check_pipe_structure(block))
        issues.extend(_check_assignment_in_where(block))
        issues.extend(_check_time_field(block))

    issues.extend(_check_headers(lines))
    issues.extend(_check_semicolons(lines))

    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]
    status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    return ValidationResult(file=filepath, level=1, status=status,
                            errors=errors, warnings=warnings)
