"""Parse trr-source-scraper JSON output and merge into project state."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from core.models import (
    EmulationTest,
    Reference,
    ScraperImportInfo,
    SourceLibraryEntry,
    now_iso,
    next_reference_id,
)

# Tested scraper versions — warn (non-blocking) if unrecognized
TESTED_VERSIONS = {"1.3", "1.4"}


def _normalize_url(url: str) -> str:
    """Normalize a URL for dedup comparison (lowercase, strip trailing slash)."""
    if not url:
        return ""
    return url.lower().rstrip("/")


def _existing_urls(items, url_attr: str = "url") -> set[str]:
    """Collect normalized URLs from a list of objects."""
    urls = set()
    for item in items:
        u = getattr(item, url_attr, "") if hasattr(item, url_attr) else item.get(url_attr, "")
        norm = _normalize_url(u)
        if norm:
            urls.add(norm)
    return urls


def import_scraper_json(state, json_path: Path, replace: bool = False):
    """Import scraper JSON output into project state.

    Args:
        state: ProjectState to merge into
        json_path: Path to the scraper's JSON output file
        replace: If True, overwrite imported data. If False (default), merge.

    Returns:
        (state, summary_dict) — updated state and import statistics.
    """
    raw = json.loads(json_path.read_text(encoding="utf-8"))

    # Version check
    version = raw.get("report_version", "unknown")
    if version not in TESTED_VERSIONS:
        print(
            f"⚠ Warning: Scraper report version '{version}' has not been tested. "
            f"Tested versions: {', '.join(sorted(TESTED_VERSIONS))}. "
            "Proceeding anyway.",
            file=sys.stderr,
        )

    technique_info = raw.get("technique_info") or {}

    summary = {
        "sources_added": 0,
        "sources_skipped": 0,
        "tests_added": 0,
        "tests_skipped": 0,
        "references_added": 0,
        "references_skipped": 0,
        "related_trrs": 0,
        "related_ddms": 0,
        "version": version,
        "prerequisites_seeded": False,
    }

    # --- Seed basic_questions (only if field is empty or replace=True) ---
    bq = state.basic_questions

    ti_name = technique_info.get("name", "")
    if ti_name and (not bq.technique_name or replace):
        bq.technique_name = ti_name

    ti_tactics = technique_info.get("tactics", [])
    if ti_tactics and (not bq.tactics or replace):
        bq.tactics = ti_tactics

    ti_platforms = technique_info.get("platforms", [])
    if ti_platforms and (not bq.platforms or replace):
        bq.platforms = ti_platforms

    ti_desc = technique_info.get("description", "")
    if ti_desc and (not bq.attacker_objective or replace):
        bq.attacker_objective = ti_desc

    ti_perms = technique_info.get("permissions_required", [])
    if ti_perms and (not bq.prerequisites or replace):
        bq.prerequisites = ", ".join(ti_perms)
        summary["prerequisites_seeded"] = True

    # --- Telemetry hints ---
    ti_data_sources = technique_info.get("data_sources", [])
    if ti_data_sources:
        existing_hints = set(state.telemetry_hints)
        for ds in ti_data_sources:
            if ds and ds not in existing_hints:
                state.telemetry_hints.append(ds)
                existing_hints.add(ds)

    # --- References from technique_info.references ---
    ti_refs = technique_info.get("references", [])
    existing_ref_urls = _existing_urls(state.references)
    for ref_data in ti_refs:
        ref_url = ref_data.get("url", "")
        if not ref_url:
            continue
        if _normalize_url(ref_url) in existing_ref_urls and not replace:
            summary["references_skipped"] += 1
            continue
        ref_name = ref_data.get("source_name", "") or ref_data.get("description", "") or ref_url
        new_ref = Reference(
            id=next_reference_id(state.references),
            name=ref_name,
            url=ref_url,
            source="scraper_import",
        )
        state.references.append(new_ref)
        existing_ref_urls.add(_normalize_url(ref_url))
        summary["references_added"] += 1

    # --- Existing TRRs ---
    existing_trrs = raw.get("existing_trrs", [])
    if replace:
        state.related_trrs = existing_trrs
    else:
        existing_trr_ids = {t.get("trr_id", "") for t in state.related_trrs}
        for trr in existing_trrs:
            tid = trr.get("trr_id", "")
            if tid and tid not in existing_trr_ids:
                state.related_trrs.append(trr)
                existing_trr_ids.add(tid)
    summary["related_trrs"] = len(existing_trrs)

    # --- Existing DDMs ---
    existing_ddms = raw.get("existing_ddms", [])
    if replace:
        state.related_ddms = existing_ddms
    else:
        existing_ddm_files = {d.get("file_name", "") for d in state.related_ddms}
        for ddm in existing_ddms:
            fname = ddm.get("file_name", "")
            if fname and fname not in existing_ddm_files:
                state.related_ddms.append(ddm)
                existing_ddm_files.add(fname)
    summary["related_ddms"] = len(existing_ddms)

    # --- Atomic tests → emulation_tests ---
    atomic_tests = raw.get("atomic_tests", [])
    existing_test_guids = {t.atomic_guid for t in state.emulation_tests if t.atomic_guid}
    existing_test_names = {t.name for t in state.emulation_tests}

    for test in atomic_tests:
        guid = test.get("auto_generated_guid", "")
        name = test.get("name", "Unnamed Test")

        # Dedup by GUID first, then by name
        if guid and guid in existing_test_guids and not replace:
            summary["tests_skipped"] += 1
            continue
        if not guid and name in existing_test_names and not replace:
            summary["tests_skipped"] += 1
            continue

        new_test = EmulationTest(
            name=name,
            source="Atomic Red Team",
            atomic_guid=guid,
            github_url=test.get("github_url", ""),
        )
        state.emulation_tests.append(new_test)
        if guid:
            existing_test_guids.add(guid)
        existing_test_names.add(name)
        summary["tests_added"] += 1

    # --- Search results → source_library (flatten all categories) ---
    search_results = raw.get("search_results", {})
    existing_source_urls = _existing_urls(state.source_library)

    for category, results in search_results.items():
        for result in results:
            url = result.get("url", "")
            if not url:
                continue
            if _normalize_url(url) in existing_source_urls and not replace:
                summary["sources_skipped"] += 1
                continue

            entry = SourceLibraryEntry(
                title=result.get("title", ""),
                url=url,
                category=category,
                relevance_score=result.get("relevance_score", 0.0),
                domain=result.get("domain", ""),
            )
            state.source_library.append(entry)
            existing_source_urls.add(_normalize_url(url))
            summary["sources_added"] += 1

    # --- Record import metadata ---
    state.meta.scraper_import = ScraperImportInfo(
        source_file=str(json_path),
        imported_at=now_iso(),
        report_version=version,
    )

    return state, summary
