from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BUILDS = ROOT / "builds"
CANDIDATE = "stacks-errata-a04446e-r28"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def artifact(path: Path) -> dict:
    return {
        "bytes": path.stat().st_size,
        "path": path.relative_to(ROOT).as_posix(),
        "sha256": sha256(path),
    }


def main() -> int:
    config = load(ROOT / "candidate.config.json")
    source_validation = load(ROOT / "source-validation.json")
    execution = load(BUILDS / "build-execution.json")
    deterministic = load(BUILDS / "deterministic-replay.json")
    receipt = load(BUILDS / "build-receipt.json")
    page_map = load(BUILDS / "source-page-map.json")
    visual = load(BUILDS / "visual-qa.json")
    if config["candidate_id"] != CANDIDATE or config["operation_count"] != 1:
        raise AssertionError("candidate configuration mismatch")
    for name, row in (
        ("source validation", source_validation),
        ("build execution", execution),
        ("deterministic replay", deterministic),
        ("build receipt", receipt),
        ("visual QA", visual),
    ):
        if row.get("candidate_id") != CANDIDATE or row.get("passed") is not True:
            raise AssertionError(f"{name} is stale or failed")

    if page_map.get("candidate_id") != CANDIDATE:
        raise AssertionError("source-page map is stale")

    if page_map["unique_pages"] != [16] or len(page_map["operations"]) != 1:
        raise AssertionError("source-page mapping mismatch")
    if page_map["operations"][0]["stable_id"] != "MC-STK-ERR-1216":
        raise AssertionError("source-page map stable ID mismatch")
    configured_map = config["visual_qa"]["source_page_map"]
    if (
        configured_map["bytes"] != (BUILDS / "source-page-map.json").stat().st_size
        or configured_map["sha256"] != sha256(BUILDS / "source-page-map.json")
        or config["visual_qa"]["correction_sensitive_pages"]["smoothing"] != [16]
        or config["visual_qa"]["high_resolution_pages"]["smoothing"] != [16]
    ):
        raise AssertionError("visual-page configuration is stale")

    chapter = receipt["chapters"][0]
    if chapter["stem"] != "smoothing" or chapter["candidate_log_summary"]["pages"] != 37:
        raise AssertionError("build chapter/page closure mismatch")
    if chapter["authority_log_summary"]["pages"] != 37 or chapter["candidate_page_delta_matches"] is not True:
        raise AssertionError("authority/candidate page comparison failed")
    if chapter["candidate_log_summary"]["fatal_markers"] or chapter["candidate_log_summary"]["missing_glyph_markers"]:
        raise AssertionError("candidate log has fatal or missing-glyph markers")
    if chapter["undefined_target_multisets_match_authority"] is not True:
        raise AssertionError("bounded cross-chapter reference multiset changed")
    if chapter["candidate_pdf"]["sha256"] != sha256(BUILDS / "smoothing.pdf"):
        raise AssertionError("candidate PDF binding mismatch")
    if chapter["authority_pdf"]["sha256"] != sha256(BUILDS / "smoothing.authority.pdf"):
        raise AssertionError("authority PDF binding mismatch")

    replay_rows = deterministic["pdfs"]
    if (
        deterministic.get("fresh_builds_compared") != 2
        or {(row["stem"], row["phase"]) for row in replay_rows}
        != {("smoothing", "candidate"), ("smoothing", "authority")}
        or any(row["byte_identical"] is not True for row in replay_rows)
    ):
        raise AssertionError("non-deterministic candidate or authority build")
    visual_pdf = visual["pdfs"][0]
    if (
        visual_pdf["stem"] != "smoothing"
        or visual_pdf["pages"] != 37
        or visual_pdf["full_page_render_count"] != 37
        or visual_pdf["manual_findings"]["passed"] is not True
        or visual_pdf["manual_findings"]["high_resolution_pages_inspected"] != [16]
        or visual_pdf["malformed_link_rectangles"]
        or visual_pdf["out_of_bounds_link_rectangles"]
        or visual_pdf["unembedded_fonts"]
        or visual_pdf["fonts_without_tounicode"]
    ):
        raise AssertionError("PDF/render/visual gate failed")

    # All public text evidence must be sanitized. Binary PDFs and TeX sources are
    # checked for credential patterns separately without decoding assumptions.
    forbidden = [
        re.compile(rb"C:[\\/]Users[\\/]", re.I),
        re.compile(rb"gh[pousr]_[A-Za-z0-9_]{20,}"),
        re.compile(rb"zenodo.*access[_ -]?token", re.I),
    ]
    hygiene_hits: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        data = path.read_bytes()
        if any(pattern.search(data) for pattern in forbidden):
            hygiene_hits.append(path.relative_to(ROOT).as_posix())
    if hygiene_hits:
        raise AssertionError(f"public hygiene failure: {hygiene_hits}")

    report = {
        "schema": "mathematics-commons-stacks-r28-validation/v1",
        "candidate_id": CANDIDATE,
        "passed": True,
        "checks": {
            "build_receipt": artifact(BUILDS / "build-receipt.json"),
            "composition_projection": artifact(ROOT / "composition-projection/smoothing.tex"),
            "deterministic_replay": artifact(BUILDS / "deterministic-replay.json"),
            "operation_count": 1,
            "pdf_pages": 37,
            "public_hygiene": {"forbidden_hits": [], "passed": True},
            "source_page_map": artifact(BUILDS / "source-page-map.json"),
            "source_validation": artifact(ROOT / "source-validation.json"),
            "stable_ids": ["MC-STK-ERR-1216"],
            "supersedes_unit_id": "MC-STK-ERR-1183",
            "visual_qa": artifact(BUILDS / "visual-qa.json"),
        },
    }
    output = BUILDS / "validation.json"
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="",
    )
    print(json.dumps({"passed": True, "validation_sha256": sha256(output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
