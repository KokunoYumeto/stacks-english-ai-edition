from __future__ import annotations
import hashlib, json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent
IDS = [f"MC-STK-ERR-{n:04d}" for n in range(1217, 1247)]
def sha(data: bytes) -> str: return hashlib.sha256(data).hexdigest().upper()
def load_jsonl(path: Path) -> list[dict]: return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
def main() -> int:
    config = json.loads((ROOT / "candidate.config.json").read_text(encoding="utf-8"))
    stable = json.loads((ROOT / "stable-units.json").read_text(encoding="utf-8"))
    source_map = load_jsonl(ROOT / "source-map.jsonl")
    spec = json.loads((ROOT / "operation-spec.json").read_text(encoding="utf-8"))
    authority = (ROOT / "authority/source/sites-modules.tex").read_bytes()
    payload = (ROOT / "payload/sites-modules.tex").read_bytes()
    if config["expected_unit_ids"] != IDS: raise AssertionError("stable ID range mismatch")
    if [row["id"] for row in stable["units"]] != IDS: raise AssertionError("stable-unit order mismatch")
    if [row["unit_id"] for row in source_map] != IDS: raise AssertionError("source-map order mismatch")
    ops = spec["operations"]
    if len(ops) != 31 or spec["operation_count"] != 31: raise AssertionError("operation count mismatch")
    if sha(authority) != spec["authority_sha256"]: raise AssertionError("authority hash mismatch")
    intervals = []
    for row in ops:
        start, end = row["start_byte"], row["end_byte_exclusive"]
        old, new = row["old_text"].encode(), row["replacement_text"].encode()
        if authority[start:end] != old: raise AssertionError(f"preimage mismatch: {row['operation_id']}")
        if sha(old) != row["old_sha256"] or sha(new) != row["replacement_sha256"]: raise AssertionError("span hash mismatch")
        if authority[:start].count(b"\n") + 1 != row["source_start_line"]: raise AssertionError("start line mismatch")
        if authority[:max(start, end-1)].count(b"\n") + 1 != row["source_end_line"]: raise AssertionError("end line mismatch")
        intervals.append((start, end, row))
    for left, right in zip(sorted(intervals), sorted(intervals)[1:]):
        if left[1] > right[0]: raise AssertionError("overlap")
    replay = authority
    for start, end, row in sorted(intervals, reverse=True):
        replay = replay[:start] + row["replacement_text"].encode() + replay[end:]
    if replay != payload: raise AssertionError("payload replay mismatch")
    expected_payload = config["stems"]["sites-modules"]
    if len(payload) != expected_payload["payload_bytes"] or sha(payload) != expected_payload["payload_sha256"]: raise AssertionError("payload identity mismatch")
    mapped = [op["operation_id"] for unit in source_map for op in unit["operations"]]
    if mapped != [op["operation_id"] for op in ops]: raise AssertionError("source-map/spec operation mismatch")
    report = json.loads((ROOT / "source-validation.json").read_text(encoding="utf-8"))
    if report["passed"] is not True or report["payload"]["sha256"] != sha(payload): raise AssertionError("source-validation receipt stale")
    print(json.dumps({"passed": True, "units": 30, "operations": 31, "payload_sha256": sha(payload)}, sort_keys=True))
    return 0
if __name__ == "__main__": raise SystemExit(main())
