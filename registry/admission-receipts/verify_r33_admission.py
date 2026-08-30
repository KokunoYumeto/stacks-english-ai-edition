from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CANDIDATE = ROOT / "candidates/commons/stacks/errata/r33"
REGISTRY = ROOT / "registry/overlays.json"
LEASES = ROOT / "registry/leases.json"
RECEIPT = ROOT / "registry/admission-receipts/r33.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> int:
    manifest_path = CANDIDATE / "candidate.manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    references = []
    for key in ("source_authorities", "builds"):
        references.extend(manifest[key])
    for key in ("stable_unit_manifest", "source_map", "decision_ledger", "rejection_ledger", "formula_diagram_inventory"):
        references.append(manifest[key])
    paths = [row["path"] for row in references]
    actual = sorted(path.relative_to(CANDIDATE).as_posix() for path in CANDIDATE.rglob("*") if path.is_file() and path.name != "candidate.manifest.json" and "__pycache__" not in path.parts)
    if len(paths) != len(set(paths)) or sorted(paths) != actual:
        raise AssertionError("candidate manifest closure mismatch")
    for row in references:
        if sha(CANDIDATE / row["path"]) != row["sha256"]:
            raise AssertionError(f"candidate manifest hash mismatch: {row['path']}")

    spec = json.loads((CANDIDATE / "operation-spec.json").read_text(encoding="utf-8"))
    authority = (CANDIDATE / "authority/source/spaces-morphisms.tex").read_bytes()
    replay = authority
    for op in sorted(spec["operations"], key=lambda item: item["start_byte"], reverse=True):
        start, end = op["start_byte"], op["end_byte_exclusive"]
        old = op["old_text"].encode("utf-8")
        new = op["replacement_text"].encode("utf-8")
        if replay[start:end] != old:
            raise AssertionError(f"operation preimage mismatch: {op['operation_id']}")
        replay = replay[:start] + new + replay[end:]
    if replay != (CANDIDATE / "payload/spaces-morphisms.tex").read_bytes():
        raise AssertionError("fresh payload replay mismatch")

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    entry = registry["registered_entries"][-1]
    stable_ids = [f"MC-STK-ERR-{number}" for number in range(1288, 1295)]
    if entry["id"] != "stacks-errata-a04446e-r33" or entry["manifest_sha256"] != sha(manifest_path) or entry["stable_ids"] != stable_ids:
        raise AssertionError("R33 registry binding mismatch")
    all_ids = [stable for row in registry["registered_entries"] for stable in row["stable_ids"]]
    if len(all_ids) != len(set(all_ids)):
        raise AssertionError("registry stable ID collision")

    leases = json.loads(LEASES.read_text(encoding="utf-8"))["events"]
    if [(row["event_id"], row["event"], row["lease_id"], row["state"]) for row in leases[-2:]] != [
        ("lease-event-000070", "issued", "stacks-lease-000037-errata-r33", "active"),
        ("lease-event-000071", "released", "stacks-lease-000037-errata-r33", "released"),
    ]:
        raise AssertionError("R33 lease tail mismatch")
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    if receipt.get("status") != "PASS" or receipt["manifest"]["sha256"] != sha(manifest_path) or receipt["registry"]["after_sha256"] != sha(REGISTRY) or receipt["leases"]["after_sha256"] != sha(LEASES):
        raise AssertionError("R33 admission receipt mismatch")
    print(json.dumps({"passed": True, "candidate_id": entry["id"], "manifest_sha256": sha(manifest_path), "registry_sha256": sha(REGISTRY), "leases_sha256": sha(LEASES), "manifest_references": len(references), "operations": len(spec["operations"]), "stable_ids": len(stable_ids)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
