from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
AUTHORITY = ROOT.parents[6] / "upstream/src/stacks-project-a04446e57ec1fbc252a871afcec7752fb2807b14/more-algebra.tex"
AUTHORITY_SHA256 = "0106554339E8966FE04411B2AE9F9CD856B165849FEEF0C7BC37634819064708"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def main() -> int:
    authority = AUTHORITY.read_bytes()
    if sha(authority) != AUTHORITY_SHA256 or len(authority) != 1_492_039:
        raise AssertionError("authority mismatch")
    lease = json.loads((ROOT / "LEASE.json").read_text(encoding="utf-8"))
    spec = json.loads((ROOT / "R22_MORE_ALGEBRA_ADJUDICATION_SPEC.json").read_text(encoding="utf-8"))
    ops = json.loads((ROOT / "operation-spec.input.json").read_text(encoding="utf-8"))["operations"]
    stable = json.loads((ROOT / "stable-units.input.json").read_text(encoding="utf-8"))["units"]
    config = json.loads((ROOT / "candidate.config.input.json").read_text(encoding="utf-8"))
    rejections = [json.loads(line) for line in (ROOT / "rejections.input.jsonl").read_text(encoding="utf-8").splitlines() if line]
    unresolved = json.loads((ROOT / "unresolved-intake.json").read_text(encoding="utf-8"))
    validation = json.loads((ROOT / "INTAKE_VALIDATION.json").read_text(encoding="utf-8"))
    if lease["lease_id"] != "stacks-lease-000025-errata-r22":
        raise AssertionError("lease mismatch")
    expected = [f"MC-STK-ERR-{n:04d}" for n in range(915, 998)]
    if [row["stable_id"] for row in spec["accepted"]] != expected or [row["id"] for row in stable] != expected:
        raise AssertionError("stable-ID sequence mismatch")
    if len(spec["accepted"]) != 83 or len(ops) != 94 or len(spec["rejected"]) != 1 or len(rejections) != 1 or unresolved["count"] != 0:
        raise AssertionError("closure count mismatch")
    if validation["payload_preview_sha256"] != "7C6237F71A81886DD72B6F85BFF52182D653FB98668B0124DC10C05E93960623":
        raise AssertionError("payload preview identity drift")
    if config["accepted"] != 83 or config["operation_count"] != 94 or config["rejected"] != 1:
        raise AssertionError("config closure mismatch")
    if spec["intentionally_absent_producer_ids"] != ["MORE-ALGEBRA-I-009"]:
        raise AssertionError("intentionally absent producer record drift")
    if spec["accepted"][58]["producer_id"] != "MORE-ALGEBRA-I-039" or spec["accepted"][58]["stable_id"] != "MC-STK-ERR-0973":
        raise AssertionError("Lease-I physical-source order drift")
    if spec["rejected"][0]["producer_id"] != "MORE-ALGEBRA-I-027" or rejections[0]["producer_id"] != "MORE-ALGEBRA-I-027":
        raise AssertionError("Lease-I rejection drift")
    rejected_op = spec["rejected"][0]["proposed_operation"]
    if authority[rejected_op["start_byte"]:rejected_op["end_byte_exclusive"]] != rejected_op["old_text"].encode():
        raise AssertionError("rejected proposal preimage mismatch")
    lease_i = spec["accepted"][-31:]
    expected_aliases = [
        "P02-E0437", "P02-E0438", "P02-E0441", "P02-E0443", "P02-E0446", "P02-E0450",
        "P02-E0456", "P02-E0457", "P02-E0460", "P02-E0461", "P02-E0462", "P02-E0463",
        "P02-E0474", "P02-E0476", "P02-E0483", "P02-E0484", "P02-E0487", "P02-E0489",
        "P02-E0490", "P02-E0492", "P02-E0493", "P02-E0494", "P02-E0495", "P02-E0500",
        "P02-E0503", "P02-E0505", "P02-E0506", "P02-E0507", "P02-E0508", "P02-E0509", "P02-E0510",
    ]
    if [row["prior_p02_aliases"] for row in lease_i] != [[alias] for alias in expected_aliases]:
        raise AssertionError("Lease-I P02 alias dedup drift")
    linked = {
        row["producer_id"]: row["producer_ids"] for row in lease_i if len(row["producer_ids"]) > 1
    }
    expected_linked = {
        "MORE-ALGEBRA-I-007": ["MORE-ALGEBRA-I-007", "MORE-ALGEBRA-I-008"],
        "MORE-ALGEBRA-I-012": ["MORE-ALGEBRA-I-012", "MORE-ALGEBRA-I-013"],
        "MORE-ALGEBRA-I-015": ["MORE-ALGEBRA-I-015", "MORE-ALGEBRA-I-016"],
        "MORE-ALGEBRA-I-028": ["MORE-ALGEBRA-I-028", "MORE-ALGEBRA-I-029", "MORE-ALGEBRA-I-030"],
        "MORE-ALGEBRA-I-037": ["MORE-ALGEBRA-I-037", "MORE-ALGEBRA-I-038"],
    }
    if linked != expected_linked:
        raise AssertionError("Lease-I linked-unit collapse drift")
    normalized = {row["producer_id"]: row["operations"] for row in lease_i}
    if normalized["MORE-ALGEBRA-I-004"][0]["replacement_text"] != "the usual (equivalently, derived) completions":
        raise AssertionError("I-004 normalized wording drift")
    if normalized["MORE-ALGEBRA-I-025"][0]["replacement_text"] != "Let $M, N$ be finite $B$-modules.":
        raise AssertionError("I-025 normalized statement drift")
    if normalized["MORE-ALGEBRA-I-035"][0]["replacement_text"] != "|N_1(E, F)^\\bullet| \\leq \\max(\\kappa, |M_1^\\bullet|, |N_1^\\bullet|)":
        raise AssertionError("I-035 normalized bound drift")
    payload = authority
    ordered = sorted(ops, key=lambda row: row["start_byte"])
    for left, right in zip(ordered, ordered[1:]):
        if left["end_byte_exclusive"] > right["start_byte"]:
            raise AssertionError("operation overlap")
    for row in reversed(ordered):
        start, end = row["start_byte"], row["end_byte_exclusive"]
        old, new = row["old_text"].encode(), row["replacement_text"].encode()
        if payload[start:end] != old or sha(old) != row["old_sha256"] or sha(new) != row["replacement_sha256"]:
            raise AssertionError(f"operation mismatch: {row['operation_id']}")
        payload = payload[:start] + new + payload[end:]
    if sha(payload) != validation["payload_preview_sha256"] or len(payload) != validation["payload_preview_bytes"]:
        raise AssertionError("payload replay mismatch")
    print(json.dumps({"passed": True, "units": 83, "operations": 94, "rejected": 1, "payload_sha256": sha(payload)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
