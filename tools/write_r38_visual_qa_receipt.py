#!/usr/bin/env python3
"""Validate completed direct-image inspection ledgers and write the R38 receipt.

This program does not render PDFs, inspect images on a reviewer's behalf, or
create inspection ledgers. Each supplied ledger must use schema
unofficial-ai-integrated-stacks-visual-inspection-ledger/v1, status COMPLETE,
inspection_method direct_image_inspection, a nonempty reviewer, the exact
build.source, page_map_sha256, and render_manifests identities keyed by every
stem covered by that ledger. Every inspection has stem, kind (contact_sheet
or high_resolution), a stem-relative file, image={bytes,sha256}, an expanded
pages list, result PASS, nonempty observations, checks, and defects. Defects
must contain exactly the six DEFECTS keys, each an integer zero. Required
checks are CONTACT_CHECKS or HIGH_RESOLUTION_CHECKS below. A high-resolution
inspection also has locus_checks=[{operation_id,result,observations},...]
covering exactly every applied edit or historical no-op mapped to its page.

Optional top-level layout_observations retain nonblocking findings. Each entry
has kind (margin_overflow or external_reference), stem, integer page,
nonempty unique operation_ids, blocking=false, nonempty observations, and
evidence={kind:high_resolution,file,image:{bytes,sha256}}. The evidence must
match a validated high-resolution inspection in that same ledger, and every
operation ID must be among that image's checked loci. Notes are preserved
verbatim with reviewer/ledger provenance; they never relax the six defect
gates. A passing receipt is not a claim of complete references or absence of
all other layout issues. Numerical log diagnostics remain attributed notes,
not measurements independently inferred from image appearance.

The complete ledger set must cover every contact sheet and every mapped
high-resolution page exactly once. Repeated, missing, conflicting, or stale
evidence is an error. Passing these checks verifies the supplied records;
the visual findings themselves remain attributable to their named reviewers.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

from PIL import Image
from pypdf import PdfReader

from map_r38_visual_qa import (
    EXPECTED_APPLIED,
    NOOP_ID,
    ROOT,
    STEMS,
    git_blob,
    identity,
    load_build,
    load_json,
    relative_path,
    sha256,
    utc_now,
)


LEDGER_SCHEMA = "unofficial-ai-integrated-stacks-visual-inspection-ledger/v1"
PAGE_MAP_SCHEMA = "unofficial-ai-integrated-stacks-operation-page-map/v1"
RENDER_SCHEMA = "unofficial-ai-integrated-stacks-private-render-manifest/v1"
DEFECTS = (
    "clipped_content", "overlapping_content", "blank_pages", "corrupted_pages",
    "missing_or_unreadable_glyphs", "broken_diagrams",
)
CONTACT_CHECKS = (
    "headers_and_page_numbers_consistent", "layout_intact", "diagrams_intact",
)
HIGH_RESOLUTION_CHECKS = (
    "text_and_formulas_legible", "diagrams_intact", "correction_loci_legible",
)
LAYOUT_OBSERVATION_KINDS = ("margin_overflow", "external_reference")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def integer(value: object, label: str, minimum: int = 0) -> int:
    require(type(value) is int and value >= minimum, f"invalid integer: {label}")
    return value


def text(value: object, label: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), f"missing text: {label}")
    return value


def public_reviewer_label(value: str) -> str:
    """Keep reviewer attribution without serializing a private agent path."""
    label = value.replace("/root/", "agent/").replace("\\root\\", "agent/")
    require("/root/" not in label and "\\root\\" not in label,
            "reviewer label contains a private agent path")
    return label


def require_identity(value: object, expected: dict, label: str) -> None:
    require(isinstance(value, dict) and all(
        value.get(key) == expected[key] for key in ("bytes", "sha256")
    ), f"identity mismatch: {label}")


def numbered_pages(value: object, count: int, label: str) -> list[int]:
    require(isinstance(value, list) and bool(value), f"missing pages: {label}")
    for page in value:
        require(integer(page, label, 1) <= count, f"page outside PDF: {label}")
    require(value == sorted(set(value)), f"duplicated or unordered pages: {label}")
    return value


class Evidence:
    """Keep exact identities and refuse inputs changed during verification."""

    def __init__(self) -> None:
        self.files: dict[Path, dict] = {}

    def bind(self, path: Path) -> dict:
        path = path.resolve()
        observed = identity(path)
        if path in self.files:
            require(observed == self.files[path], f"evidence changed: {path}")
        self.files[path] = observed
        return observed

    def json(self, path: Path) -> dict:
        self.bind(path)
        value = load_json(path)
        self.bind(path)
        return value

    def recheck(self) -> None:
        for path, expected in self.files.items():
            require(identity(path) == expected, f"evidence changed during QA: {path}")


def artifact_path(record: dict, fallback: str) -> Path:
    value = record.get("path", fallback)
    path = Path(text(value, "mapped artifact path"))
    require(path.name == Path(fallback).name, f"incorrect mapped artifact filename: {path}")
    return path.resolve() if path.is_absolute() else (ROOT / path).resolve()


def frozen_admission(build: dict) -> tuple[dict[str, dict], dict, str]:
    """Read only the five admitted maps and one registry at the build commit."""
    revision = build["source"]["commit"]
    admitted: dict[str, dict] = {}
    for number in range(34, 39):
        path = f"ai-integrated/candidates/commons/stacks/errata/r{number}/source-map.jsonl"
        for line in git_blob(revision, path).decode("utf-8").splitlines():
            require(bool(line.strip()), f"blank row in frozen admission map: {path}")
            unit = json.loads(line)
            require(isinstance(unit, dict) and isinstance(unit.get("operations"), list),
                    f"malformed frozen admission row: {path}")
            for operation in unit["operations"]:
                require(isinstance(operation, dict), f"malformed frozen operation: {path}")
                op_id = text(operation.get("operation_id"), path)
                require(op_id not in admitted, f"duplicate frozen admission ID: {op_id}")
                require(operation.get("source") == unit.get("source")
                        and operation.get("stable_id") == unit.get("unit_id"),
                        f"frozen operation/unit binding mismatch: {op_id}")
                admitted[op_id] = {"source": operation["source"], "round": number,
                                   "stable_id": operation["stable_id"],
                                   "replacement_text": operation["replacement_text"]}
    require(len(admitted) == 77 and NOOP_ID in admitted,
            "frozen admission inventory is not the expected 77 operations")
    registry_bytes = git_blob(revision, "validation/overlay-composition-semantic-dispositions-v1.json")
    registry = json.loads(registry_bytes)
    require(isinstance(registry, dict) and registry.get("status") == "PASS"
            and registry.get("schema") == "unofficial-ai-integrated-stacks-semantic-composition-dispositions/v1",
            "frozen semantic-disposition registry is invalid")
    rows = registry.get("dispositions")
    require(isinstance(rows, list), "frozen semantic-disposition inventory is missing")
    matches = [row for row in rows if isinstance(row, dict)
               and isinstance(row.get("operation"), dict)
               and row["operation"].get("operation_id") == NOOP_ID]
    require(len(matches) == 1, "historical no-op has no unique frozen disposition")
    disposition = matches[0]
    require(disposition.get("disposition") == "structurally_superseded_by_ancestor_rewrite"
            and disposition["operation"].get("source") == admitted[NOOP_ID]["source"]
            and disposition["operation"].get("stable_id") == admitted[NOOP_ID]["stable_id"],
            "frozen historical no-op disposition binding mismatch")
    return admitted, disposition, sha256(registry_bytes)


def validate_page_map(page_map: dict, build: dict, build_path: Path,
                      artifacts: dict[str, dict], evidence: Evidence) -> dict:
    require(page_map.get("schema") == PAGE_MAP_SCHEMA and page_map.get("status") == "PASS",
            "a successful operation-page map is required")
    require(page_map.get("source") == build["source"], "page-map source binding mismatch")
    require(page_map.get("composition_base") == build["composition"]["composition_base_commit"]
            and page_map.get("composition_source") == build["composition"]["composition_source_commit"],
            "page-map composition binding mismatch")
    require(page_map.get("build_receipt") == {
        "path": relative_path(build_path), **evidence.bind(build_path),
    }, "page-map build-receipt binding mismatch")
    for key, expected in (("operation_count", 76), ("accepted_operation_count", 77),
                          ("historical_noop_operation_count", 1), ("mapping_failures", 0)):
        require(integer(page_map.get(key), key) == expected, f"incorrect page-map {key}")
    sources = page_map.get("sources")
    require(isinstance(sources, dict) and set(sources) == {f"{stem}.tex" for stem in STEMS},
            "page-map source inventory mismatch")
    global_ids: set[str] = set()
    admitted, noop_disposition, disposition_hash = frozen_admission(build)
    expected_loci: dict[str, dict[int, list[str]]] = {}
    noop_count = 0
    for stem in STEMS:
        source_name = f"{stem}.tex"
        source = sources[source_name]
        require(isinstance(source, dict), f"invalid source map: {stem}")
        final = git_blob(build["source"]["commit"], source_name)
        source_identity = {"bytes": len(final), "sha256": sha256(final)}
        require_identity({"bytes": source.get("composed_bytes"),
                          "sha256": source.get("composed_sha256")}, source_identity, source_name)
        require_identity(evidence.bind(ROOT / source_name), source_identity, f"live {source_name}")
        require_identity(source.get("pdf"), artifacts[stem], f"mapped {stem}.pdf")
        require_identity(evidence.bind(artifact_path(source["pdf"], f"{stem}.pdf")),
                         artifacts[stem], f"mapped live {stem}.pdf")
        page_count = artifacts[stem]["pages"]
        require(integer(source["pdf"].get("pages"), f"{stem} mapped pages", 1) == page_count,
                f"page-map PDF page count differs from build: {stem}")
        require(isinstance(source.get("synctex"), dict), f"missing mapped sidecar: {stem}")
        require_identity(source.get("synctex"), evidence.bind(artifact_path(
            source["synctex"], f"{stem}.synctex.gz")),
                         f"mapped {stem} SyncTeX")
        require(source.get("pdf_and_synctex_identity_preserved") is True,
                f"page map lacks preserved instrumentation identity: {stem}")
        operations, historical = source.get("operations"), source.get("historical_noop_evidence")
        require(isinstance(operations, list) and len(operations) == EXPECTED_APPLIED[stem],
                f"incorrect applied operation inventory: {stem}")
        require(integer(source.get("operation_count"), f"{stem} operation count") == len(operations),
                f"inconsistent operation count: {stem}")
        require(isinstance(historical, list) and len(historical) == (1 if stem == "cohomology" else 0),
                f"incorrect historical no-op inventory: {stem}")
        source_lines = final.decode("utf-8").splitlines()
        by_page: dict[int, list[str]] = {}
        byte_pages: set[int] = set()
        historical_pages: set[int] = set()
        for is_historical, rows in ((False, operations), (True, historical)):
            for row in rows:
                require(isinstance(row, dict), f"invalid mapped operation: {stem}")
                op_id = text(row.get("operation_id"), "operation_id")
                require(re.fullmatch(r"MC-STK-ERR-\d+-OP[1-9]\d*", op_id) is not None,
                        f"invalid operation identifier: {op_id}")
                require(op_id not in global_ids, f"duplicate mapped operation: {op_id}")
                require(op_id in admitted, f"operation is not in the frozen admitted inventory: {op_id}")
                frozen = admitted[op_id]
                require(frozen["source"] == source_name
                        and row.get("round") == frozen["round"]
                        and row.get("stable_id") == frozen["stable_id"],
                        f"operation/source/round differs from frozen admission: {op_id}")
                global_ids.add(op_id)
                require(row.get("stable_id") == op_id.rsplit("-OP", 1)[0],
                        f"stable ID mismatch: {op_id}")
                require(34 <= integer(row.get("round"), op_id, 1) <= 38,
                        f"operation outside R34--R38: {op_id}")
                if is_historical:
                    require(op_id == NOOP_ID and row.get("applied_byte_edit") is False
                            and row.get("disposition") == "structurally_superseded_by_ancestor_rewrite",
                            "historical no-op disposition mismatch")
                    payload_key = "evidence"
                    noop_count += 1
                else:
                    require(op_id != NOOP_ID and row.get("disposition") == "applied_byte_edit",
                            f"invalid applied disposition: {op_id}")
                    payload_key = "replacement"
                payload = text(row.get(f"{payload_key}_text"), op_id).encode("utf-8")
                if is_historical:
                    frozen_evidence = noop_disposition.get("evidence")
                    require(isinstance(frozen_evidence, dict)
                            and row.get("evidence_text") == frozen_evidence.get("text")
                            and row.get("disposition_registry_sha256") == disposition_hash
                            and final.count(payload) == 1,
                            "historical no-op evidence differs from its unique frozen disposition")
                    require_identity(frozen_evidence,
                                     {"bytes": len(payload), "sha256": sha256(payload)}, op_id)
                else:
                    require(row.get("replacement_text") == frozen["replacement_text"],
                            f"replacement differs from frozen admission: {op_id}")
                require_identity({"bytes": row.get(f"{payload_key}_bytes"),
                                  "sha256": row.get(f"{payload_key}_sha256")},
                                 {"bytes": len(payload), "sha256": sha256(payload)}, op_id)
                first_byte = integer(row.get("final_start_byte"), op_id)
                end_byte = integer(row.get("final_end_byte_exclusive"), op_id, 1)
                require(end_byte == first_byte + len(payload) and end_byte <= len(final)
                        and final[first_byte:end_byte] == payload,
                        f"final source bytes do not match mapped evidence: {op_id}")
                first_line = final.count(b"\n", 0, first_byte) + 1
                end_line = final.count(b"\n", 0, end_byte - 1) + 1
                require(integer(row.get("final_cumulative_line"), op_id, 1) == first_line
                        and integer(row.get("final_end_line"), op_id, 1) == end_line,
                        f"final line interval mismatch: {op_id}")
                line_rows = row.get("final_source_lines")
                require(isinstance(line_rows, list) and len(line_rows) == end_line - first_line + 1,
                        f"incomplete final source-line coverage: {op_id}")
                line_pages: set[int] = set()
                for number, line_row in zip(range(first_line, end_line + 1), line_rows):
                    require(isinstance(line_row, dict)
                            and integer(line_row.get("line"), op_id, 1) == number
                            and line_row.get("text") == source_lines[number - 1],
                            f"final source-line identity mismatch: {op_id}")
                    line_pages.update(numbered_pages(line_row.get("pages"), page_count, op_id))
                pages = numbered_pages(row.get("pages"), page_count, op_id)
                require(pages == sorted(line_pages), f"operation page union mismatch: {op_id}")
                (historical_pages if is_historical else byte_pages).update(pages)
                for page in pages:
                    by_page.setdefault(page, []).append(op_id)
                if op_id == "MC-STK-ERR-1345-OP1":
                    qualification = text(row.get("qualification"), op_id)
                    require("Optional equivalent" in qualification and "not a substantive" in qualification,
                            "1345 must retain its optional-equivalent-notation qualification")
        require(source.get("byte_edit_pages") == sorted(byte_pages)
                and source.get("historical_noop_pages") == sorted(historical_pages)
                and source.get("unique_pages") == sorted(by_page),
                f"page-map page unions are inconsistent: {stem}")
        expected_loci[stem] = {page: sorted(ids) for page, ids in by_page.items()}
    require(global_ids == set(admitted) and noop_count == 1, "operation/no-op inventory is not closed")
    return expected_loci


def manifest_image(root: Path, folder: str, row: dict, evidence: Evidence,
                   *, count_ink: bool = False) -> tuple[Path, dict, tuple[int, int], int | None]:
    name = text(row.get("file"), "rendered filename")
    require("/" not in name and "\\" not in name and Path(name).suffix == ".png",
            f"invalid manifest image filename: {name}")
    path = root / folder / name
    require(path.resolve().is_relative_to(root.resolve()), f"image escapes render root: {path}")
    observed = evidence.bind(path)
    require_identity(row, observed, name)
    with Image.open(path) as image:
        require(image.format == "PNG", f"not a PNG image: {path}")
        image.verify()
    with Image.open(path) as image:
        image.load()
        dimensions = image.size
        require(dimensions[0] > 0 and dimensions[1] > 0, f"empty PNG dimensions: {path}")
        ink = sum(image.convert("L").histogram()[:245]) if count_ink else None
    return path, observed, dimensions, ink


def require_png_inventory(root: Path, folder: str, names: set[str]) -> None:
    actual = {path.name for path in (root / folder).iterdir()
              if path.is_file() and path.suffix.lower() == ".png"}
    require(actual == names, f"extra or missing PNGs in {root / folder}")


def validate_render(stem: str, root: Path, artifact: dict, mapped_loci: dict[int, list[str]],
                    evidence: Evidence, pdf_path: Path | None = None) -> dict:
    manifest_path = root / "render-manifest.json"
    manifest = evidence.json(manifest_path)
    require(manifest.get("schema") == RENDER_SCHEMA and manifest.get("status") == "PASS"
            and manifest.get("published") is False, f"invalid private render manifest: {stem}")
    pdf_path = pdf_path or ROOT / f"{stem}.pdf"
    pdf_identity = evidence.bind(pdf_path)
    require_identity(pdf_identity, artifact, f"live {stem} PDF/build")
    pdf = manifest.get("pdf")
    require_identity(pdf, pdf_identity, f"{stem} render manifest PDF")
    with pdf_path.open("rb") as stream:
        reader = PdfReader(stream)
        require(not reader.is_encrypted and pdf.get("encrypted") is False,
                f"encrypted or ambiguously encrypted PDF: {stem}")
        count = len(reader.pages)
        require(count == artifact["pages"]
                and integer(pdf.get("pages"), f"{stem} manifest pages", 1) == count,
                f"live PDF page count mismatch: {stem}")
        boxes = sorted({tuple(float(value) for value in page.mediabox) for page in reader.pages})
        require(len(boxes) == 1 and pdf.get("page_boxes_points") == [list(box) for box in boxes],
                f"inconsistent or mismatched PDF page dimensions: {stem}")
        catalog = reader.trailer["/Root"]
        accessibility = {"struct_tree_root_present": "/StructTreeRoot" in catalog,
                         "mark_info_present": "/MarkInfo" in catalog}
    full, contact, high = (manifest.get(key) for key in (
        "full_page_render", "contact_sheets", "high_resolution_render"))
    require(all(isinstance(value, dict) for value in (full, contact, high)),
            f"incomplete render manifest: {stem}")
    full_dpi = integer(full.get("dpi"), f"{stem} full DPI", 96)
    high_dpi = integer(high.get("dpi"), f"{stem} high-resolution DPI", 180)
    require(high_dpi > full_dpi, f"high-resolution DPI is not higher than full-page DPI: {stem}")
    rows = full.get("pages")
    require(isinstance(rows, list) and len(rows) == count
            and integer(full.get("count"), f"{stem} full count") == count,
            f"incomplete full-page render: {stem}")
    dimensions: set[tuple[int, int]] = set()
    hashes: set[str] = set()
    names: set[str] = set()
    minimum_ink: int | None = None
    box = boxes[0]
    for number, row in enumerate(rows, 1):
        require(isinstance(row, dict) and integer(row.get("page"), stem, 1) == number,
                f"unordered or duplicated full-page inventory: {stem}")
        path, observed, size, ink = manifest_image(root, "full-pages", row, evidence, count_ink=True)
        require(row.get("dimensions_pixels") == list(size), f"PNG dimension mismatch: {path}")
        require(all(abs(actual - (extent * full_dpi / 72)) <= 1.01 for actual, extent in
                    zip(size, (box[2] - box[0], box[3] - box[1]))),
                f"full-page PNG dimensions disagree with PDF/DPI: {path}")
        require(ink is not None and ink > 0
                and integer(row.get("ink_pixels_below_245"), str(path)) == ink,
                f"blank or mismatched full-page ink evidence: {path}")
        require(path.name not in names and observed["sha256"] not in hashes,
                f"duplicated full-page filename or render bytes: {stem}")
        names.add(path.name)
        hashes.add(observed["sha256"])
        dimensions.add(size)
        minimum_ink = ink if minimum_ink is None else min(minimum_ink, ink)
    require_png_inventory(root, "full-pages", names)
    require(len(dimensions) == 1 and full.get("dimension_sets") == [list(size) for size in sorted(dimensions)]
            and integer(full.get("pages_without_ink"), stem) == 0
            and integer(full.get("duplicate_render_hashes"), stem) == 0
            and integer(full.get("minimum_ink_pixels_below_245"), stem, 1) == minimum_ink,
            f"full-page summary disagrees with decoded PNGs: {stem}")
    expected_images: dict[tuple[str, str, str], dict] = {}
    sheets = contact.get("sheets")
    sheet_count = math.ceil(count / 16)
    require(contact.get("layout") == "ordered 4-by-4" and isinstance(sheets, list)
            and len(sheets) == sheet_count and integer(contact.get("count"), stem) == sheet_count,
            f"incomplete contact-sheet inventory: {stem}")
    names = set()
    full_size = next(iter(dimensions))
    expected_sheet_size = (1240, 4 * (round(full_size[1] * 300 / full_size[0]) + 24) + 40)
    for index, row in enumerate(sheets, 1):
        require(isinstance(row, dict) and integer(row.get("sheet"), stem, 1) == index,
                f"unordered or duplicated contact sheets: {stem}")
        first, last = (index - 1) * 16 + 1, min(index * 16, count)
        require(row.get("pages") == [first, last], f"contact-sheet page interval mismatch: {stem}/{index}")
        path, observed, size, _ = manifest_image(root, "contact-sheets", row, evidence)
        require(size == expected_sheet_size and path.name not in names,
                f"incorrect contact-sheet dimensions or duplicate filename: {path}")
        names.add(path.name)
        file = f"contact-sheets/{path.name}"
        expected_images[(stem, "contact_sheet", file)] = {
            "image": observed, "pages": list(range(first, last + 1)), "locus_ids": [],
        }
    require_png_inventory(root, "contact-sheets", names)
    high_rows = high.get("pages")
    selected = sorted(mapped_loci)
    require(isinstance(high_rows, list) and len(high_rows) == len(selected)
            and integer(high.get("count"), stem) == len(selected),
            f"high-resolution inventory differs from mapped pages: {stem}")
    names = set()
    for page, row in zip(selected, high_rows):
        require(isinstance(row, dict) and integer(row.get("page"), stem, 1) == page,
                f"high-resolution pages are missing, duplicated, or out of order: {stem}")
        path, observed, size, _ = manifest_image(root, "high-resolution", row, evidence)
        require(path.name not in names and all(
            abs(actual - (extent * high_dpi / 72)) <= 1.01 for actual, extent in
            zip(size, (box[2] - box[0], box[3] - box[1]))
        ), f"high-resolution filename or PDF/DPI dimension mismatch: {path}")
        names.add(path.name)
        expected_images[(stem, "high_resolution", f"high-resolution/{path.name}")] = {
            "image": observed, "pages": [page], "locus_ids": mapped_loci[page],
        }
    require_png_inventory(root, "high-resolution", names)
    return {
        "manifest": {"path": relative_path(manifest_path), **evidence.bind(manifest_path)},
        "images": expected_images, "full_dpi": full_dpi, "high_dpi": high_dpi,
        "contact_count": sheet_count, "accessibility": accessibility,
        "artifact": {
            "pdf": f"{stem}.pdf", **pdf_identity, "pages": count, "encrypted": False,
            "media_box_points": list(box), "render_dimensions_pixels": list(full_size),
            "pages_without_ink": 0, "minimum_ink_pixels_below_245": minimum_ink,
            "duplicate_render_hashes": 0,
        },
    }


def validate_inspection(row: dict, expected: dict, label: str) -> int:
    require(row.get("result") == "PASS", f"inspection did not pass: {label}")
    text(row.get("observations"), f"observations for {label}")
    require_identity(row.get("image"), expected["image"], f"inspected image {label}")
    require(row.get("pages") == expected["pages"]
            and all(type(page) is int for page in row.get("pages", [])),
            f"inspected page coverage mismatch: {label}")
    checks = row.get("checks")
    required = CONTACT_CHECKS if row["kind"] == "contact_sheet" else HIGH_RESOLUTION_CHECKS
    require(isinstance(checks, dict) and all(checks.get(key) is True for key in required),
            f"required direct-inspection check absent or failed: {label}")
    defects = row.get("defects")
    require(isinstance(defects, dict) and set(defects) == set(DEFECTS)
            and all(type(defects[key]) is int and defects[key] == 0 for key in DEFECTS),
            f"defect counts are incomplete, ambiguous, or nonzero: {label}")
    loci = row.get("locus_checks", [])
    require(isinstance(loci, list), f"invalid locus checks: {label}")
    ids = []
    for locus in loci:
        require(isinstance(locus, dict), f"invalid locus check: {label}")
        op_id = text(locus.get("operation_id"), label)
        require(locus.get("result") == "PASS", f"locus did not pass: {label}/{op_id}")
        text(locus.get("observations"), f"locus observations for {label}/{op_id}")
        ids.append(op_id)
    require(len(ids) == len(set(ids)) and sorted(ids) == expected["locus_ids"],
            f"missing, duplicated, or extraneous operation-level inspection: {label}")
    return len(ids)


def validate_layout_observations(ledger: dict, inspections: dict, expected: dict,
                                 reviewer: str, provenance: dict) -> list[dict]:
    """Retain actual ledger notes, bound to that ledger's inspected image/loci."""
    rows = ledger.get("layout_observations", [])
    require(isinstance(rows, list), "layout_observations must be a list")
    retained: list[dict] = []
    seen: set[tuple] = set()
    for row in rows:
        require(isinstance(row, dict), "malformed nonblocking layout observation")
        require(set(row) == {"kind", "stem", "page", "operation_ids", "blocking",
                             "observations", "evidence"},
                "nonblocking observation fields are incomplete or unrecognized")
        kind = text(row.get("kind"), "layout observation kind")
        require(kind in LAYOUT_OBSERVATION_KINDS, f"unsupported layout observation kind: {kind}")
        stem = text(row.get("stem"), "layout observation stem")
        page = integer(row.get("page"), "layout observation page", 1)
        require(row.get("blocking") is False, "only explicitly nonblocking observations can be retained")
        description = text(row.get("observations"), "layout observation text")
        image = row.get("evidence")
        require(isinstance(image, dict) and set(image) == {"kind", "file", "image"}
                and image.get("kind") == "high_resolution",
                "layout observation requires high-resolution image evidence")
        file = text(image.get("file"), "layout observation image file")
        key = (stem, "high_resolution", file)
        require(key in inspections and key in expected,
                f"layout observation image was not inspected in this ledger: {key}")
        inspected, required = inspections[key], expected[key]
        require(inspected["pages"] == [page] and required["pages"] == [page],
                f"layout observation page differs from inspected image: {key}")
        require_identity(image.get("image"), required["image"], f"layout observation {key}")
        ids = row.get("operation_ids")
        require(isinstance(ids, list) and bool(ids), "layout observation lacks operation evidence")
        for op_id in ids:
            text(op_id, "layout observation operation ID")
        require(len(ids) == len(set(ids)), "duplicated layout observation operation IDs")
        inspected_ids = {item["operation_id"] for item in inspected.get("locus_checks", [])}
        require(set(ids) <= inspected_ids and set(ids) <= set(required["locus_ids"]),
                f"layout observation operation is not mapped and inspected on its page: {key}")
        signature = (kind, stem, page, tuple(sorted(ids)), description)
        require(signature not in seen, "duplicate nonblocking layout observation")
        seen.add(signature)
        retained.append({
            "kind": kind, "stem": stem, "page": page, "operation_ids": list(ids),
            "blocking": False, "observations": description,
            "evidence": {"kind": "high_resolution", "file": file,
                         "image": dict(required["image"])},
            "reviewer": reviewer, "inspection_ledger": dict(provenance),
        })
    return retained


