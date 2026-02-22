"""Generate the full TRR draft markdown from project state via Jinja2."""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from core.models import ProjectState


def get_templates_dir() -> Path:
    """Return the templates/ directory path."""
    return Path(__file__).resolve().parent.parent / "templates"


def generate_trr_draft(state: ProjectState) -> str:
    """Render the full TRR draft markdown.

    Always works regardless of phase — missing data renders with [TODO] markers.
    """
    env = Environment(
        loader=FileSystemLoader(str(get_templates_dir())),
        keep_trailing_newline=True,
    )
    template = env.get_template("trr_draft.md.j2")

    # Build title: "Technique Name" or fallback
    title = state.basic_questions.technique_name or f"{state.meta.technique_id} Research Report"

    return template.render(
        title=title,
        trr_id=state.meta.trr_id,
        technique_id=state.meta.technique_id,
        tactics=state.basic_questions.tactics,
        platforms=state.basic_questions.platforms,
        contributors=state.meta.contributors,
        scoping=state.scoping,
        basic_questions=state.basic_questions,
        procedures=state.procedures,
        emulation_tests=state.emulation_tests,
        references=state.references,
        notes=state.notes,
    )


def write_trr_draft(state: ProjectState, output_dir: Path) -> Path:
    """Generate and write the TRR draft to disk."""
    content = generate_trr_draft(state)
    output_path = output_dir / f"{state.meta.trr_id}_trr_draft.md"
    output_path.write_text(content, encoding="utf-8")
    return output_path
