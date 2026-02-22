#!/usr/bin/env python3
"""TRR Research Assistant — CLI entry point.

A CLI tool that structures the non-DDM portions of the TRR research
methodology. It tracks phases, manages scoping artifacts, documents
procedures, runs validation checklists, and generates TRR drafts.

Usage:
    python trr_research.py [--project TRR_ID] <command> [args...]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Add tool root to path so core/generators/etc. can be imported
TOOL_ROOT = Path(__file__).resolve().parent
if str(TOOL_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOL_ROOT))

from core.models import (
    PLATFORM_ABBREVIATIONS,
    Constraint,
    EmulationTest,
    Exclusion,
    Note,
    Procedure,
    ProjectState,
    Reference,
    next_constraint_id,
    next_note_id,
    next_procedure_letter,
    next_reference_id,
    now_iso,
)
from core.phases import (
    PHASE_ORDER,
    check_gate,
    check_understanding_gate,
    complete_phase,
    get_current_phase,
)
from core.project import (
    create_project,
    list_projects,
    load_project,
    resolve_project,
    save_project,
    set_active,
)
from validators.completeness import (
    CHECK_ALIASES,
    is_accuracy_check,
    is_completeness_check,
    parse_check_value,
    resolve_check_name,
    run_accuracy,
    run_all,
    run_completeness,
    set_check,
)


# ─────────────────────────────────────────────────────────────────────
# Helper: resolve project from context
# ─────────────────────────────────────────────────────────────────────

def _get_project(ctx) -> tuple[str, ProjectState]:
    """Resolve and load the active project from Click context."""
    project_id = resolve_project(ctx.obj.get("project_id"))
    state = load_project(project_id)
    return project_id, state


# ─────────────────────────────────────────────────────────────────────
# Root CLI group
# ─────────────────────────────────────────────────────────────────────

@click.group()
@click.option("-P", "--project", "project_id", default=None, help="Project ID (TRR ID)")
@click.pass_context
def cli(ctx, project_id):
    """TRR Research Assistant — structure your technique research."""
    ctx.ensure_object(dict)
    ctx.obj["project_id"] = project_id


# ─────────────────────────────────────────────────────────────────────
# PROJECT MANAGEMENT
# ─────────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("technique_id")
@click.option("-n", "--name", required=True, help="Technique name")
@click.option("-p", "--platform", required=True, help="Platform (windows, linux, macos, ad, azure, aws, gcp, k8s, network)")
@click.option("--trr-id", required=True, help="TRR identifier (e.g. TRR0028)")
def init(technique_id, name, platform, trr_id):
    """Create a new project and set it as active."""
    try:
        state = create_project(technique_id, name, platform, trr_id)
        click.echo(f"✅ Created project {trr_id} ({technique_id} — {name})")
        click.echo(f"   Platform: {platform} ({state.meta.platform_abbrev})")
        click.echo(f"   Active project set to: {trr_id}")
    except (ValueError, FileExistsError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("trr_id")
def use(trr_id):
    """Set active project."""
    try:
        load_project(trr_id)  # Verify it exists
        set_active(trr_id)
        click.echo(f"Active project: {trr_id}")
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def status(ctx):
    """Show active project status."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    phase = get_current_phase(state)
    click.echo(f"Project:      {state.meta.trr_id}")
    click.echo(f"Technique:    {state.meta.technique_id} — {state.meta.technique_name}")
    click.echo(f"Platform:     {state.meta.platform} ({state.meta.platform_abbrev})")
    click.echo(f"Phase:        {phase}")
    click.echo(f"Procedures:   {len(state.procedures)}")
    click.echo(f"References:   {len(state.references)}")
    click.echo(f"Sources:      {len(state.source_library)}")
    click.echo(f"Tests:        {len(state.emulation_tests)}")
    click.echo(f"Notes:        {len(state.notes)}")
    click.echo(f"Last modified: {state.meta.last_modified}")

    if state.meta.contributors:
        click.echo(f"Contributors: {', '.join(state.meta.contributors)}")


@cli.command("list")
def list_cmd():
    """List all projects."""
    projects = list_projects()
    if not projects:
        click.echo("No projects found.")
        return

    # Table header
    click.echo(f"{'TRR ID':<12} {'Technique':<20} {'Platform':<10} {'Phase':<16} {'Modified'}")
    click.echo(f"{'─'*12} {'─'*20} {'─'*10} {'─'*16} {'─'*20}")
    for p in projects:
        name = p["technique_name"][:20] if p["technique_name"] else ""
        click.echo(
            f"{p['trr_id']:<12} {name:<20} {p['platform']:<10} "
            f"{p['current_phase']:<16} {p['last_modified'][:19]}"
        )