def validate_ledgers(paths: list[Path], build: dict, page_map_identity: dict,
                     rendered: dict, evidence: Evidence) -> dict:
    require(bool(paths) and len(paths) == len(set(paths)), "missing or duplicate ledger paths")
    expected = {key: value for stem in STEMS for key, value in rendered[stem]["images"].items()}
    seen: set[tuple[str, str, str]] = set()
    records = []
    layout_observations: list[dict] = []
    locus_count = 0
    contact_pages = {stem: set() for stem in STEMS}
    high_pages = {stem: set() for stem in STEMS}
    for path in paths:
        ledger = evidence.json(path)
        require(ledger.get("schema") == LEDGER_SCHEMA and ledger.get("status") == "COMPLETE"
                and ledger.get("inspection_method") == "direct_image_inspection",
                f"ledger is not a completed direct-image inspection: {path}")
        reviewer = public_reviewer_label(
            text(ledger.get("reviewer"), f"reviewer for {path}")
        )
        require(ledger.get("source") == build["source"]
                and ledger.get("page_map_sha256") == page_map_identity["sha256"],
                f"ledger is bound to a different build or page map: {path}")
        inspections = ledger.get("inspections")
        require(isinstance(inspections, list) and bool(inspections), f"empty inspection ledger: {path}")
        covered_stems: set[str] = set()
        ledger_inspections: dict[tuple[str, str, str], dict] = {}
        for row in inspections:
            require(isinstance(row, dict), f"malformed inspection in {path}")
            stem, kind, file = (text(row.get(key), key) for key in ("stem", "kind", "file"))
            key = (stem, kind, file)
            require(key in expected, f"inspection is not a required manifest image: {key}")
            require(key not in seen, f"duplicate/conflicting inspection coverage: {key}")
            locus_count += validate_inspection(row, expected[key], str(key))
            seen.add(key)
            ledger_inspections[key] = row
            covered_stems.add(stem)
            covered = contact_pages if kind == "contact_sheet" else high_pages
            require(not covered[stem].intersection(row["pages"]),
                    f"duplicate/conflicting page coverage: {key}")
            covered[stem].update(row["pages"])
        manifests = ledger.get("render_manifests")
        require(isinstance(manifests, dict) and set(manifests) == covered_stems,
                f"ledger render-manifest inventory mismatch: {path}")
        for stem in covered_stems:
            require_identity(manifests[stem], rendered[stem]["manifest"], f"{path}/{stem} manifest")
        provenance = {"path": relative_path(path), **evidence.bind(path)}
        layout_observations.extend(validate_layout_observations(
            ledger, ledger_inspections, expected, reviewer, provenance))
        records.append({**provenance, "reviewer": reviewer,
                        "inspection_count": len(inspections), "covered_stems": sorted(covered_stems)})
    require(seen == set(expected), f"missing completed image inspections: {sorted(set(expected) - seen)}")
    for stem in STEMS:
        require(contact_pages[stem] == set(range(1, rendered[stem]["artifact"]["pages"] + 1)),
                f"contact-sheet review does not cover every page: {stem}")
    return {"ledgers": records, "inspection_count": len(seen), "locus_check_count": locus_count,
            "contact_pages": contact_pages, "high_pages": high_pages,
            "layout_observations": layout_observations}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-receipt", type=Path, required=True)
    parser.add_argument("--page-map", type=Path, required=True)
    parser.add_argument("--render-root", type=Path, required=True,
                        help="base directory containing the three chapter-stem directories")
    parser.add_argument("--inspection-ledger", type=Path, action="append", required=True,
                        help="completed direct-image ledger; repeat for disjoint reviewer batches")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    output = args.output.resolve()
    require(not output.exists(), f"refusing to overwrite {output}")
    evidence = Evidence()
    ledger_paths = [path.resolve() for path in args.inspection_ledger]
    require(len(ledger_paths) == len(set(ledger_paths)), "duplicate ledger paths")
    for path in ledger_paths:
        require(path.is_file(), f"inspection ledger does not exist: {path}")
        ledger = evidence.json(path)
        require(isinstance(ledger.get("inspections"), list) and bool(ledger["inspections"]),
                f"empty inspection ledger: {path}")
    build_path, page_map_path = args.build_receipt.resolve(), args.page_map.resolve()
    evidence.bind(build_path)
    build, artifacts = load_build(build_path)
    evidence.bind(build_path)
    page_map = evidence.json(page_map_path)
    page_map_identity = evidence.bind(page_map_path)
    mapped_loci = validate_page_map(page_map, build, build_path, artifacts, evidence)
    rendered = {stem: validate_render(stem, args.render_root.resolve() / stem,
                                      artifacts[stem], mapped_loci[stem], evidence,
                                      artifact_path(page_map["sources"][f"{stem}.tex"]["pdf"], f"{stem}.pdf"))
                for stem in STEMS}
    require(len({rendered[stem]["full_dpi"] for stem in STEMS}) == 1
            and len({rendered[stem]["high_dpi"] for stem in STEMS}) == 1,
            "render DPI differs between chapters")
    inspection = validate_ledgers(ledger_paths, build, page_map_identity, rendered, evidence)
    previous = text(build.get("composition", {}).get("previous_public_main_head"),
                    "previous_public_main_head")
    current_simplicial = git_blob(build["source"]["commit"], "simplicial.tex")
    previous_simplicial = git_blob(previous, "simplicial.tex")
    require(current_simplicial == previous_simplicial,
            "simplicial.tex differs from the previous public main; preservation is unproved")
    simplicial_identity = {"bytes": len(current_simplicial), "sha256": sha256(current_simplicial)}
    pages = {stem: sorted(mapped_loci[stem]) for stem in STEMS}
    full_count = sum(rendered[stem]["artifact"]["pages"] for stem in STEMS)
    contact_count = sum(rendered[stem]["contact_count"] for stem in STEMS)
    high_count = sum(len(value) for value in pages.values())
    affected_stems = build["composition"]["affected_source_stems"]
    require(isinstance(affected_stems, list) and len(affected_stems) == len(STEMS)
            and set(affected_stems) == set(STEMS), "invalid build affected-chapter order")
    receipt = {
        "schema": "unofficial-ai-integrated-stacks-visual-qa/v1", "status": "PASS",
        "created_utc": utc_now(), "source": build["source"],
        "build_receipt": {"path": relative_path(build_path), **evidence.bind(build_path),
                          "status": build["status"],
                          "global_fixed_point_sweep": build["build"]["global_fixed_point_sweep"]},
        "scope": {"affected_chapters": affected_stems, "full_page_render_count": full_count,
                  "full_page_contact_sheet_review_count": sum(len(value) for value in inspection["contact_pages"].values()),
                  "high_resolution_locus_page_count": high_count, "high_resolution_locus_pages": pages,
                  "applied_byte_edit_count": 76, "accepted_operation_count": 77,
                  "historical_noop_operation_count": 1,
                  "nonblocking_layout_observation_count": len(inspection["layout_observations"])},
        "artifacts": {stem: rendered[stem]["artifact"] for stem in STEMS},
        "render_protocol": {
            "renderer": "Poppler pdftoppm via tools/render_visual_qa.py (version not recorded in manifests)",
            "full_page_dpi": rendered[STEMS[0]]["full_dpi"],
            "full_page_layout": "ordered 4-by-4 contact sheets", "contact_sheet_count": contact_count,
            "high_resolution_dpi": rendered[STEMS[0]]["high_dpi"],
            "high_resolution_selection": "Every mapped page of all 76 applied R34--R38 byte edits and the one historical no-op",
            "render_intermediates_published": False,
        },
        "source_page_mapping": {"path": relative_path(page_map_path), **page_map_identity,
                                "operation_count": 76, "accepted_operation_count": 77,
                                "historical_noop_operation_count": 1, "mapping_failures": 0},
        "private_render_evidence": {"published": False,
                                    "manifests": {stem: rendered[stem]["manifest"] for stem in STEMS}},
        "direct_inspection_evidence": {
            "method": "direct_image_inspection", "ledgers": inspection["ledgers"],
            "inspection_count": inspection["inspection_count"],
            "operation_page_locus_check_count": inspection["locus_check_count"],
            "attribution": "Visual findings are the named reviewers' recorded direct-image observations; this writer validates evidence and coverage, not visual appearance.",
        },
        "layout_observations": inspection["layout_observations"],
        "qualification": {
            "serious_defect_gates_unchanged": True,
            "absence_of_all_layout_issues_claimed": False,
            "reference_completeness_claimed": False,
            "note": "Recorded nonblocking margin-overflow and external-reference observations are preserved verbatim with their inspection provenance. Passing the six serious-defect gates does not assert absence of all layout issues or complete references; numerical log diagnostics remain attributed observations.",
        },
        "checks": {
            "all_pages_rendered": True, "all_pages_manually_inspected": True,
            "all_manifest_bound_locus_pages_inspected_at_high_resolution": True,
            "page_dimensions_consistent": True, "headers_and_page_numbers_consistent": True,
            "text_and_formulas_legible": True, "diagrams_intact": True,
            "rejected_simplicial_007_parenthesis_preserved": True,
            "historical_noop_evidence_inspected_without_duplicate_byte_edit": True,
            **{key: 0 for key in DEFECTS},
        },
        "source_preservation_evidence": {
            "rejected_simplicial_007_parenthesis_preserved": {
                "method": "exact Git-blob byte equality", "path": "simplicial.tex",
                "source_commit": build["source"]["commit"], "previous_public_main_head": previous,
                "source_blob": simplicial_identity, "previous_public_blob": simplicial_identity,
                "identical": True,
            },
        },
        "semantic_qualification": {
            "operation_id": "MC-STK-ERR-1345-OP1",
            "description": "Optional equivalent summation-notation normalization; not a substantive mathematical defect.",
        },
        "accessibility": {
            "artifacts": {stem: rendered[stem]["accessibility"] for stem in STEMS},
            "note": "PDF structure-tree and marking flags are reported from the live PDFs; direct visual inspection is not an accessibility-conformance audit.",
        },
        "conclusion": (
            f"Completed, hash-bound direct-image ledgers record review of all {full_count} pages "
            f"in {contact_count} contact sheets and all {high_count} mapped high-resolution pages. "
            "Every required operation/page locus has an explicit passing observation, including the "
            "historical no-op evidence. The ledgers report zero clipping, overlap, blank or corrupted "
            "pages, unreadable glyphs, or broken diagrams. "
            f"The receipt retains {len(inspection['layout_observations'])} nonblocking layout/reference "
            "observations; it does not claim absence of all layout issues or complete references."
        ),
    }
    evidence.recheck()
    payload = json.dumps(receipt, indent=2, ensure_ascii=False) + "\n"
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(payload)
    print(json.dumps({"status": "PASS", "output": relative_path(output), **identity(output),
                      "full_page_review_count": full_count, "high_resolution_page_count": high_count,
                      "inspection_ledger_count": len(inspection["ledgers"])}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}), file=sys.stderr)
        raise SystemExit(1)
