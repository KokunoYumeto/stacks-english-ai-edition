from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent
EXPECTED_UNIT_COUNT = 12
MANIFEST = ROOT / "candidate.manifest.json"
SINGLED = {
    "stable_unit_manifest": ROOT / "stable-units.json",
    "source_map": ROOT / "source-map.jsonl",
    "decision_ledger": ROOT / "decisions.jsonl",
    "rejection_ledger": ROOT / "rejections.jsonl",
    "formula_diagram_inventory": ROOT / "formula-diagram-inventory.json",
}
REQUIRED_RECEIPTS = (
    ROOT / "builds" / "build-receipt.json",
    ROOT / "builds" / "validation.json",
    ROOT / "builds" / "visual-qa.json",
)


class BuildManifestError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BuildManifestError(message)


def repo_root() -> Path:
    for directory in (ROOT, *ROOT.parents):
        if (
            (directory / "schemas" / "candidate-manifest.schema.json").is_file()
            and (directory / "registry" / "leases.json").is_file()
            and (directory / "upstream" / "stacks.lock.json").is_file()
        ):
            return directory.resolve()
    raise BuildManifestError("cannot resolve repository root")


REPO = repo_root()


def display(path: Path) -> str:
    resolved = path.resolve()
    for base in (ROOT, REPO):
        try:
            return resolved.relative_to(base.resolve()).as_posix()
        except ValueError:
            pass
    return str(path)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise BuildManifestError(f"cannot parse {display(path)}: {exc}") from exc
    require(isinstance(value, dict), f"{display(path)} must contain a JSON object")
    return value


def latest_jsonl_time(path: Path, key: str = "timestamp_utc") -> datetime:
    times: list[datetime] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (FileNotFoundError, OSError, UnicodeError) as exc:
        raise BuildManifestError(f"cannot read {display(path)}: {exc}") from exc
    for line_number, line in enumerate(lines, start=1):
        require(bool(line), f"{display(path)}:{line_number} is blank")
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise BuildManifestError(f"cannot parse {display(path)}:{line_number}: {exc}") from exc
        require(isinstance(row, dict), f"{display(path)}:{line_number} must contain a JSON object")
        times.append(parse_time(row.get(key), f"{display(path)}:{line_number}.{key}"))
    require(times, f"{display(path)} contains no timestamped rows")
    return max(times)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def evidence(path: Path) -> dict[str, str]:
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise BuildManifestError(f"manifest evidence is outside the candidate: {path}") from exc
    require(resolved != MANIFEST.resolve(), "candidate manifest may not hash itself")
    require(resolved.is_file(), f"manifest evidence is missing: {relative.as_posix()}")
    return {"path": relative.as_posix(), "sha256": sha256(resolved)}


def all_candidate_files() -> list[Path]:
    files: list[Path] = []
    stack = [ROOT]
    while stack:
        directory = stack.pop()
        with os.scandir(directory) as entries:
            ordered = sorted(entries, key=lambda entry: entry.name)
        for entry in ordered:
            if entry.is_dir(follow_symlinks=False):
                if entry.name in {".work", ".git", "__pycache__"}:
                    continue
                stack.append(Path(entry.path))
            elif entry.is_file(follow_symlinks=False):
                path = Path(entry.path)
                if path.resolve() != MANIFEST.resolve():
                    files.append(path)
    return sorted(files, key=lambda path: path.relative_to(ROOT).as_posix())


