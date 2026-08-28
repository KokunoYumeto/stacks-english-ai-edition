from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / "candidate.config.json").read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def evidence(path: Path) -> dict[str, str]:
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path)}


def main() -> int:
    validation_path = ROOT / "builds/validation.json"
    visual_path = ROOT / "builds/visual-qa.json"
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    visual = json.loads(visual_path.read_text(encoding="utf-8"))
    if validation.get("candidate_id") != CONFIG["candidate_id"] or validation.get("passed") is not True:
        raise AssertionError("R28 validation is absent, stale, or failed")
    if (
        visual.get("candidate_id") != CONFIG["candidate_id"]
        or visual.get("passed") is not True
        or visual.get("render_protocol", {}).get("manual_review_attested") is not True
    ):
        raise AssertionError("R28 visual QA is absent, stale, or failed")

    replay_path = ROOT / "replay/independent-review.json"
    replay = json.loads(replay_path.read_text(encoding="utf-8")) if replay_path.exists() else None
    if replay is not None:
        current_manifest = ROOT / "candidate.manifest.json"
        if (
            replay.get("schema") != "mathematics-commons-stacks-errata-independent-review/v1"
            or replay.get("candidate_id") != CONFIG["candidate_id"]
            or replay.get("passed") is not True
            or replay.get("result") != "PASS"
            or replay.get("pass_is_unconditional") is not True
            or not current_manifest.is_file()
            or replay.get("pre_review_manifest_sha256") != sha256(current_manifest)
            or replay.get("validation_sha256") != sha256(validation_path)
        ):
            raise AssertionError("R28 independent review receipt is stale or failed")
        generated_at = replay["recorded_at_utc"]
        replay_note = (
            "Independent replay passed against the pre-review manifest "
            f"{replay['pre_review_manifest_sha256']}; this final manifest rebind adds only the replay receipt."
        )
    else:
        execution = json.loads((ROOT / "builds/build-execution.json").read_text(encoding="utf-8"))
        generated_at = execution["completed_at_utc"]
        replay_note = "Independent replay is pending against this pre-review manifest."

    authority_paths = sorted(path for path in (ROOT / "authority").rglob("*") if path.is_file())
    singled = {
        "stable_unit_manifest": ROOT / "stable-units.json",
        "source_map": ROOT / "source-map.jsonl",
        "decision_ledger": ROOT / "decisions.jsonl",
        "rejection_ledger": ROOT / "rejections.jsonl",
        "formula_diagram_inventory": ROOT / "formula-diagram-inventory.json",
    }
    excluded = {ROOT / "candidate.manifest.json", *authority_paths, *singled.values()}
    build_paths = sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file() and path not in excluded and "__pycache__" not in path.parts
    )
    manifest = {
        "$schema": "../../../../../schemas/candidate-manifest.schema.json",
        "schema": "mathematics-commons-stacks-candidate-manifest/v1",
        "candidate_id": CONFIG["candidate_id"],
        "lease_id": CONFIG["lease_id"],
        "namespace": CONFIG["namespace"],
        "writer_task": CONFIG["writer_task"],
        "upstream": {
            "lock": "upstream/stacks.lock.json",
            "commit": CONFIG["authority_commit"],
            "tree": CONFIG["authority_tree"],
        },
        "source_authorities": [evidence(path) for path in authority_paths],
        "source_closure": {
            "enumerated": True,
            "expected_units": 1,
            "manifested_units": 1,
            "complete": True,
        },
        **{key: evidence(path) for key, path in singled.items()},
        "builds": [evidence(path) for path in build_paths],
        "rights_state": (
            "The official authority, public cumulative composition base, standalone payload, and composition projection retain "
            "the Stacks Project GNU Free Documentation License 1.2; metadata and receipts do not relicense upstream content. "
            "This is an independently maintained AI-produced English correction with no Stacks Project review, approval, "
            "affiliation, or endorsement. Legal certification was not performed."
        ),
        "review_state": "performed" if replay else "partial",
        "independent_replay": "passed" if replay else "not_performed",
        "unresolved_defects": [
            replay_note,
            "R28 supersedes the mathematical replacement in MC-STK-ERR-1183 while retaining R26 byte-for-byte as historical provenance.",
            "The isolated smoothing.tex reader retains the same cross-chapter undefined-reference target multiset as the frozen authority reader.",
            "Three inherited overfull-box diagnostics and one inherited underfull-box diagnostic remain; all 37 candidate pages and correction-sensitive page 16 were visually inspected with no clipping, overlap, broken diagram, blank page, missing glyph, or unreadable content.",
            "The standalone PDF is untagged; its fonts are embedded and have ToUnicode maps.",
            "Cumulative composition must apply only the exact superseding fragment against public commit f8e6c227aa3dc89256427f3b64a2ad330d5ff221; the isolated payload must not be copied wholesale.",
            "Canonical translations preserve their own frozen authority/emendation contracts and are not silently changed by this English corrected overlay.",
        ],
        "stop_conditions": [
            "Do not mutate the literal stacks-project master mirror or the admitted R26 candidate.",
            "Do not reuse stable ID MC-STK-ERR-1183; compose MC-STK-ERR-1216 as its explicit last-wins supersession.",
            "Do not copy the isolated R28 payload wholesale into the cumulative English edition.",
            "Do not apply this correction silently to canonical translation source or PDFs.",
            "Do not contact or submit to upstream Stacks maintainers under the current no-AI-contribution boundary.",
            "Do not admit R28 except in a separate registry commit bound to this final manifest and passed replay receipt.",
        ],
        "generated_at_utc": generated_at,
    }
    output = ROOT / "candidate.manifest.json"
    output.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="",
    )
    print(json.dumps({"passed": True, "reviewed": bool(replay), "manifest_sha256": sha256(output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
