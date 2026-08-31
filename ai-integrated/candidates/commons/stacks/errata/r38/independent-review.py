from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def ev(path: Path, display: str | None = None) -> dict:
    return {"path": display or path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-render-manifest", type=Path, required=True)
    args = parser.parse_args()
    pre_manifest = ROOT / "candidate.manifest.json"
    config = json.loads((ROOT / "candidate.config.json").read_text(encoding="utf-8"))
    spec = json.loads((ROOT / "operation-spec.json").read_text(encoding="utf-8"))
    source_validation = json.loads((ROOT / "source-validation.json").read_text(encoding="utf-8"))
    build_receipt = json.loads((ROOT / "builds/build-receipt.json").read_text(encoding="utf-8"))
    deterministic = json.loads((ROOT / "builds/deterministic-replay.json").read_text(encoding="utf-8"))
    visual = json.loads((ROOT / "builds/visual-qa.json").read_text(encoding="utf-8"))
    visual_adjudication = json.loads((ROOT / "replay/VISUAL_INSPECTION_ADJUDICATION.json").read_text(encoding="utf-8"))
    if not all((source_validation["passed"], build_receipt["passed"], deterministic["passed"], visual["passed"], visual_adjudication["status"] == "PASS")):
        raise AssertionError("sealed validation gate failed")
    authority = (ROOT / "authority/source/more-algebra.tex").read_bytes()
    payload = authority
    for operation in sorted(spec["operations"], key=lambda row: row["start_byte"], reverse=True):
        start, end = operation["start_byte"], operation["end_byte_exclusive"]
        old, new = operation["old_text"].encode(), operation["replacement_text"].encode()
        if payload[start:end] != old:
            raise AssertionError(f"independent preimage mismatch: {operation['operation_id']}")
        payload = payload[:start] + new + payload[end:]
    sealed_payload = ROOT / "payload/more-algebra.tex"
    if payload != sealed_payload.read_bytes():
        raise AssertionError("independent payload replay mismatch")
    render_manifest_path = args.private_render_manifest.resolve()
    render_manifest = json.loads(render_manifest_path.read_text(encoding="utf-8"))
    renders = render_manifest["pdfs"]["more-algebra"]["renders"]
    if [row["page"] for row in renders] != list(range(1, 402)):
        raise AssertionError("independent full-page render closure mismatch")
    render_root = render_manifest_path.parent
    for row in renders:
        path = render_root / "more-algebra" / row["file"]
        if path.stat().st_size != row["bytes"] or sha(path) != row["sha256"]:
            raise AssertionError(f"independent render mismatch page {row['page']}")
    highres = render_manifest["high_resolution"]["renders"]
    expected_pages = config["visual_qa"]["high_resolution_pages"]["more-algebra"]
    if [row["page"] for row in highres] != expected_pages:
        raise AssertionError("independent high-resolution page closure mismatch")
    for row in highres:
        path = render_root / "highres" / row["file"]
        if path.stat().st_size != row["bytes"] or sha(path) != row["sha256"]:
            raise AssertionError(f"independent high-resolution mismatch page {row['page']}")
    if len(render_manifest["contact_sheets"]) != 26:
        raise AssertionError("independent contact-sheet closure mismatch")
    registry = ROOT.parents[4] / "registry/overlays.json"
    if sha(registry) != source_validation["deduplication"]["registry"]["sha256"]:
        raise AssertionError("registry changed after deduplication")
    review = {
        "schema": "mathematics-commons-stacks-independent-review/v1",
        "candidate_id": config["candidate_id"],
        "reviewed_at_utc": "2026-08-31T02:15:00Z",
        "passed": True,
        "result": "PASS",
        "pre_review_manifest": ev(pre_manifest),
        "authority": ev(ROOT / "authority/source/more-algebra.tex"),
        "payload": ev(sealed_payload),
        "operation_spec": ev(ROOT / "operation-spec.json"),
        "source_validation": ev(ROOT / "source-validation.json"),
        "build_receipt": ev(ROOT / "builds/build-receipt.json"),
        "deterministic_replay": ev(ROOT / "builds/deterministic-replay.json"),
        "visual_qa": ev(ROOT / "builds/visual-qa.json"),
        "visual_inspection_adjudication": ev(ROOT / "replay/VISUAL_INSPECTION_ADJUDICATION.json"),
        "private_render_manifest": {"logical_path": config["private_render_logical_path"] + "/render-manifest.json", "bytes": render_manifest_path.stat().st_size, "sha256": sha(render_manifest_path), "published": False},
        "closure": {"stable_units": 23, "original_producer_allegations": 29, "registrar_additive_aliases": 2, "operations": 31, "rejections": 0, "unresolved": 0, "stable_id_start": "MC-STK-ERR-1336", "stable_id_end": "MC-STK-ERR-1358"},
        "deduplication": source_validation["deduplication"],
        "page_392_dispute_resolved": visual_adjudication["page_392_adjudication"],
        "constraints": {"authority_mutated": False, "producer_target_mutated": False, "registry_mutated": False, "generated_source_mutated": False, "git_mutated": False, "publication_performed": False},
    }
    output = ROOT / "replay/independent-review.json"
    output.write_text(json.dumps(review, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")
    print(json.dumps({"passed": True, "review": str(output), "bytes": output.stat().st_size, "sha256": sha(output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