def run_read_only_verifier() -> None:
    verifier = ROOT / "verify.py"
    require(verifier.is_file(), "verify.py is missing")
    completed = subprocess.run(
        [sys.executable, str(verifier)],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode:
        detail = (completed.stderr or completed.stdout).strip()
        raise BuildManifestError(f"verify.py did not pass; manifest refused: {detail}")


def validate_receipts() -> dict[Path, dict[str, Any]]:
    build_receipts = sorted((ROOT / "builds").glob("*receipt*.json")) if (ROOT / "builds").is_dir() else []
    require(build_receipts, "at least one build receipt is required before manifest construction")
    missing = [path.relative_to(ROOT).as_posix() for path in REQUIRED_RECEIPTS if not path.is_file()]
    require(not missing, f"required build/QA receipts are missing: {missing}")
    receipts = {path: load_json(path) for path in REQUIRED_RECEIPTS}
    for path, receipt in receipts.items():
        require(receipt.get("passed") is True, f"required receipt has not passed: {path.relative_to(ROOT).as_posix()}")
        if "status" in receipt:
            require(receipt.get("status") == "PASS", f"required receipt status disagrees with passed=true: {path.relative_to(ROOT).as_posix()}")
    return receipts


def parse_time(value: Any, locus: str) -> datetime:
    require(isinstance(value, str) and bool(value), f"{locus} is missing a timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise BuildManifestError(f"invalid timestamp at {locus}: {value}") from exc
    require(parsed.tzinfo is not None, f"timestamp at {locus} has no timezone")
    return parsed.astimezone(timezone.utc)


def receipt_time(receipt: dict[str, Any], path: Path) -> datetime | None:
    for key in ("recorded_at_utc", "completed_at_utc", "generated_at_utc", "reviewed_at_utc", "created_utc"):
        if key in receipt:
            return parse_time(receipt[key], f"{path.relative_to(ROOT).as_posix()}.{key}")
    return None


def iso_z(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def review_states(receipts: dict[Path, dict[str, Any]]) -> tuple[str, str, datetime]:
    times = [moment for path, receipt in receipts.items() if (moment := receipt_time(receipt, path)) is not None]
    require(times, "build/QA receipts contain no deterministic timestamp")
    generated = max(times)
    replay_path = ROOT / "replay" / "independent-review.json"
    if not replay_path.exists():
        return "partial", "not_performed", generated
    replay = load_json(replay_path)
    replay_time = receipt_time(replay, replay_path)
    if replay_time is not None:
        generated = max(generated, replay_time)
    explicit_review = replay.get("review_state")
    if explicit_review is not None:
        require(explicit_review == "performed", "independent-review receipt must record review_state=performed")
        review = explicit_review
    else:
        review = "performed"
    passed = replay.get("passed")
    require(isinstance(passed, bool), "independent-review receipt must contain a Boolean passed field")
    return review, "passed" if passed else "failed", generated


def rights_text(config: dict[str, Any]) -> str:
    rights = config.get("rights_state")
    if isinstance(rights, str):
        require(bool(rights.strip()), "config.rights_state is empty")
        return rights
    require(isinstance(rights, dict), "config.rights_state must be a string or object")
    if isinstance(rights.get("manifest_declaration"), str) and rights["manifest_declaration"].strip():
        return rights["manifest_declaration"]
    boundary = rights.get("rights_boundary", rights)
    require(isinstance(boundary, dict), "config.rights_state has no rights boundary")
    require(
        boundary.get("verbatim_source_prose_in_candidate") is False,
        "rights state does not affirm that verbatim source prose is absent",
    )
    return (
        "Historical-source evidence is limited to locators, hashes, and independent paraphrase. "
        "No verbatim source prose is included, no source-work license is asserted or granted by "
        "this candidate, and no upstream content is relicensed. The proposed Stacks payload is "
        "independently written, subject to GFDL compatibility at composition, and is not reviewed, "
        "approved, affiliated with, or endorsed by the Stacks Project."
    )


def string_array(config: dict[str, Any], key: str, *, nonempty: bool, default: list[str] | None = None) -> list[str]:
    value = config.get(key)
    if value is None and default is not None:
        value = default
    require(isinstance(value, list) and all(isinstance(item, str) for item in value), f"config.{key} must be a string array")
    if nonempty:
        require(bool(value), f"config.{key} may not be empty")
    return list(value)


def source_authorities(authority_paths: Iterable[Path]) -> list[dict[str, str]]:
    rows = [evidence(path) for path in authority_paths]
    require(rows, "authority directory contains no source-authority evidence")
    return rows


def main() -> int:
    try:
        run_read_only_verifier()
        receipts = validate_receipts()
        config = load_json(ROOT / "candidate.config.json")
        stable = load_json(ROOT / "stable-units.json")
        units = stable.get("units")
        require(
            isinstance(units, list)
            and stable.get("unit_count") == len(units) == EXPECTED_UNIT_COUNT,
            "stable-unit closure is not exactly 12",
        )
        review_state, replay_state, generated = review_states(receipts)
        generated = max(
            generated,
            parse_time(config.get("state_updated_at_utc"), "candidate.config.json.state_updated_at_utc"),
            latest_jsonl_time(ROOT / "decisions.jsonl"),
            latest_jsonl_time(ROOT / "rejections.jsonl"),
        )

        authority_paths = sorted(
            (path for path in (ROOT / "authority").rglob("*") if path.is_file()),
            key=lambda path: path.relative_to(ROOT).as_posix(),
        )
        singled_paths = set(SINGLED.values())
        all_files = all_candidate_files()
        build_paths = [path for path in all_files if path not in singled_paths and path not in authority_paths]
        require(any(path.name == "build-receipt.json" for path in build_paths), "build receipt is absent from manifest build evidence")

        lock = load_json(REPO / "upstream" / "stacks.lock.json")
        relative_schema = Path(os.path.relpath(REPO / "schemas" / "candidate-manifest.schema.json", ROOT)).as_posix()
        manifest = {
            "$schema": relative_schema,
            "schema": "mathematics-commons-stacks-candidate-manifest/v1",
            "candidate_id": config["candidate_id"],
            "lease_id": config["lease_id"],
            "namespace": config["namespace"],
            "writer_task": config["writer_task"],
            "upstream": {
                "lock": "upstream/stacks.lock.json",
                "commit": lock["commit"],
                "tree": lock["tree"],
            },
            "source_authorities": source_authorities(authority_paths),
            "source_closure": {
                "enumerated": True,
                "expected_units": EXPECTED_UNIT_COUNT,
                "manifested_units": EXPECTED_UNIT_COUNT,
                "complete": True,
            },
            **{key: evidence(path) for key, path in SINGLED.items()},
            "builds": [evidence(path) for path in build_paths],
            "rights_state": rights_text(config),
            "review_state": review_state,
            "independent_replay": replay_state,
            "unresolved_defects": string_array(
                config,
                "unresolved_defects",
                nonempty=False,
                default=(
                    []
                    if replay_state == "passed"
                    else ["Independent replay has not passed; this manifest records candidate closure, not overlay admission."]
                ),
            ),
            "stop_conditions": string_array(
                config,
                "stop_conditions",
                nonempty=True,
                default=[
                    "Do not mutate the literal Stacks Project mirror or the pinned composition-base preimage.",
                    "Do not copy thesis prose into the candidate; retain only locators, hashes, structural facts, and independently written mathematics.",
                    "Do not claim an official Stacks tag, upstream review, affiliation, approval, or endorsement for the proposed lemma.",
                    "Do not admit or compose this candidate except in a separate hash-bound transition after deterministic build, visual QA, and independent replay gates.",
                ],
            ),
            "generated_at_utc": iso_z(generated),
        }
        payload = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        MANIFEST.write_text(payload, encoding="utf-8", newline="")

        checked = subprocess.run(
            [sys.executable, str(ROOT / "check-manifest.py")],
            cwd=ROOT,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if checked.returncode:
            detail = (checked.stderr or checked.stdout).strip()
            raise BuildManifestError(f"manifest was written but failed check-manifest.py: {detail}")
        print(
            json.dumps(
                {
                    "passed": True,
                    "manifest_sha256": sha256(MANIFEST),
                    "review_state": review_state,
                    "independent_replay": replay_state,
                    "references": len(authority_paths) + len(SINGLED) + len(build_paths),
                },
                sort_keys=True,
            )
        )
        return 0
    except (BuildManifestError, OSError, UnicodeError, KeyError, TypeError, ValueError) as exc:
        print(f"MANIFEST BUILD FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