# ─────────────────────────────────────────────────────────────────────
# IMPORT: auto-advance and summary helpers
# ─────────────────────────────────────────────────────────────────────

def _auto_advance_phases(state):
    """After import, check phase gates and auto-advance through any
    phases whose requirements are already satisfied.

    Returns a list of (phase_name, status) tuples describing what happened.
    """
    advanced = []

    # Only auto-advance from understanding — that's the only phase
    # the scraper can fully populate. Scoping, procedures, and validation
    # require human/AI judgment that the scraper doesn't provide.
    if state.phases.understanding.status != "complete":
        passed, errors, warnings = check_understanding_gate(state)
        if passed:
            state.phases.understanding.status = "complete"
            state.phases.understanding.completed_at = now_iso()
            state.phases.scoping.status = "in_progress"
            advanced.append(("understanding", "auto-completed"))
        else:
            state.phases.understanding.status = "in_progress"
            advanced.append(("understanding", "in_progress — missing fields"))

    return advanced


def _truncate(text, max_len):
    """Truncate text with ellipsis if longer than max_len."""
    if not text:
        return ""
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."


def _print_import_summary(state, import_stats, advanced_phases):
    """Print structured post-import summary."""
    click.echo("")
    click.echo("   Import Summary")
    click.echo("   " + "─" * 42)
    click.echo(f"   Sources:       {import_stats['sources_added']} added, {import_stats['sources_skipped']} skipped")
    click.echo(f"   Emulation:     {import_stats['tests_added']} test(s) from Atomic Red Team")
    click.echo(f"   References:    {import_stats['references_added']} from MITRE ATT&CK")
    click.echo(f"   Related TRRs:  {import_stats['related_trrs']}")
    click.echo(f"   Related DDMs:  {import_stats['related_ddms']}")

    # Understanding phase status
    click.echo("")
    bq = state.basic_questions
    understanding_status = state.phases.understanding.status

    if understanding_status == "complete":
        click.echo("   Understanding Phase — auto-completed ✓")
    else:
        click.echo("   Understanding Phase — needs attention")
    click.echo("   " + "─" * 42)

    # Show each field with its value and status
    fields = [
        ("Technique",     bq.technique_name,      bool(bq.technique_name)),
        ("Tactics",       ", ".join(bq.tactics) if bq.tactics else "",  bool(bq.tactics)),
        ("Platforms",     ", ".join(bq.platforms) if bq.platforms else "", bool(bq.platforms)),
        ("Objective",     _truncate(bq.attacker_objective, 60), bool(bq.attacker_objective)),
        ("Prerequisites", bq.prerequisites,        bool(bq.prerequisites)),
        ("Why Used",      bq.why_used or "[empty]", bool(bq.why_used)),
    ]

    for label, value, filled in fields:
        marker = "✓" if filled else "✗"
        click.echo(f"   {marker} {label + ':':16s} {value}")

    # Warnings for seeded fields that might need refinement
    click.echo("")
    if bq.attacker_objective and len(bq.attacker_objective) > 100:
        click.echo("   ⚠ attacker_objective was seeded from MITRE description.")
        click.echo('     Consider refining: understand set attacker_objective "..."')

    if import_stats.get("prerequisites_seeded") and bq.prerequisites and len(bq.prerequisites) < 30:
        click.echo("   ⚠ prerequisites was seeded from MITRE permissions_required (just privilege levels).")
        click.echo('     Consider expanding: understand set prerequisites "..."')

    if not bq.why_used:
        click.echo("   ⚠ why_used is empty (optional).")
        click.echo('     Set with: understand set why_used "..."')

    if not bq.prerequisites:
        click.echo("   ⚠ prerequisites is empty — MITRE had no permissions_required.")
        click.echo('     Set with: understand set prerequisites "..."')

    # Missing required fields (gate failed)
    if understanding_status != "complete":
        missing = []
        if not bq.technique_name: missing.append("technique_name")
        if not bq.tactics: missing.append("tactics")
        if not bq.platforms: missing.append("platforms")
        if not bq.attacker_objective: missing.append("attacker_objective")
        if not bq.prerequisites: missing.append("prerequisites")

        if missing:
            click.echo("")
            click.echo(f"   ✗ Cannot auto-advance: missing {', '.join(missing)}")
            for field in missing:
                click.echo(f'     understand set {field} "..."')
            click.echo("     understand complete")

    # Current phase and next steps
    click.echo("")
    current = get_current_phase(state)
    click.echo(f"   Current Phase: {current}")
    click.echo("   " + "─" * 42)

    if current == "scoping":
        click.echo("   Next steps:")
        click.echo('     scope set-statement "..."')
        click.echo('     scope add-exclusion "..." --rationale "..."')
        click.echo('     scope add-constraint "..." --essential --immutable --observable --telemetry "..."')
    elif current == "understanding":
        click.echo("   Next steps:")
        click.echo("     Fill missing fields listed above, then:")
        click.echo("     understand complete")


