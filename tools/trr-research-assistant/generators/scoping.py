"""Render the scoping document from project state via Jinja2."""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from core.models import ProjectState


def get_templates_dir() -> Path:
    """Return the templates/ directory path."""
    return Path(__file__).resolve().parent.parent / "templates"


def generate_scoping_doc(state: ProjectState) -> str:
    """Render the scoping document markdown.

    Always works regardless of phase — missing data renders as empty.
    """
    env = Environment(
        loader=FileSystemLoader(str(get_templates_dir())),
        keep_trailing_newline=True,
    )
    template = env.get_template("scoping_doc.md.j2")

    # Filter notes to scoping phase (or all if not phase-tagged)
    scoping_notes = [n for n in state.notes if n.phase in ("scoping", "")]

    return template.render(
        meta=state.meta,
        basic_questions=state.basic_questions,
        scoping=state.scoping,
        notes=scoping_notes,
    )


def write_scoping_doc(state: ProjectState, output_dir: Path) -> Path:
    """Generate and write the scoping document to disk."""
    content = generate_scoping_doc(state)
    output_path = output_dir / f"{state.meta.trr_id}_scoping_doc.md"
    output_path.write_text(content, encoding="utf-8")
    return output_path
