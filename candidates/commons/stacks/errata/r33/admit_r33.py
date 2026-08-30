from __future__ import annotations

import hashlib
import json
from pathlib import Path

import regenerate_r33
import verify_r33


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
REGISTRY = REPO / "registry/overlays.json"
LEASES = REPO / "registry/leases.json"
RECEIPT = REPO / "registry/admission-receipts/r33.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="")


def main() -> int:
    core = verify_r33.verify_core()
    verify_r33.verify_manifest()
    review = json.loads((ROOT / "replay/independent-review.json").read_text(encoding="utf-8"))
    if review.get("passed") is not True or review.get("pass_is_unconditional") is not True:
        raise AssertionError("independent review is absent or failed")
    manifest_sha = sha(ROOT / "candidate.manifest.json")
    registry_before_sha = sha(REGISTRY)
    leases_before_sha = sha(LEASES)
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    entries = registry["registered_entries"]
    if entries[-1]["id"] != "stacks-errata-a04446e-r32" or any(row["id"] == regenerate_r33.CANDIDATE for row in entries):
        raise AssertionError("registry is not at the exact R32 head")
    stable_ids = [f"MC-STK-ERR-{number}" for number in range(1288, 1295)]
    allocated = {stable for row in entries for stable in row["stable_ids"]}
    collisions = sorted(set(stable_ids) & allocated)
    if collisions:
        raise AssertionError(f"stable ID collision: {collisions}")
    entries.append({
        "id": regenerate_r33.CANDIDATE,
        "namespace": "commons/stacks/errata/r33",
        "writer": regenerate_r33.WRITER,
        "source_commit": regenerate_r33.COMMIT,
        "source_tree": regenerate_r33.TREE,
        "manifest_sha256": manifest_sha,
        "stable_ids": stable_ids,
        "rights_state": "The authority and modified payload retain the Stacks Project GNU Free Documentation License 1.2; metadata and receipts do not relicense upstream content. This independently maintained AI-produced English correction overlay has no Stacks Project review, approval, affiliation, or endorsement.",
        "review_receipt": "candidates/commons/stacks/errata/r33/replay/independent-review.json",
        "admitted_at_utc": regenerate_r33.STAMP,
    })
    write(REGISTRY, registry)

    leases = json.loads(LEASES.read_text(encoding="utf-8"))
    events = leases["events"]
    if events[-1]["event_id"] != "lease-event-000069" or events[-1]["state"] != "released":
        raise AssertionError("lease registry is not at the exact R32 head")
    common = {
        "lease_id": regenerate_r33.LEASE, "namespace": "commons/stacks/errata/r33",
        "candidate_path": "candidates/commons/stacks/errata/r33", "writer_task": regenerate_r33.WRITER,
        "upstream_commit": regenerate_r33.COMMIT, "upstream_tree": regenerate_r33.TREE,
        "issued_at_utc": regenerate_r33.STAMP, "writer_contract": "candidates/CONTRACT.md",
    }
    events.append({"event_id": "lease-event-000070", "event": "issued", **common, "state": "active", "supersedes_event_id": "lease-event-000069"})
    events.append({"event_id": "lease-event-000071", "event": "released", **common, "state": "released", "supersedes_event_id": "lease-event-000070"})
    write(LEASES, leases)

    receipt = {
        "schema": "mathematics-commons-stacks-registry-admission-receipt/v1",
        "candidate_id": regenerate_r33.CANDIDATE, "admitted_at_utc": regenerate_r33.STAMP,
        "manifest": {"path": "candidates/commons/stacks/errata/r33/candidate.manifest.json", "bytes": (ROOT / "candidate.manifest.json").stat().st_size, "sha256": manifest_sha},
        "source_map": {"path": "candidates/commons/stacks/errata/r33/source-map.jsonl", "bytes": (ROOT / "source-map.jsonl").stat().st_size, "sha256": sha(ROOT / "source-map.jsonl")},
        "stable_ids": stable_ids, "stable_id_count": 7,
        "producer_ids": ["P08-E262", "P08-E263", "P08-E264", "P08-E265", "P08-E266", "P08-E588", "P08-E589", "P08-E590", "P08-E591", "P08-E592", "P08-E593", "P08-E594"],
        "canonical_representatives": ["P08-E262", "P08-E263", "P08-E264", "P08-E265", "P08-E266", "P08-E593", "P08-E594"],
        "duplicate_aliases": ["P08-E588", "P08-E589", "P08-E590", "P08-E591", "P08-E592"],
        "registry": {"before_sha256": registry_before_sha, "after_sha256": sha(REGISTRY), "last_overlay": regenerate_r33.CANDIDATE},
        "leases": {"before_sha256": leases_before_sha, "after_sha256": sha(LEASES), "issued_event": "lease-event-000070", "released_event": "lease-event-000071"},
        "fresh_replay": {"passed": True, **core},
        "constraints": {"authority_mutated": False, "producer_target_mutated": False, "generated_source_composed": False, "generated_source_pushed": False, "published": False},
        "status": "PASS",
    }
    write(RECEIPT, receipt)
    print(json.dumps({"passed": True, "candidate_id": regenerate_r33.CANDIDATE, "manifest_sha256": manifest_sha, "registry_sha256": sha(REGISTRY), "leases_sha256": sha(LEASES), "receipt_sha256": sha(RECEIPT)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
