from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CANDIDATE = Path(__file__).resolve().parent
SOURCE = CANDIDATE / ".work" / "unified-main"
COMPOSITION = CANDIDATE / "composition.jsonl"
BUILD_DIR = CANDIDATE / "builds"
PAYLOAD = CANDIDATE / "payload" / "fragments" / "derived-functorial-triangles.tex"

# These are exactly the chapters that define labels referenced by derived.tex,
# plus derived.tex itself.  Missing unrelated external-document auxiliaries are
# held constant in the baseline and candidate builds.
STEMS = (
    "sets",
    "categories",
    "algebra",
    "homology",
    "more-algebra",
    "injectives",
    "examples",
    "derived",
)

VECTOR_SUFFIXES = (".pdf", ".aux", ".toc", ".out", ".bbl")
GENERATED_SUFFIXES = VECTOR_SUFFIXES + (".blg", ".log", ".synctex.gz")
MAX_SWEEPS = 6

DIAGNOSTIC_PATTERNS = (
    re.compile(r"^! .*"),
    re.compile(r"LaTeX Warning:.*(?:undefined|multiply defined)", re.IGNORECASE),
    re.compile(r"Package .* Warning:.*(?:undefined|multiply defined)", re.IGNORECASE),
    re.compile(r"(?:Citation|Reference) .* undefined", re.IGNORECASE),
    re.compile(r"There were undefined (?:references|citations)", re.IGNORECASE),
    re.compile(r"destination with the same identifier", re.IGNORECASE),
    re.compile(r"Rerun to get cross-references right", re.IGNORECASE),
    re.compile(r"rerunfilecheck Warning:.*has changed", re.IGNORECASE),
    re.compile(r"Missing character:", re.IGNORECASE),
    re.compile(r"Undefined control sequence", re.IGNORECASE),
    re.compile(r"Emergency stop", re.IGNORECASE),
    re.compile(r"Fatal error", re.IGNORECASE),
)


class BuildError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BuildError(message)


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest().upper()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def run(
    command: list[str],
    *,
    env: dict[str, str],
    binary: bool = False,
    announce: bool = False,
) -> bytes | str:
    if announce:
        print("RUN " + " ".join(command), flush=True)
    completed = subprocess.run(
        command,
        cwd=SOURCE,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=not binary,
        encoding=None if binary else "utf-8",
        errors=None if binary else "replace",
        check=False,
    )
    if completed.returncode:
        if binary:
            detail = completed.stdout.decode("utf-8", errors="replace")
        else:
            detail = completed.stdout
        raise BuildError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n"
            + "\n".join(detail.splitlines()[-100:])
        )
    return completed.stdout


def git_bytes(*args: str, env: dict[str, str]) -> bytes:
    result = run(["git", "-C", str(SOURCE), *args], env=env, binary=True)
    assert isinstance(result, bytes)
    return result


def git_text(*args: str, env: dict[str, str]) -> str:
    result = run(["git", "-C", str(SOURCE), *args], env=env)
    assert isinstance(result, str)
    return result.strip()


def load_composition() -> dict[str, Any]:
    rows = [line for line in COMPOSITION.read_text(encoding="utf-8").splitlines() if line.strip()]
    require(len(rows) == 1, "composition.jsonl must contain exactly one nonblank row")
    value = json.loads(rows[0])
    require(isinstance(value, dict), "composition row is not a JSON object")
    return value


def raw_preimage(operation: dict[str, Any], env: dict[str, str]) -> bytes:
    target = operation["target"]
    commit = target["commit"]
    path = target["path"]
    require(git_text("rev-parse", f"{commit}^{{tree}}", env=env) == target["tree"], "base tree mismatch")
    require(git_text("rev-parse", f"{commit}:{path}", env=env) == target["blob"], "base blob mismatch")
    raw = git_bytes("show", f"{commit}:{path}", env=env)
    require(len(raw) == target["bytes"], "base byte count mismatch")
    require(sha_bytes(raw) == target["preimage_sha256"], "base SHA-256 mismatch")
    return raw


