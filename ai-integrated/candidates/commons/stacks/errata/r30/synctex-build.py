from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / "candidate.config.json").read_text(encoding="utf-8"))
if len(CONFIG["stems"]) != 1:
    raise AssertionError("R30 SyncTeX build requires exactly one configured stem")
STEM = next(iter(CONFIG["stems"]))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def run(argv: list[str], cwd: Path, env: dict[str, str]) -> None:
    result = subprocess.run(argv, cwd=cwd, env=env, check=False)
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {' '.join(argv)}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a private SyncTeX-enabled replay of the sealed R30 candidate PDF."
    )
    parser.add_argument("--upstream-root", type=Path, required=True)
    parser.add_argument("--work-root", type=Path, required=True)
    args = parser.parse_args()
    upstream = args.upstream_root.resolve()
    work = args.work_root.resolve()
    if not upstream.is_dir():
        raise FileNotFoundError(upstream)
    if work.exists():
        raise FileExistsError(f"work root must be new and absent: {work}")
    if work == ROOT or ROOT in work.parents or work == upstream or upstream in work.parents:
        raise ValueError("work root must be outside candidate and frozen upstream")

    source = upstream / f"{STEM}.tex"
    expected = CONFIG["stems"][STEM]
    if not source.is_file() or sha256(source) != expected["authority_sha256"]:
        raise AssertionError("frozen upstream source identity mismatch")
    shutil.copytree(upstream, work)
    shutil.copy2(ROOT / "payload" / f"{STEM}.tex", work / f"{STEM}.tex")
    if sha256(work / f"{STEM}.tex") != expected["payload_sha256"]:
        raise AssertionError("candidate payload identity mismatch")

    env = os.environ.copy()
    env["SOURCE_DATE_EPOCH"] = str(CONFIG["source_date_epoch"])
    env["FORCE_SOURCE_DATE"] = "1"
    env["TZ"] = "UTC"
    latex = [
        "pdflatex", "-interaction=nonstopmode", "-halt-on-error",
        "-file-line-error", "-synctex=1", f"{STEM}.tex",
    ]
    run(latex, work, env)
    run(["bibtex", STEM], work, env)
    run(latex, work, env)
    run(latex, work, env)

    sealed = ROOT / "builds" / f"{STEM}.pdf"
    auxiliary = work / f"{STEM}.pdf"
    synctex = work / f"{STEM}.synctex.gz"
    if not sealed.is_file() or not synctex.is_file():
        raise FileNotFoundError("sealed PDF or generated SyncTeX file is missing")
    if auxiliary.stat().st_size != sealed.stat().st_size or sha256(auxiliary) != sha256(sealed):
        raise AssertionError("SyncTeX-enabled auxiliary PDF differs from the sealed deterministic PDF")
    receipt = {
        "schema": "mathematics-commons-stacks-private-synctex-build/v1",
        "candidate_id": CONFIG["candidate_id"],
        "source_date_epoch": CONFIG["source_date_epoch"],
        "source_sha256": sha256(work / f"{STEM}.tex"),
        "pdf_sha256": sha256(auxiliary),
        "synctex_sha256": sha256(synctex),
        "private_paths_published": False,
        "passed": True,
    }
    (work / ".r30-synctex-build.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline=""
    )
    print(json.dumps({"passed": True, "work_root": str(work), "pdf_sha256": receipt["pdf_sha256"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
