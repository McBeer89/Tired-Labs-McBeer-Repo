"""Render the procedure summary table from project state via Jinja2."""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from core.models import ProjectState


def get_templates_dir() -> Path:
    """Return the templates/ directory path."""
    return Path(__file__).resolve().parent.parent / "templates"


def generate_procedure_table(state: ProjectState) -> str:
    """Render the procedure summary table markdown."""
    env = Environment(
        loader=FileSystemLoader(str(get_templates_dir())),
        keep_trailing_newline=True,
    )
    template = env.get_template("procedure_table.md.j2")

    return template.render(
        meta=state.meta,
        procedures=state.procedures,
        tactics=state.basic_questions.tactics,
    )


def write_procedure_table(state: ProjectState, output_dir: Path) -> Path:
    """Generate and write the procedure table to disk."""
    content = generate_procedure_table(state)
    output_path = output_dir / f"{state.meta.trr_id}_procedure_table.md"
    output_path.write_text(content, encoding="utf-8")
    return output_path
