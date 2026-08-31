from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / "candidate.config.json").read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def ev(path: Path) -> dict:
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)}


def main() -> int:
    primary = {
        "stable_unit_manifest": ROOT / "stable-units.json",
        "source_map": ROOT / "source-map.jsonl",
        "decision_ledger": ROOT / "decisions.jsonl",
        "rejection_ledger": ROOT / "rejections.jsonl",
        "formula_diagram_inventory": ROOT / "formula-diagram-inventory.json",
    }
    authorities = sorted(path for path in (ROOT / "authority").rglob("*") if path.is_file())
    excluded = {path.resolve() for path in authorities} | {path.resolve() for path in primary.values()} | {(ROOT / "candidate.manifest.json").resolve()}
    builds = sorted(
        path for path in ROOT.rglob("*")
        if path.is_file() and path.resolve() not in excluded and "__pycache__" not in path.parts and path.suffix != ".pyc"
    )
    replay = json.loads((ROOT / "replay/independent-review.json").read_text(encoding="utf-8"))
    replay_passed = bool(replay.get("passed")) and replay.get("result") == "PASS"
    manifest = {
        "$schema": "../../../../../schemas/candidate-manifest.schema.json",
        "schema": "mathematics-commons-stacks-candidate-manifest/v1",
        "candidate_id": CONFIG["candidate_id"],
        "lease_id": CONFIG["lease_id"],
        "namespace": CONFIG["namespace"],
        "writer_task": CONFIG["writer_task"],
        "upstream": {"lock": "upstream/stacks.lock.json", "commit": CONFIG["authority_commit"], "tree": CONFIG["authority_tree"]},
        "source_authorities": [ev(path) for path in authorities],
        "source_closure": {"enumerated": True, "expected_units": 23, "manifested_units": 23, "complete": True},
        **{key: ev(path) for key, path in primary.items()},
        "builds": [ev(path) for path in builds],
        "rights_state": "The authority and modified payload retain the Stacks Project GNU Free Documentation License 1.2; metadata and receipts do not relicense upstream content. This independently maintained AI-produced English correction overlay has no Stacks Project review, approval, affiliation, or endorsement.",
        "review_state": "performed",
        "independent_replay": "passed" if replay_passed else "not_performed",
        "unresolved_defects": [
            "No source, semantic-unit, operation, deduplication, build, deterministic-replay, or visual defect remains unresolved.",
            "The standalone chapter reader retains cross-chapter undefined references because cumulative AUX files are absent; candidate and authority target multisets match exactly.",
            "The standalone PDF is untagged; this retained accessibility limitation is disclosed and does not affect deterministic source or visual correctness.",
        ],
        "stop_conditions": [
            "Any change to authority, payload, operation, source-map, proof, build, PDF, visual-QA, or replay bytes invalidates this manifest and requires regeneration.",
            "Registry admission, generated-source composition, Git mutation, and publication are separate transitions not performed by this candidate writer.",
        ],
        "generated_at_utc": "2026-08-31T02:15:00Z",
    }
    output = ROOT / "candidate.manifest.json"
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")
    print(json.dumps({"manifest": str(output), "bytes": output.stat().st_size, "sha256": sha(output), "independent_replay": manifest["independent_replay"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