# ─────────────────────────────────────────────────────────────────────
# IMPORT
# ─────────────────────────────────────────────────────────────────────

@cli.command("import")
@click.argument("json_path", type=click.Path(exists=True))
@click.option("--replace", is_flag=True, default=False, help="Overwrite imported data instead of merging")
@click.pass_context
def import_cmd(ctx, json_path, replace):
    """Import scraper JSON output."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    from importers.scraper_import import import_scraper_json

    state, summary = import_scraper_json(state, Path(json_path), replace=replace)
    advanced = _auto_advance_phases(state)
    save_project(project_id, state)

    mode = "replace" if replace else "merge"
    click.echo(f"✅ Imported scraper data ({mode} mode, v{summary['version']})")
    _print_import_summary(state, summary, advanced)


# ─────────────────────────────────────────────────────────────────────
# METADATA
# ─────────────────────────────────────────────────────────────────────

@cli.group()
def meta():
    """Project metadata commands."""
    pass


@meta.command("set-contributors")
@click.argument("names")
@click.pass_context
def meta_set_contributors(ctx, names):
    """Set contributors (comma-separated names)."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    state.meta.contributors = [n.strip() for n in names.split(",") if n.strip()]
    save_project(project_id, state)
    click.echo(f"Contributors: {', '.join(state.meta.contributors)}")


@meta.command("show")
@click.pass_context
def meta_show(ctx):
    """Display project metadata."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    m = state.meta
    click.echo(f"TRR ID:       {m.trr_id}")
    click.echo(f"Technique:    {m.technique_id} — {m.technique_name}")
    click.echo(f"Platform:     {m.platform} ({m.platform_abbrev})")
    click.echo(f"Contributors: {', '.join(m.contributors) if m.contributors else '(none)'}")
    click.echo(f"Created:      {m.created}")
    click.echo(f"Modified:     {m.last_modified}")
    if m.scraper_import:
        click.echo(f"Import:       v{m.scraper_import.report_version} from {m.scraper_import.source_file}")
        click.echo(f"              at {m.scraper_import.imported_at}")


# ─────────────────────────────────────────────────────────────────────
# UNDERSTANDING PHASE
# ─────────────────────────────────────────────────────────────────────

@cli.group()
def understand():
    """Understanding phase commands."""
    pass


# Fields that accept comma-separated lists
_LIST_FIELDS = {"tactics", "platforms"}
_STRING_FIELDS = {"technique_name", "attacker_objective", "why_used", "prerequisites"}
_ALL_BQ_FIELDS = _LIST_FIELDS | _STRING_FIELDS


@understand.command("set")
@click.argument("field")
@click.argument("value")
@click.pass_context
def understand_set(ctx, field, value):
    """Set a basic question field.

    String fields: technique_name, attacker_objective, why_used, prerequisites.
    List fields (comma-separated): tactics, platforms.
    """
    if field not in _ALL_BQ_FIELDS:
        click.echo(f"Error: Unknown field '{field}'. Valid: {', '.join(sorted(_ALL_BQ_FIELDS))}", err=True)
        sys.exit(1)

    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    if field in _LIST_FIELDS:
        parsed = [v.strip() for v in value.split(",") if v.strip()]
        setattr(state.basic_questions, field, parsed)
        click.echo(f"{field}: {', '.join(parsed)}")
    else:
        setattr(state.basic_questions, field, value)
        click.echo(f"{field}: {value}")

    save_project(project_id, state)


@understand.command("show")
@click.pass_context
def understand_show(ctx):
    """Display current basic questions and answers."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    bq = state.basic_questions
    labels = [
        ("technique_name", "Technique Name"),
        ("tactics", "Tactics"),
        ("platforms", "Platforms"),
        ("attacker_objective", "Attacker Objective"),
        ("why_used", "Why Adversaries Use This"),
        ("prerequisites", "Prerequisites"),
    ]
    for field, label in labels:
        val = getattr(bq, field)
        if isinstance(val, list):
            display = ", ".join(val) if val else "[TODO]"
        else:
            display = val if val else "[TODO]"
        click.echo(f"  {label}: {display}")


