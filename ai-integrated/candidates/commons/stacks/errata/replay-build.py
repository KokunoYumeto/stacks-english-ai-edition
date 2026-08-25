from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BUILDS = ROOT / "builds"
STEMS = ("smoothing", "crystalline", "spaces-cohomology")
SOURCE_DATE_EPOCH = "1785270512"  # 2026-07-28T20:28:32Z, frozen commit time
AUTHORITY_COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
AUTHORITY_TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
AUTHORITY_HASHES = {
    "smoothing.tex": "FD28CF874BB7DAD3C5C5FF03314D1C83701613A8A98730A99B9CA7A4BCFE6068",
    "crystalline.tex": "466C0634A5E8E3899B157A42A4B4BB5F4357199F96708CAF5854F5A92BE58054",
    "spaces-cohomology.tex": "63F19991B7B2BCE90B5FB30FCDBB8A3B06CBBFFEC42FA7C413776C29AE4B69C5",
    "tags/tags": "098F77CCE75F8359F1EACB22B7AA0088099B09E5B3FFCAD2DE513CBD1A8A9F1C",
}
PAYLOAD_HASHES = {
    "smoothing.tex": "9CF7DCF31E447C585E81515C9A8059B37A566998DCAFA77A16AB7CB1D27A0A46",
    "crystalline.tex": "EDA38E502E0C6B3743C0FCD769203EAA6186440002A9AD2C97DC6F642B03DEC7",
    "spaces-cohomology.tex": "81438F655CEAB1A2E07CFEEC645A9A7C2447DB983D6BCEFAED6575859B75D196",
    "tags/tags": "C47887DB37D78437C0E7C72BEC0F7840DCA2D36535D1241E1CBCAEF1412DC788",
}
GENERATED_EXTENSIONS = (
    ".aux",
    ".bbl",
    ".blg",
    ".brf",
    ".idx",
    ".ilg",
    ".ind",
    ".log",
    ".out",
    ".pdf",
    ".toc",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def file_evidence(path: Path, *, display_path: str | None = None) -> dict:
    return {
        "path": display_path or path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sanitize(text: str) -> str:
    text = re.sub(r"(?i)F\s*l\s*o\s*r\s*i\s*s", "<USER>", text)
    text = re.sub(r"C:(?:\\|/)Users(?:\\|/)<USER>", "<USER_ROOT>", text)
    text = re.sub(r"C:(?:\\|/)Users(?:\\|/)", "<USERS_ROOT>/", text)
    return text


def write_public_text(path: Path, raw: bytes) -> dict:
    text = raw.decode("utf-8", errors="replace")
    path.write_text(sanitize(text), encoding="utf-8", newline="")
    return file_evidence(path, display_path=path.relative_to(ROOT).as_posix())


def copy_private(path: Path, raw: bytes) -> dict:
    path.write_bytes(raw)
    return file_evidence(path, display_path=path.name)


def command_version(argv: list[str]) -> str:
    completed = subprocess.run(
        argv,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return sanitize(completed.stdout.splitlines()[0])


def run(argv: list[str], cwd: Path, env: dict[str, str]) -> tuple[dict, bytes]:
    completed = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    record = {
        "argv": [sanitize(str(argument)) for argument in argv],
        "exit_code": completed.returncode,
        "stdout_bytes": len(completed.stdout),
        "stdout_sha256_raw": hashlib.sha256(completed.stdout).hexdigest().upper(),
    }
    if completed.returncode != 0:
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(argv)}")
    return record, completed.stdout


def verify_hashes(root: Path, expected: dict[str, str], label: str) -> dict:
    observed = {}
    for relative, expected_hash in expected.items():
        path = root / relative
        actual = sha256(path)
        if actual != expected_hash:
            raise AssertionError(f"{label} hash mismatch for {relative}: {actual} != {expected_hash}")
        observed[relative] = file_evidence(path, display_path=relative)
    return observed


def clear_stem_outputs(root: Path) -> None:
    for stem in STEMS:
        for extension in GENERATED_EXTENSIONS:
            path = root / f"{stem}{extension}"
            if path.exists():
                path.unlink()


def build_phase(
    phase: str,
    work_root: Path,
    private_root: Path,
    env: dict[str, str],
) -> tuple[dict, dict]:
    phase_record: dict[str, object] = {"stems": {}}
    private_record: dict[str, object] = {"stems": {}}
    for stem in STEMS:
        source = work_root / f"{stem}.tex"
        stem_record: dict[str, object] = {
            "source": file_evidence(source, display_path=f"{stem}.tex"),
            "commands": [],
        }
        for pass_number in (1,):
            command, _ = run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", f"{stem}.tex"],
                work_root,
                env,
            )
            command["role"] = f"pdflatex_pass_{pass_number}"
            stem_record["commands"].append(command)
        command, bibtex_stdout = run(["bibtex", stem], work_root, env)
        command["role"] = "bibtex"
        stem_record["commands"].append(command)
        for pass_number in (2, 3):
            command, stdout = run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", f"{stem}.tex"],
                work_root,
                env,
            )
            command["role"] = f"pdflatex_pass_{pass_number}"
            stem_record["commands"].append(command)
            if pass_number == 3:
                pass3_stdout = stdout

        raw_log = (work_root / f"{stem}.log").read_bytes()
        raw_pdf = (work_root / f"{stem}.pdf").read_bytes()
        if phase == "candidate":
            public_log = BUILDS / f"{stem}.log"
            public_pdf = BUILDS / f"{stem}.pdf"
            public_bibtex = BUILDS / f"{stem}.bibtex.txt"
            public_pass3 = BUILDS / f"{stem}.pass3.txt"
            private_prefix = f"{stem}.candidate"
        else:
            public_log = BUILDS / f"{stem}.authority.log"
            public_pdf = BUILDS / f"{stem}.authority.pdf"
            public_bibtex = BUILDS / f"{stem}.authority.bibtex.txt"
            public_pass3 = BUILDS / f"{stem}.authority.pass3.txt"
            private_prefix = f"{stem}.authority"

        public_pdf.write_bytes(raw_pdf)
        stem_record["outputs"] = {
            "pdf": file_evidence(public_pdf, display_path=public_pdf.relative_to(ROOT).as_posix()),
            "log": write_public_text(public_log, raw_log),
            "bibtex_stdout": write_public_text(public_bibtex, bibtex_stdout),
            "pass3_stdout": write_public_text(public_pass3, pass3_stdout),
        }
        private_record["stems"][stem] = {
            "pdf": copy_private(private_root / f"{private_prefix}.pdf", raw_pdf),
            "log": copy_private(private_root / f"{private_prefix}.log", raw_log),
            "bibtex_stdout": copy_private(private_root / f"{private_prefix}.bibtex.txt", bibtex_stdout),
            "pass3_stdout": copy_private(private_root / f"{private_prefix}.pass3.txt", pass3_stdout),
        }
        phase_record["stems"][stem] = stem_record
    return phase_record, private_record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream-root", type=Path, required=True)
    parser.add_argument("--work-root", type=Path, required=True)
    parser.add_argument("--private-evidence-root", type=Path, required=True)
    args = parser.parse_args()

    upstream_root = args.upstream_root.resolve()
    work_root = args.work_root.resolve()
    private_root = args.private_evidence_root.resolve()
    if not upstream_root.is_dir():
        raise FileNotFoundError(f"upstream root missing: {upstream_root}")
    if work_root.exists():
        raise FileExistsError(f"work root must not exist: {work_root}")
    if ROOT in work_root.parents or work_root == ROOT:
        raise ValueError("work root must be outside the candidate")
    private_root.mkdir(parents=True, exist_ok=True)
    BUILDS.mkdir(parents=True, exist_ok=True)

    execution: dict[str, object] = {
        "schema": "mathematics-commons-stacks-errata-build-execution/v1",
        "candidate_id": "stacks-errata-a04446e-r1",
        "authority_commit": AUTHORITY_COMMIT,
        "authority_tree": AUTHORITY_TREE,
        "started_at_utc": utc_now(),
        "source_date_epoch": SOURCE_DATE_EPOCH,
        "work_root": "new empty temporary directory outside source and candidate; exact local path retained only in private receipt",
        "tools": {
            "python": sanitize(sys.version.splitlines()[0]),
            "pdflatex": command_version(["pdflatex", "--version"]),
            "bibtex": command_version(["bibtex", "--version"]),
        },
        "passed": False,
    }
    private_execution = {
        "schema": "mathematics-commons-stacks-private-build-execution/v1",
        "public_candidate_id": "stacks-errata-a04446e-r1",
        "upstream_root": str(upstream_root),
        "work_root": str(work_root),
        "private_root": str(private_root),
    }

    shutil.copytree(upstream_root, work_root)
    execution["authority_inputs"] = verify_hashes(work_root, AUTHORITY_HASHES, "authority copy")
    for relative in PAYLOAD_HASHES:
        source = ROOT / "payload" / relative
        destination = work_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    execution["candidate_inputs"] = verify_hashes(work_root, PAYLOAD_HASHES, "candidate overlay")

    env = os.environ.copy()
    env["SOURCE_DATE_EPOCH"] = SOURCE_DATE_EPOCH
    env["FORCE_SOURCE_DATE"] = "1"
    env["TZ"] = "UTC"
    allocator_code = (
        "import json,sys; sys.path.insert(0,'scripts'); "
        "from functions import get_tags,get_new_tags; "
        "print(json.dumps(get_new_tags('./',get_tags('./'))))"
    )
    allocator_command, allocator_stdout = run([sys.executable, "-c", allocator_code], work_root, env)
    allocator_text = allocator_stdout.decode("utf-8", errors="replace").strip()
    if allocator_text != "[]":
        raise AssertionError(f"allocator did not close: {allocator_text!r}")
    execution["allocator"] = {**allocator_command, "result": []}

    candidate_phase, private_candidate_phase = build_phase("candidate", work_root, private_root, env)
    execution["candidate_phase"] = candidate_phase
    private_execution["candidate_phase"] = private_candidate_phase
    clear_stem_outputs(work_root)
    for relative in AUTHORITY_HASHES:
        if relative == "tags/tags":
            source = ROOT / "authority" / "tags" / "tags"
        else:
            source = ROOT / "authority" / "source" / relative
        destination = work_root / relative
        shutil.copy2(source, destination)
    execution["restored_authority_inputs"] = verify_hashes(work_root, AUTHORITY_HASHES, "restored authority")
    authority_phase, private_authority_phase = build_phase("authority", work_root, private_root, env)
    execution["authority_phase"] = authority_phase
    private_execution["authority_phase"] = private_authority_phase

    execution["completed_at_utc"] = utc_now()
    execution["passed"] = True
    public_execution_path = BUILDS / "build-execution.json"
    public_execution_path.write_text(
        json.dumps(execution, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    private_execution["public_execution"] = file_evidence(
        public_execution_path,
        display_path="builds/build-execution.json",
    )
    private_execution["completed_at_utc"] = execution["completed_at_utc"]
    (private_root / "private-build-execution.json").write_text(
        json.dumps(private_execution, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    shutil.rmtree(work_root)
    print(json.dumps({"passed": True, "receipt": str(public_execution_path), "work_root_removed": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
