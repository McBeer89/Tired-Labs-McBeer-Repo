"""Level 2 KQL schema validation (stub).

When implemented, this module will validate KQL queries against a
populated environment profile (kql-environment-profile.md). It will:

- Promote "unknown table" warnings from Level 1 to errors if the table
  is not declared in the environment profile.
- Validate every field name referenced in where, project, extend, and
  summarize clauses against the declared schema for each table.
- Flag field names that exist under a different name in the target
  environment (using the field mapping from the environment profile).
- Check that telemetry sources marked "No" in the profile don't have
  queries generated for them.

Dependencies:
  - Populated kql-environment-profile.md with Available Log Sources
    and Field Name Mappings sections.
  - No external services required (fully offline).
"""

from __future__ import annotations

from .level1_syntax import ValidationResult


def validate(text: str, filepath: str = "<stdin>") -> ValidationResult:
    """Run Level 2 schema checks. Currently a stub returning empty results."""
    return ValidationResult(
        file=filepath,
        level=2,
        status="PASS",
        errors=[],
        warnings=[],
    )