@understand.command("complete")
@click.option("--force", is_flag=True, default=False, help="Force completion past gate check")
@click.pass_context
def understand_complete(ctx, force):
    """Mark understanding phase complete. Runs gate check."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    success, errors, warnings = complete_phase(state, "understanding", force=force)

    for w in warnings:
        click.echo(f"  ⚠ {w}")

    if not success:
        click.echo("❌ Gate check failed:")
        for err in errors:
            click.echo(f"  ✗ {err}")
        click.echo("\nUse --force to override.")
        sys.exit(2)

    save_project(project_id, state)
    if force and errors:
        click.echo("⚠ Understanding phase completed with --force (gate issues overridden):")
        for err in errors:
            click.echo(f"  ✗ {err}")
    else:
        click.echo("✅ Understanding phase complete. Now in: scoping")


# ─────────────────────────────────────────────────────────────────────
# SCOPING PHASE
# ─────────────────────────────────────────────────────────────────────

@cli.group()
def scope():
    """Scoping phase commands."""
    pass


@scope.command("set-statement")
@click.argument("statement")
@click.pass_context
def scope_set_statement(ctx, statement):
    """Set the scope statement."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    state.scoping.scope_statement = statement
    save_project(project_id, state)
    click.echo(f"Scope statement: {statement}")


@scope.command("add-exclusion")
@click.argument("item")
@click.option("--rationale", required=True, help="Reason for exclusion")
@click.pass_context
def scope_add_exclusion(ctx, item, rationale):
    """Add an exclusion to the table."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    state.scoping.exclusions.append(Exclusion(item=item, rationale=rationale))
    save_project(project_id, state)
    idx = len(state.scoping.exclusions)
    click.echo(f"Added exclusion #{idx}: {item} — {rationale}")


@scope.command("remove-exclusion")
@click.argument("index", type=int)
@click.pass_context
def scope_remove_exclusion(ctx, index):
    """Remove an exclusion by display index (1-based)."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    if index < 1 or index > len(state.scoping.exclusions):
        click.echo(f"Error: Invalid index {index}. Range: 1-{len(state.scoping.exclusions)}", err=True)
        sys.exit(1)

    removed = state.scoping.exclusions.pop(index - 1)
    save_project(project_id, state)
    click.echo(f"Removed exclusion #{index}: {removed.item}")


@scope.command("add-constraint")
@click.argument("constraint_text")
@click.option("--essential/--not-essential", default=True, help="Essential constraint (default: true)")
@click.option("--immutable/--not-immutable", default=True, help="Immutable constraint (default: true)")
@click.option("--observable/--not-observable", default=False, help="Observable constraint (default: false)")
@click.option("--telemetry", default="", help="Telemetry sources")
@click.pass_context
def scope_add_constraint(ctx, constraint_text, essential, immutable, observable, telemetry):
    """Add a constraint. Auto-assigns ID (C1, C2, ...)."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    cid = next_constraint_id(state.scoping.constraints)
    constraint = Constraint(
        id=cid,
        constraint=constraint_text,
        essential=essential,
        immutable=immutable,
        observable=observable,
        telemetry=telemetry,
    )
    state.scoping.constraints.append(constraint)
    save_project(project_id, state)
    click.echo(f"Added constraint {cid}: {constraint_text}")
    flags = []
    if essential:
        flags.append("essential")
    if immutable:
        flags.append("immutable")
    if observable:
        flags.append("observable")
    click.echo(f"  Flags: {', '.join(flags) if flags else '(none)'}")
    if telemetry:
        click.echo(f"  Telemetry: {telemetry}")


@scope.command("remove-constraint")
@click.argument("constraint_id")
@click.pass_context
def scope_remove_constraint(ctx, constraint_id):
    """Remove a constraint by ID (e.g. C1)."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    original_len = len(state.scoping.constraints)
    state.scoping.constraints = [c for c in state.scoping.constraints if c.id != constraint_id]

    if len(state.scoping.constraints) == original_len:
        click.echo(f"Error: Constraint {constraint_id} not found.", err=True)
        sys.exit(1)

    save_project(project_id, state)
    click.echo(f"Removed constraint {constraint_id}")


