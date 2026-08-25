#!/usr/bin/env python3
"""Build selected Stacks chapters sequentially to a global PDF fixed point."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_STEMS = (
    "sets",
    "categories",
    "topology",
    "sheaves",
    "sites",
    "algebra",
    "brauer",
    "derived",
    "homology",
    "more-algebra",
    "smoothing",
    "schemes",
    "properties",
    "morphisms",
    "more-morphisms",
    "crystalline",
    "spaces-cohomology",
    "stacks-limits",
    "injectives",
    "gaga",
    "moduli",
)

DEFAULT_COMPOSITION_RECEIPT = Path("validation/composition-current.json")
STEM_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
SHA1_PATTERN = re.compile(r"^[0-9a-f]{40}$")
SHA256_PATTERN = re.compile(r"^[0-9A-Fa-f]{64}$")

GENERATED_SUFFIXES = (
    ".aux",
    ".bbl",
    ".blg",
    ".log",
    ".out",
    ".pdf",
    ".toc",
    ".synctex.gz",
)

FIXED_POINT_SUFFIXES = (
    ".aux",
    ".bbl",
    ".idx",
    ".ind",
    ".lof",
    ".lot",
    ".out",
    ".toc",
    ".pdf",
)

def run(command: list[str], source: Path, env: dict[str, str]) -> str:
    completed = subprocess.run(
        command,
        cwd=source,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode:
        tail = "\n".join(completed.stdout.splitlines()[-80:])
        raise RuntimeError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n{tail}"
        )
    return completed.stdout


def git(source: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(source), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip())
    return completed.stdout.strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def build_state_vector(source: Path, stems: tuple[str, ...]) -> tuple[str, ...]:
    state: list[str] = []
    for stem in stems:
        for suffix in FIXED_POINT_SUFFIXES:
            path = source / f"{stem}{suffix}"
            state.append(sha256(path) if path.is_file() else "ABSENT")
    return tuple(state)


def version_line(executable: str, env: dict[str, str], source: Path) -> str:
    version_flag = "-v" if executable == "pdfinfo" else "--version"
    output = run([executable, version_flag], source, env)
    return output.splitlines()[0].strip()


def resolved_git_path(source: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = source / path
    return path.resolve()


def worktree_kind(source: Path) -> str:
    top_level = Path(git(source, "rev-parse", "--show-toplevel")).resolve()
    if top_level != source:
        raise RuntimeError(
            f"--source must be a Git worktree root: {source} != {top_level}"
        )
    git_dir = resolved_git_path(source, git(source, "rev-parse", "--absolute-git-dir"))
    common_dir = resolved_git_path(source, git(source, "rev-parse", "--git-common-dir"))
    return "primary" if git_dir == common_dir else "linked"


def require_clean_build_tree(source: Path) -> None:
    tracked = subprocess.run(
        ["git", "-C", str(source), "status", "--porcelain=v1", "--untracked-files=no"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if tracked.returncode != 0:
        raise RuntimeError(
            "could not verify tracked build inputs: " + tracked.stderr.strip()
        )
    if tracked.stdout.strip():
        raise RuntimeError("tracked build tree is not clean at HEAD")

    untracked = subprocess.run(
        [
            "git",
            "-C",
            str(source),
            "ls-files",
            "--others",
            "--exclude-standard",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if untracked.returncode != 0:
        raise RuntimeError(
            "could not inspect untracked build inputs: " + untracked.stderr.strip()
        )
    if untracked.stdout.strip():
        names = ", ".join(untracked.stdout.splitlines()[:8])
        raise RuntimeError(f"build worktree contains untracked files: {names}")


def require_ancestor(source: Path, commit: str, label: str) -> None:
    if not SHA1_PATTERN.fullmatch(commit):
        raise RuntimeError(f"invalid {label} commit in composition receipt: {commit!r}")
    completed = subprocess.run(
        ["git", "-C", str(source), "merge-base", "--is-ancestor", commit, "HEAD"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or "commit is not an ancestor of HEAD"
        raise RuntimeError(f"missing {label} ancestry {commit}: {detail}")


def require_clean_path(source: Path, relative: str) -> None:
    completed = subprocess.run(
        ["git", "-C", str(source), "diff", "--quiet", "HEAD", "--", relative],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode == 1:
        raise RuntimeError(f"affected source has uncommitted changes: {relative}")
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"could not verify affected source cleanliness: {detail}")


def git_blob_sha256(source: Path, blob: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(source), "cat-file", "blob", blob],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"could not read composed Git blob {blob}: {detail}")
    return hashlib.sha256(completed.stdout).hexdigest().upper()


def validate_stems(raw_stems: object, label: str) -> tuple[str, ...]:
    if not isinstance(raw_stems, list) or not raw_stems:
        raise RuntimeError(f"{label} must be a nonempty list")
    if not all(isinstance(stem, str) and STEM_PATTERN.fullmatch(stem) for stem in raw_stems):
        raise RuntimeError(f"{label} contains an invalid chapter stem")
    stems = tuple(raw_stems)
    if len(set(stems)) != len(stems):
        raise RuntimeError(f"{label} contains duplicate chapter stems")
    return stems


def load_composition_receipt(
    source: Path, requested_path: Path
) -> tuple[dict[str, object], tuple[str, ...], tuple[str, ...]]:
    receipt_path = requested_path
    if not receipt_path.is_absolute():
        receipt_path = source / receipt_path
    receipt_path = receipt_path.resolve()
    try:
        logical_path = receipt_path.relative_to(source).as_posix()
    except ValueError as exc:
        raise RuntimeError("composition receipt must be inside the source worktree") from exc
    if not receipt_path.is_file():
        raise RuntimeError(f"composition receipt is missing: {logical_path}")
    require_clean_path(source, logical_path)
    receipt_blob = git(source, "rev-parse", f"HEAD:{logical_path}")
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"invalid composition receipt {logical_path}: {exc}") from exc
    if not isinstance(receipt, dict):
        raise RuntimeError("composition receipt must contain a JSON object")
    if (
        receipt.get("schema") != "unofficial-ai-integrated-stacks-composition/v1"
        or receipt.get("status") != "PASS"
    ):
        raise RuntimeError("composition receipt schema or pass state is invalid")

    registry = receipt.get("registry")
    composition = receipt.get("composition")
    if not isinstance(registry, dict) or not isinstance(composition, dict):
        raise RuntimeError("composition receipt lacks registry or composition state")
    cutoff = registry.get("cutoff_commit")
    unified_merge = composition.get("unified_merge_commit")
    if not isinstance(cutoff, str) or not isinstance(unified_merge, str):
        raise RuntimeError("composition receipt lacks cutoff or unified merge commit")
    if not SHA1_PATTERN.fullmatch(cutoff):
        raise RuntimeError(f"invalid registry cutoff commit: {cutoff!r}")
    require_ancestor(source, cutoff, "registry cutoff")
    require_ancestor(source, unified_merge, "unified merge")

    overlays_relative = registry.get("overlays_path")
    overlays_sha = registry.get("overlays_sha256")
    overlays_bytes = registry.get("overlays_bytes")
    if (
        not isinstance(overlays_relative, str)
        or not isinstance(overlays_sha, str)
        or not SHA256_PATTERN.fullmatch(overlays_sha)
        or not isinstance(overlays_bytes, int)
        or overlays_bytes < 1
    ):
        raise RuntimeError("composition receipt has invalid registry-file binding")
    overlays_path = (source / overlays_relative).resolve()
    try:
        overlays_path.relative_to(source)
    except ValueError as exc:
        raise RuntimeError("registry overlay path escapes the source worktree") from exc
    if not overlays_path.is_file():
        raise RuntimeError("imported overlay registry is missing")
    require_clean_path(source, overlays_relative)
    overlays_blob = git(source, "rev-parse", f"HEAD:{overlays_relative}")
    cutoff_overlays_blob = git(source, "rev-parse", f"{cutoff}:registry/overlays.json")
    if cutoff_overlays_blob != overlays_blob:
        raise RuntimeError("imported overlay registry differs from the cutoff commit")
    try:
        observed_overlays_bytes = int(git(source, "cat-file", "-s", overlays_blob))
    except ValueError as exc:
        raise RuntimeError("could not read imported overlay registry size") from exc
    if (
        observed_overlays_bytes != overlays_bytes
        or git_blob_sha256(source, overlays_blob) != overlays_sha.upper()
    ):
        raise RuntimeError("imported overlay registry identity mismatch")
    try:
        overlays = json.loads(overlays_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"invalid imported overlay registry: {exc}") from exc
    entries = overlays.get("registered_entries") if isinstance(overlays, dict) else None
    if not isinstance(entries, list):
        raise RuntimeError("imported overlay registry lacks registered_entries")
    stable_ids: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise RuntimeError("imported overlay registry contains an invalid entry")
        raw_ids = entry.get("stable_ids")
        ids = raw_ids if isinstance(raw_ids, list) else raw_ids.split() if isinstance(raw_ids, str) else None
        if ids is None or not all(isinstance(item, str) for item in ids):
            raise RuntimeError("imported overlay registry contains invalid stable IDs")
        stable_ids.extend(ids)
    if (
        len(entries) != registry.get("registered_overlays")
        or len(stable_ids) != registry.get("registered_stable_ids")
        or len(set(stable_ids)) != len(stable_ids)
    ):
        raise RuntimeError("imported overlay registry counts or stable-ID uniqueness mismatch")
    if not entries or entries[-1].get("id") != registry.get("last_admitted_overlay"):
        raise RuntimeError("imported overlay registry cutoff entry mismatch")

    required_stems = validate_stems(
        receipt.get("required_build_stems"), "required_build_stems"
    )
    missing_profile = [stem for stem in DEFAULT_STEMS if stem not in required_stems]
    if missing_profile:
        raise RuntimeError(
            "composition receipt weakens the full build profile; missing: "
            + ", ".join(missing_profile)
        )

    affected_sources = composition.get("affected_sources")
    if not isinstance(affected_sources, dict) or not affected_sources:
        raise RuntimeError("composition receipt has no affected source inventory")
    affected_stems: list[str] = []
    for relative, evidence in affected_sources.items():
        if not isinstance(relative, str) or not isinstance(evidence, dict):
            raise RuntimeError("invalid affected-source entry in composition receipt")
        relative_path = Path(relative)
        if (
            relative_path.is_absolute()
            or len(relative_path.parts) != 1
            or relative_path.suffix != ".tex"
            or not STEM_PATTERN.fullmatch(relative_path.stem)
        ):
            raise RuntimeError(f"affected source is not a root chapter file: {relative!r}")
        expected_sha = evidence.get("projection_sha256")
        expected_blob = evidence.get("projection_git_blob")
        if (
            not isinstance(expected_sha, str)
            or not SHA256_PATTERN.fullmatch(expected_sha)
            or not isinstance(expected_blob, str)
            or not SHA1_PATTERN.fullmatch(expected_blob)
        ):
            raise RuntimeError(f"invalid projection identity for {relative}")
        path = source / relative_path
        if not path.is_file():
            raise RuntimeError(f"composed source is missing: {relative}")
        require_clean_path(source, relative)
        observed_blob = git(source, "rev-parse", f"HEAD:{relative}")
        if (
            observed_blob != expected_blob
            or git_blob_sha256(source, observed_blob) != expected_sha.upper()
        ):
            raise RuntimeError(f"composed source identity mismatch: {relative}")
        if evidence.get("committed_matches_projection") is not True:
            raise RuntimeError(f"composition receipt does not close {relative}")
        affected_stems.append(relative_path.stem)
    if len(set(affected_stems)) != len(affected_stems):
        raise RuntimeError("affected source inventory contains duplicate chapter stems")
    if any(stem not in required_stems for stem in affected_stems):
        raise RuntimeError("required_build_stems omits an affected source stem")

    binding: dict[str, object] = {
        "receipt": logical_path,
        # Bind canonical committed bytes rather than platform-dependent checkout
        # newlines. The clean-path check above proves the parsed worktree copy is
        # the same Git content.
        "receipt_sha256": git_blob_sha256(source, receipt_blob),
        "registry_cutoff_commit": cutoff,
        "registry_overlays_path": overlays_relative,
        "registry_overlays_git_blob": overlays_blob,
        "registry_overlays_sha256": overlays_sha.upper(),
        "registered_overlays": len(entries),
        "registered_stable_ids": len(stable_ids),
        "unified_merge_commit": unified_merge,
        "last_admitted_overlay": registry.get("last_admitted_overlay"),
        "required_build_stems": list(required_stems),
        "affected_source_stems": affected_stems,
    }
    return binding, required_stems, tuple(affected_stems)


def scan_tex_diagnostics(log_path: Path, blg_path: Path) -> dict[str, int]:
    if not log_path.is_file():
        raise RuntimeError(f"final TeX log is missing: {log_path.name}")
    text = log_path.read_text(encoding="utf-8", errors="replace")
    fatal_patterns = (
        r"(?m)^! (?:Emergency stop\.|Undefined control sequence\.|LaTeX Error:|"
        r"Package [^\r\n]+ Error:|TeX capacity exceeded)",
        r"(?m)^!  ==> Fatal error occurred",
        r"(?m)^Emergency stop\.",
        r"Fatal error occurred",
    )
    reference_patterns = (
        r"LaTeX Warning:[^\r\n]*(?:Hyper\s+)?Reference\b[^\r\n]*\bundefined\b",
        r"LaTeX Warning:\s*There were undefined references\.",
    )
    citation_patterns = (
        r"(?:LaTeX|Package [^\r\n]+) Warning:[^\r\n]*Citation\b[^\r\n]*\bundefined\b",
        r"LaTeX Warning:\s*There were undefined citations\.",
    )
    multiply_defined_patterns = (
        r"LaTeX Warning:[^\r\n]*Label[^\r\n]*multiply defined",
        r"LaTeX Warning:\s*There were multiply-defined labels\.",
    )
    rerun_patterns = (
        r"Rerun to get cross-references right",
        r"Label\(s\) may have changed",
        r"Package rerunfilecheck Warning:[^\r\n]*has changed",
        r"Rerun to get (?:outlines|bookmarks) right",
    )
    destination_patterns = (
        r"pdfTeX warning \(dest\):",
        r"pdfTeX warning \(ext4\): destination with the same identifier",
    )
    diagnostics = {
        "fatal_markers": sum(
            len(re.findall(pattern, text, re.IGNORECASE))
            for pattern in fatal_patterns
        ),
        "missing_glyph_markers": text.count("Missing character:"),
        "undefined_reference_markers": sum(
            len(re.findall(pattern, text, re.IGNORECASE))
            for pattern in reference_patterns
        ),
        "undefined_citation_markers": sum(
            len(re.findall(pattern, text, re.IGNORECASE))
            for pattern in citation_patterns
        ),
        "multiply_defined_markers": sum(
            len(re.findall(pattern, text, re.IGNORECASE))
            for pattern in multiply_defined_patterns
        ),
        "rerun_required_markers": sum(
            len(re.findall(pattern, text, re.IGNORECASE))
            for pattern in rerun_patterns
        ),
        "destination_warning_markers": sum(
            len(re.findall(pattern, text, re.IGNORECASE))
            for pattern in destination_patterns
        ),
    }
    if blg_path.is_file():
        blg = blg_path.read_text(encoding="utf-8", errors="replace")
        diagnostics["undefined_citation_markers"] += len(
            re.findall(
                r"Warning--I didn't find a database entry for",
                blg,
                re.IGNORECASE,
            )
        )
    return diagnostics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--composition-receipt",
        type=Path,
        default=DEFAULT_COMPOSITION_RECEIPT,
        help="source-relative composition receipt (default: %(default)s)",
    )
    parser.add_argument(
        "--allow-primary-worktree",
        action="store_true",
        help="allow generated-file mutation in the repository's primary worktree",
    )
    parser.add_argument("--source-date-epoch", default="1785270512")
    parser.add_argument("--max-sweeps", type=int, default=6)
    parser.add_argument(
        "stems",
        nargs="*",
        help="explicit stems; omitted means required_build_stems from the composition receipt",
    )
    args = parser.parse_args()

    source = args.source.resolve()
    kind = worktree_kind(source)
    if kind == "primary" and not args.allow_primary_worktree:
        raise RuntimeError(
            "refusing to mutate generated files in the primary worktree; "
            "use a linked disposable worktree or pass --allow-primary-worktree explicitly"
        )
    require_clean_build_tree(source)
    composition_binding, required_stems, affected_stems = load_composition_receipt(
        source, args.composition_receipt
    )
    output = args.output
    if not output.is_absolute():
        output = source / output
    output = output.resolve()
    if args.stems:
        stems = validate_stems(args.stems, "explicit stems")
        selection_mode = "explicit"
    else:
        stems = required_stems
        selection_mode = "composition_receipt"
    missing_affected = [stem for stem in affected_stems if stem not in stems]
    if missing_affected:
        raise RuntimeError(
            "build stem selection omits affected source stems: "
            + ", ".join(missing_affected)
        )
    full_profile = stems == required_stems
    if args.max_sweeps < 2:
        parser.error("--max-sweeps must be at least 2")

    for executable in ("pdflatex", "bibtex", "pdfinfo"):
        if shutil.which(executable) is None:
            raise RuntimeError(f"required executable is unavailable: {executable}")
    for stem in stems:
        if not (source / f"{stem}.tex").is_file():
            raise RuntimeError(f"missing chapter source: {stem}.tex")

    env = os.environ.copy()
    env["SOURCE_DATE_EPOCH"] = args.source_date_epoch
    env["FORCE_SOURCE_DATE"] = "1"
    env["TZ"] = "UTC"

    for stem in stems:
        for suffix in GENERATED_SUFFIXES:
            artifact = source / f"{stem}{suffix}"
            if artifact.is_file():
                artifact.unlink()

    latex = [
        "pdflatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
    ]
    for stem in stems:
        print(f"prime {stem}", flush=True)
        run([*latex, f"{stem}.tex"], source, env)
    for stem in stems:
        print(f"bibtex {stem}", flush=True)
        run(["bibtex", stem], source, env)

    previous: tuple[str, ...] | None = None
    fixed_sweep: int | None = None
    for sweep in range(1, args.max_sweeps + 1):
        print(f"global sweep {sweep}", flush=True)
        for stem in stems:
            run([*latex, f"{stem}.tex"], source, env)
        current = build_state_vector(source, stems)
        if current == previous:
            fixed_sweep = sweep
            break
        previous = current
    if fixed_sweep is None:
        raise RuntimeError(
            f"generated build state did not reach a fixed point in "
            f"{args.max_sweeps} sweeps"
        )

    artifacts: list[dict[str, object]] = []
    diagnostic_totals = {
        "fatal_markers": 0,
        "missing_glyph_markers": 0,
        "undefined_reference_markers": 0,
        "undefined_citation_markers": 0,
        "multiply_defined_markers": 0,
        "rerun_required_markers": 0,
        "destination_warning_markers": 0,
    }
    pages_pattern = re.compile(r"^Pages:\s+(\d+)\s*$", re.MULTILINE)
    for stem in stems:
        pdf = source / f"{stem}.pdf"
        info = run(["pdfinfo", str(pdf)], source, env)
        match = pages_pattern.search(info)
        if not match or int(match.group(1)) < 1:
            raise RuntimeError(f"pdfinfo did not report a positive page count: {pdf}")
        diagnostics = scan_tex_diagnostics(
            source / f"{stem}.log", source / f"{stem}.blg"
        )
        for key, value in diagnostics.items():
            diagnostic_totals[key] += value
        artifacts.append(
            {
                "stem": stem,
                "pages": int(match.group(1)),
                "bytes": pdf.stat().st_size,
                "sha256": sha256(pdf),
                "diagnostics": diagnostics,
            }
        )
    failed_diagnostics = {
        key: value for key, value in diagnostic_totals.items() if value
    }
    if failed_diagnostics:
        detail = ", ".join(
            f"{key}={value}" for key, value in failed_diagnostics.items()
        )
        raise RuntimeError(f"final TeX diagnostics are not clean: {detail}")

    builder_path = "tools/build_fixed_point.py"
    builder_blob = git(source, "rev-parse", f"HEAD:{builder_path}")
    receipt = {
        "schema": "unofficial-ai-integrated-stacks-fixed-point-build/v1",
        "status": "PASS" if full_profile else "PASS_PARTIAL",
        "created_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
            "+00:00", "Z"
        ),
        "source": {
            "commit": git(source, "rev-parse", "HEAD"),
            "tree": git(source, "rev-parse", "HEAD^{tree}"),
        },
        "builder": {
            "path": builder_path,
            "git_blob": builder_blob,
            "sha256": git_blob_sha256(source, builder_blob),
        },
        "composition": composition_binding,
        "environment": {
            "operating_system": platform.platform(),
            "python": platform.python_version(),
            "pdftex": version_line("pdflatex", env, source),
            "bibtex": version_line("bibtex", env, source),
            "pdfinfo": version_line("pdfinfo", env, source),
            "source_date_epoch": args.source_date_epoch,
        },
        "build": {
            "strategy": "sequential-prime-bibtex-global-state-sweeps",
            "fixed_point_suffixes": list(FIXED_POINT_SUFFIXES),
            "stem_selection": selection_mode,
            "stems": list(stems),
            "chapter_count": len(stems),
            "global_fixed_point_sweep": fixed_sweep,
            "pdfinfo_readable": len(artifacts),
            "diagnostics": diagnostic_totals,
            "worktree_kind": kind,
            "primary_worktree_override": args.allow_primary_worktree,
        },
        "artifacts": artifacts,
        "pdfs_committed": False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(
        f"{receipt['status']}: {len(stems)} PDFs reached a fixed point "
        f"on sweep {fixed_sweep}"
    )
    print(f"receipt: {output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
