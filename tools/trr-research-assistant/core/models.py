"""Pydantic v2 models for the TRR Research Assistant state schema."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


PLATFORM_ABBREVIATIONS = {
    "windows": "WIN",
    "linux": "LNX",
    "macos": "MAC",
    "ad": "AD",
    "azure": "AZR",
    "aws": "AWS",
    "gcp": "GCP",
    "k8s": "K8S",
    "network": "NET",
}

VALID_PLATFORMS = set(PLATFORM_ABBREVIATIONS.keys())


def now_iso() -> str:
    """Return current UTC time as ISO string."""
    return datetime.now(timezone.utc).isoformat()


# --- Sub-models ---

class ScraperImportInfo(BaseModel):
    source_file: str = ""
    imported_at: str = ""
    report_version: str = ""


class Meta(BaseModel):
    trr_id: str
    technique_id: str
    technique_name: str = ""
    platform: str = ""
    platform_abbrev: str = ""
    contributors: list[str] = Field(default_factory=list)
    created: str = ""
    last_modified: str = ""
    scraper_import: Optional[ScraperImportInfo] = None


class PhaseStatus(BaseModel):
    status: str = "not_started"  # not_started | in_progress | complete
    completed_at: Optional[str] = None


class Phases(BaseModel):
    understanding: PhaseStatus = Field(default_factory=PhaseStatus)
    scoping: PhaseStatus = Field(default_factory=PhaseStatus)
    procedures: PhaseStatus = Field(default_factory=PhaseStatus)
    validation: PhaseStatus = Field(default_factory=PhaseStatus)


class BasicQuestions(BaseModel):
    technique_name: str = ""
    tactics: list[str] = Field(default_factory=list)
    platforms: list[str] = Field(default_factory=list)
    attacker_objective: str = ""
    why_used: str = ""
    prerequisites: str = ""


class Exclusion(BaseModel):
    item: str
    rationale: str


class Constraint(BaseModel):
    id: str  # C1, C2, ...
    constraint: str
    essential: bool = True
    immutable: bool = True
    observable: bool = False
    telemetry: str = ""


class Scoping(BaseModel):
    scope_statement: str = ""
    exclusions: list[Exclusion] = Field(default_factory=list)
    constraints: list[Constraint] = Field(default_factory=list)


class Procedure(BaseModel):
    id: str  # e.g. TRR0028.AD.A
    letter: str  # A, B, C, ...
    name: str = ""
    summary: str = ""
    distinguishing_operations: str = ""
    narrative: str = ""
    ddm_filename: str = ""
    ddm_description: str = ""


class EmulationTest(BaseModel):
    name: str = ""
    source: str = ""  # e.g. "Atomic Red Team"
    atomic_guid: str = ""
    github_url: str = ""
    procedure_mapping: str = ""  # procedure ID or empty


class Reference(BaseModel):
    id: str  # R001, R002, ...
    name: str = ""
    url: str = ""
    source: str = ""  # "scraper_import" or "manual"
    used_in_sections: list[str] = Field(default_factory=list)


class SourceLibraryEntry(BaseModel):
    title: str = ""
    url: str = ""
    category: str = ""
    relevance_score: float = 0.0
    domain: str = ""


class Note(BaseModel):
    id: str  # N001, N002, ...
    text: str = ""
    phase: str = ""
    created_at: str = ""


class CompletenessChecklist(BaseModel):
    all_ops_pass_inclusion_test: Optional[bool] = None
    all_ops_understood: Optional[bool] = None
    all_paths_explored: Optional[bool] = None
    telemetry_identified: Optional[bool] = None
    procedures_distinct: Optional[bool] = None
    scoping_documented: Optional[bool] = None


class AccuracyChecklist(BaseModel):
    technical_details_correct: Optional[bool] = None
    no_hidden_assumptions: Optional[bool] = None
    no_tangential_elements: Optional[bool] = None
    matches_real_world: Optional[bool] = None
    references_cited: Optional[bool] = None
    ddm_conventions_followed: Optional[bool] = None


class Validation(BaseModel):
    completeness: CompletenessChecklist = Field(default_factory=CompletenessChecklist)
    accuracy: AccuracyChecklist = Field(default_factory=AccuracyChecklist)


# --- Root state model ---

class ProjectState(BaseModel):
    meta: Meta
    phases: Phases = Field(default_factory=Phases)
    basic_questions: BasicQuestions = Field(default_factory=BasicQuestions)
    scoping: Scoping = Field(default_factory=Scoping)
    procedures: list[Procedure] = Field(default_factory=list)
    emulation_tests: list[EmulationTest] = Field(default_factory=list)
    references: list[Reference] = Field(default_factory=list)
    source_library: list[SourceLibraryEntry] = Field(default_factory=list)
    notes: list[Note] = Field(default_factory=list)
    telemetry_hints: list[str] = Field(default_factory=list)
    related_trrs: list[dict] = Field(default_factory=list)
    related_ddms: list[dict] = Field(default_factory=list)
    validation: Validation = Field(default_factory=Validation)


# --- ID generation helpers ---

def next_procedure_letter(procedures: list[Procedure]) -> str:
    """Return the next available procedure letter (A, B, C, ...)."""
    if not procedures:
        return "A"
    existing = sorted(p.letter for p in procedures)
    last = existing[-1]
    if last == "Z":
        return "AA"
    return chr(ord(last) + 1)


def next_reference_id(references: list[Reference]) -> str:
    """Return the next available reference ID (R001, R002, ...)."""
    if not references:
        return "R001"
    nums = []
    for r in references:
        try:
            nums.append(int(r.id[1:]))
        except (ValueError, IndexError):
            continue
    max_num = max(nums) if nums else 0
    return f"R{max_num + 1:03d}"


def next_constraint_id(constraints: list[Constraint]) -> str:
    """Return the next available constraint ID (C1, C2, ...)."""
    if not constraints:
        return "C1"
    nums = []
    for c in constraints:
        try:
            nums.append(int(c.id[1:]))
        except (ValueError, IndexError):
            continue
    max_num = max(nums) if nums else 0
    return f"C{max_num + 1}"


def next_note_id(notes: list[Note]) -> str:
    """Return the next available note ID (N001, N002, ...)."""
    if not notes:
        return "N001"
    nums = []
    for n in notes:
        try:
            nums.append(int(n.id[1:]))
        except (ValueError, IndexError):
            continue
    max_num = max(nums) if nums else 0
    return f"N{max_num + 1:03d}"