@scope.command("show")
@click.pass_context
def scope_show(ctx):
    """Display scope statement, exclusions, and constraints."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    s = state.scoping
    click.echo(f"Scope Statement: {s.scope_statement or '[TODO]'}")
    click.echo("")

    if s.exclusions:
        click.echo("Exclusions:")
        for i, ex in enumerate(s.exclusions, 1):
            click.echo(f"  {i}. {ex.item} — {ex.rationale}")
    else:
        click.echo("Exclusions: (none)")

    click.echo("")

    if s.constraints:
        click.echo("Constraints:")
        for c in s.constraints:
            flags = []
            if c.essential:
                flags.append("essential")
            if c.immutable:
                flags.append("immutable")
            if c.observable:
                flags.append("observable")
            click.echo(f"  {c.id}: {c.constraint}")
            click.echo(f"       Flags: {', '.join(flags)} | Telemetry: {c.telemetry or '(none)'}")
    else:
        click.echo("Constraints: (none)")


@scope.command("complete")
@click.option("--force", is_flag=True, default=False, help="Force completion past gate check")
@click.pass_context
def scope_complete(ctx, force):
    """Mark scoping phase complete. Runs gate check."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    success, errors, warnings = complete_phase(state, "scoping", force=force)

    for w in warnings:
        click.echo(f"  ⚠ {w}")

    if not success:
        click.echo("❌ Gate check failed:")
        for err in errors:
            click.echo(f"  ✗ {err}")
        click.echo("\nUse --force to override.")
        sys.exit(2)

    save_project(project_id, state)
    if force and errors:
        click.echo("⚠ Scoping phase completed with --force (gate issues overridden):")
        for err in errors:
            click.echo(f"  ✗ {err}")
    else:
        click.echo("✅ Scoping phase complete. Now in: procedures")


# ─────────────────────────────────────────────────────────────────────
# PROCEDURES PHASE
# ─────────────────────────────────────────────────────────────────────

@cli.group()
def proc():
    """Procedure commands."""
    pass


@proc.command("add")
@click.argument("name")
@click.option("--summary", default="", help="Procedure summary")
@click.option("--distinguishing", default="", help="Distinguishing operations")
@click.pass_context
def proc_add(ctx, name, summary, distinguishing):
    """Add a procedure. ID auto-generated (e.g. TRR0028.AD.A)."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    letter = next_procedure_letter(state.procedures)
    proc_id = f"{state.meta.trr_id}.{state.meta.platform_abbrev}.{letter}"

    procedure = Procedure(
        id=proc_id,
        letter=letter,
        name=name,
        summary=summary,
        distinguishing_operations=distinguishing,
    )
    state.procedures.append(procedure)
    save_project(project_id, state)
    click.echo(f"Added procedure {proc_id}: {name}")


@proc.command("edit")
@click.argument("proc_id")
@click.option("--name", default=None, help="Procedure name")
@click.option("--summary", default=None, help="Summary")
@click.option("--distinguishing", default=None, help="Distinguishing operations")
@click.option("--narrative", default=None, help="Full narrative text")
@click.option("--ddm-filename", default=None, help="DDM image filename")
@click.option("--ddm-description", default=None, help="DDM description")
@click.pass_context
def proc_edit(ctx, proc_id, name, summary, distinguishing, narrative, ddm_filename, ddm_description):
    """Edit fields on an existing procedure."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    target = None
    for p in state.procedures:
        if p.id == proc_id:
            target = p
            break

    if target is None:
        click.echo(f"Error: Procedure {proc_id} not found.", err=True)
        sys.exit(1)

    updates = []
    if name is not None:
        target.name = name
        updates.append("name")
    if summary is not None:
        target.summary = summary
        updates.append("summary")
    if distinguishing is not None:
        target.distinguishing_operations = distinguishing
        updates.append("distinguishing_operations")
    if narrative is not None:
        target.narrative = narrative
        updates.append("narrative")
    if ddm_filename is not None:
        target.ddm_filename = ddm_filename
        updates.append("ddm_filename")
    if ddm_description is not None:
        target.ddm_description = ddm_description
        updates.append("ddm_description")

    if not updates:
        click.echo("No fields updated. Provide at least one --flag.")
        sys.exit(1)

    save_project(project_id, state)
    click.echo(f"Updated {proc_id}: {', '.join(updates)}")


