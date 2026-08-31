#!/usr/bin/env python3
"""Produce fresh source-page sidecars without changing fixed-point artifacts."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
from datetime import datetime, timezone

from build_fixed_point import FIXED_POINT_SUFFIXES

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "validation/stacks-errata-a04446e-r38-build-2026-08-31.json"
OUTPUT = ROOT / "validation/stacks-errata-a04446e-r38-synctex-instrumentation-2026-08-31.json"
STEMS = ("cohomology", "more-algebra", "sites-cohomology")


def identity(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest().upper()}


def snapshot(stem):
    return {stem + suffix: identity(ROOT / (stem + suffix))
            for suffix in FIXED_POINT_SUFFIXES if (ROOT / (stem + suffix)).is_file()}


def utc():
    return datetime.now(timezone.utc).isoformat()


def main():
    if OUTPUT.exists():
        raise RuntimeError("instrumentation receipt already exists; verify it rather than rerunning")
    build = json.loads(BUILD.read_bytes())
    if build.get("status") != "PASS":
        raise RuntimeError("a completed passing fixed-point build is required")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if head != build["source"]["commit"]:
        raise RuntimeError("instrumentation must run at the exact first-build head")
    artifacts = {row["stem"]: row for row in build["artifacts"]}
    environment = {"SOURCE_DATE_EPOCH": build["environment"]["source_date_epoch"],
                   "FORCE_SOURCE_DATE": "1", "TZ": "UTC"}
    task_env = {**os.environ, **environment}
    for stem in STEMS:
        if (ROOT / f"{stem}.synctex.gz").exists():
            raise RuntimeError(f"sidecar already exists before instrumentation: {stem}")
        expected = {key: artifacts[stem][key] for key in ("bytes", "sha256")}
        if identity(ROOT / f"{stem}.pdf") != expected:
            raise RuntimeError(f"PDF differs from fixed-point receipt: {stem}")
    rows = []
    for stem in STEMS:
        command = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                   "-file-line-error", "-synctex=1", f"{stem}.tex"]
        before = snapshot(stem)
        started_at, started_ns = utc(), time.time_ns()
        run = subprocess.run(command, cwd=ROOT, env=task_env,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        completed_ns, completed_at = time.time_ns(), utc()
        if run.returncode:
            raise RuntimeError(f"SyncTeX instrumentation failed for {stem}; inspect its local TeX log")
        after = snapshot(stem)
        if before != after:
            raise RuntimeError(f"SyncTeX instrumentation changed fixed-point artifacts: {stem}")
        sidecar = ROOT / f"{stem}.synctex.gz"
        if not sidecar.is_file() or sidecar.stat().st_size == 0:
            raise RuntimeError(f"SyncTeX sidecar was not generated: {stem}")
        rows.append({"stem": stem, "command": command, "exit_code": 0,
                     "synctex_regenerated": True, "sidecar_absent_before": True,
                     "started_at_utc": started_at, "completed_at_utc": completed_at,
                     "started_ns": started_ns, "completed_ns": completed_ns,
                     "synctex_mtime_ns": sidecar.stat().st_mtime_ns,
                     "pdf_before": before[f"{stem}.pdf"],
                     "pdf_after": after[f"{stem}.pdf"], "synctex": identity(sidecar),
                     "fixed_point_artifacts_before": before,
                     "fixed_point_artifacts_after": after})
        print(f"PASS: {stem} fresh SyncTeX; fixed-point bytes unchanged", flush=True)
    receipt = {"schema": "unofficial-ai-integrated-stacks-synctex-instrumentation/v1",
               "status": "PASS", "created_utc": utc(), "source": build["source"],
               "build_receipt": {"path": BUILD.relative_to(ROOT).as_posix(), **identity(BUILD)},
               "environment": environment, "artifacts": rows,
               "scope": "Source-page instrumentation only. Canonical PDF and fixed-point auxiliary bytes are unchanged; visual inspection is a separate step."}
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
