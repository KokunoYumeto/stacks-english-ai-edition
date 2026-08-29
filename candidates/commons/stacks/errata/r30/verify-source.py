from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    config = json.loads((ROOT / "candidate.config.json").read_text(encoding="utf-8"))
    spec = json.loads((ROOT / "operation-spec.json").read_text(encoding="utf-8"))
    units = json.loads((ROOT / "stable-units.json").read_text(encoding="utf-8"))["units"]
    source_map = load_jsonl(ROOT / "source-map.jsonl")
    authority = (ROOT / "authority/source/injectives.tex").read_bytes()
    payload = (ROOT / "payload/injectives.tex").read_bytes()
    expected_ids = [f"MC-STK-ERR-{number:04d}" for number in range(1247, 1287)]
    if config["expected_unit_ids"] != expected_ids:
        raise AssertionError("config stable-ID range mismatch")
    if [row["id"] for row in units] != expected_ids or [row["unit_id"] for row in source_map] != expected_ids:
        raise AssertionError("stable-unit/source-map order mismatch")
    operations = spec["operations"]
    if len(units) != 40 or len(source_map) != 40 or len(operations) != 40 or spec["operation_count"] != 40:
        raise AssertionError("40-unit/40-operation closure mismatch")
    if sha(authority) != config["stems"]["injectives"]["authority_sha256"]:
        raise AssertionError("authority identity mismatch")
    intervals = []
    for operation in operations:
        start, end = operation["start_byte"], operation["end_byte_exclusive"]
        old = operation["old_text"].encode()
        new = operation["replacement_text"].encode()
        if authority[start:end] != old:
            raise AssertionError(f"preimage mismatch: {operation['operation_id']}")
        if sha(old) != operation["old_sha256"] or sha(new) != operation["replacement_sha256"]:
            raise AssertionError(f"span hash mismatch: {operation['operation_id']}")
        actual_first = authority[:start].count(b"\n") + 1
        actual_last = authority[:max(start, end - 1)].count(b"\n") + 1
        if (actual_first, actual_last) != (operation["source_start_line"], operation["source_end_line"]):
            raise AssertionError(f"line mismatch: {operation['operation_id']}")
        intervals.append((start, end, operation))
    ascending = sorted(intervals)
    for left, right in zip(ascending, ascending[1:]):
        if left[1] > right[0]:
            raise AssertionError(f"overlapping operations: {left[2]['operation_id']}, {right[2]['operation_id']}")
    replay = authority
    for start, end, operation in sorted(intervals, reverse=True):
        replay = replay[:start] + operation["replacement_text"].encode() + replay[end:]
    if replay != payload:
        raise AssertionError("descending operation replay does not equal payload")
    authority_long_lines = sum(len(line) > 80 for line in authority.decode("utf-8").splitlines())
    payload_long_lines = sum(len(line) > 80 for line in payload.decode("utf-8").splitlines())
    if payload_long_lines > authority_long_lines:
        raise AssertionError(
            f"payload introduces new >80-character lines: authority={authority_long_lines}, payload={payload_long_lines}"
        )
    expected = config["stems"]["injectives"]
    if len(payload) != expected["payload_bytes"] or sha(payload) != expected["payload_sha256"]:
        raise AssertionError("payload identity mismatch")
    mapped = [operation for row in source_map for operation in row["operations"]]
    if mapped != operations:
        raise AssertionError("source-map and operation-spec differ")
    if (ROOT / "rejections.jsonl").read_bytes() != b"":
        raise AssertionError("R30 final adjudication has no rejected units")
    print(json.dumps({"passed": True, "units": 40, "operations": 40, "payload_bytes": len(payload), "payload_sha256": sha(payload), "stable_id_range": [expected_ids[0], expected_ids[-1]], "authority_long_lines_gt_80": authority_long_lines, "payload_long_lines_gt_80": payload_long_lines}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
