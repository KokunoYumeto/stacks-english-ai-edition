from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
def sha(data: bytes) -> str: return hashlib.sha256(data).hexdigest().upper()
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    spec = json.loads((ROOT / "operation-spec.json").read_text(encoding="utf-8"))
    authority = (ROOT / "authority/source/sites-modules.tex").read_bytes()
    if sha(authority) != spec["authority_sha256"]: raise AssertionError("authority hash mismatch")
    data = authority
    intervals = sorted((row["start_byte"], row["end_byte_exclusive"], row) for row in spec["operations"])
    for left, right in zip(intervals, intervals[1:]):
        if left[1] > right[0]: raise AssertionError("overlapping operations")
    for start, end, row in reversed(intervals):
        old = row["old_text"].encode("utf-8")
        if data[start:end] != old: raise AssertionError(f"preimage mismatch: {row['operation_id']}")
        data = data[:start] + row["replacement_text"].encode("utf-8") + data[end:]
    payload = ROOT / "payload/sites-modules.tex"
    if args.write:
        payload.parent.mkdir(parents=True, exist_ok=True)
        payload.write_bytes(data)
    elif payload.read_bytes() != data:
        raise AssertionError("payload differs from deterministic replay")
    print(json.dumps({"bytes": len(data), "sha256": sha(data), "passed": True}, sort_keys=True))
    return 0
if __name__ == "__main__": raise SystemExit(main())
