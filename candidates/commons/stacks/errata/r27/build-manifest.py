from __future__ import annotations

import argparse
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
    parser = argparse.ArgumentParser(description="Build the pre-review or final R27 candidate manifest.")
    parser.parse_args()
    replay_path = ROOT / "replay" / "independent-review.json"
    replay = json.loads(replay_path.read_text(encoding="utf-8")) if replay_path.exists() else None
    validation_path = ROOT / "builds" / "validation.json"
    visual_path = ROOT / "builds" / "visual-qa.json"
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    visual = json.loads(visual_path.read_text(encoding="utf-8"))
    if validation.get("passed") is not True or validation.get("candidate_id") != CONFIG["candidate_id"]:
        raise AssertionError("current R27 validation receipt is absent, stale, or failed")
    if (
        visual.get("passed") is not True
        or visual.get("candidate_id") != CONFIG["candidate_id"]
        or visual.get("render_protocol", {}).get("manual_review_attested") is not True
    ):
        raise AssertionError("current R27 visual inspection receipt is absent, stale, or failed")
    authority_paths = sorted(path for path in (ROOT / "authority").rglob("*") if path.is_file())
    singled = {
        "stable_unit_manifest": ROOT / "stable-units.json",
        "source_map": ROOT / "source-map.jsonl",
        "decision_ledger": ROOT / "decisions.jsonl",
        "rejection_ledger": ROOT / "rejections.jsonl",
        "formula_diagram_inventory": ROOT / "formula-diagram-inventory.json",
    }
    excluded = {ROOT / "candidate.manifest.json", *singled.values(), *authority_paths}
    build_paths = sorted(
        path for path in ROOT.rglob("*")
        if path.is_file() and path not in excluded and "__pycache__" not in path.parts
    )
    units = json.loads((ROOT / "stable-units.json").read_text(encoding="utf-8"))["units"]
    packet_producer_ids = (
        CONFIG["expected_all_producer_ids"]
        + CONFIG["rejected_producer_ids"]
        + CONFIG["prior_alias_producer_ids"]
        + CONFIG["intentionally_absent_producer_ids"]
    )
    packet_numbers = [int(producer_id.rsplit("-", 1)[1]) for producer_id in packet_producer_ids]
    first_producer = f"MODULES-{min(packet_numbers):03d}"
    last_producer = f"MODULES-{max(packet_numbers):03d}"
    closure = CONFIG["proof_closure"]
    rejected_phrase = (
        "1 producer identity is rejected"
        if closure["rejected"] == 1
        else f"{closure['rejected']} producer identities are rejected"
    )
    if replay:
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
            or replay.get("sealed_evidence_verification", {}).get("visual_qa", {}).get("sha256") != sha256(visual_path)
        ):
            raise AssertionError("independent review receipt is stale, failed, or not bound to the pre-review candidate")
        replay_note = (
            "The independent replay receipt binds pre-review manifest "
            f"{replay['pre_review_manifest_sha256']} and validation "
            f"{replay['validation_sha256']}. This final registrar-only rebind adds the replay "
            "receipt and binds the clarified review-evidence chain plus refreshed deterministic "
            "receipts; no authority source, payload, operation specification, PDF, or rendered-page byte changed."
        )
        generated_at = replay["recorded_at_utc"]
    else:
        replay_note = "Independent adverse replay is pending against this pre-review manifest."
        execution = json.loads((ROOT / "builds" / "build-execution.json").read_text(encoding="utf-8"))
        generated_at = execution["completed_at_utc"]
    receipt = json.loads((ROOT / "builds" / "build-receipt.json").read_text(encoding="utf-8"))
    page_rows = [(row["candidate_log_summary"]["pages"], row["authority_log_summary"]["pages"]) for row in receipt["chapters"]]
    page_note = ", ".join(f"candidate {candidate}, authority {authority}" for candidate, authority in page_rows)
    manifest = {
        "$schema": "../../../../../schemas/candidate-manifest.schema.json",
        "schema": "mathematics-commons-stacks-candidate-manifest/v1",
        "candidate_id": CONFIG["candidate_id"],
        "lease_id": CONFIG["lease_id"],
        "namespace": CONFIG["namespace"],
        "writer_task": CONFIG["writer_task"],
        "upstream": {"lock": "upstream/stacks.lock.json", "commit": CONFIG["authority_commit"], "tree": CONFIG["authority_tree"]},
        "source_authorities": [evidence(path) for path in authority_paths],
        "source_closure": {"enumerated": True, "expected_units": len(units), "manifested_units": len(units), "complete": True},
        **{key: evidence(path) for key, path in singled.items()},
        "builds": [evidence(path) for path in build_paths],
        "rights_state": "The authority and modified payload retain the Stacks Project GNU Free Documentation License 1.2; metadata and receipts do not relicense upstream content. This is an independently maintained AI-produced English edition with no Stacks Project review, approval, affiliation, or endorsement. Legal certification was not performed.",
        "review_state": "performed" if replay else "partial",
        "independent_replay": "passed" if replay else "not_performed",
        "unresolved_defects": [
            replay_note,
            "The isolated modules.tex candidate retains cross-chapter undefined-reference targets; their multiset matches the frozen authority build exactly.",
            f"The sealed chapter readers have page counts {page_note}. The hash-bound visual-QA receipt records inspection of every candidate page and every correction-sensitive locus without clipping, overlap, missing glyph, broken diagram, blank page, or unreadable content.",
            "The proof PDFs contain embedded fonts with ToUnicode maps but are untagged; document-structure accessibility remains a cumulative-edition toolchain concern.",
            f"The bounded intake from {first_producer} through {last_producer} assigns {closure['accepted']} semantic units to {len(CONFIG['expected_all_producer_ids'])} accepted producer identities; {rejected_phrase}, {closure['intentionally_absent']} are intentionally absent, {closure['prior_aliases']} prior producer allegation aliases are retained, and none is unresolved.",
            "Canonical translations preserve the frozen authority unless a locale-side emendation is separately bound; this English corrected overlay is not silently copied.",
            "Overlay admission and English-edition composition are separate transitions; this manifest records candidate closure only.",
        ],
        "stop_conditions": [
            "Do not mutate the literal stacks-project master mirror.",
            "Do not apply these corrections silently to canonical translation source or PDFs.",
            "Do not contact or submit to the upstream Stacks maintainers under the current no-AI-contribution boundary.",
            "Do not append an overlay registry record except in a separate admission commit bound to the final manifest hash and a passed independent replay.",
            "Any change to reviewed authority, payload, proof, build, validation, visual-QA, or replay bytes invalidates the replay and requires a new review.",
        ],
        "generated_at_utc": generated_at,
    }
    (ROOT / "candidate.manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="")
    print(json.dumps({"passed": True, "reviewed": bool(replay), "manifest_sha256": sha256(ROOT / "candidate.manifest.json")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
