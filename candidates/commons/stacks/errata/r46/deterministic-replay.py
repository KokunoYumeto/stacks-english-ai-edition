from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / "candidate.config.json").read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first-private-build-root", type=Path, required=True)
    args = parser.parse_args()
    rows = []
    passed = True
    for stem in CONFIG["stems"]:
        for phase, suffix in (("candidate", ""), ("authority", ".authority")):
            first = args.first_private_build_root / f"{stem}.{phase}.pdf"
            second = ROOT / "builds" / f"{stem}{suffix}.pdf"
            same = first.stat().st_size == second.stat().st_size and sha256(first) == sha256(second)
            rows.append(
                {
                    "stem": stem,
                    "phase": phase,
                    "first_bytes": first.stat().st_size,
                    "first_sha256": sha256(first),
                    "second_path": second.relative_to(ROOT).as_posix(),
                    "second_bytes": second.stat().st_size,
                    "second_sha256": sha256(second),
                    "byte_identical": same,
                }
            )
            passed = passed and same
            first_fls = args.first_private_build_root / f"{stem}.{phase}.fls-dependencies.json"
            second_fls = ROOT / "builds" / f"{stem}{suffix}.fls-dependencies.json"
            first_inventory = json.loads(first_fls.read_text(encoding="utf-8"))
            second_inventory = json.loads(second_fls.read_text(encoding="utf-8"))
            closure_same = (
                first_inventory["input_closure_sha256"] == second_inventory["input_closure_sha256"]
                and first_inventory["input_count"] == second_inventory["input_count"]
                and first_inventory["output_count"] == second_inventory["output_count"]
                and first_inventory["all_inputs_exist_and_hashed"] is True
                and second_inventory["all_inputs_exist_and_hashed"] is True
                and first_inventory["outputs_confined_to_worktree"] is True
                and second_inventory["outputs_confined_to_worktree"] is True
            )
            rows[-1]["first_fls_inventory_bytes"] = first_fls.stat().st_size
            rows[-1]["first_fls_inventory_sha256"] = sha256(first_fls)
            rows[-1]["second_fls_inventory_path"] = second_fls.relative_to(ROOT).as_posix()
            rows[-1]["second_fls_inventory_bytes"] = second_fls.stat().st_size
            rows[-1]["second_fls_inventory_sha256"] = sha256(second_fls)
            rows[-1]["fls_input_closure_sha256"] = second_inventory["input_closure_sha256"]
            rows[-1]["fls_input_closure_byte_identical"] = closure_same
            passed = passed and closure_same
    receipt = {
        "schema": "mathematics-commons-stacks-deterministic-pdf-replay/v1",
        "candidate_id": CONFIG["candidate_id"],
        "source_date_epoch": CONFIG["source_date_epoch"],
        "fresh_builds_compared": 2,
        "recorder_fls_closures_compared": 2 * len(CONFIG["stems"]),
        "pdfs": rows,
        "passed": passed,
        "private_paths_published": False,
    }
    output = ROOT / "builds/deterministic-replay.json"
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")
    print(json.dumps({"passed": passed, "receipt": str(output)}))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
