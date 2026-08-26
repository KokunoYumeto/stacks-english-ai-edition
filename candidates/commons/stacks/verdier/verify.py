from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


CANDIDATE = Path(__file__).resolve().parent
EXPECTED_UNIT_COUNT = 12
SHA256_RE = re.compile(r"[0-9A-F]{64}")
COMMIT_RE = re.compile(r"[0-9a-f]{40}")
TASK_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
LABEL_RE = re.compile(r"\\label\{([^{}]+)\}")
STACKS_LABEL_RE = re.compile(
    r"(?:section|subsection|definition|lemma|proposition|theorem|corollary|"
    r"remark|remarks|example|examples|construction|situation|equation|diagram|"
    r"item|proof)-[a-z0-9][a-z0-9-]*"
)
OFFICIAL_TAG_CLAIM_RE = re.compile(
    r"(?:official\s+Stacks(?:\s+Project)?\s+(?:tag|result|addition|status|lemma)\s+"
    r"(?:is|has\s+been)\s+(?:assigned|accepted|admitted|approved|established|recognized)|"
    r"Stacks(?:\s+Project)?\s+(?:official\s+)?tag\s*(?:=|:)\s*[0-9A-Z]|"
    r"Stacks(?:\s+Project)?\s+(?:official\s+)?tag\s+is\s+(?:Tag\s+)?[0-9A-Z]{4}\b|"
    r"officially\s+(?:tagged|admitted|accepted)\s+(?:in|by)\s+the\s+Stacks\s+Project)",
    re.IGNORECASE,
)


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def find_repo_root() -> Path:
    for directory in (CANDIDATE, *CANDIDATE.parents):
        if (
            (directory / "schemas" / "candidate-manifest.schema.json").is_file()
            and (directory / "registry" / "leases.json").is_file()
            and (directory / "upstream" / "stacks.lock.json").is_file()
        ):
            return directory.resolve()
    raise VerificationError("cannot resolve repository root from the candidate directory")


REPO = find_repo_root()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise VerificationError(f"required JSON file is missing: {display(path)}") from exc
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise VerificationError(f"cannot parse JSON {display(path)}: {exc}") from exc
    require(isinstance(value, dict), f"JSON root must be an object: {display(path)}")
    return value


