"""Tests for Level 1 KQL syntax validation."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the kql_validator package is importable
_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from kql_validator.level1_syntax import validate, ValidationIssue

GOOD_DIR = Path(__file__).resolve().parent / "good"
BAD_DIR = Path(__file__).resolve().parent / "bad"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _codes(result) -> list[str]:
    """Extract all issue codes from a result."""
    return [i.code for i in result.errors + result.warnings]


def _error_codes(result) -> list[str]:
    """Extract error codes only."""
    return [i.code for i in result.errors]


def _warning_codes(result) -> list[str]:
    """Extract warning codes only."""
    return [i.code for i in result.warnings]


# ---------------------------------------------------------------------------
# Good fixtures: should pass with zero errors
# ---------------------------------------------------------------------------

class TestGoodFixtures:
    """All files in tests/good/ should produce zero errors."""

    def test_basic_query(self):
        text = (GOOD_DIR / "basic_query.kql").read_text(encoding="utf-8")
        result = validate(text, "basic_query.kql")
        assert result.status in ("PASS", "WARN"), (
            f"Expected PASS or WARN, got {result.status}: "
            f"{[f'{i.code}: {i.message}' for i in result.errors]}"
        )
        assert len(result.errors) == 0, (
            f"Unexpected errors: {[f'{i.code}: {i.message}' for i in result.errors]}"
        )

    def test_let_binding(self):
        text = (GOOD_DIR / "let_binding.kql").read_text(encoding="utf-8")
        result = validate(text, "let_binding.kql")
        assert len(result.errors) == 0, (
            f"Unexpected errors: {[f'{i.code}: {i.message}' for i in result.errors]}"
        )

    def test_multi_query(self):
        text = (GOOD_DIR / "multi_query.kql").read_text(encoding="utf-8")
        result = validate(text, "multi_query.kql")
        assert len(result.errors) == 0, (
            f"Unexpected errors: {[f'{i.code}: {i.message}' for i in result.errors]}"
        )

    def test_join_query(self):
        text = (GOOD_DIR / "join_query.kql").read_text(encoding="utf-8")
        result = validate(text, "join_query.kql")
        assert len(result.errors) == 0, (
            f"Unexpected errors: {[f'{i.code}: {i.message}' for i in result.errors]}"
        )


# ---------------------------------------------------------------------------
# Bad fixtures: should produce expected error codes
# ---------------------------------------------------------------------------

class TestBadFixtures:
    """Files in tests/bad/ should produce specific errors."""

    def test_sql_keywords(self):
        text = (BAD_DIR / "sql_keywords.kql").read_text(encoding="utf-8")
        result = validate(text, "sql_keywords.kql")
        assert result.status == "FAIL"
        codes = _error_codes(result)
        # Should flag SELECT, FROM, WHERE, AND
        assert any("KEYWORD" in c for c in codes), (
            f"Expected KEYWORD errors, got: {codes}"
        )

    def test_unclosed_paren(self):
        text = (BAD_DIR / "unclosed_paren.kql").read_text(encoding="utf-8")
        result = validate(text, "unclosed_paren.kql")
        assert result.status == "FAIL"
        codes = _error_codes(result)
        assert "L1-DELIM-001" in codes, (
            f"Expected L1-DELIM-001, got: {codes}"
        )

    def test_trailing_pipe(self):
        text = (BAD_DIR / "trailing_pipe.kql").read_text(encoding="utf-8")
        result = validate(text, "trailing_pipe.kql")
        assert result.status == "FAIL"
        codes = _error_codes(result)
        assert "L1-STRUCT-001" in codes, (
            f"Expected L1-STRUCT-001, got: {codes}"
        )

    def test_ago_string(self):
        text = (BAD_DIR / "ago_string.kql").read_text(encoding="utf-8")
        result = validate(text, "ago_string.kql")
        assert result.status == "FAIL"
        codes = _error_codes(result)
        assert "L1-FUNC-001" in codes, (
            f"Expected L1-FUNC-001, got: {codes}"
        )


# ---------------------------------------------------------------------------
# Inline fixtures: targeted checks
# ---------------------------------------------------------------------------

class TestDelimiters:
    """Test delimiter balancing."""

    def test_balanced_parens(self):
        kql = '// TRR0001\n// n1\nT\n| where (a == "b")\n;'
        result = validate(kql)
        delim_errors = [i for i in result.errors if "DELIM" in i.code]
        assert len(delim_errors) == 0

    def test_unclosed_paren(self):
        kql = '// TRR0001\n// n1\nT\n| where (a == "b"\n;'
        result = validate(kql)
        assert any(i.code == "L1-DELIM-001" for i in result.errors)

    def test_extra_close_paren(self):
        kql = '// TRR0001\n// n1\nT\n| where a == "b")\n;'
        result = validate(kql)
        assert any(i.code == "L1-DELIM-002" for i in result.errors)

    def test_unclosed_bracket(self):
        kql = '// TRR0001\n// n1\nT\n| where a in ["x"\n;'
        result = validate(kql)
        assert any(i.code == "L1-DELIM-003" for i in result.errors)

    def test_unclosed_string(self):
        kql = '// TRR0001\n// n1\nT\n| where a == "unclosed\n;'
        result = validate(kql)
        assert any(i.code == "L1-DELIM-005" for i in result.errors)


class TestSQLKeywords:
    """Test SQL keyword detection."""

    def test_select_flagged(self):
        kql = "// TRR0001\n// n1\nSELECT a FROM T\n;"
        result = validate(kql)
        assert any(
            i.code == "L1-KEYWORD-001" and "SELECT" in i.message
            for i in result.errors
        )

    def test_and_flagged(self):
        kql = '// TRR0001\n// n1\nT\n| where a == "b" AND c == "d"\n;'
        result = validate(kql)
        assert any(
            i.code == "L1-KEYWORD-002" and "AND" in i.message
            for i in result.errors
        )

    def test_lowercase_and_not_flagged(self):
        kql = '// TRR0001\n// n1\nT\n| where a == "b" and c == "d"\n;'
        result = validate(kql)
        keyword_errors = [
            i for i in result.errors if "KEYWORD" in i.code
        ]
        assert len(keyword_errors) == 0

    def test_or_flagged(self):
        kql = '// TRR0001\n// n1\nT\n| where a == "1" OR b == "2"\n;'
        result = validate(kql)
        assert any(
            i.code == "L1-KEYWORD-002" and "OR" in i.message
            for i in result.errors
        )

    def test_group_by_flagged(self):
        kql = "// TRR0001\n// n1\nT\n| GROUP BY col\n;"
        result = validate(kql)
        assert any("KEYWORD" in i.code for i in result.errors)

    def test_sql_keywords_in_strings_not_flagged(self):
        kql = '// TRR0001\n// n1\nT\n| where col == "SELECT FROM WHERE"\n;'
        result = validate(kql)
        keyword_errors = [
            i for i in result.errors if "KEYWORD" in i.code
        ]
        assert len(keyword_errors) == 0

    def test_sql_keywords_in_comments_not_flagged(self):
        kql = "// SELECT FROM WHERE AND OR\n// TRR0001 n1\nT\n| where a == b\n;"
        result = validate(kql)
        keyword_errors = [
            i for i in result.errors if "KEYWORD" in i.code
        ]
        assert len(keyword_errors) == 0


class TestAgoFormat:
    """Test ago() argument validation."""

    def test_valid_ago(self):
        kql = '// TRR0001\n// n1\nT\n| where TimeGenerated > ago(24h)\n;'
        result = validate(kql)
        func_errors = [i for i in result.errors if "FUNC" in i.code]
        assert len(func_errors) == 0

    def test_string_ago(self):
        kql = '// TRR0001\n// n1\nT\n| where TimeGenerated > ago("24h")\n;'
        result = validate(kql)
        assert any(i.code == "L1-FUNC-001" for i in result.errors)

    def test_single_quote_ago(self):
        kql = "// TRR0001\n// n1\nT\n| where TimeGenerated > ago('1d')\n;"
        result = validate(kql)
        assert any(i.code == "L1-FUNC-001" for i in result.errors)


class TestAssignmentVsEquality:
    """Test = vs == detection in where clauses."""

    def test_equality_ok(self):
        kql = '// TRR0001\n// n1\nT\n| where a == "b"\n;'
        result = validate(kql)
        equal_errors = [i for i in result.errors if "EQUAL" in i.code]
        assert len(equal_errors) == 0

    def test_not_equal_ok(self):
        kql = '// TRR0001\n// n1\nT\n| where a != "b"\n;'
        result = validate(kql)
        equal_errors = [i for i in result.errors if "EQUAL" in i.code]
        assert len(equal_errors) == 0

    def test_bare_equals_in_where(self):
        kql = '// TRR0001\n// n1\nT\n| where a = "b"\n;'
        result = validate(kql)
        assert any(i.code == "L1-EQUAL-001" for i in result.errors)

    def test_let_assignment_not_flagged(self):
        kql = '// TRR0001\n// n1\nlet x = 5;\nT\n| where a == "b"\n;'
        result = validate(kql)
        equal_errors = [i for i in result.errors if "EQUAL" in i.code]
        assert len(equal_errors) == 0

    def test_extend_assignment_not_flagged(self):
        kql = '// TRR0001\n// n1\nT\n| extend x = col + 1\n| where a == "b"\n;'
        result = validate(kql)
        equal_errors = [i for i in result.errors if "EQUAL" in i.code]
        assert len(equal_errors) == 0

    def test_gte_not_flagged(self):
        kql = '// TRR0001\n// n1\nT\n| where a >= 5\n;'
        result = validate(kql)
        equal_errors = [i for i in result.errors if "EQUAL" in i.code]
        assert len(equal_errors) == 0

    def test_case_insensitive_eq_not_flagged(self):
        kql = '// TRR0001\n// n1\nT\n| where a =~ "b"\n;'
        result = validate(kql)
        equal_errors = [i for i in result.errors if "EQUAL" in i.code]
        assert len(equal_errors) == 0


class TestTrailingPipe:
    """Test trailing pipe detection."""

    def test_trailing_pipe_error(self):
        kql = "// TRR0001\n// n1\nT\n| where a == b\n|"
        result = validate(kql)
        assert any(i.code == "L1-STRUCT-001" for i in result.errors)

    def test_pipe_with_operator_ok(self):
        kql = '// TRR0001\n// n1\nT\n| where a == "b"\n;'
        result = validate(kql)
        struct_errors = [
            i for i in result.errors if i.code == "L1-STRUCT-001"
        ]
        assert len(struct_errors) == 0


class TestHeaders:
    """Test header comment validation."""

    def test_missing_header(self):
        kql = 'T\n| where a == "b"\n;'
        result = validate(kql)
        assert any(i.code == "L1-HEADER-001" for i in result.warnings)

    def test_missing_trr_ref(self):
        kql = '// Some query\n// n1 operation\nT\n| where a == "b"\n;'
        result = validate(kql)
        assert any(i.code == "L1-HEADER-002" for i in result.warnings)

    def test_missing_ddm_ref(self):
        kql = '// TRR0001.WIN.A query\nT\n| where a == "b"\n;'
        result = validate(kql)
        assert any(i.code == "L1-HEADER-003" for i in result.warnings)

    def test_good_header(self):
        kql = '// TRR0001.WIN.A -- Query 1\n// DDM Operation: n3 "Spawn"\nT\n| where a == "b"\n;'
        result = validate(kql)
        header_warnings = [
            i for i in result.warnings if "HEADER" in i.code
        ]
        assert len(header_warnings) == 0


class TestTableName:
    """Test table name validation."""

    def test_known_table(self):
        kql = '// TRR0001\n// n1\nSecurityEvent\n| where a == "b"\n;'
        result = validate(kql)
        table_warnings = [
            i for i in result.warnings if "TABLE" in i.code
        ]
        assert len(table_warnings) == 0

    def test_unknown_table(self):
        kql = '// TRR0001\n// n1\nCustomTable_CL\n| where a == "b"\n;'
        result = validate(kql)
        assert any(i.code == "L1-TABLE-001" for i in result.warnings)


class TestTimeField:
    """Test time field consistency."""

    def test_sentinel_table_with_timegenerated(self):
        kql = '// TRR0001\n// n1\nSecurityEvent\n| where TimeGenerated > ago(24h)\n;'
        result = validate(kql)
        time_warnings = [i for i in result.warnings if "TIME" in i.code]
        assert len(time_warnings) == 0

    def test_defender_table_with_timestamp(self):
        kql = '// TRR0001\n// n1\nDeviceProcessEvents\n| where Timestamp > ago(24h)\n;'
        result = validate(kql)
        time_warnings = [i for i in result.warnings if "TIME" in i.code]
        assert len(time_warnings) == 0

    def test_sentinel_table_with_wrong_field(self):
        kql = '// TRR0001\n// n1\nSecurityEvent\n| where Timestamp > ago(24h)\n;'
        result = validate(kql)
        assert any(i.code == "L1-TIME-001" for i in result.warnings)

    def test_defender_table_with_wrong_field(self):
        kql = '// TRR0001\n// n1\nDeviceProcessEvents\n| where TimeGenerated > ago(24h)\n;'
        result = validate(kql)
        assert any(i.code == "L1-TIME-001" for i in result.warnings)


class TestSemicolons:
    """Test semicolon termination warnings."""

    def test_with_semicolon(self):
        kql = '// TRR0001\n// n1\nT\n| where a == "b"\n;'
        result = validate(kql)
        struct_warnings = [
            i for i in result.warnings if i.code == "L1-STRUCT-002"
        ]
        assert len(struct_warnings) == 0

    def test_without_semicolon(self):
        kql = '// TRR0001\n// n1\nT\n| where a == "b"'
        result = validate(kql)
        assert any(i.code == "L1-STRUCT-002" for i in result.warnings)


# ---------------------------------------------------------------------------
# Ground truth: existing KQL files must produce zero errors
# ---------------------------------------------------------------------------

class TestGroundTruth:
    """Existing completed KQL files are ground truth -- zero errors allowed."""

    def _validate_ground_truth(self, path: Path):
        if not path.exists():
            return  # Skip if file not present in test environment
        text = path.read_text(encoding="utf-8")
        result = validate(text, str(path.name))
        assert len(result.errors) == 0, (
            f"Ground truth file {path.name} has errors: "
            f"{[f'L{i.line}:C{i.column} {i.code}: {i.message}' for i in result.errors]}"
        )

    def test_trr0011_ad_a(self):
        self._validate_ground_truth(
            _project_root / "Completed TRR Reports" / "trr0011" / "ad" / "kql" / "trr0011_ad_a.kql"
        )

    def test_trr0012_ad_a(self):
        self._validate_ground_truth(
            _project_root / "Completed TRR Reports" / "trr0012" / "ad" / "kql" / "trr0012_ad_a.kql"
        )

    def test_trr0012_ad_b(self):
        self._validate_ground_truth(
            _project_root / "Completed TRR Reports" / "trr0012" / "ad" / "kql" / "trr0012_ad_b.kql"
        )

    def test_trr0012_ad_c(self):
        self._validate_ground_truth(
            _project_root / "Completed TRR Reports" / "trr0012" / "ad" / "kql" / "trr0012_ad_c.kql"
        )

    def test_trr0012_ad_d(self):
        self._validate_ground_truth(
            _project_root / "Completed TRR Reports" / "trr0012" / "ad" / "kql" / "trr0012_ad_d.kql"
        )

    def test_trr0013_ad_a(self):
        self._validate_ground_truth(
            _project_root / "Completed TRR Reports" / "trr0013" / "ad" / "kql" / "trr0013_ad_a.kql"
        )

    def test_trr0013_ad_b(self):
        self._validate_ground_truth(
            _project_root / "Completed TRR Reports" / "trr0013" / "ad" / "kql" / "trr0013_ad_b.kql"
        )
