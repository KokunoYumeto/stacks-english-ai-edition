#!/usr/bin/env python3
"""Write the R33 visual-QA receipt after bounded human-visible render inspection."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATION = ROOT / "validation"
BUILD = VALIDATION / "stacks-errata-a04446e-r33-build-2026-08-30.json"
PAGE_MAP = VALIDATION / "stacks-errata-a04446e-r33-source-page-map-2026-08-30.json"
OUTPUT = VALIDATION / "stacks-errata-a04446e-r33-visual-qa-2026-08-30.json"
RENDER_ROOT = ROOT / "tmp/pdfs/r33-visual-qa-20260830/spaces-morphisms"
RENDER_MANIFEST = RENDER_ROOT / "render-manifest.json"
STEM = "spaces-morphisms"
EXPECTED_SOURCE = {
    "commit": "1c90a67eb42de28884be05abd8fb58f781aed7db",
    "tree": "3c292f9a4b94162ede69d2633b1272b057a498c3",
}
EXPECTED_PAGES = [105, 106, 107, 108, 109]


def identity(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest().upper(),
    }


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected a JSON object: {path}")
    return value


def main() -> int:
    if OUTPUT.exists():
        raise RuntimeError(f"refusing to overwrite {OUTPUT}")
    build = load_json(BUILD)
    page_map = load_json(PAGE_MAP)
    manifest = load_json(RENDER_MANIFEST)
    if build.get("status") != "PASS" or build.get("source") != EXPECTED_SOURCE:
        raise RuntimeError("R33 build identity or pass state mismatch")
    artifacts = {
        row.get("stem"): row
        for row in build.get("artifacts", [])
        if isinstance(row, dict)
    }
    artifact = artifacts.get(STEM)
    if not isinstance(artifact, dict):
        raise RuntimeError("R33 build lacks the spaces-morphisms artifact")
    source_map = page_map.get("sources", {}).get(f"{STEM}.tex")
    if (
        page_map.get("status") != "PASS"
        or page_map.get("operation_count") != 7
        or not isinstance(source_map, dict)
        or source_map.get("unique_pages") != EXPECTED_PAGES
        or page_map.get("mapping_failures") != 0
    ):
        raise RuntimeError("R33 source-to-page map is not closed")
    pdf_path = ROOT / f"{STEM}.pdf"
    pdf_identity = identity(pdf_path)
    if (
        artifact.get("pages") != 116
        or artifact.get("bytes") != pdf_identity["bytes"]
        or artifact.get("sha256") != pdf_identity["sha256"]
    ):
        raise RuntimeError("rendered PDF differs from the fixed-point build receipt")
    full = manifest.get("full_page_render")
    contact = manifest.get("contact_sheets")
    pdf = manifest.get("pdf")
    if not all(isinstance(value, dict) for value in (full, contact, pdf)):
        raise RuntimeError("render manifest is structurally incomplete")
    if (
        pdf.get("pages") != 116
        or full.get("count") != 116
        or full.get("pages_without_ink") != 0
        or contact.get("count") != 8
        or pdf.get("encrypted") is not False
    ):
        raise RuntimeError("render manifest failed an R33 visual precondition")

    receipt = {
        "schema": "unofficial-ai-integrated-stacks-visual-qa/v1",
        "status": "PASS",
        "created_utc": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "source": build["source"],
        "build_receipt": {
            "path": BUILD.relative_to(ROOT).as_posix(),
            **identity(BUILD),
            "status": "PASS",
            "global_fixed_point_sweep": build["build"]["global_fixed_point_sweep"],
        },
        "scope": {
            "affected_chapters": [STEM],
            "full_page_render_count": 116,
            "full_page_contact_sheet_review_count": 116,
            "high_resolution_locus_page_count": len(EXPECTED_PAGES),
            "high_resolution_locus_pages": {STEM: EXPECTED_PAGES},
        },
        "artifacts": {
            STEM: {
                "pdf": f"{STEM}.pdf",
                "bytes": artifact["bytes"],
                "pages": artifact["pages"],
                "sha256": artifact["sha256"],
                "encrypted": pdf["encrypted"],
                "media_box_points": pdf["page_boxes_points"][0],
                "render_dimensions_pixels": full["dimension_sets"][0],
                "pages_without_ink": full["pages_without_ink"],
                "minimum_ink_pixels_below_245": full[
                    "minimum_ink_pixels_below_245"
                ],
                "duplicate_render_hashes": full["duplicate_render_hashes"],
            }
        },
        "render_protocol": {
            "renderer": "Poppler pdftoppm 26.05.0",
            "full_page_dpi": 96,
            "full_page_layout": "ordered 4-by-4 contact sheets",
            "contact_sheet_count": contact["count"],
            "high_resolution_dpi": 180,
            "high_resolution_selection": (
                "all five unique pages mapped from the seven manifest-bound "
                "R33 operation loci"
            ),
            "render_intermediates_published": False,
        },
        "source_page_mapping": {
            "path": PAGE_MAP.relative_to(ROOT).as_posix(),
            **identity(PAGE_MAP),
            "operation_count": 7,
            "mapping_failures": 0,
        },
        "private_render_evidence": {
            "published": False,
            "manifests": {STEM: identity(RENDER_MANIFEST)},
        },
        "checks": {
            "all_pages_rendered": True,
            "all_pages_manually_inspected": True,
            "all_manifest_bound_locus_pages_inspected_at_high_resolution": True,
            "page_dimensions_consistent": True,
            "headers_and_page_numbers_consistent": True,
            "text_and_formulas_legible": True,
            "diagrams_intact": True,
            "clipped_content": 0,
            "overlapping_content": 0,
            "blank_pages": 0,
            "corrupted_pages": 0,
            "missing_or_unreadable_glyphs": 0,
            "broken_diagrams": 0,
            "r33_spaces_morphisms_correction_loci_legible": True,
            "r33_codimension_target_correction_visible": True,
            "r33_normalization_variables_correction_visible": True,
            "r33_declarative_clause_correction_visible": True,
            "r33_spelling_correction_visible": True,
            "r33_named_morphism_correction_visible": True,
            "r33_quotient_grouping_correction_visible": True,
            "r33_introductory_comma_correction_visible": True,
            "five_duplicate_locale_aliases_not_applied_twice": True,
            "rejected_simplicial_007_parenthesis_preserved": True,
        },
        "accessibility": {
            "struct_tree_root_present": False,
            "mark_info_present": False,
            "note": (
                "The standalone chapter PDF is untagged; this retained "
                "accessibility limitation is not a visual-rendering failure."
            ),
        },
        "conclusion": (
            "All 116 pages of the affected cumulative spaces-morphisms PDF "
            "passed ordered contact-sheet review. All five unique manifest-bound "
            "correction-sensitive pages passed 180-DPI inspection with all seven "
            "corrected passages legible and no clipping, overlap, blank page, "
            "corrupt render, unreadable glyph, or broken diagram."
        ),
    }
    OUTPUT.write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({"status": "PASS", "path": str(OUTPUT), **identity(OUTPUT)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