def load_jsonl(path: Path, *, id_fields: tuple[str, ...]) -> list[dict[str, Any]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise VerificationError(f"required JSONL file is missing: {display(path)}") from exc
    except (OSError, UnicodeError) as exc:
        raise VerificationError(f"cannot read JSONL {display(path)}: {exc}") from exc
    rows: list[dict[str, Any]] = []
    identities: list[str] = []
    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise VerificationError(f"invalid JSONL at {display(path)}:{line_number}: {exc}") from exc
        require(isinstance(row, dict), f"JSONL row is not an object at {display(path)}:{line_number}")
        identity = next((row.get(field) for field in id_fields if isinstance(row.get(field), str)), None)
        require(
            isinstance(identity, str) and bool(identity.strip()),
            f"JSONL row lacks one of {id_fields!r} at {display(path)}:{line_number}",
        )
        identities.append(identity)
        rows.append(row)
    duplicates = sorted({item for item in identities if identities.count(item) > 1})
    require(not duplicates, f"duplicate JSONL IDs in {display(path)}: {duplicates}")
    return rows


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest().upper()


def display(path: Path) -> str:
    resolved = path.resolve()
    for base in (CANDIDATE, REPO):
        try:
            return resolved.relative_to(base.resolve()).as_posix()
        except ValueError:
            pass
    return str(path)


def safe_path(base: Path, logical: str) -> Path:
    require(isinstance(logical, str) and bool(logical), "empty evidence path")
    require("\\" not in logical, f"evidence path must use forward slashes: {logical}")
    relative = Path(logical)
    require(not relative.is_absolute(), f"absolute evidence path is forbidden: {logical}")
    resolved = (base / relative).resolve()
    try:
        resolved.relative_to(base.resolve())
    except ValueError as exc:
        raise VerificationError(f"evidence path escapes its root: {logical}") from exc
    return resolved


def candidate_or_repo_path(logical: str) -> Path:
    if logical.startswith(("registry/", "schemas/", "upstream/", "releases/", "translations/")):
        return safe_path(REPO, logical)
    return safe_path(CANDIDATE, logical)


def validate_timestamp(value: Any, locus: str) -> None:
    require(isinstance(value, str) and bool(value), f"missing timestamp at {locus}")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise VerificationError(f"invalid ISO-8601 timestamp at {locus}: {value}") from exc
    require(parsed.tzinfo is not None, f"timestamp has no timezone at {locus}: {value}")


def get_nested(mapping: dict[str, Any], *paths: tuple[str, ...]) -> Any:
    for path in paths:
        value: Any = mapping
        for component in path:
            if not isinstance(value, dict) or component not in value:
                break
            value = value[component]
        else:
            return value
    return None


def unique_strings(value: Any, locus: str, *, exact_count: int | None = None) -> list[str]:
    require(isinstance(value, list), f"{locus} must be an array")
    require(all(isinstance(item, str) and bool(item) for item in value), f"{locus} contains a non-string or empty ID")
    result = list(value)
    require(len(result) == len(set(result)), f"{locus} contains duplicate IDs")
    if exact_count is not None:
        require(len(result) == exact_count, f"{locus} must contain exactly {exact_count} IDs, found {len(result)}")
    return result


def validate_hash_row(row: dict[str, Any], locus: str) -> None:
    if "sha256" not in row or "path" not in row:
        return
    logical = row["path"]
    expected = row["sha256"]
    require(isinstance(expected, str) and bool(SHA256_RE.fullmatch(expected)), f"invalid uppercase SHA-256 at {locus}")
    path = candidate_or_repo_path(logical)
    require(path.is_file(), f"hashed evidence is missing at {locus}: {logical}")
    require(path != CANDIDATE / "candidate.manifest.json", "candidate manifest must not hash itself")
    actual = sha256(path)
    require(actual == expected, f"SHA-256 mismatch at {locus}: {logical}; expected {expected}, found {actual}")
    if "bytes" in row:
        require(row["bytes"] == path.stat().st_size, f"byte-count mismatch at {locus}: {logical}")


def walk_hash_rows(value: Any, locus: str = "$") -> Iterable[tuple[dict[str, Any], str]]:
    if isinstance(value, dict):
        if "path" in value and "sha256" in value:
            yield value, locus
        for key, item in value.items():
            yield from walk_hash_rows(item, f"{locus}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk_hash_rows(item, f"{locus}[{index}]")


def validate_lease(config: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    pointer = load_json(CANDIDATE / "LEASE.json")
    registry = load_json(REPO / pointer.get("lease_registry", "registry/leases.json"))
    events = registry.get("events")
    require(isinstance(events, list), "lease registry events must be an array")
    lease_id = pointer.get("lease_id")
    matching = [row for row in events if isinstance(row, dict) and row.get("lease_id") == lease_id]
    require(matching, f"lease {lease_id!r} is absent from the registry")
    active = matching[-1]
    require(active.get("state") == "active" and active.get("event") == "issued", f"lease {lease_id} is not active")
    expected_path = CANDIDATE.relative_to(REPO).as_posix()
    identity_fields = ("lease_id", "namespace", "writer_task", "upstream_commit")
    for field in identity_fields:
        require(pointer.get(field) == active.get(field), f"lease pointer/registry mismatch for {field}")
        config_value = config.get(field)
        if field == "upstream_commit" and config_value is None:
            config_value = get_nested(config, ("upstream", "commit")) or config.get("authority_commit")
        require(config_value == active.get(field), f"config/active-lease mismatch for {field}")
    require(pointer.get("writer_task") and TASK_RE.fullmatch(pointer["writer_task"]), "invalid lease writer_task")
    require(active.get("candidate_path") == expected_path, f"active lease path is {active.get('candidate_path')!r}, expected {expected_path!r}")
    require(pointer.get("namespace") == "commons/stacks/verdier", "unexpected Verdier namespace")

    lock = load_json(REPO / "upstream" / "stacks.lock.json")
    commit = get_nested(config, ("upstream", "commit")) or config.get("upstream_commit") or config.get("authority_commit")
    tree = get_nested(config, ("upstream", "tree")) or config.get("upstream_tree") or config.get("authority_tree")
    require(isinstance(commit, str) and COMMIT_RE.fullmatch(commit), "config has no valid pinned upstream commit")
    require(isinstance(tree, str) and COMMIT_RE.fullmatch(tree), "config has no valid pinned upstream tree")
    require(active.get("upstream_commit") == commit == lock.get("commit"), "upstream commit differs across config, lease, and lock")
    require(active.get("upstream_tree") == tree == lock.get("tree"), "upstream tree differs across config, lease, and lock")
    return pointer, active


def validate_config(config: dict[str, Any]) -> list[str]:
    required = ("schema", "candidate_id", "lease_id", "namespace", "writer_task", "expected_unit_ids")
    for field in required:
        require(field in config, f"candidate config is missing {field}")
    require(
        config["schema"] == "mathematics-commons-stacks-verdier-candidate-config/v1",
        f"unexpected candidate config schema: {config.get('schema')!r}",
    )
    require(re.fullmatch(r"[a-z0-9][a-z0-9._-]*", str(config["candidate_id"])) is not None, "invalid candidate_id")
    require(config["namespace"] == "commons/stacks/verdier", "config namespace is not commons/stacks/verdier")
    unit_ids = unique_strings(config["expected_unit_ids"], "config.expected_unit_ids", exact_count=EXPECTED_UNIT_COUNT)
    for unit_id in unit_ids:
        require(
            re.fullmatch(r"verdier:ast239:1\.2\.13(?::[a-z0-9.-]+)*", unit_id) is not None,
            f"stable unit ID is outside the bounded Verdier 1.2.13 namespace: {unit_id}",
        )
    anchors = unique_strings(config.get("expected_anchor_ids"), "config.expected_anchor_ids", exact_count=EXPECTED_UNIT_COUNT)
    require(config.get("proposed_stacks_label") == "lemma-functorial-triangles-decomposable", "unexpected proposed Stacks label")
    closure = config.get("source_closure")
    require(isinstance(closure, dict), "config.source_closure must be an object")
    require(
        closure.get("enumerated") is True
        and closure.get("complete") is True
        and closure.get("expected_units") == closure.get("manifested_units") == EXPECTED_UNIT_COUNT
        and closure.get("mapped_to_proposed_lemma") == 10
        and closure.get("duplicate_dispositions_to_existing_tags") == 2
        and closure.get("unresolved_source_units") == 0,
        "config source closure is not exactly 12 = 10 proposed + 2 duplicate dispositions",
    )
    require(len(anchors) == EXPECTED_UNIT_COUNT, "config anchor closure is not 12")
    return unit_ids


def stable_unit_id(row: dict[str, Any]) -> Any:
    return row.get("id", row.get("unit_id"))


def validate_units(config: dict[str, Any], expected_ids: list[str]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    stable = load_json(CANDIDATE / "stable-units.json")
    require(stable.get("schema") == "mathematics-commons-stacks-verdier-units/v1", "wrong stable-unit schema")
    require(stable.get("candidate_id") == config.get("candidate_id"), "stable-unit candidate_id mismatch")
    units = stable.get("units")
    require(isinstance(units, list), "stable-units.json has no units array")
    ids = [stable_unit_id(row) for row in units if isinstance(row, dict)]
    require(len(ids) == len(units), "stable-units.json contains a non-object row")
    require(stable.get("unit_count") == EXPECTED_UNIT_COUNT == len(units), "stable-unit count is not exactly 12")
    require(ids == expected_ids, "stable-unit IDs/order do not exactly match candidate config")
    require(len(ids) == len(set(ids)), "stable-unit IDs are duplicated")
    anchors = [row.get("anchor_id") for row in units if isinstance(row, dict)]
    require(anchors == config.get("expected_anchor_ids"), "stable-unit anchors do not exactly match config")
    require(len(anchors) == len(set(anchors)), "stable-unit anchors are duplicated")
    for index, unit in enumerate(units):
        require(isinstance(unit, dict), f"stable unit {index} is not an object")
        require(
            unit.get("status")
            in {
                "mapped_not_built",
                "mapped_payload_authored_not_built",
                "mapped_payload_built",
                "mapped_payload_validated",
                "mapped_payload_authored_built_validated",
                "dispositioned_existing_no_payload",
            },
            f"stable unit {ids[index]} has invalid status",
        )
        for field in ("title", "source_locus"):
            if field in unit:
                require(isinstance(unit[field], str) and bool(unit[field].strip()), f"stable unit {ids[index]} has empty {field}")
    return stable, units


def source_ids_from_row(row: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for key in ("source_unit_id", "source_id", "authority_unit_id", "anchor_id"):
        if isinstance(row.get(key), str):
            values.append(row[key])
    for key in ("source_unit_ids", "source_ids", "authority_unit_ids", "source_loci"):
        if isinstance(row.get(key), list):
            values.extend(item for item in row[key] if isinstance(item, str))
    return values


def authority_unit_ids(authority_lock: dict[str, Any]) -> list[str]:
    for key in ("source_units", "units", "authorities"):
        rows = authority_lock.get(key)
        if isinstance(rows, list):
            result = []
            for row in rows:
                if isinstance(row, str):
                    result.append(row)
                elif isinstance(row, dict):
                    value = row.get("id", row.get("source_unit_id", row.get("authority_unit_id")))
                    if isinstance(value, str):
                        result.append(value)
            if result:
                return result
    return []


def validate_source_map(config: dict[str, Any], expected_ids: list[str]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = load_jsonl(CANDIDATE / "source-map.jsonl", id_fields=("id", "map_id", "unit_id"))
    require(rows, "source-map.jsonl is empty")
    mapped = [row.get("unit_id", row.get("candidate_unit_id")) for row in rows]
    require(all(isinstance(value, str) for value in mapped), "a source-map row lacks unit_id")
    require(len(mapped) == len(set(mapped)), "source-map unit IDs are not one-to-one")
    require(mapped == expected_ids, "source-map coverage/order does not exactly match the 12 stable units")
    require(
        all(row.get("schema") == "mathematics-commons-stacks-verdier-map/v1" for row in rows),
        "source-map row schema mismatch",
    )
    require([row.get("sequence") for row in rows] == list(range(1, EXPECTED_UNIT_COUNT + 1)), "source-map sequence is not exactly 1..12")

    authority_lock = load_json(CANDIDATE / "authority" / "authority.lock.json")
    require(authority_lock.get("schema") == "mathematics-commons-stacks-verdier-authority-lock/v1", "wrong authority-lock schema")
    expected_sources = config.get("expected_anchor_ids", config.get("expected_source_unit_ids"))
    if expected_sources is None:
        expected_sources = authority_unit_ids(authority_lock)
    expected_sources = unique_strings(expected_sources, "authority source-unit closure", exact_count=EXPECTED_UNIT_COUNT)
    mapped_sources: list[str] = []
    for row in rows:
        values = source_ids_from_row(row)
        require(values, f"source-map row for {row.get('unit_id')} has no source authority ID")
        require(len(values) == len(set(values)), f"source-map row for {row.get('unit_id')} repeats a source authority ID")
        mapped_sources.extend(values)
    require(len(mapped_sources) == len(set(mapped_sources)), "source authority IDs are mapped more than once")
    require(mapped_sources == expected_sources, "source-map does not give exact ordered closure of all source authority units")
    declared = get_nested(authority_lock, ("scope", "source_unit_count")) or authority_lock.get("unit_count", authority_lock.get("source_unit_count"))
    if declared is not None:
        require(declared == EXPECTED_UNIT_COUNT, f"authority lock declares {declared} source units instead of 12")
    return rows, authority_lock


def numeric_suffix(identifier: str, locus: str) -> tuple[str, int, int]:
    match = re.fullmatch(r"(.+?)([0-9]+)", identifier)
    require(match is not None, f"append-only ID has no numeric suffix at {locus}: {identifier}")
    assert match is not None
    return match.group(1), int(match.group(2)), len(match.group(2))


def validate_append_only(rows: list[dict[str, Any]], *, locus: str, expected_schema: str) -> None:
    require(rows, f"{locus} is empty")
    ids = [row["id"] for row in rows]
    parsed = [numeric_suffix(identifier, locus) for identifier in ids]
    require(len({prefix for prefix, _, _ in parsed}) == 1, f"{locus} IDs do not share one append-only prefix")
    require(len({width for _, _, width in parsed}) == 1, f"{locus} IDs do not use one fixed numeric width")
    numbers = [number for _, number, _ in parsed]
    require(numbers == list(range(numbers[0], numbers[0] + len(numbers))), f"{locus} IDs are not a contiguous append-only sequence")
    seen: set[str] = set()
    for index, row in enumerate(rows, 1):
        require(row.get("schema") == expected_schema, f"wrong schema in {locus} row {index}")
        validate_timestamp(row.get("timestamp_utc", row.get("recorded_at_utc")), f"{locus} row {index}")
        supersedes = row.get("supersedes")
        require(supersedes is None or supersedes in seen, f"{locus} row {row['id']} supersedes a non-earlier ID")
        seen.add(row["id"])


def validate_ledgers() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    decisions = load_jsonl(CANDIDATE / "decisions.jsonl", id_fields=("id",))
    rejections = load_jsonl(CANDIDATE / "rejections.jsonl", id_fields=("id",))
    validate_append_only(
        decisions,
        locus="decisions.jsonl",
        expected_schema="mathematics-commons-stacks-candidate-decision/v1",
    )
    validate_append_only(
        rejections,
        locus="rejections.jsonl",
        expected_schema="mathematics-commons-stacks-candidate-rejection/v1",
    )
    for row in decisions:
        require(isinstance(row.get("choice"), str) and bool(row["choice"].strip()), f"empty decision choice: {row['id']}")
        require(isinstance(row.get("rationale"), str) and bool(row["rationale"].strip()), f"empty decision rationale: {row['id']}")
    for row in rejections:
        require(isinstance(row.get("reason"), str) and bool(row["reason"].strip()), f"empty rejection reason: {row['id']}")
        require(isinstance(row.get("disposition"), str) and bool(row["disposition"].strip()), f"empty rejection disposition: {row['id']}")
    return decisions, rejections


def validate_inventory(expected_ids: list[str]) -> dict[str, Any]:
    inventory = load_json(CANDIDATE / "formula-diagram-inventory.json")
    require(inventory.get("schema") == "mathematics-commons-stacks-verdier-formula-diagram-inventory/v1", "wrong formula/diagram inventory schema")
    classified: list[str] = []
    if isinstance(inventory.get("units"), list):
        for row in inventory["units"]:
            require(isinstance(row, dict), "formula inventory contains a non-object unit")
            unit_id = row.get("unit_id", row.get("id"))
            require(isinstance(unit_id, str), "formula inventory unit lacks an ID")
            require(
                row.get("classification") in {"formula", "diagram", "prose_only", "formula_and_diagram"},
                f"invalid formula/diagram classification for {unit_id}",
            )
            classified.append(unit_id)
    else:
        for key in ("formula_units", "diagram_units", "prose_only_units", "formula_and_diagram_units"):
            values = inventory.get(key, [])
            require(isinstance(values, list), f"inventory.{key} is invalid")
            for item in values:
                if isinstance(item, str):
                    classified.append(item)
                elif isinstance(item, dict) and isinstance(item.get("unit_id"), str):
                    classified.append(item["unit_id"])
                else:
                    raise VerificationError(f"inventory.{key} contains a row without unit_id")
    require(inventory.get("unit_count") == EXPECTED_UNIT_COUNT, "formula/diagram inventory unit_count is not 12")
    require(inventory.get("classified_unit_count", EXPECTED_UNIT_COUNT) == EXPECTED_UNIT_COUNT, "formula/diagram classified count is not 12")
    require(inventory.get("formula_unit_count", 9) == 9 and inventory.get("diagram_unit_count", 3) == 3, "formula/diagram 9+3 split is stale")
    require(len(classified) == len(set(classified)), "formula/diagram inventory classifies a unit more than once")
    require(sorted(classified) == sorted(expected_ids), "formula/diagram inventory does not cover exactly all 12 units")
    require(inventory.get("unmapped_formula_or_diagram_changes", 0) == 0, "formula/diagram inventory has unmapped changes")
    return inventory


def row_field(row: dict[str, Any], names: tuple[str, ...], locus: str) -> Any:
    for name in names:
        if name in row:
            return row[name]
    raise VerificationError(f"composition row {locus} lacks one of {names!r}")


def validate_sha_value(value: Any, locus: str) -> str:
    require(isinstance(value, str) and bool(SHA256_RE.fullmatch(value)), f"invalid uppercase SHA-256 at {locus}")
    return value


def validate_composition(config: dict[str, Any], expected_ids: list[str]) -> list[dict[str, Any]]:
    rows = load_jsonl(CANDIDATE / "composition.jsonl", id_fields=("id", "operation_id", "unit_id"))
    require(len(rows) == 1, f"composition.jsonl must contain exactly one insertion operation, found {len(rows)}")
    row = rows[0]
    require(row.get("schema") == "mathematics-commons-stacks-composition-operation/v1", "wrong composition schema")
    require(row.get("operation") == "insert_bytes" and row.get("mode") == "insertion_only", "composition is not insertion-only")
    configured_operation = config.get("composition_operation")
    require(isinstance(configured_operation, dict), "config does not bind composition_operation")
    for key in ("operation_id", "operation", "mode"):
        require(configured_operation.get(key) == row.get(key), f"config/composition mismatch for {key}")
    target = row.get("target")
    insertion = row.get("insertion")
    payload = row.get("payload")
    source = row.get("source")
    constraints = row.get("constraints")
    for name, value in (("target", target), ("insertion", insertion), ("payload", payload), ("source", source), ("constraints", constraints)):
        require(isinstance(value, dict), f"composition {name} must be an object")
    assert isinstance(target, dict) and isinstance(insertion, dict) and isinstance(payload, dict)
    assert isinstance(source, dict) and isinstance(constraints, dict)

    base = config.get("composition_base")
    require(isinstance(base, dict), "config.composition_base must be an object")
    require(target.get("repository") == base.get("repository"), "composition target repository differs from config")
    require(target.get("commit") == base.get("commit") and target.get("tree") == base.get("tree"), "composition target commit/tree differs from config")
    require(target.get("path") == "derived.tex", "composition target is not derived.tex")
    for key in ("commit", "tree", "blob"):
        require(isinstance(target.get(key), str) and COMMIT_RE.fullmatch(target[key]), f"invalid composition target {key}")
    preimage_hash = validate_sha_value(target.get("preimage_sha256"), "composition target preimage")
    postimage_hash = validate_sha_value(target.get("postimage_sha256"), "composition target postimage")

    payload_logical = payload.get("path")
    require(payload_logical == "payload/fragments/derived-functorial-triangles.tex", "unexpected composition payload path")
    fragment = candidate_or_repo_path(payload_logical)
    fragment_bytes = fragment.read_bytes()
    require(payload.get("bytes") == len(fragment_bytes), "composition payload byte count mismatch")
    require(validate_sha_value(payload.get("sha256"), "composition payload") == sha_bytes(fragment_bytes), "composition payload hash mismatch")
    require(payload.get("encoding") == "UTF-8" and payload.get("line_endings") == "LF", "payload encoding/line-ending declaration mismatch")
    require(b"\r" not in fragment_bytes and not fragment_bytes.startswith(b"\xef\xbb\xbf"), "payload is not BOM-free UTF-8 LF")
    try:
        fragment_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise VerificationError(f"payload is not UTF-8: {exc}") from exc
    require(payload.get("proposed_label") == config.get("proposed_stacks_label"), "composition payload label differs from config")
    configured_payload = config.get("payload_artifact")
    require(isinstance(configured_payload, dict), "config does not bind payload_artifact")
    require(configured_payload.get("path") == payload_logical, "config/composition payload path mismatch")
    require(configured_payload.get("bytes") == payload.get("bytes"), "config/composition payload byte mismatch")
    require(configured_payload.get("sha256") == payload.get("sha256"), "config/composition payload hash mismatch")
    require(configured_payload.get("proposed_label") == payload.get("proposed_label"), "config/composition proposed-label mismatch")

    base_path = CANDIDATE / ".work" / "unified-main" / "derived.tex"
    require(base_path.is_file(), "frozen composition-base derived.tex is missing from .work/unified-main")
    base_bytes = base_path.read_bytes()
    proposed_label_bytes = f"\\label{{{config['proposed_stacks_label']}}}".encode("utf-8")
    require(base_bytes.count(proposed_label_bytes) == 0, "proposed Stacks label already exists in the composition base")
    payload_text = fragment_bytes.decode("utf-8")
    referenced_labels = re.findall(r"\\(?:ref|eqref|pageref|autoref)\{([^{}]+)\}", payload_text)
    require(referenced_labels, "payload proof contains no bound Stacks references")
    for label in referenced_labels:
        require(STACKS_LABEL_RE.fullmatch(label) is not None, f"payload reference has non-Stacks label style: {label}")
        require(base_bytes.count(f"\\label{{{label}}}".encode("utf-8")) == 1, f"payload reference is missing or nonunique in the composition base: {label}")
    require(target.get("bytes") == len(base_bytes), "composition preimage byte count mismatch")
    require(preimage_hash == sha_bytes(base_bytes), "composition preimage hash mismatch")
    offset = insertion.get("byte_offset")
    start = insertion.get("context_start_byte")
    end = insertion.get("context_end_byte_exclusive")
    require(all(isinstance(value, int) for value in (start, offset, end)), "composition context offsets are not integers")
    require(0 <= start <= offset <= end <= len(base_bytes), "composition context offsets are out of range")
    context = base_bytes[start:end]
    before = base_bytes[start:offset]
    after = base_bytes[offset:end]
    require(insertion.get("context_bytes") == len(context), "composition context byte count mismatch")
    require(insertion.get("before_context_bytes") == len(before), "composition before-context byte count mismatch")
    require(insertion.get("after_context_bytes") == len(after), "composition after-context byte count mismatch")
    require(validate_sha_value(insertion.get("context_sha256"), "composition context") == sha_bytes(context), "composition context hash mismatch")
    require(validate_sha_value(insertion.get("before_context_sha256"), "composition before context") == sha_bytes(before), "composition before-context hash mismatch")
    require(validate_sha_value(insertion.get("after_context_sha256"), "composition after context") == sha_bytes(after), "composition after-context hash mismatch")
    after_label = insertion.get("after_complete_proof_of_label")
    before_label = insertion.get("before_noindent_for_label")
    require(after_label == "lemma-projectors-have-images-triangulated", "unexpected preceding Stacks label")
    require(before_label == "lemma-easier-axiom-four", "unexpected following Stacks label")
    require(base_bytes.count(f"\\label{{{after_label}}}".encode()) == insertion.get("required_anchor_occurrences") == 1, "preceding anchor is not unique")
    require(base_bytes.count(f"\\label{{{before_label}}}".encode()) == 1, "following anchor is not unique")
    require(f"\\label{{{after_label}}}".encode() in before and b"\\end{proof}" in before, "insertion is not after the complete preceding proof")
    require(f"\\label{{{before_label}}}".encode() in after and b"\\noindent" in after, "insertion is not before the declared following noindent block")

    postimage = base_bytes[:offset] + fragment_bytes + base_bytes[offset:]
    require(target.get("postimage_bytes") == len(postimage), "composition postimage byte count mismatch")
    require(postimage_hash == sha_bytes(postimage), "composition postimage hash mismatch")
    require(constraints.get("existing_target_bytes_changed") == 0, "composition changes existing target bytes")
    require(constraints.get("delete_bytes") == constraints.get("replace_bytes") == 0, "composition deletes or replaces target bytes")
    require(constraints.get("insert_payload_once") is True, "composition does not require exactly one insertion")
    require(source.get("anchor") == "VDR-A239-CH2-1-2-13", "composition source anchor is outside the bounded proposition")
    require(
        source.get("locus") == "Chapter II, Proposition 1.2.13; printed pages 104-105; physical PDF pages 121-122",
        "composition source locus reverses or obscures printed versus physical PDF pages",
    )
    return rows


def validate_labels_and_claims(config: dict[str, Any], evidence: Iterable[Any]) -> list[str]:
    payload_logical = config.get("payload_fragment", "payload/fragments/derived-functorial-triangles.tex")
    payload_path = candidate_or_repo_path(payload_logical)
    try:
        payload = payload_path.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError, UnicodeError) as exc:
        raise VerificationError(f"cannot read payload fragment {payload_logical}: {exc}") from exc
    labels = LABEL_RE.findall(payload)
    require(labels, "payload fragment defines no Stacks-style labels")
    require(len(labels) == len(set(labels)), "payload fragment defines duplicate labels")
    invalid = [label for label in labels if not STACKS_LABEL_RE.fullmatch(label)]
    require(not invalid, f"payload fragment has non-Stacks label style: {invalid}")
    expected_labels = config.get("expected_labels")
    if expected_labels is not None:
        require(labels == unique_strings(expected_labels, "config.expected_labels"), "payload labels differ from config.expected_labels")
    require("\\tag{" not in payload, "payload contains a manual LaTeX tag; Stacks tags must be generated from labels")

    combined = "\n".join(json.dumps(item, ensure_ascii=False, sort_keys=True) for item in evidence) + "\n" + payload
    require(OFFICIAL_TAG_CLAIM_RE.search(combined) is None, "candidate overclaims an official Stacks tag or status")
    for item in evidence:
        if isinstance(item, dict):
            for key in ("official_tag", "stacks_tag", "official_stacks_tag"):
                require(item.get(key) in (None, "", False), f"candidate field {key} overclaims an official tag")
    stable = next((item for item in evidence if isinstance(item, dict) and isinstance(item.get("units"), list)), None)
    if stable:
        for unit in stable["units"]:
            if not isinstance(unit, dict) or not isinstance(unit.get("target"), dict):
                continue
            target = unit["target"]
            if target.get("kind") == "proposed_new_lemma":
                require("tag" not in target, f"proposed unit {unit.get('id')} claims an official tag")
                require(target.get("label") == config.get("proposed_stacks_label"), f"proposed unit {unit.get('id')} uses another label")
            elif target.get("kind") == "existing_stacks_result":
                require(target.get("tag") in {"05QW", "05QU"}, f"unexpected duplicate tag for {unit.get('id')}")
                require(
                    isinstance(target.get("label"), str) and target["label"].startswith("derived-lemma-"),
                    f"existing-result disposition for {unit.get('id')} lacks a qualified Stacks label",
                )
                require(target.get("disposition") == "duplicate_excluded_from_new_payload", f"existing tag is not excluded from the new payload: {unit.get('id')}")
    return labels


def validate_rights(config: dict[str, Any], authority_lock: dict[str, Any]) -> dict[str, Any]:
    readme_path = CANDIDATE / "README.md"
    try:
        readme = readme_path.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError, UnicodeError) as exc:
        raise VerificationError(f"cannot read rights declarations in README.md: {exc}") from exc
    rights = config.get("rights_state")
    locked = authority_lock.get("rights_boundary")
    require(isinstance(rights, dict) and isinstance(locked, dict), "rights/no-copy boundary must be object-valued in config and authority lock")
    expected = {
        "evidence_mode": "locators_hashes_and_independent_paraphrase_only",
        "verbatim_source_prose_in_candidate": False,
        "source_work_license_assertion": "none_by_candidate",
        "source_relicensed": False,
        "future_payload_requires_independent_wording_and_gfdl_compatibility": True,
    }
    for key, value in expected.items():
        require(rights.get(key) == value, f"config rights boundary mismatch for {key}")
        require(locked.get(key) == value, f"authority-lock rights boundary mismatch for {key}")
    require(locked.get("source_public_domain_claimed") is False, "authority lock makes a public-domain claim")
    require(locked.get("source_provenance_and_release_terms_remain_controlling") is True, "authority lock does not preserve controlling provenance/terms")
    combined = f"{json.dumps(rights, sort_keys=True)}\n{json.dumps(locked, sort_keys=True)}\n{readme}".casefold()
    require(
        ("independently written" in combined or "independent synthesis" in combined),
        "rights evidence does not declare independent writing/synthesis",
    )
    require(
        (
            "no verbatim" in combined
            or "does not copy" in combined
            or "not copied" in combined
            or "no thesis prose is copied" in combined
            or '"verbatim_source_prose_in_candidate": false' in combined
        ),
        "rights evidence does not declare the no-copy boundary",
    )
    require(
        (
            "no endorsement" in combined
            or "not endorsed" in combined
            or "no upstream endorsement" in combined
            or "asserts no official stacks tag, endorsement" in combined
        ),
        "rights evidence does not disclaim upstream endorsement",
    )
    require(OFFICIAL_TAG_CLAIM_RE.search(combined) is None, "rights text overclaims official Stacks status")
    return rights


def validate_external_authority(config: dict[str, Any], authority_lock: dict[str, Any], source_map: list[dict[str, Any]]) -> int:
    workspace = REPO.parents[1]
    source_project = authority_lock.get("source_project")
    require(isinstance(source_project, dict), "authority lock has no source_project object")
    project_relative = source_project.get("workspace_relative_root")
    require(isinstance(project_relative, str) and bool(project_relative), "authority lock has no project-relative root")
    project = safe_path(workspace, project_relative)
    require(project.is_dir(), f"source project is missing: {project_relative}")

    verified = 0
    evidence_by_path: dict[str, dict[str, Any]] = {}
    rows = authority_lock.get("evidence_files")
    require(isinstance(rows, list) and bool(rows), "authority lock evidence_files is empty")
    for index, row in enumerate(rows):
        require(isinstance(row, dict), f"authority evidence row {index} is not an object")
        logical = row.get("project_relative_path")
        require(isinstance(logical, str) and bool(logical), f"authority evidence row {index} lacks project_relative_path")
        path = safe_path(project, logical)
        require(path.is_file(), f"external authority evidence is missing: {logical}")
        expected_hash = validate_sha_value(row.get("sha256"), f"authority evidence {logical}")
        require(sha256(path) == expected_hash, f"external authority evidence hash mismatch: {logical}")
        require(row.get("bytes") == path.stat().st_size, f"external authority evidence byte mismatch: {logical}")
        evidence_by_path[logical] = row
        verified += 1

    authority = authority_lock.get("authority")
    require(isinstance(authority, dict), "authority lock has no authority object")
    authority_hash = validate_sha_value(authority.get("sha256"), "controlling authority PDF")
    require(authority.get("copied_into_candidate") is False, "controlling authority PDF was copied into the candidate")
    require(authority.get("physical_pages") == 270, "controlling authority PDF page count changed")
    for row in source_map:
        require(row.get("authority_sha256") == authority_hash, f"source-map authority hash mismatch for {row.get('unit_id')}")
        logical = row.get("english_source")
        require(logical in evidence_by_path, f"source-map references unbound English evidence: {logical}")
        require(row.get("english_source_sha256") == evidence_by_path[logical]["sha256"], f"source-map English hash mismatch: {logical}")
        lines = row.get("english_lines")
        require(isinstance(lines, dict) and isinstance(lines.get("start"), int) and isinstance(lines.get("end"), int), f"invalid English line span for {row.get('unit_id')}")
        line_count = safe_path(project, logical).read_text(encoding="utf-8").count("\n") + 1
        require(1 <= lines["start"] <= lines["end"] <= line_count, f"English line span is out of bounds for {row.get('unit_id')}")

    upstream = config.get("upstream")
    require(isinstance(upstream, dict) and upstream.get("lock") == "upstream/stacks.lock.json", "config does not bind the upstream lock")
    upstream_path = REPO / "upstream" / "stacks.lock.json"
    require(upstream.get("lock_bytes") == upstream_path.stat().st_size, "upstream lock byte count mismatch")
    require(validate_sha_value(upstream.get("lock_sha256"), "config upstream lock") == sha256(upstream_path), "upstream lock hash mismatch")
    locked_base = authority_lock.get("composition_base")
    require(isinstance(locked_base, dict), "authority lock lacks composition_base")
    for key in ("repository", "branch", "commit", "tree"):
        require(locked_base.get(key) == config["composition_base"].get(key), f"authority-lock composition base differs for {key}")
    require(locked_base.get("pinned_official_stacks_commit") == config["upstream"]["commit"], "authority lock pins another official commit")
    require(locked_base.get("pinned_official_stacks_tree") == config["upstream"]["tree"], "authority lock pins another official tree")
    return verified


def validate_lifecycle(
    config: dict[str, Any],
    units: list[dict[str, Any]],
    source_map: list[dict[str, Any]],
    inventory: dict[str, Any],
    composition: list[dict[str, Any]],
) -> dict[str, Any]:
    require(config.get("payload_operation_count") == len(composition) == 1, "payload operation count is stale")
    require(
        config.get("payload_state")
        in {"authored_not_built", "built", "validated", "built_validated", "authored_built_validated"},
        "payload lifecycle still says it is absent/not built",
    )
    proposed = [unit for unit in units if unit.get("target", {}).get("kind") == "proposed_new_lemma"]
    duplicates = [unit for unit in units if unit.get("target", {}).get("kind") == "existing_stacks_result"]
    require(len(proposed) == 10 and len(duplicates) == 2, "stable-unit lifecycle is not 10 proposed + 2 duplicate")
    require(all(unit.get("status", "").startswith("mapped_payload_") for unit in proposed), "a proposed stable unit still says no payload exists")
    require(all(unit.get("status") == "dispositioned_existing_no_payload" for unit in duplicates), "duplicate stable-unit lifecycle is stale")
    require(all(row.get("payload_state") not in {"not_built", "future_payload"} for row in source_map[:10]), "source-map lifecycle still says the authored payload is absent")
    require(all(row.get("payload_state") == "no_payload_duplicate" for row in source_map[10:]), "duplicate source-map lifecycle is stale")
    require(inventory.get("payload_comparison_state") not in {"not_performed_no_payload", "no_payload"}, "formula inventory still says no payload exists")

    receipt_specs = {
        "build_state": CANDIDATE / "builds" / "build-receipt.json",
        "visual_qa_state": CANDIDATE / "builds" / "visual-qa.json",
        "independent_replay": CANDIDATE / "replay" / "independent-review.json",
    }
    states: dict[str, Any] = {}
    for field, path in receipt_specs.items():
        declared = config.get(field)
        if not path.exists():
            require(declared == "not_performed", f"config.{field} overstates a missing receipt")
            states[field] = declared
            continue
        receipt = load_json(path)
        require(isinstance(receipt.get("passed"), bool), f"receipt lacks Boolean passed: {display(path)}")
        if "status" in receipt:
            require(receipt.get("status") == ("PASS" if receipt["passed"] else "FAIL"), f"receipt status/passed disagreement: {display(path)}")
        if field == "independent_replay":
            expected = "passed" if receipt["passed"] else "failed"
            require(declared == expected, f"config independent_replay is stale; receipt says {expected}")
        elif field == "build_state":
            require(
                receipt["passed"] is True
                and declared in {"performed", "passed", "built", "validated", "validated_pass"},
                "config build_state is stale or build receipt failed",
            )
            require(
                config.get("payload_state") in {"built", "validated", "built_validated", "authored_built_validated"},
                "payload_state is not synchronized to the passed build receipt",
            )
        else:
            require(
                receipt["passed"] is True and declared in {"performed", "passed", "visual_qa_passed"},
                "config visual_qa_state is stale or visual QA failed",
            )
        for hash_row, locus in walk_hash_rows(receipt, display(path)):
            validate_hash_row(hash_row, locus)
        states[field] = declared
    validation_path = CANDIDATE / "builds" / "validation.json"
    if validation_path.exists():
        validation = load_json(validation_path)
        require(validation.get("passed") is True, "builds/validation.json exists but is not passed")
        if "status" in validation:
            require(validation.get("status") == "PASS", "validation status/passed disagreement")
        for hash_row, locus in walk_hash_rows(validation, "builds/validation.json"):
            validate_hash_row(hash_row, locus)
    review_path = CANDIDATE / "replay" / "independent-review.json"
    if review_path.exists():
        require(config.get("review_state") == "performed", "config review_state is stale after independent review")
    else:
        require(config.get("review_state") == "not_performed", "config review_state overstates absent independent review")
    states["review_state"] = config.get("review_state")
    return states


def bounded_public_files() -> Iterable[Path]:
    stack = [CANDIDATE]
    while stack:
        directory = stack.pop()
        with os.scandir(directory) as entries:
            ordered = sorted(entries, key=lambda entry: entry.name)
        for entry in reversed(ordered):
            if entry.is_dir(follow_symlinks=False):
                if entry.name in {".work", ".git"}:
                    continue
                require(entry.name != "__pycache__", f"Python cache remains in public candidate path: {display(Path(entry.path))}")
                stack.append(Path(entry.path))
            elif entry.is_file(follow_symlinks=False):
                yield Path(entry.path)


def validate_public_hygiene() -> dict[str, int]:
    private_root = re.compile(re.escape("C:") + r"(?:\\+|/+)" + "Us" + "ers" + r"(?:\\+|/+)", re.IGNORECASE)
    credential_prefixes = ("g" + "hp_", "github" + "_pat_", "Bearer " + "eyJ", "zenodo" + "_token=")
    checked = 0
    for path in bounded_public_files():
        if path.suffix.lower() not in {".py", ".md", ".json", ".jsonl", ".tex", ".txt", ".csv", ".log", ""}:
            continue
        data = path.read_bytes()
        if path.suffix.lower() in {".pdf"}:
            continue
        require(not data.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM remains in {display(path)}")
        require(b"\r" not in data, f"non-LF line ending remains in {display(path)}")
        text = data.decode("utf-8", errors="strict")
        require(private_root.search(text) is None, f"private absolute path remains in {display(path)}")
        for prefix in credential_prefixes:
            require(prefix not in text, f"credential-like material remains in {display(path)}")
        if path.suffix.lower() == ".json":
            json.loads(text)
        elif path.suffix.lower() == ".jsonl":
            for number, line in enumerate(text.splitlines(), 1):
                if line.strip():
                    value = json.loads(line)
                    require(isinstance(value, dict), f"non-object JSONL row at {display(path)}:{number}")
        checked += 1
    return {"text_files": checked, "python_caches": 0}


def validate_referenced_hashes(documents: Iterable[tuple[Any, str]]) -> int:
    seen: set[tuple[str, str]] = set()
    count = 0
    for document, name in documents:
        for row, locus in walk_hash_rows(document, name):
            key = (str(row.get("path")), str(row.get("sha256")))
            if key in seen:
                continue
            validate_hash_row(row, locus)
            seen.add(key)
            count += 1
    return count


def main() -> int:
    try:
        config = load_json(CANDIDATE / "candidate.config.json")
        expected_ids = validate_config(config)
        pointer, active_lease = validate_lease(config)
        stable, units = validate_units(config, expected_ids)
        source_map, authority_lock = validate_source_map(config, expected_ids)
        decisions, rejections = validate_ledgers()
        inventory = validate_inventory(expected_ids)
        composition = validate_composition(config, expected_ids)
        rights = validate_rights(config, authority_lock)
        external_hashes = validate_external_authority(config, authority_lock, source_map)
        labels = validate_labels_and_claims(
            config,
            (config, stable, source_map, decisions, rejections, inventory, composition, authority_lock),
        )
        hash_count = validate_referenced_hashes(
            (
                (config, "candidate.config.json"),
                (authority_lock, "authority/authority.lock.json"),
                (stable, "stable-units.json"),
                (source_map, "source-map.jsonl"),
                (decisions, "decisions.jsonl"),
                (rejections, "rejections.jsonl"),
                (inventory, "formula-diagram-inventory.json"),
                (composition, "composition.jsonl"),
            )
        )
        lifecycle = validate_lifecycle(config, units, source_map, inventory, composition)
        hygiene = validate_public_hygiene()
        result = {
            "passed": True,
            "candidate_id": config["candidate_id"],
            "lease_id": pointer["lease_id"],
            "active_lease_event": active_lease.get("event_id"),
            "stable_units": len(units),
            "source_map_rows": len(source_map),
            "decision_rows": len(decisions),
            "rejection_rows": len(rejections),
            "composition_rows": len(composition),
            "labels": len(labels),
            "referenced_hashes_verified": hash_count,
            "external_authority_hashes_verified": external_hashes,
            "rights_declared": bool(rights),
            "lifecycle": lifecycle,
            "public_hygiene": hygiene,
        }
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (VerificationError, OSError, UnicodeError, KeyError, TypeError, ValueError) as exc:
        print(f"VERIFICATION FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