def materialize(operation: dict[str, Any], base: bytes) -> bytes:
    insertion = operation["insertion"]
    payload_meta = operation["payload"]
    payload = PAYLOAD.read_bytes()
    require(len(payload) == payload_meta["bytes"], "payload byte count mismatch")
    require(sha_bytes(payload) == payload_meta["sha256"], "payload SHA-256 mismatch")
    require(b"\r" not in payload and not payload.startswith(b"\xef\xbb\xbf"), "payload is not BOM-free LF")

    start = insertion["context_start_byte"]
    offset = insertion["byte_offset"]
    end = insertion["context_end_byte_exclusive"]
    require(0 <= start <= offset <= end <= len(base), "composition offsets are invalid")
    require(sha_bytes(base[start:end]) == insertion["context_sha256"], "context SHA-256 mismatch")
    require(sha_bytes(base[start:offset]) == insertion["before_context_sha256"], "before-context SHA-256 mismatch")
    require(sha_bytes(base[offset:end]) == insertion["after_context_sha256"], "after-context SHA-256 mismatch")
    result = base[:offset] + payload + base[offset:]
    target = operation["target"]
    require(len(result) == target["postimage_bytes"], "postimage byte count mismatch")
    require(sha_bytes(result) == target["postimage_sha256"], "postimage SHA-256 mismatch")
    label = f"\\label{{{payload_meta['proposed_label']}}}".encode("ascii")
    require(result.count(label) == 1, "proposed label does not occur exactly once")
    require(result[:offset] == base[:offset] and result[offset + len(payload) :] == base[offset:], "existing target bytes changed")
    return result


def remove_generated() -> None:
    for stem in STEMS:
        for suffix in GENERATED_SUFFIXES:
            path = SOURCE / f"{stem}{suffix}"
            if path.is_file():
                path.unlink()


def latex_command(stem: str) -> list[str]:
    return [
        "pdflatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        f"{stem}.tex",
    ]


def artifact_vector() -> tuple[str, ...]:
    vector: list[str] = []
    for stem in STEMS:
        for suffix in VECTOR_SUFFIXES:
            path = SOURCE / f"{stem}{suffix}"
            vector.append(sha_file(path) if path.is_file() else "ABSENT")
    return tuple(vector)


def build_to_fixed_point(env: dict[str, str], phase: str, *, prime: bool) -> tuple[int, tuple[str, ...]]:
    if prime:
        for stem in STEMS:
            print(f"{phase}: prime {stem}", flush=True)
            run(latex_command(stem), env=env)
        for stem in STEMS:
            print(f"{phase}: bibtex {stem}", flush=True)
            run(["bibtex", stem], env=env)

    previous: tuple[str, ...] | None = None
    for sweep in range(1, MAX_SWEEPS + 1):
        print(f"{phase}: global sweep {sweep}/{MAX_SWEEPS}", flush=True)
        for stem in STEMS:
            run(latex_command(stem), env=env)
        current = artifact_vector()
        if current == previous:
            return sweep, current
        previous = current
    raise BuildError(f"{phase} artifact vector did not reach a fixed point in {MAX_SWEEPS} sweeps")


def diagnostics(log_text: str) -> list[str]:
    found: list[str] = []
    for raw_line in log_text.splitlines():
        line = " ".join(raw_line.strip().split())
        if line and any(pattern.search(line) for pattern in DIAGNOSTIC_PATTERNS):
            # Page and input-line numbers are volatile when a legitimate
            # insertion changes pagination.  Preserve the warning class and
            # referenced identity, but remove only that location suffix so the
            # baseline/candidate multiset comparison remains semantic.
            line = re.sub(r"\s+on page \d+ undefined.*$", " undefined", line)
            line = re.sub(r"\s+on input line \d+\.?$", "", line)
            line = re.sub(r"\bpage \d+\b", "page <N>", line)
            line = re.sub(r"\bline \d+\b", "line <N>", line)
            found.append(line)
    return found


def sanitized_log(raw: str) -> str:
    result = raw
    # TeX wraps long font paths at its log line width and can split a username
    # across a newline.  Remove the complete wrapped private path before the
    # exact-root substitutions below.
    result = re.sub(
        r"C:(?:/+|\\+)Users(?:/+|\\+)[^\s}\]]+(?:\r?\n[^\s}\]]+)*",
        "<USERPROFILE>",
        result,
        flags=re.IGNORECASE,
    )
    home = str(Path.home())
    source = str(SOURCE)
    candidate = str(CANDIDATE)
    replacements = (
        (source, "<SOURCE_ROOT>"),
        (source.replace("\\", "/"), "<SOURCE_ROOT>"),
        (candidate, "<CANDIDATE_ROOT>"),
        (candidate.replace("\\", "/"), "<CANDIDATE_ROOT>"),
        (home, "<USERPROFILE>"),
        (home.replace("\\", "/"), "<USERPROFILE>"),
    )
    for needle, replacement in replacements:
        result = re.sub(re.escape(needle), replacement, result, flags=re.IGNORECASE)
    return result


