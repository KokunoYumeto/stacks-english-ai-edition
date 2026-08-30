from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import regenerate_r33


ROOT = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def verify_manifest() -> int:
    manifest = json.loads((ROOT / "candidate.manifest.json").read_text(encoding="utf-8"))
    references = []
    for key in ("source_authorities", "builds"):
        references.extend(manifest[key])
    for key in ("stable_unit_manifest", "source_map", "decision_ledger", "rejection_ledger", "formula_diagram_inventory"):
        references.append(manifest[key])
    paths = [row["path"] for row in references]
    actual = sorted(path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file() and path.name != "candidate.manifest.json" and "__pycache__" not in path.parts)
    if len(paths) != len(set(paths)) or sorted(paths) != actual:
        raise AssertionError(f"manifest closure mismatch: missing={sorted(set(actual)-set(paths))}, extra={sorted(set(paths)-set(actual))}")
    for row in references:
        if sha(ROOT / row["path"]) != row["sha256"]:
            raise AssertionError(f"manifest hash mismatch: {row['path']}")
    return len(references)


def verify_core() -> dict[str, object]:
    config = json.loads((ROOT / "candidate.config.json").read_text(encoding="utf-8"))
    authority = (ROOT / "authority/source/spaces-morphisms.tex").read_bytes()
    payload = (ROOT / "payload/spaces-morphisms.tex").read_bytes()
    if sha(ROOT / "authority/source/spaces-morphisms.tex") != regenerate_r33.AUTHORITY_SHA:
        raise AssertionError("authority hash mismatch")
    if sha(ROOT / "authority/producer/ERRATA_CANDIDATES.jsonl") != regenerate_r33.PRODUCER_SHA:
        raise AssertionError("producer hash mismatch")
    spec = json.loads((ROOT / "operation-spec.json").read_text(encoding="utf-8"))
    units = json.loads((ROOT / "stable-units.json").read_text(encoding="utf-8"))["units"]
    maps = [json.loads(line) for line in (ROOT / "source-map.jsonl").read_text(encoding="utf-8").splitlines() if line]
    crosswalk = json.loads((ROOT / "authority/producer/P08_E262_E266_E588_E594_ALIAS_CROSSWALK.json").read_text(encoding="utf-8"))
    expected_ids = [f"MC-STK-ERR-{number}" for number in range(1288, 1295)]
    if config["expected_unit_ids"] != expected_ids or [row["id"] for row in units] != expected_ids or [row["unit_id"] for row in maps] != expected_ids:
        raise AssertionError("stable ID order mismatch")
    if spec["operation_count"] != 7 or len(spec["operations"]) != 7 or len({op["operation_id"] for op in spec["operations"]}) != 7:
        raise AssertionError("operation closure mismatch")
    replay = authority
    for op in sorted(spec["operations"], key=lambda item: item["start_byte"], reverse=True):
        start, end = op["start_byte"], op["end_byte_exclusive"]
        old = op["old_text"].encode("utf-8")
        new = op["replacement_text"].encode("utf-8")
        if replay[start:end] != old or hashlib.sha256(old).hexdigest().upper() != op["old_sha256"] or hashlib.sha256(new).hexdigest().upper() != op["replacement_sha256"]:
            raise AssertionError(f"operation replay mismatch: {op['operation_id']}")
        replay = replay[:start] + new + replay[end:]
    if replay != payload or sha(ROOT / "payload/spaces-morphisms.tex") != config["stems"]["spaces-morphisms.tex"]["payload_sha256"]:
        raise AssertionError("fresh payload replay mismatch")
    if crosswalk["semantic_unit_count"] != 7 or crosswalk["producer_id_count"] != 12 or crosswalk["duplicate_alias_pair_count"] != 5:
        raise AssertionError("alias crosswalk counts mismatch")
    alias_map = {row["canonical_producer_id"]: row["duplicate_aliases"] for row in crosswalk["records"]}
    if alias_map != {"P08-E262": ["P08-E588"], "P08-E263": ["P08-E589"], "P08-E264": ["P08-E590"], "P08-E265": ["P08-E591"], "P08-E266": ["P08-E592"], "P08-E593": [], "P08-E594": []}:
        raise AssertionError("alias map mismatch")
    return {"authority_bytes": len(authority), "payload_bytes": len(payload), "payload_sha256": sha(ROOT / "payload/spaces-morphisms.tex"), "operations": 7, "stable_units": 7, "producer_ids": 12, "duplicate_alias_pairs": 5}


