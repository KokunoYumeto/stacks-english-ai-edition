"""Append-only R43 finalization; every stage fails closed."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
PRIVATE = (
    REPO.parent
    / "03_projects/language_management/cjk/03_working_translations/"
      "stacks_cjk_20260821/canon/private_evidence/errata-r43-20260905/render"
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def ev(path: Path) -> dict:
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)}


def dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")


def bound(row: dict) -> None:
    path = (ROOT / row["path"]).resolve()
    assert path.is_relative_to(ROOT) and path.is_file(), row["path"]
    assert path.stat().st_size == row.get("bytes", path.stat().st_size), row["path"]
    assert sha(path) == row["sha256"], row["path"]


def mechanical() -> dict:
    source_review = load(ROOT / "replay/SOURCE_INDEPENDENT_VALIDATION.json")
    assert source_review["passed"] is True
    for row in source_review["observed_files"]:
        bound(row)

    build_receipt_path = ROOT / "builds/build-receipt.json"
    deterministic_path = ROOT / "builds/deterministic-replay.json"
    mutex_path = ROOT / "builds/TEX_MUTEX_RECEIPT.json"
    build_receipt = load(build_receipt_path)
    deterministic = load(deterministic_path)
    mutex = load(mutex_path)
    assert build_receipt["passed"] is True
    assert deterministic["passed"] is True and deterministic["fresh_builds_compared"] == 2
    assert mutex["passed"] is True and mutex["acquired"] is True and mutex["released"] is True
    assert mutex["mutex_name"] == "Global\\InterlanguageTeXSlotV1"
    bound(build_receipt["deterministic_replay"])
    bound(build_receipt["tex_mutex"])

    chapter = build_receipt["chapters"][0]
    for name in (
        "candidate_source", "authority_source", "candidate_pdf", "authority_pdf",
        "candidate_log", "authority_log", "candidate_stdout", "authority_stdout",
        "candidate_bibtex", "authority_bibtex",
    ):
        bound(chapter[name])
    pdf = ROOT / chapter["candidate_pdf"]["path"]
    reader = PdfReader(pdf)
    pages = len(reader.pages)
    assert pages == chapter["candidate_log_summary"]["pages"] == chapter["authority_log_summary"]["pages"] == 93
    rect_bad: list[int] = []
    links = 0
    for number, page in enumerate(reader.pages, 1):
        box = [float(value) for value in page.mediabox]
        for annotation in page.get("/Annots", []):
            obj = annotation.get_object()
            if obj.get("/Subtype") != "/Link":
                continue
            links += 1
            rect = obj.get("/Rect")
            if not rect or len(rect) != 4:
                rect_bad.append(number)
                continue
            x0, y0, x1, y1 = map(float, rect)
            if x0 > x1 or y0 > y1 or x0 < box[0] - .01 or y0 < box[1] - .01 or x1 > box[2] + .01 or y1 > box[3] + .01:
                rect_bad.append(number)
    assert not rect_bad, rect_bad

    stage = load(ROOT / "builds/BUILD_RENDER_STAGE.json")
    assert stage["status"] == "BUILD_DETERMINISTIC_RENDER_VISUAL_PASS"
    manifest_path = PRIVATE / "render-manifest.json"
    assert sha(manifest_path) == stage["render"]["sha256"]
    renders = load(manifest_path)
    rows = renders["pdfs"]["descent"]["renders"]
    assert [row["page"] for row in rows] == list(range(1, pages + 1))
    assert renders["pdfs"]["descent"]["pdf_sha256"] == sha(pdf)
    all_rows = [(PRIVATE / "descent" / row["file"], row) for row in rows]
    all_rows += [(PRIVATE / "contact_sheets" / row["file"], row) for row in renders["contact_sheets"]]
    all_rows += [(PRIVATE / "highres" / row["file"], row) for row in renders["high_resolution"]["renders"]]
    for path, row in all_rows:
        assert path.is_file() and path.stat().st_size == row["bytes"] and sha(path) == row["sha256"], path

    mapping = load(ROOT / "builds/source-page-map.json")
    assert mapping["operation_spec"]["sha256"] == sha(ROOT / "operation-spec.json")
    assert mapping["auxiliary_build"]["candidate_pdf_sha256"] == sha(pdf)
    assert len(mapping["operations"]) == 7
    operation_ids = {op["operation_id"] for op in load(ROOT / "operation-spec.json")["operations"]}
    assert {row["operation_id"] for row in mapping["operations"]} == operation_ids
    high_pages = [row["page"] for row in renders["high_resolution"]["renders"]]
    assert set(mapping["unique_pages"]).issubset(high_pages)

    report = {
        "schema": "stacks-r43-final-mechanical-validation-v1",
        "passed": True,
        "scope": "Source-stage identity preservation, build binding, mutex receipt, repeated-PDF identity, PDF link geometry, render bytes, and source-page mapping. Visual conclusions are separate.",
        "source_independent_validation": ev(ROOT / "replay/SOURCE_INDEPENDENT_VALIDATION.json"),
        "preserved_source_stage_bindings": source_review["observed_files"],
        "build_receipt": ev(build_receipt_path),
        "deterministic_replay": ev(deterministic_path),
        "tex_mutex": ev(mutex_path),
        "source_page_map": ev(ROOT / "builds/source-page-map.json"),
        "build_render_stage": ev(ROOT / "builds/BUILD_RENDER_STAGE.json"),
        "candidate_pdf": ev(pdf),
        "pdf_pages": pages,
        "links": links,
        "bad_link_rectangles": rect_bad,
        "tagged_pdf": "/StructTreeRoot" in reader.trailer["/Root"],
        "render_artifacts_rehashed": len(all_rows),
        "source_operations_mapped": 7,
        "high_resolution_pages": high_pages,
        "visual_inspection": "NOT_ASSERTED_BY_THIS_RECEIPT",
        "full_independent_final_review": "NOT_PERFORMED",
        "adverse_evidence": [
            f"Authority and candidate each have {chapter['candidate_log_summary']['overfull_hboxes']} overfull hboxes and {chapter['candidate_log_summary']['underfull_vboxes']} underfull vbox; visual disposition is bound separately.",
            "Unresolved cross-chapter reference multisets match authority; standalone AUX is intentionally incomplete.",
        ],
    }
    dump(ROOT / "builds/FINAL_MECHANICAL_VALIDATION.json", report)
    return report


def visual_receipts() -> list[dict]:
    aggregate_path = ROOT / "replay/VISUAL_ADJUDICATION.json"
    adjudication = load(aggregate_path)
    assert adjudication.get("passed") is True
    assert adjudication.get("pdf_sha256") == sha(ROOT / "builds/descent.pdf")
    assert adjudication.get("covered_pages") == list(range(1, 94))
    assert adjudication.get("blocking_findings") == []
    reviews = adjudication.get("reviews")
    assert isinstance(reviews, list) and len(reviews) == 1
    row = reviews[0]
    assert (row["path"], row["page_start"], row["page_end"]) == ("replay/VISUAL_PAGES_001_093.json", 1, 93)
    assert isinstance(row.get("method"), str) and row["method"].strip()
    bound(row)
    raw = load(ROOT / row["path"])
    assert raw["blocking_layout_defects"] == []
    assert raw["scope"]["reviewed_pages_count"] == 93
    render = load(PRIVATE / "render-manifest.json")
    assert len(raw["viewed_contact_artifacts"]) == len(render["contact_sheets"])
    assert len(raw["viewed_high_resolution_artifacts"]) == len(render["high_resolution"]["renders"])
    return [ev(aggregate_path), ev(ROOT / row["path"])]


def prepare() -> dict:
    assert load(ROOT / "builds/FINAL_MECHANICAL_VALIDATION.json")["passed"] is True
    visuals = visual_receipts()
    destination = ROOT / "replay/FINAL_STAGE.json"
    if destination.exists():
        raise FileExistsError("Final-stage snapshot is immutable; make a successor instead.")
    excluded = {"candidate.manifest.json", "replay/FINAL_STAGE.json", "replay/FINAL_INDEPENDENT_REVIEW.json"}
    inventory = [
        ev(path) for path in sorted(ROOT.rglob("*"))
        if path.is_file()
        and path.relative_to(ROOT).as_posix() not in excluded
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    ]
    report = {
        "schema": "stacks-r43-final-stage-snapshot-v1",
        "candidate_id": "stacks-errata-a04446e-r43",
        "status": "READY_FOR_FULL_INDEPENDENT_REVIEW_NOT_ADMITTED",
        "visual_receipts": visuals,
        "snapshot_inventory": inventory,
        "mechanical_validation": ev(ROOT / "builds/FINAL_MECHANICAL_VALIDATION.json"),
        "independent_replay": "not_performed",
        "historical_states": "Source-stage NOT_PERFORMED fields and builds/PENDING.json remain historical receipts, not current final-stage claims.",
        "closure_order": "Freeze this snapshot; independent review writes FINAL_INDEPENDENT_REVIEW.json binding its SHA; then seal candidate.manifest.json last. Never rewrite this snapshot to hash its future reviewer.",
    }
    dump(destination, report)
    return report


def seal() -> dict:
    snapshot_path = ROOT / "replay/FINAL_STAGE.json"
    stage = load(snapshot_path)
    for row in stage["snapshot_inventory"]:
        bound(row)
    review_path = ROOT / "replay/FINAL_INDEPENDENT_REVIEW.json"
    review = load(review_path)
    assert review.get("passed") is True
    assert review.get("final_stage_sha256") == sha(snapshot_path)
    visual_receipts()

    config = load(ROOT / "candidate.config.json")
    primary = {
        "stable_unit_manifest": "stable-units.json",
        "source_map": "source-map.jsonl",
        "decision_ledger": "decisions.jsonl",
        "rejection_ledger": "rejections.jsonl",
        "formula_diagram_inventory": "formula-diagram-inventory.json",
    }
    authorities = sorted(path for path in (ROOT / "authority").rglob("*") if path.is_file())
    excluded = {path.resolve() for path in authorities}
    excluded |= {(ROOT / relative).resolve() for relative in primary.values()}
    excluded.add((ROOT / "candidate.manifest.json").resolve())
    others = [
        path for path in sorted(ROOT.rglob("*"))
        if path.is_file() and path.resolve() not in excluded and "__pycache__" not in path.parts and path.suffix != ".pyc"
    ]
    manifest = {
        "schema": "mathematics-commons-stacks-candidate-manifest/v1",
        "candidate_id": config["candidate_id"],
        "lease_id": config["lease_id"],
        "namespace": config["namespace"],
        "writer_task": config["writer_task"],
        "upstream": {"lock": "upstream/stacks.lock.json", "commit": config["authority_commit"], "tree": config["authority_tree"]},
        "source_authorities": [ev(path) for path in authorities],
        "source_closure": {"enumerated": True, "expected_units": 7, "manifested_units": 7, "complete": True},
        **{key: ev(ROOT / relative) for key, relative in primary.items()},
        "builds": [ev(path) for path in others],
        "rights_state": "Upstream GNU FDL rights are preserved in authority/COPYING; this independently prepared AI correction overlay is not an official Stacks Project edition or endorsement.",
        "review_state": "performed",
        "independent_replay": "passed",
        "unresolved_defects": ["Standalone cross-chapter reference warnings match authority; cumulative AUX is not supplied. Accessibility tagging is not asserted."],
        "stop_conditions": ["A changed referenced byte invalidates this final manifest. Registry admission and composition remain separate."],
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    schema = load(REPO / "schemas/candidate-manifest.schema.json")
    Draft202012Validator(schema).validate(manifest)
    destination = ROOT / "candidate.manifest.json"
    if destination.exists():
        raise FileExistsError("candidate.manifest.json is immutable; make a successor round instead.")
    dump(destination, manifest)
    return {"manifest": ev(destination), "schema_errors": 0}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["mechanical", "prepare", "seal"])
    args = parser.parse_args()
    result = {"mechanical": mechanical, "prepare": prepare, "seal": seal}[args.stage]()
    print(json.dumps({"stage": args.stage, "passed": True, "result": result.get("status", result.get("manifest", result.get("scope")))}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
