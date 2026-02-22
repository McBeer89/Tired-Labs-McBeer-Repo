"""Phase definitions and gate validation for the TRR research workflow."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models import ProjectState


PHASE_ORDER = ["understanding", "scoping", "procedures", "validation"]


def get_phase_index(phase_name: str) -> int:
    """Return the ordinal position of a phase."""
    return PHASE_ORDER.index(phase_name)


def get_current_phase(state: ProjectState) -> str:
    """Determine the current active phase from state."""
    phases = state.phases
    for phase_name in PHASE_ORDER:
        phase_status = getattr(phases, phase_name)
        if phase_status.status != "complete":
            return phase_name
    return "validation"  # all complete


def check_understanding_gate(state: ProjectState) -> tuple[bool, list[str], list[str]]:
    """Check gate: understanding → scoping.

    Returns (passed, errors, warnings).
    """
    bq = state.basic_questions
    errors = []
    warnings = []

    if not bq.technique_name:
        errors.append("technique_name is not set")
    if not bq.tactics:
        errors.append("tactics is not set (empty list)")
    if not bq.platforms:
        errors.append("platforms is not set (empty list)")
    if not bq.attacker_objective:
        errors.append("attacker_objective is not set")
    if not bq.prerequisites:
        errors.append("prerequisites is not set")
    if not bq.why_used:
        warnings.append("why_used is empty (optional but recommended)")

    passed = len(errors) == 0
    return passed, errors, warnings


def check_scoping_gate(state: ProjectState) -> tuple[bool, list[str], list[str]]:
    """Check gate: scoping → procedures."""
    errors = []
    warnings = []

    if not state.scoping.scope_statement:
        errors.append("scope_statement is not set")
    if len(state.scoping.exclusions) < 1:
        errors.append("at least 1 exclusion must be documented")
    if len(state.scoping.constraints) < 1:
        errors.append("at least 1 constraint must be documented")

    passed = len(errors) == 0
    return passed, errors, warnings


def check_procedures_gate(state: ProjectState) -> tuple[bool, list[str], list[str]]:
    """Check gate: procedures → validation."""
    errors = []
    warnings = []

    if len(state.procedures) < 1:
        errors.append("at least 1 procedure must be defined")
    for proc in state.procedures:
        missing = []
        if not proc.name:
            missing.append("name")
        if not proc.summary:
            missing.append("summary")
        if not proc.distinguishing_operations:
            missing.append("distinguishing_operations")
        if missing:
            errors.append(f"Procedure {proc.id} missing: {', '.join(missing)}")

    passed = len(errors) == 0
    return passed, errors, warnings


def check_gate(state: ProjectState, phase_name: str) -> tuple[bool, list[str], list[str]]:
    """Check the gate for completing a given phase.

    Returns (passed, errors, warnings).
    """
    if phase_name == "understanding":
        return check_understanding_gate(state)
    elif phase_name == "scoping":
        return check_scoping_gate(state)
    elif phase_name == "procedures":
        return check_procedures_gate(state)
    elif phase_name == "validation":
        # Validation phase has no blocking gate — informational only
        return True, [], []
    else:
        return False, [f"Unknown phase: {phase_name}"], []


def complete_phase(state: ProjectState, phase_name: str, force: bool = False) -> tuple[bool, list[str], list[str]]:
    """Attempt to complete a phase and advance to the next one.

    Returns (success, errors, warnings).
    If force=True, completes regardless of gate failures.
    """
    from core.models import now_iso

    passed, errors, warnings = check_gate(state, phase_name)

    if not passed and not force:
        return False, errors, warnings

    # Mark phase complete
    phase_status = getattr(state.phases, phase_name)
    phase_status.status = "complete"
    phase_status.completed_at = now_iso()

    # Advance next phase to in_progress
    idx = get_phase_index(phase_name)
    if idx + 1 < len(PHASE_ORDER):
        next_phase = PHASE_ORDER[idx + 1]
        next_status = getattr(state.phases, next_phase)
        if next_status.status == "not_started":
            next_status.status = "in_progress"

    return True, errors, warnings