@proc.command("remove")
@click.argument("proc_id")
@click.pass_context
def proc_remove(ctx, proc_id):
    """Remove a procedure."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    original_len = len(state.procedures)
    state.procedures = [p for p in state.procedures if p.id != proc_id]

    if len(state.procedures) == original_len:
        click.echo(f"Error: Procedure {proc_id} not found.", err=True)
        sys.exit(1)

    # Warn about orphaned test mappings
    orphaned = [t for t in state.emulation_tests if t.procedure_mapping == proc_id]
    if orphaned:
        click.echo(f"  ⚠ {len(orphaned)} emulation test(s) were mapped to {proc_id}")

    save_project(project_id, state)
    click.echo(f"Removed procedure {proc_id}")


@proc.command("map-test")
@click.argument("procedure_id")
@click.argument("test_name")
@click.option("--manual", is_flag=True, default=False, help="Create manual entry if no match found")
@click.pass_context
def proc_map_test(ctx, procedure_id, test_name, manual):
    """Link an emulation test to a procedure. Substring-matches imported tests."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    # Verify procedure exists
    proc_exists = any(p.id == procedure_id for p in state.procedures)
    if not proc_exists:
        click.echo(f"Error: Procedure {procedure_id} not found.", err=True)
        sys.exit(1)

    # Search for matching test (substring, case-insensitive)
    search = test_name.lower()
    matches = [t for t in state.emulation_tests if search in t.name.lower()]

    if matches:
        for t in matches:
            t.procedure_mapping = procedure_id
        save_project(project_id, state)
        click.echo(f"Mapped {len(matches)} test(s) to {procedure_id}:")
        for t in matches:
            click.echo(f"  - {t.name}")
    elif manual:
        new_test = EmulationTest(
            name=test_name,
            source="manual",
            procedure_mapping=procedure_id,
        )
        state.emulation_tests.append(new_test)
        save_project(project_id, state)
        click.echo(f"Created manual test entry and mapped to {procedure_id}: {test_name}")
    else:
        click.echo(f"No tests matching '{test_name}' found.")
        click.echo("Use --manual to create a new manual entry.")
        sys.exit(1)


@proc.command("show")
@click.argument("proc_id", required=False, default=None)
@click.pass_context
def proc_show(ctx, proc_id):
    """Show all procedures, or detail for one."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    if proc_id:
        target = None
        for p in state.procedures:
            if p.id == proc_id:
                target = p
                break
        if not target:
            click.echo(f"Error: Procedure {proc_id} not found.", err=True)
            sys.exit(1)

        click.echo(f"Procedure: {target.id}")
        click.echo(f"  Name:            {target.name}")
        click.echo(f"  Summary:         {target.summary or '[TODO]'}")
        click.echo(f"  Distinguishing:  {target.distinguishing_operations or '[TODO]'}")
        click.echo(f"  Narrative:       {target.narrative or '[TODO]'}")
        click.echo(f"  DDM Filename:    {target.ddm_filename or '[TODO]'}")
        click.echo(f"  DDM Description: {target.ddm_description or '[TODO]'}")

        # Show mapped tests
        mapped = [t for t in state.emulation_tests if t.procedure_mapping == proc_id]
        if mapped:
            click.echo(f"  Mapped Tests:")
            for t in mapped:
                click.echo(f"    - {t.name} ({t.source})")
    else:
        if not state.procedures:
            click.echo("No procedures defined.")
            return
        click.echo(f"{'ID':<20} {'Name':<30} {'Summary'}")
        click.echo(f"{'─'*20} {'─'*30} {'─'*40}")
        for p in state.procedures:
            summary_preview = (p.summary[:40] + "...") if len(p.summary) > 40 else p.summary
            click.echo(f"{p.id:<20} {p.name:<30} {summary_preview or '[TODO]'}")


@proc.command("complete")
@click.option("--force", is_flag=True, default=False, help="Force completion past gate check")
@click.pass_context
def proc_complete(ctx, force):
    """Mark procedures phase complete. Runs gate check."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    success, errors, warnings = complete_phase(state, "procedures", force=force)

    for w in warnings:
        click.echo(f"  ⚠ {w}")

    if not success:
        click.echo("❌ Gate check failed:")
        for err in errors:
            click.echo(f"  ✗ {err}")
        click.echo("\nUse --force to override.")
        sys.exit(2)

    save_project(project_id, state)
    if force and errors:
        click.echo("⚠ Procedures phase completed with --force (gate issues overridden):")
        for err in errors:
            click.echo(f"  ✗ {err}")
    else:
        click.echo("✅ Procedures phase complete. Now in: validation")


# ─────────────────────────────────────────────────────────────────────
# VALIDATION
# ─────────────────────────────────────────────────────────────────────

@cli.group()
def validate():
    """Validation commands."""
    pass


@validate.command("completeness")
@click.pass_context
def validate_completeness(ctx):
    """Run completeness checklist."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    results = run_completeness(state)
    click.echo("Completeness Checklist:")
    for r in results:
        click.echo(f"  {r['icon']} {r['label']} ({r['status']})")


@validate.command("accuracy")
@click.pass_context
def validate_accuracy(ctx):
    """Run accuracy checklist."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    results = run_accuracy(state)
    click.echo("Accuracy Checklist:")
    for r in results:
        click.echo(f"  {r['icon']} {r['label']} ({r['status']})")


