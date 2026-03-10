"""KQL Validator — CLI entry point.

Validates .kql files for structural correctness, common LLM errors,
and pipeline conventions. Runs Level 1 (syntax) checks always.
Level 2 (schema) and Level 3 (live) run only if available.

Usage:
    python validate.py path/to/file.kql
    python validate.py "kql/*.kql"
    python validate.py --format json path/to/file.kql
    python validate.py --format text path/to/file.kql

Exit codes:
    0 = all files pass
    1 = warnings only (no errors)
    2 = errors found
"""

from __future__ import annotations

import argparse
import glob
import importlib
import importlib.util
import json
import sys
from pathlib import Path

# The directory is named kql-validator (hyphen) per project convention,
# but Python packages need underscores. Register the package manually.
_this_dir = Path(__file__).resolve().parent
_package_name = "kql_validator"
if _package_name not in sys.modules:
    spec = importlib.util.spec_from_file_location(
        _package_name,
        _this_dir / "__init__.py",
        submodule_search_locations=[str(_this_dir)],
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules[_package_name] = mod
    spec.loader.exec_module(mod)

from kql_validator.level1_syntax import ValidationResult, validate as level1_validate


def run_validation(filepath: Path) -> ValidationResult:
    """Run all available validation levels against a single file."""
    text = filepath.read_text(encoding="utf-8")
    result = level1_validate(text, filepath=str(filepath.name))

    # Level 2 and 3 stubs -- call them but they return empty results.
    # When implemented, their results would be merged into the main result.
    # from kql_validator.level2_schema import validate as level2_validate
    # from kql_validator.level3_live import validate as level3_validate

    return result


def format_text(result: ValidationResult) -> str:
    """Format a validation result as human-readable text."""
    total_errors = len(result.errors)
    total_warnings = len(result.warnings)

    parts = []

    # Summary line
    counts = []
    if total_errors:
        counts.append(f"{total_errors} error{'s' if total_errors != 1 else ''}")
    if total_warnings:
        counts.append(f"{total_warnings} warning{'s' if total_warnings != 1 else ''}")

    summary = f"{result.file}: {result.status}"
    if counts:
        summary += f" ({', '.join(counts)})"
    parts.append(summary)

    # Individual issues
    all_issues = sorted(
        result.errors + result.warnings,
        key=lambda i: (i.line, i.column),
    )

    if all_issues:
        parts.append("")
        for issue in all_issues:
            severity = "ERROR" if issue.severity == "error" else "WARN "
            location = f"L{issue.line}:C{issue.column}"
            line = f"  {severity}  {location:<8}  {issue.code}  {issue.message}"
            if issue.suggestion:
                line += f" -- {issue.suggestion}"
            parts.append(line)

    return "\n".join(parts)


def format_json(result: ValidationResult) -> str:
    """Format a validation result as JSON."""
    return json.dumps(result.to_dict(), indent=2)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="KQL Validator — validate .kql files for syntax and structure",
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="File paths or glob patterns to validate",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        dest="output_format",
        help="Output format (default: text)",
    )

    args = parser.parse_args()

    # Expand glob patterns
    file_paths: list[Path] = []
    for pattern in args.files:
        expanded = glob.glob(pattern, recursive=True)
        if expanded:
            for p in expanded:
                fp = Path(p)
                if fp.is_file() and fp.suffix == ".kql":
                    file_paths.append(fp)
        else:
            # Try as a literal path
            fp = Path(pattern)
            if fp.is_file():
                file_paths.append(fp)
            else:
                print(f"Warning: No files matched '{pattern}'", file=sys.stderr)

    if not file_paths:
        print("No .kql files found to validate.", file=sys.stderr)
        return 2

    # Validate each file
    results: list[ValidationResult] = []
    for fp in sorted(set(file_paths)):
        result = run_validation(fp)
        results.append(result)

    # Output results
    has_errors = False
    has_warnings = False

    if args.output_format == "json":
        output = [r.to_dict() for r in results]
        print(json.dumps(output, indent=2))
    else:
        for i, result in enumerate(results):
            if i > 0:
                print()
            print(format_text(result))

    for result in results:
        if result.errors:
            has_errors = True
        if result.warnings:
            has_warnings = True

    if has_errors:
        return 2
    elif has_warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
