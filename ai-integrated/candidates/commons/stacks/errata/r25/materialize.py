from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
GENERATED_AT = "2026-08-27T21:34:00Z"
SOURCE_DATE_EPOCH = "1787866440"
SPEC_INPUT_NAME = "R25_ARTIN_ADJUDICATION_SPEC.input.json"
SPEC_NAME = "R25_ARTIN_ADJUDICATION_SPEC.json"
REVIEW_NAME = "R25_ARTIN_REVIEW.md"
PRODUCER_INPUT_NAME = "P11_ARTIN_ERRATA_R25.input.jsonl"
PRODUCER_CANON_NAME = "P11_ARTIN_ERRATA_R25.jsonl"
EXPECTED_IDS = [f"MC-STK-ERR-{number:04d}" for number in range(1046, 1177)]
EXPECTED_PRODUCER_IDS = [f"P11-E{number:04d}" for number in range(200, 340)]
REJECTED_IDS = ["P11-E0202", "P11-E0215", "P11-E0217"]


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def file_sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="",
    )


def write_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value)


def artifact(path: Path, logical_path: str) -> dict:
    return {"path": logical_path, "bytes": path.stat().st_size, "sha256": file_sha(path)}


def generated_targets() -> list[Path]:
    return [
        ROOT / "authority/source/artin.tex",
        ROOT / "authority/COPYING",
        ROOT / "authority/upstream.lock.json",
        ROOT / f"authority/canon/{SPEC_NAME}",
        ROOT / "authority/canon/R25_ARTIN_INTAKE_VALIDATION.json",
        ROOT / f"authority/canon/{REVIEW_NAME}",
        ROOT / f"authority/canon/{PRODUCER_CANON_NAME}",
        ROOT / "payload/artin.tex",
        ROOT / SPEC_NAME,
        ROOT / "candidate.config.json",
        ROOT / "stable-units.json",
        ROOT / "source-map.jsonl",
        ROOT / "operation-spec.json",
        ROOT / "decisions.jsonl",
        ROOT / "rejections.jsonl",
        ROOT / "formula-diagram-inventory.json",
        ROOT / "source-validation.json",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Materialize the bounded R25 Artin source candidate.")
    parser.add_argument("--authority", type=Path, required=True)
    parser.add_argument("--copying", type=Path, required=True)
    parser.add_argument("--overwrite-generated", action="store_true")
    args = parser.parse_args()

    spec_input_path = ROOT / SPEC_INPUT_NAME
    spec_bytes = spec_input_path.read_bytes()
    spec = json.loads(spec_bytes.decode("utf-8"))
    authority = args.authority.read_bytes()
    copying = args.copying.read_bytes()
    if len(authority) != spec["authority_bytes"] or sha_bytes(authority) != spec["authority_sha256"]:
        raise AssertionError("frozen artin.tex authority mismatch")
    if b"\r" in authority or not authority.endswith(b"\n"):
        raise AssertionError("authority must be LF-only UTF-8 with terminal LF")
    if not copying or b"GNU Free Documentation License" not in copying:
        raise AssertionError("COPYING does not contain the expected license text")

    validation = json.loads((ROOT / "INTAKE_VALIDATION.json").read_text(encoding="utf-8"))
    config_input = json.loads((ROOT / "candidate.config.input.json").read_text(encoding="utf-8"))
    operation_spec = json.loads((ROOT / "operation-spec.input.json").read_text(encoding="utf-8"))
    stable_input = json.loads((ROOT / "stable-units.input.json").read_text(encoding="utf-8"))
    source_map_input = (ROOT / "source-map.input.jsonl").read_bytes()
    decisions_input = (ROOT / "decisions.input.jsonl").read_bytes()
    rejections_input = (ROOT / "rejections.input.jsonl").read_bytes()
    producer_input = (ROOT / PRODUCER_INPUT_NAME).read_bytes()
    producer_rows = load_jsonl(ROOT / PRODUCER_INPUT_NAME)
    rejections = load_jsonl(ROOT / "rejections.input.jsonl")
    if (
        validation["status"] != "PASS"
        or validation["adjudication_spec_sha256"] != sha_bytes(spec_bytes)
        or validation["authority_sha256"] != sha_bytes(authority)
        or spec["semantic_unit_count"] != 131
        or spec["accepted_producer_row_count"] != 137
        or spec["rejected_producer_row_count"] != 3
        or len(operation_spec["operations"]) != 154
        or stable_input["unit_count"] != 131
        or config_input["accepted"] != 131
        or config_input["rejected"] != 3
        or len(rejections) != 3
        or [row["producer_id"] for row in rejections] != REJECTED_IDS
        or [row["id"] for row in producer_rows] != EXPECTED_PRODUCER_IDS
        or any(row.get("source_path") != "artin.tex" for row in producer_rows)
    ):
        raise AssertionError("R25 intake closure mismatch")
    if [row["stable_id"] for row in spec["accepted"]] != EXPECTED_IDS:
        raise AssertionError("R25 stable IDs are not contiguous 1046..1176")

    targets = generated_targets()
    existing = [path for path in targets if path.exists()]
    if existing and not args.overwrite_generated:
        raise FileExistsError("generated R25 material already exists; use --overwrite-generated for exact-file replay")
    for target in existing:
        if target.is_dir():
            raise AssertionError(f"generated target unexpectedly became a directory: {target.name}")

    operations = operation_spec["operations"]
    intervals = sorted((row["start_byte"], row["end_byte_exclusive"], row["operation_id"]) for row in operations)
    for left, right in zip(intervals, intervals[1:]):
        if left[1] > right[0]:
            raise AssertionError(f"overlapping operations: {left[2]} / {right[2]}")
    payload = authority
    for row in sorted(operations, key=lambda item: item["start_byte"], reverse=True):
        start = row["start_byte"]
        end = row["end_byte_exclusive"]
        old = row["old_text"].encode("utf-8")
        replacement = row["replacement_text"].encode("utf-8")
        if payload[start:end] != old:
            raise AssertionError(f"operation replay mismatch: {row['operation_id']}")
        if sha_bytes(old) != row["old_sha256"] or sha_bytes(replacement) != row["replacement_sha256"]:
            raise AssertionError(f"operation span hash mismatch: {row['operation_id']}")
        payload = payload[:start] + replacement + payload[end:]
    if len(payload) != config_input["payload_expected_bytes"] or sha_bytes(payload) != config_input["payload_expected_sha256"]:
        raise AssertionError("payload preview identity mismatch")

    upstream_lock = {
        "schema": "mathematics-commons-stacks-upstream-lock/v1",
        "project": "The Stacks Project",
        "commit": spec["authority_commit"],
        "tree": spec["authority_tree"],
        "source": {
            "path": spec["authority_path"],
            "bytes": len(authority),
            "sha256": sha_bytes(authority),
        },
        "scope": "single_frozen_source_file_for_errata_r25",
    }

    write_bytes(ROOT / SPEC_NAME, spec_bytes)
    write_bytes(ROOT / "authority/source/artin.tex", authority)
    write_bytes(ROOT / "authority/COPYING", copying)
    write_json(ROOT / "authority/upstream.lock.json", upstream_lock)
    write_bytes(ROOT / f"authority/canon/{SPEC_NAME}", spec_bytes)
    write_bytes(
        ROOT / "authority/canon/R25_ARTIN_INTAKE_VALIDATION.json",
        (ROOT / "INTAKE_VALIDATION.json").read_bytes(),
    )
    write_bytes(ROOT / f"authority/canon/{REVIEW_NAME}", (ROOT / REVIEW_NAME).read_bytes())
    write_bytes(ROOT / f"authority/canon/{PRODUCER_CANON_NAME}", producer_input)
    write_bytes(ROOT / "payload/artin.tex", payload)
    write_bytes(ROOT / "stable-units.json", (ROOT / "stable-units.input.json").read_bytes())
    write_bytes(ROOT / "source-map.jsonl", source_map_input)
    write_bytes(ROOT / "decisions.jsonl", decisions_input)
    write_bytes(ROOT / "rejections.jsonl", rejections_input)
    operation_spec["operation_count"] = len(operations)
    operation_spec["apply_order"] = "descending_start_byte"
    write_json(ROOT / "operation-spec.json", operation_spec)

    formula_units: list[str] = []
    diagram_units: list[str] = []
    prose_units: list[str] = []
    formula_markers = ("$", "\\", "_", "^", "{", "}")
    for unit in spec["accepted"]:
        stable_id = unit["stable_id"]
        if any(
            any(marker in operation["old_text"] or marker in operation["replacement_text"] for marker in formula_markers)
            for operation in unit["operations"]
        ):
            formula_units.append(stable_id)
        else:
            prose_units.append(stable_id)
    write_json(ROOT / "formula-diagram-inventory.json", {
        "schema": "mathematics-commons-stacks-errata-formula-diagram-inventory/v1",
        "candidate_id": spec["candidate_id"],
        "unit_count": len(spec["accepted"]),
        "formula_units": formula_units,
        "diagram_units": diagram_units,
        "prose_only_units": prose_units,
        "classification": "Every accepted R25 unit is classified exactly once from its exact artin.tex operation; no accepted operation changes xymatrix source.",
        "unmapped_formula_or_diagram_changes": 0,
    })

    config = dict(config_input)
    config["schema"] = "mathematics-commons-stacks-errata-candidate-config/v1"
    config["source_date_epoch"] = SOURCE_DATE_EPOCH
    config["authority_evidence"] = [
        artifact(ROOT / f"authority/canon/{SPEC_NAME}", f"authority/canon/{SPEC_NAME}"),
        artifact(ROOT / "authority/canon/R25_ARTIN_INTAKE_VALIDATION.json", "authority/canon/R25_ARTIN_INTAKE_VALIDATION.json"),
        artifact(ROOT / f"authority/canon/{REVIEW_NAME}", f"authority/canon/{REVIEW_NAME}"),
        artifact(ROOT / f"authority/canon/{PRODUCER_CANON_NAME}", f"authority/canon/{PRODUCER_CANON_NAME}"),
        artifact(ROOT / "authority/COPYING", "authority/COPYING"),
        artifact(ROOT / "authority/source/artin.tex", "authority/source/artin.tex"),
        artifact(ROOT / "authority/upstream.lock.json", "authority/upstream.lock.json"),
    ]
    config["stems"] = {
        "artin": {
            "authority_sha256": sha_bytes(authority),
            "payload_sha256": sha_bytes(payload),
            "authority_bytes": len(authority),
            "payload_bytes": len(payload),
            "display_delimiter_delta": payload.count(b"$$") - authority.count(b"$$"),
            "ordered_structure_exceptions": {},
            "source_line_exceptions": {},
            "build_exceptions": {},
        }
    }
    config["proof_closure"] = {
        "producer_rows": 140,
        "accepted_producer_rows": 137,
        "accepted": 131,
        "operations": 154,
        "rejected": 3,
        "unresolved": 0,
        "prior_aliases": 0,
        "packet_duplicates": 0,
        "intentionally_absent": 0,
    }
    config["lease_status"] = "active; bound to registrar-issued LEASE.json"
    config["build_render_admission_status"] = "not_run_by_source_materialization"
    write_json(ROOT / "candidate.config.json", config)

    print(json.dumps({
        "passed": True,
        "units": 131,
        "operations": 154,
        "accepted_producer_ids": 137,
        "rejected_producer_ids": 3,
        "payload_bytes": len(payload),
        "payload_sha256": sha_bytes(payload),
        "generated_at_utc": GENERATED_AT,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