def resanitize_public_logs() -> None:
    log_paths = (BUILD_DIR / "baseline-derived.log", BUILD_DIR / "derived.log")
    for path in log_paths:
        require(path.is_file(), f"public log is missing: {path.name}")
        value = path.read_text(encoding="utf-8", errors="strict")
        path.write_text(sanitized_log(value), encoding="utf-8", newline="\n")
    receipt_path = BUILD_DIR / "build-receipt.json"
    require(receipt_path.is_file(), "build receipt is missing")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["results"]["candidate_derived_log"] = evidence(
        BUILD_DIR / "derived.log", "builds/derived.log"
    )
    receipt["results"]["baseline_derived_log"] = evidence(
        BUILD_DIR / "baseline-derived.log", "builds/baseline-derived.log"
    )
    receipt_path.write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n"
    )


def version_line(command: list[str], env: dict[str, str]) -> str:
    value = run(command, env=env)
    assert isinstance(value, str)
    return value.splitlines()[0].strip()


def pdf_pages(path: Path, env: dict[str, str]) -> int:
    value = run(["pdfinfo", str(path)], env=env)
    assert isinstance(value, str)
    match = re.search(r"^Pages:\s+(\d+)\s*$", value, re.MULTILINE)
    require(match is not None and int(match.group(1)) > 0, "pdfinfo did not report a positive page count")
    return int(match.group(1))


def evidence(path: Path, logical: str) -> dict[str, Any]:
    return {"path": logical, "bytes": path.stat().st_size, "sha256": sha_file(path)}