@validate.command("all")
@click.pass_context
def validate_all(ctx):
    """Run both checklists."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    results = run_all(state)

    click.echo("Completeness Checklist:")
    for r in results["completeness"]:
        click.echo(f"  {r['icon']} {r['label']} ({r['status']})")

    click.echo("")
    click.echo("Accuracy Checklist:")
    for r in results["accuracy"]:
        click.echo(f"  {r['icon']} {r['label']} ({r['status']})")


@validate.command("set")
@click.argument("check")
@click.argument("value")
@click.pass_context
def validate_set(ctx, check, value):
    """Manually mark a check as pass, fail, or na."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    try:
        parsed = parse_check_value(value)
        set_check(state, check, parsed)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    save_project(project_id, state)
    canonical = resolve_check_name(check)
    click.echo(f"Set {canonical}: {value}")


# ─────────────────────────────────────────────────────────────────────
# GENERATION
# ─────────────────────────────────────────────────────────────────────

@cli.group()
def generate():
    """Generate documents from project state."""
    pass


@generate.command("scoping-doc")
@click.pass_context
def generate_scoping_doc(ctx):
    """Render scoping document."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    from generators.scoping import write_scoping_doc
    from core.project import get_projects_dir

    output_dir = get_projects_dir() / project_id
    path = write_scoping_doc(state, output_dir)
    click.echo(f"✅ Scoping document: {path}")


@generate.command("procedure-table")
@click.pass_context
def generate_procedure_table(ctx):
    """Render procedure summary table."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    from generators.procedure_table import write_procedure_table
    from core.project import get_projects_dir

    output_dir = get_projects_dir() / project_id
    path = write_procedure_table(state, output_dir)
    click.echo(f"✅ Procedure table: {path}")


@generate.command("trr-draft")
@click.pass_context
def generate_trr_draft(ctx):
    """Render full TRR draft markdown."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    from generators.trr_draft import write_trr_draft
    from core.project import get_projects_dir

    output_dir = get_projects_dir() / project_id
    path = write_trr_draft(state, output_dir)
    click.echo(f"✅ TRR draft: {path}")


# ─────────────────────────────────────────────────────────────────────
# REFERENCES
# ─────────────────────────────────────────────────────────────────────

@cli.group()
def ref():
    """Reference management commands."""
    pass


@ref.command("add")
@click.argument("name")
@click.option("--url", required=True, help="Reference URL")
@click.option("--section", default=None, help="TRR section (technique_overview, technical_background, procedures)")
@click.pass_context
def ref_add(ctx, name, url, section):
    """Add a reference. Auto-assigns ID (R001, R002, ...)."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    rid = next_reference_id(state.references)
    sections = [section] if section else []
    reference = Reference(
        id=rid,
        name=name,
        url=url,
        source="manual",
        used_in_sections=sections,
    )
    state.references.append(reference)
    save_project(project_id, state)
    click.echo(f"Added reference {rid}: {name}")
    click.echo(f"  URL: {url}")
    if section:
        click.echo(f"  Section: {section}")


@ref.command("list")
@click.pass_context
def ref_list(ctx):
    """Show all references."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    if not state.references:
        click.echo("No references.")
        return

    click.echo(f"{'ID':<6} {'Name':<35} {'Source':<15} {'Sections'}")
    click.echo(f"{'─'*6} {'─'*35} {'─'*15} {'─'*25}")
    for r in state.references:
        sections = ", ".join(r.used_in_sections) if r.used_in_sections else "(none)"
        name_display = (r.name[:35]) if len(r.name) > 35 else r.name
        click.echo(f"{r.id:<6} {name_display:<35} {r.source:<15} {sections}")


@ref.command("tag")
@click.argument("ref_id")
@click.option("--section", required=True, help="Section tag (technique_overview, technical_background, procedures)")
@click.pass_context
def ref_tag(ctx, ref_id, section):
    """Tag a reference as used in a TRR section."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    target = None
    for r in state.references:
        if r.id == ref_id:
            target = r
            break

    if not target:
        click.echo(f"Error: Reference {ref_id} not found.", err=True)
        sys.exit(1)

    if section not in target.used_in_sections:
        target.used_in_sections.append(section)

    save_project(project_id, state)
    click.echo(f"Tagged {ref_id} with section: {section}")


