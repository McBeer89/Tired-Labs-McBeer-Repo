"""Phase gate checks, validation checklists, and check alias resolution."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from core.models import ProjectState


# --- Check aliases (short name → full field name) ---

CHECK_ALIASES = {
    "ops-tested": "all_ops_pass_inclusion_test",
    "ops-understood": "all_ops_understood",
    "paths-explored": "all_paths_explored",
    "telemetry-id": "telemetry_identified",
    "procs-distinct": "procedures_distinct",
    "scope-documented": "scoping_documented",
    "details-correct": "technical_details_correct",
    "no-assumptions": "no_hidden_assumptions",
    "no-tangential": "no_tangential_elements",
    "matches-real": "matches_real_world",
    "refs-cited": "references_cited",
    "ddm-conventions": "ddm_conventions_followed",
}

# Completeness check keys
COMPLETENESS_KEYS = [
    "all_ops_pass_inclusion_test",
    "all_ops_understood",
    "all_paths_explored",
    "telemetry_identified",
    "procedures_distinct",
    "scoping_documented",
]

# Accuracy check keys
ACCURACY_KEYS = [
    "technical_details_correct",
    "no_hidden_assumptions",
    "no_tangential_elements",
    "matches_real_world",
    "references_cited",
    "ddm_conventions_followed",
]

# Human-readable labels
CHECK_LABELS = {
    "all_ops_pass_inclusion_test": "All operations pass the inclusion test",
    "all_ops_understood": "All operations understood (no unknowns)",
    "all_paths_explored": "All realistic paths explored",
    "telemetry_identified": "Telemetry identified for each operation",
    "procedures_distinct": "Procedures are distinct",
    "scoping_documented": "Scoping decisions documented with rationale",
    "technical_details_correct": "Technical details verified against documentation",
    "no_hidden_assumptions": "No hidden assumptions in the model",
    "no_tangential_elements": "No tangential elements in DDM",
    "matches_real_world": "Model matches real-world implementations",
    "references_cited": "References cited for technical claims",
    "ddm_conventions_followed": "DDM follows structural conventions",
}


def resolve_check_name(name: str) -> Optional[str]:
    """Resolve a check alias or full name to the canonical field name.

    Returns None if unrecognized.
    """
    if name in CHECK_ALIASES:
        return CHECK_ALIASES[name]
    all_keys = set(COMPLETENESS_KEYS + ACCURACY_KEYS)
    if name in all_keys:
        return name
    return None


def is_completeness_check(name: str) -> bool:
    """Return True if the canonical name is a completeness check."""
    return name in COMPLETENESS_KEYS


def is_accuracy_check(name: str) -> bool:
    """Return True if the canonical name is an accuracy check."""
    return name in ACCURACY_KEYS


def parse_check_value(value_str: str) -> Optional[bool]:
    """Parse 'pass', 'fail', or 'na' into a bool or None.

    pass → True, fail → False, na → None
    """
    v = value_str.lower().strip()
    if v == "pass":
        return True
    elif v == "fail":
        return False
    elif v == "na":
        return None
    else:
        raise ValueError(f"Invalid value: {value_str}. Use: pass, fail, or na")


def set_check(state: ProjectState, check_name: str, value: Optional[bool]) -> None:
    """Set a validation check value on the state."""
    canonical = resolve_check_name(check_name)
    if canonical is None:
        raise ValueError(
            f"Unknown check: {check_name}\n"
            f"Valid checks: {', '.join(sorted(CHECK_ALIASES.keys()))}"
        )

    if is_completeness_check(canonical):
        setattr(state.validation.completeness, canonical, value)
    elif is_accuracy_check(canonical):
        setattr(state.validation.accuracy, canonical, value)


def run_completeness(state: ProjectState) -> list[dict]:
    """Run completeness checklist. Returns list of {check, label, value, status}."""
    results = []
    for key in COMPLETENESS_KEYS:
        value = getattr(state.validation.completeness, key)
        if value is True:
            status = "pass"
            icon = "✅"
        elif value is False:
            status = "fail"
            icon = "❌"
        else:
            status = "not checked"
            icon = "⬜"
        results.append({
            "check": key,
            "label": CHECK_LABELS[key],
            "value": value,
            "status": status,
            "icon": icon,
        })
    return results


def run_accuracy(state: ProjectState) -> list[dict]:
    """Run accuracy checklist. Returns list of {check, label, value, status}."""
    results = []
    for key in ACCURACY_KEYS:
        value = getattr(state.validation.accuracy, key)
        if value is True:
            status = "pass"
            icon = "✅"
        elif value is False:
            status = "fail"
            icon = "❌"
        else:
            status = "not checked"
            icon = "⬜"
        results.append({
            "check": key,
            "label": CHECK_LABELS[key],
            "value": value,
            "status": status,
            "icon": icon,
        })
    return results


def run_all(state: ProjectState) -> dict:
    """Run both checklists. Returns {completeness: [...], accuracy: [...]}."""
    return {
        "completeness": run_completeness(state),
        "accuracy": run_accuracy(state),
    }
