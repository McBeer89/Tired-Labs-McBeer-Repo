"""Project CRUD and active project resolution."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Optional

from core.models import (
    PLATFORM_ABBREVIATIONS,
    VALID_PLATFORMS,
    BasicQuestions,
    Meta,
    Phases,
    PhaseStatus,
    ProjectState,
    now_iso,
)


def get_tool_root() -> Path:
    """Return the root directory of the trr-research-assistant tool."""
    return Path(__file__).resolve().parent.parent


def get_projects_dir() -> Path:
    """Return the projects/ directory, creating it if needed."""
    projects_dir = get_tool_root() / "projects"
    projects_dir.mkdir(parents=True, exist_ok=True)
    return projects_dir


def create_project(
    technique_id: str,
    name: str,
    platform: str,
    trr_id: str,
) -> ProjectState:
    """Create a new project directory and initial state.json."""
    _validate_project_id(trr_id)
    platform = platform.lower()
    if platform not in VALID_PLATFORMS:
        raise ValueError(
            f"Invalid platform: {platform}. "
            f"Valid: {', '.join(sorted(VALID_PLATFORMS))}"
        )

    projects_dir = get_projects_dir()
    project_dir = projects_dir / trr_id

    if project_dir.exists():
        raise FileExistsError(f"Project {trr_id} already exists at {project_dir}")

    project_dir.mkdir(parents=True)

    ts = now_iso()
    state = ProjectState(
        meta=Meta(
            trr_id=trr_id,
            technique_id=technique_id,
            technique_name=name,
            platform=platform,
            platform_abbrev=PLATFORM_ABBREVIATIONS[platform],
            created=ts,
            last_modified=ts,
        ),
        phases=Phases(
            understanding=PhaseStatus(status="in_progress"),
        ),
        basic_questions=BasicQuestions(
            technique_name=name,
        ),
    )

    save_project(trr_id, state)
    set_active(trr_id)
    return state


def load_project(project_id: str) -> ProjectState:
    """Load a project's state.json and return a ProjectState."""
    _validate_project_id(project_id)
    state_file = get_projects_dir() / project_id / "state.json"
    if not state_file.exists():
        raise FileNotFoundError(f"Project {project_id} not found (no state.json at {state_file})")

    data = json.loads(state_file.read_text(encoding="utf-8"))
    return ProjectState.model_validate(data)


def _validate_project_id(project_id: str) -> None:
    """Validate that a project ID is safe for use as a directory name."""
    if not project_id:
        raise ValueError("Project ID cannot be empty")
    if ".." in project_id or "/" in project_id or "\\" in project_id:
        raise ValueError(f"Invalid project ID: {project_id} (must not contain path separators or '..')")
    # Ensure the resolved path stays within the projects directory
    projects_dir = get_projects_dir()
    resolved = (projects_dir / project_id).resolve()
    if not str(resolved).startswith(str(projects_dir.resolve())):
        raise ValueError(f"Invalid project ID: {project_id} (path traversal detected)")


def save_project(project_id: str, state: ProjectState) -> None:
    """Write state to state.json atomically (write tmp, then rename)."""
    _validate_project_id(project_id)
    state.meta.last_modified = now_iso()
    project_dir = get_projects_dir() / project_id
    project_dir.mkdir(parents=True, exist_ok=True)
    state_file = project_dir / "state.json"

    data = json.dumps(state.model_dump(mode="json"), indent=2, ensure_ascii=False)

    # Atomic write: write to temp file in same dir, then replace
    fd, tmp_path = tempfile.mkstemp(dir=str(project_dir), suffix=".tmp")
    fd_closed = False
    try:
        os.write(fd, data.encode("utf-8"))
        os.close(fd)
        fd_closed = True
        # On Windows, can't rename over an existing file — remove first
        if state_file.exists():
            state_file.unlink()
        os.rename(tmp_path, str(state_file))
    except Exception:
        if not fd_closed:
            os.close(fd)
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise


def list_projects() -> list[dict]:
    """List all projects found in projects/ directory."""
    projects_dir = get_projects_dir()
    result = []

    for entry in sorted(projects_dir.iterdir()):
        if entry.is_dir() and (entry / "state.json").exists():
            try:
                state = load_project(entry.name)
                from core.phases import get_current_phase
                result.append({
                    "trr_id": state.meta.trr_id,
                    "technique_name": state.meta.technique_name,
                    "technique_id": state.meta.technique_id,
                    "platform": state.meta.platform,
                    "current_phase": get_current_phase(state),
                    "last_modified": state.meta.last_modified,
                })
            except Exception:
                result.append({
                    "trr_id": entry.name,
                    "technique_name": "(error loading)",
                    "technique_id": "",
                    "platform": "",
                    "current_phase": "unknown",
                    "last_modified": "",
                })
    return result


def set_active(project_id: str) -> None:
    """Write the active project ID to projects/.active."""
    active_file = get_projects_dir() / ".active"
    active_file.write_text(project_id, encoding="utf-8")


def get_active() -> Optional[str]:
    """Read the active project ID from projects/.active, or None."""
    active_file = get_projects_dir() / ".active"
    if active_file.exists():
        content = active_file.read_text(encoding="utf-8").strip()
        if content:
            return content
    return None


def resolve_project(explicit_id: Optional[str] = None) -> str:
    """Resolve which project to use.

    Resolution order:
    1. Explicit --project flag
    2. projects/.active file
    3. If exactly one project exists, use it
    4. Error with instructions
    """
    # 1. Explicit flag
    if explicit_id:
        state_file = get_projects_dir() / explicit_id / "state.json"
        if not state_file.exists():
            raise FileNotFoundError(f"Project {explicit_id} not found")
        return explicit_id

    # 2. .active file
    active = get_active()
    if active:
        state_file = get_projects_dir() / active / "state.json"
        if state_file.exists():
            return active

    # 3. Single project
    projects = [
        d.name for d in get_projects_dir().iterdir()
        if d.is_dir() and (d / "state.json").exists()
    ]
    if len(projects) == 1:
        return projects[0]

    # 4. Error
    if not projects:
        raise FileNotFoundError(
            "No projects found. Create one with:\n"
            "  python trr_research.py init <technique_id> --name <name> --platform <platform> --trr-id <id>"
        )
    raise FileNotFoundError(
        f"Multiple projects found ({', '.join(projects)}) but no active project set.\n"
        "Set one with:  python trr_research.py use <trr_id>\n"
        "Or specify:    python trr_research.py --project <trr_id> <command>"
    )