def verify_registry_pre_admission() -> dict[str, object]:
    registry_path = ROOT.parents[4] / "registry/overlays.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    entries = registry["registered_entries"]
    if entries[-1]["id"] != "stacks-errata-a04446e-r32" or any(entry["id"] == regenerate_r33.CANDIDATE for entry in entries):
        raise AssertionError("registry pre-admission head mismatch")
    allocated = {stable for entry in entries for stable in entry["stable_ids"]}
    collisions = sorted(allocated & {f"MC-STK-ERR-{number}" for number in range(1288, 1295)})
    if collisions:
        raise AssertionError(f"stable ID collisions: {collisions}")
    return {"path": "registry/overlays.json", "bytes": registry_path.stat().st_size, "sha256": sha(registry_path), "last_overlay": entries[-1]["id"], "stable_id_collisions": 0, "r33_absent": True, "passed": True}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-review", action="store_true")
    args = parser.parse_args()
    core = verify_core()
    registry = verify_registry_pre_admission()
    references = verify_manifest()
    if args.write_review:
        pre_manifest_sha = sha(ROOT / "candidate.manifest.json")
        receipt = {
            "schema": "mathematics-commons-stacks-errata-independent-review/v1",
            "candidate_id": regenerate_r33.CANDIDATE,
            "review_kind": "independent_exact_preimage_context_alias_and_payload_replay",
            "recorded_at_utc": regenerate_r33.STAMP,
            "passed": True, "result": "PASS", "conclusion": "UNCONDITIONAL PASS", "pass_is_unconditional": True,
            "pre_review_manifest_sha256": pre_manifest_sha,
            "scratch_replay": {"passed": True, "apply_order": "descending_start_byte", **core},
            "deduplication": {"passed": True, "canonical_representatives": ["P08-E262", "P08-E263", "P08-E264", "P08-E265", "P08-E266"], "duplicate_aliases": ["P08-E588", "P08-E589", "P08-E590", "P08-E591", "P08-E592"], "new_unique_rows": ["P08-E593", "P08-E594"], "semantic_units": 7, "producer_rows_preserved": 12},
            "registry_pre_admission": registry,
            "closure_checks": {"passed": True, "manifest_references": references, "stable_ids_unique": 7, "operation_ids_unique": 7, "source_map_rows": 7},
            "constraints_observed": {"upstream_authority_mutated": False, "locale_targets_mutated": False, "generated_source_composed": False, "generated_source_pushed": False, "registry_mutated_by_review": False},
            "adverse_observations": ["The five later ko-KR rows are preserved as duplicate aliases rather than applied twice.", "R33 is registrar-only; downstream source composition and publication are excluded."],
        }
        regenerate_r33.dump(ROOT / "replay/independent-review.json", receipt)
        regenerate_r33.build_manifest()
        references = verify_manifest()
    review = ROOT / "replay/independent-review.json"
    if review.is_file():
        parsed = json.loads(review.read_text(encoding="utf-8"))
        if parsed.get("passed") is not True or parsed.get("result") != "PASS":
            raise AssertionError("review receipt failed")
    print(json.dumps({"passed": True, "candidate_id": regenerate_r33.CANDIDATE, "manifest_sha256": sha(ROOT / "candidate.manifest.json"), "manifest_references": references, **core}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
