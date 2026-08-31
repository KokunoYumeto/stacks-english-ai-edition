from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> int:
    required = [
        ROOT / "source-validation.json", ROOT / "builds/build-receipt.json",
        ROOT / "builds/deterministic-replay.json", ROOT / "builds/visual-qa.json",
        ROOT / "builds/validation.json", ROOT / "replay/independent-review.json",
    ]
    for path in required:
        row = json.loads(path.read_text(encoding="utf-8"))
        if not row.get("passed", row.get("status") == "PASS"):
            raise AssertionError(f"nonpassing receipt: {path}")
    config = json.loads((ROOT / "candidate.config.json").read_text(encoding="utf-8"))
    if config["expected_unit_ids"] != [f"MC-STK-ERR-{number:04d}" for number in range(1336, 1359)]:
        raise AssertionError("stable-ID sequence mismatch")
    if config["operation_count"] != 31 or config["proof_closure"] != {"accepted":23,"operations":31,"producer_rows":29,"registrar_additive_aliases":2,"rejected":0,"unresolved":0}:
        raise AssertionError("proof closure mismatch")
    local_account = Path.home().name.lower()
    windows_profile_marker = "c:" + chr(92) + "users" + chr(92)
    slash_profile_marker = "c:" + chr(47) + "users" + chr(47)
    for path in ROOT.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix.lower() in {".pdf", ".png", ".pyc"} or path.name.endswith(".tex"):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        if windows_profile_marker in text or slash_profile_marker in text or (local_account and local_account in text):
            raise AssertionError(f"private-path leakage: {path.relative_to(ROOT)}")
    result = subprocess.run([sys.executable, str(ROOT / "check-manifest.py")], cwd=ROOT, check=True, text=True, stdout=subprocess.PIPE)
    print(json.dumps({"passed": True, "candidate_manifest_sha256": sha(ROOT / "candidate.manifest.json"), "manifest_check": json.loads(result.stdout)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