def main() -> int:
    if "--resanitize-public-logs" in sys.argv[1:]:
        require(sys.argv[1:] == ["--resanitize-public-logs"], "unexpected command-line arguments")
        resanitize_public_logs()
        print(
            "PASS: public logs sanitized and build-receipt log hashes refreshed",
            flush=True,
        )
        return 0
    for executable in ("git", "pdflatex", "bibtex", "pdfinfo"):
        require(shutil.which(executable) is not None, f"required executable unavailable: {executable}")
    require(SOURCE.is_dir(), "bounded source worktree is missing")
    for stem in STEMS:
        require((SOURCE / f"{stem}.tex").is_file(), f"source chapter is missing: {stem}.tex")

    operation = load_composition()
    env = os.environ.copy()
    commit = operation["target"]["commit"]
    source_date_epoch = git_text("show", "-s", "--format=%ct", commit, env=env)
    require(source_date_epoch.isdigit(), "cannot derive SOURCE_DATE_EPOCH")
    env["SOURCE_DATE_EPOCH"] = source_date_epoch
    env["FORCE_SOURCE_DATE"] = "1"
    env["TZ"] = "UTC"

    base = raw_preimage(operation, env)
    candidate = materialize(operation, base)
    derived_source = SOURCE / "derived.tex"
    if "--restore-preimage-only" in sys.argv[1:]:
        require(sys.argv[1:] == ["--restore-preimage-only"], "unexpected command-line arguments")
        derived_source.write_bytes(base)
        print(
            f"PASS: restored raw composition preimage: {len(base)} bytes/{sha_bytes(base)}",
            flush=True,
        )
        return 0
    derived_source.write_bytes(base)
    remove_generated()

    baseline_sweep, baseline_vector = build_to_fixed_point(env, "baseline", prime=True)
    baseline_log_raw = (SOURCE / "derived.log").read_text(encoding="utf-8", errors="replace")
    baseline_diagnostics = diagnostics(baseline_log_raw)
    baseline_pdf_sha = sha_file(SOURCE / "derived.pdf")
    baseline_log_copy = BUILD_DIR / "baseline-derived.log"

    derived_source.write_bytes(candidate)
    candidate_sweep, candidate_vector = build_to_fixed_point(env, "candidate", prime=False)
    candidate_log_raw = (SOURCE / "derived.log").read_text(encoding="utf-8", errors="replace")
    candidate_diagnostics = diagnostics(candidate_log_raw)
    new_diagnostics = list((Counter(candidate_diagnostics) - Counter(baseline_diagnostics)).elements())
    require(not new_diagnostics, "candidate introduced diagnostics: " + " | ".join(new_diagnostics))
    require(not any("Rerun to get cross-references right" in item for item in candidate_diagnostics), "candidate log still requests a rerun")

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    baseline_log_copy.write_text(sanitized_log(baseline_log_raw), encoding="utf-8", newline="\n")
    final_log = BUILD_DIR / "derived.log"
    final_log.write_text(sanitized_log(candidate_log_raw), encoding="utf-8", newline="\n")
    final_pdf = BUILD_DIR / "derived.pdf"
    shutil.copyfile(SOURCE / "derived.pdf", final_pdf)

    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    validation = {
        "schema": "mathematics-commons-stacks-verdier-build-validation/v1",
        "status": "PASS",
        "passed": True,
        "generated_at_utc": generated_at,
        "scope": "bounded baseline-versus-candidate build of derived.tex and its seven direct external-label providers",
        "stems": list(STEMS),
        "composition": {
            "operation_id": operation["operation_id"],
            "preimage_bytes": len(base),
            "preimage_sha256": sha_bytes(base),
            "payload_bytes": PAYLOAD.stat().st_size,
            "payload_sha256": sha_file(PAYLOAD),
            "postimage_bytes": len(candidate),
            "postimage_sha256": sha_bytes(candidate),
            "prefix_and_suffix_unchanged": True,
            "payload_inserted_once": True,
        },
        "fixed_point": {
            "vector_suffixes": list(VECTOR_SUFFIXES),
            "baseline_confirming_sweep": baseline_sweep,
            "candidate_confirming_sweep": candidate_sweep,
            "baseline_vector_sha256": sha_bytes("\n".join(baseline_vector).encode("ascii")),
            "candidate_vector_sha256": sha_bytes("\n".join(candidate_vector).encode("ascii")),
        },
        "diagnostics": {
            "baseline_count": len(baseline_diagnostics),
            "candidate_count": len(candidate_diagnostics),
            "new_candidate_diagnostics": new_diagnostics,
            "new_candidate_diagnostic_count": len(new_diagnostics),
        },
    }
    validation_path = BUILD_DIR / "validation.json"
    validation_path.write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8", newline="\n")

    receipt = {
        "schema": "mathematics-commons-stacks-verdier-build-receipt/v1",
        "status": "PASS",
        "passed": True,
        "created_utc": generated_at,
        "source": {
            "repository": operation["target"]["repository"],
            "commit": commit,
            "tree": operation["target"]["tree"],
            "target": operation["target"]["path"],
            "source_date_epoch": source_date_epoch,
        },
        "environment": {
            "python": sys.version.split()[0],
            "pdftex": version_line(["pdflatex", "--version"], env),
            "bibtex": version_line(["bibtex", "--version"], env),
            "pdfinfo": version_line(["pdfinfo", "-v"], env),
            "timezone": "UTC",
        },
        "strategy": {
            "name": "bounded-direct-label-provider-fixed-point-with-baseline",
            "stems": list(STEMS),
            "stems_count": len(STEMS),
            "fixed_point_vector_suffixes": list(VECTOR_SUFFIXES),
            "maximum_sweeps": MAX_SWEEPS,
            "unrelated_external_auxiliaries": "held absent and identical between baseline and candidate",
        },
        "results": {
            "baseline_derived_pdf_sha256": baseline_pdf_sha,
            "candidate_derived_pages": pdf_pages(final_pdf, env),
            "candidate_derived_pdf": evidence(final_pdf, "builds/derived.pdf"),
            "candidate_derived_log": evidence(final_log, "builds/derived.log"),
            "baseline_derived_log": evidence(baseline_log_copy, "builds/baseline-derived.log"),
            "validation": evidence(validation_path, "builds/validation.json"),
        },
    }
    receipt_path = BUILD_DIR / "build-receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
    # Leave the bounded checkout at the declared raw Git preimage.  The
    # materialized postimage is fully bound by composition.jsonl and the build
    # receipts, while validators must be able to replay it independently.
    derived_source.write_bytes(base)
    print(
        "PASS: candidate fixed point; "
        f"derived.pdf={final_pdf.stat().st_size} bytes/{sha_file(final_pdf)}; "
        f"new diagnostics={len(new_diagnostics)}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (BuildError, OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"BUILD FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