@ref.command("remove")
@click.argument("ref_id")
@click.pass_context
def ref_remove(ctx, ref_id):
    """Remove a reference by ID."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    original_len = len(state.references)
    state.references = [r for r in state.references if r.id != ref_id]

    if len(state.references) == original_len:
        click.echo(f"Error: Reference {ref_id} not found.", err=True)
        sys.exit(1)

    save_project(project_id, state)
    click.echo(f"Removed reference {ref_id}")


# ─────────────────────────────────────────────────────────────────────
# NOTES
# ─────────────────────────────────────────────────────────────────────

@cli.group()
def notes():
    """Research notes commands."""
    pass


@notes.command("add")
@click.argument("text")
@click.option("--phase", default=None, help="Phase tag (understanding, scoping, procedures)")
@click.pass_context
def notes_add(ctx, text, phase):
    """Add a freeform research note."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    # Default phase to current phase
    if phase is None:
        phase = get_current_phase(state)

    nid = next_note_id(state.notes)
    note = Note(
        id=nid,
        text=text,
        phase=phase,
        created_at=now_iso(),
    )
    state.notes.append(note)
    save_project(project_id, state)
    click.echo(f"Added note {nid} [{phase}]: {text}")


@notes.command("list")
@click.option("--phase", default=None, help="Filter by phase")
@click.pass_context
def notes_list(ctx, phase):
    """Show all notes, optionally filtered by phase."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    filtered = state.notes
    if phase:
        filtered = [n for n in filtered if n.phase == phase]

    if not filtered:
        click.echo("No notes." if not phase else f"No notes for phase: {phase}")
        return

    for n in filtered:
        click.echo(f"  {n.id} [{n.phase}] {n.text}")
        click.echo(f"       {n.created_at}")


@notes.command("remove")
@click.argument("note_id")
@click.pass_context
def notes_remove(ctx, note_id):
    """Remove a note by ID (e.g. N001)."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    original_len = len(state.notes)
    state.notes = [n for n in state.notes if n.id != note_id]

    if len(state.notes) == original_len:
        click.echo(f"Error: Note {note_id} not found.", err=True)
        sys.exit(1)

    save_project(project_id, state)
    click.echo(f"Removed note {note_id}")


# ─────────────────────────────────────────────────────────────────────
# TELEMETRY
# ─────────────────────────────────────────────────────────────────────

@cli.group()
def telemetry():
    """Telemetry catalog commands."""
    pass


def _load_platforms_catalog() -> dict:
    """Load config/platforms.json."""
    catalog_path = TOOL_ROOT / "config" / "platforms.json"
    return json.loads(catalog_path.read_text(encoding="utf-8"))


@telemetry.command("suggest")
@click.argument("operation_type")
@click.pass_context
def telemetry_suggest(ctx, operation_type):
    """Look up telemetry for an operation type on the project's platform."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    catalog = _load_platforms_catalog()
    platform = state.meta.platform

    if platform not in catalog:
        click.echo(f"No telemetry catalog for platform: {platform}")
        click.echo(f"Available: {', '.join(sorted(catalog.keys()))}")
        sys.exit(1)

    platform_data = catalog[platform]

    if operation_type not in platform_data:
        click.echo(f"Unknown operation type '{operation_type}' for {platform}.")
        click.echo(f"Available: {', '.join(sorted(platform_data.keys()))}")
        sys.exit(1)

    entry = platform_data[operation_type]
    click.echo(f"Telemetry for '{operation_type}' on {platform}:")
    for src in entry.get("sources", []):
        click.echo(f"  • {src}")
    if entry.get("notes"):
        click.echo(f"  Note: {entry['notes']}")


@telemetry.command("list")
@click.pass_context
def telemetry_list(ctx):
    """Show all operation types for the project's platform."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    catalog = _load_platforms_catalog()
    platform = state.meta.platform

    if platform not in catalog:
        click.echo(f"No telemetry catalog for platform: {platform}")
        click.echo(f"Available: {', '.join(sorted(catalog.keys()))}")
        sys.exit(1)

    platform_data = catalog[platform]
    click.echo(f"Operation types for {platform} ({len(platform_data)}):")
    for op_type in sorted(platform_data.keys()):
        source_count = len(platform_data[op_type].get("sources", []))
        click.echo(f"  {op_type} ({source_count} sources)")


# ─────────────────────────────────────────────────────────────────────
# EXPORT
# ─────────────────────────────────────────────────────────────────────

@cli.group()
def export():
    """Export commands."""
    pass


@export.command("state")
@click.pass_context
def export_state(ctx):
    """Dump state.json to stdout."""
    try:
        project_id, state = _get_project(ctx)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    click.echo(json.dumps(state.model_dump(mode="json"), indent=2, ensure_ascii=False))


# ─────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    cli()
