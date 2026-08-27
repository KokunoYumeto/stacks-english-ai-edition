from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
AUTHORITY_SHA256 = "0106554339E8966FE04411B2AE9F9CD856B165849FEEF0C7BC37634819064708"
AUTHORITY_BYTES = 1_492_039
UPSTREAM_LOCK_SHA256 = "B195ECC83AB0F32C574A60D1FDBA9B0DA4D35B04E0DF7CB106DC9C0FDAD99C0D"
COPYING_SHA256 = "4B2C8FC390F802CD92F0622DC00A708A588BEC54D0145D2EE135D6D7672BFE85"
GENERATED_AT = "2026-08-26T03:45:08Z"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def file_sha(path: Path) -> str:
    return sha(path.read_bytes())


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="",
    )


def artifact(path: Path, logical_path: str) -> dict:
    return {"path": logical_path, "bytes": path.stat().st_size, "sha256": file_sha(path)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Materialize the bounded R23 More Algebra H/J candidate.")
    parser.add_argument("--authority", type=Path, required=True)
    parser.add_argument("--upstream-lock", type=Path, required=True)
    parser.add_argument("--copying", type=Path, required=True)
    parser.add_argument("--overwrite-generated", action="store_true")
    args = parser.parse_args()

    authority = args.authority.read_bytes()
    if len(authority) != AUTHORITY_BYTES or sha(authority) != AUTHORITY_SHA256:
        raise AssertionError("frozen more-algebra.tex authority mismatch")
    if b"\r" in authority or not authority.endswith(b"\n"):
        raise AssertionError("authority must be LF-only UTF-8 with terminal LF")
    if file_sha(args.upstream_lock) != UPSTREAM_LOCK_SHA256:
        raise AssertionError("upstream lock mismatch")
    if file_sha(args.copying) != COPYING_SHA256:
        raise AssertionError("COPYING mismatch")

    spec = json.loads((ROOT / "R23_MORE_ALGEBRA_ADJUDICATION_SPEC.json").read_text(encoding="utf-8"))
    operation_spec = json.loads((ROOT / "operation-spec.input.json").read_text(encoding="utf-8"))
    config_input = json.loads((ROOT / "candidate.config.input.json").read_text(encoding="utf-8"))
    validation = json.loads((ROOT / "INTAKE_VALIDATION.json").read_text(encoding="utf-8"))
    if (
        validation["status"] != "PASS"
        or spec["semantic_unit_count"] != 10
        or len(operation_spec["operations"]) != 12
        or len(spec["rejected"]) != 1
        or config_input["accepted"] != 10
    ):
        raise AssertionError("R23 intake closure mismatch")
    expected_ids = [f"MC-STK-ERR-{number:04d}" for number in range(998, 1008)]
    if [row["stable_id"] for row in spec["accepted"]] != expected_ids:
        raise AssertionError("R23 stable IDs are not contiguous 0998..1007")

    payload = authority
    operations = operation_spec["operations"]
    ascending = sorted(operations, key=lambda row: row["start_byte"])
    for left, right in zip(ascending, ascending[1:]):
        if left["end_byte_exclusive"] > right["start_byte"]:
            raise AssertionError(f"overlap: {left['operation_id']} / {right['operation_id']}")
    for row in sorted(operations, key=lambda item: item["start_byte"], reverse=True):
        start, end = row["start_byte"], row["end_byte_exclusive"]
        old = row["old_text"].encode("utf-8")
        new = row["replacement_text"].encode("utf-8")
        if payload[start:end] != old:
            raise AssertionError(f"operation replay mismatch: {row['operation_id']}")
        if sha(old) != row["old_sha256"] or sha(new) != row["replacement_sha256"]:
            raise AssertionError(f"operation span hash mismatch: {row['operation_id']}")
        payload = payload[:start] + new + payload[end:]
    if len(payload) != config_input["payload_expected_bytes"] or sha(payload) != config_input["payload_expected_sha256"]:
        raise AssertionError("payload preview identity mismatch")

    generated = [
        ROOT / "authority",
        ROOT / "payload",
        ROOT / "candidate.config.json",
        ROOT / "stable-units.json",
        ROOT / "source-map.jsonl",
        ROOT / "operation-spec.json",
        ROOT / "decisions.jsonl",
        ROOT / "rejections.jsonl",
        ROOT / "formula-diagram-inventory.json",
        ROOT / "source-validation.json",
    ]
    existing = [path for path in generated if path.exists()]
    if existing and not args.overwrite_generated:
        raise FileExistsError("generated candidate material already exists")
    if args.overwrite_generated:
        for path in existing:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

    (ROOT / "authority/source").mkdir(parents=True)
    (ROOT / "authority/canon").mkdir(parents=True)
    (ROOT / "payload").mkdir(parents=True)
    (ROOT / "authority/source/more-algebra.tex").write_bytes(authority)
    (ROOT / "payload/more-algebra.tex").write_bytes(payload)
    shutil.copy2(args.upstream_lock, ROOT / "authority/upstream.lock.json")
    shutil.copy2(args.copying, ROOT / "authority/COPYING")
    shutil.copy2(
        ROOT / "R23_MORE_ALGEBRA_ADJUDICATION_SPEC.json",
        ROOT / "authority/canon/R23_MORE_ALGEBRA_ADJUDICATION_SPEC.json",
    )
    shutil.copy2(
        ROOT / "R23_MORE_ALGEBRA_REVIEW.md",
        ROOT / "authority/canon/R23_MORE_ALGEBRA_REVIEW.md",
    )
    shutil.copy2(
        ROOT / "INTAKE_VALIDATION.json",
        ROOT / "authority/canon/R23_MORE_ALGEBRA_INTAKE_VALIDATION.json",
    )
    for source_name, target_name in (
        ("stable-units.input.json", "stable-units.json"),
        ("source-map.input.jsonl", "source-map.jsonl"),
        ("decisions.input.jsonl", "decisions.jsonl"),
        ("rejections.input.jsonl", "rejections.jsonl"),
    ):
        shutil.copy2(ROOT / source_name, ROOT / target_name)
    operation_spec["operation_count"] = len(operation_spec["operations"])
    operation_spec["apply_order"] = "descending_start_byte"
    write_json(ROOT / "operation-spec.json", operation_spec)

    formula_units: list[str] = []
    prose_units: list[str] = []
    for unit in spec["accepted"]:
        target = formula_units if any(
            "$" in op["old_text"]
            or "\\" in op["old_text"]
            or "$" in op["replacement_text"]
            or "\\" in op["replacement_text"]
            for op in unit["operations"]
        ) else prose_units
        target.append(unit["stable_id"])
    write_json(ROOT / "formula-diagram-inventory.json", {
        "schema": "mathematics-commons-stacks-errata-formula-diagram-inventory/v1",
        "candidate_id": "stacks-errata-a04446e-r23",
        "unit_count": 10,
        "formula_units": formula_units,
        "diagram_units": [],
        "prose_only_units": prose_units,
        "classification": "Every accepted unit is classified exactly once; no diagram operation is declared.",
        "unmapped_formula_or_diagram_changes": 0,
    })

    config = dict(config_input)
    config["schema"] = "mathematics-commons-stacks-errata-candidate-config/v1"
    config["source_date_epoch"] = "1787715908"
    config["authority_evidence"] = [
        artifact(ROOT / "authority/canon/R23_MORE_ALGEBRA_ADJUDICATION_SPEC.json", "authority/canon/R23_MORE_ALGEBRA_ADJUDICATION_SPEC.json"),
        artifact(ROOT / "authority/canon/R23_MORE_ALGEBRA_INTAKE_VALIDATION.json", "authority/canon/R23_MORE_ALGEBRA_INTAKE_VALIDATION.json"),
        artifact(ROOT / "authority/canon/R23_MORE_ALGEBRA_REVIEW.md", "authority/canon/R23_MORE_ALGEBRA_REVIEW.md"),
        artifact(ROOT / "authority/COPYING", "authority/COPYING"),
        artifact(ROOT / "authority/source/more-algebra.tex", "authority/source/more-algebra.tex"),
        artifact(ROOT / "authority/upstream.lock.json", "authority/upstream.lock.json"),
    ]
    config["stems"] = {"more-algebra": {
        "authority_sha256": AUTHORITY_SHA256,
        "payload_sha256": sha(payload),
        "authority_bytes": len(authority),
        "payload_bytes": len(payload),
        "display_delimiter_delta": 0,
        "ordered_structure_exceptions": {},
        "build_exceptions": {"candidate_page_delta": 0},
    }}
    config["proof_closure"] = {
        "producer_rows": 13,
        "accepted": 10,
        "operations": 12,
        "rejected": 1,
        "unresolved": 0,
        "prior_p02_aliases": 10,
        "packet_duplicates": 0,
        "intentionally_absent": 0,
    }
    config["lease_status"] = "active; bound to registrar-issued LEASE.json"
    config["build_render_admission_status"] = "not_run_by_source_materialization"
    write_json(ROOT / "candidate.config.json", config)
    print(json.dumps({
        "passed": True,
        "units": 10,
        "operations": 12,
        "rejected": 1,
        "payload_bytes": len(payload),
        "payload_sha256": sha(payload),
        "generated_at_utc": GENERATED_AT,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
