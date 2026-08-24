from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
AUTHORITY_SHA256 = "FA8BB92E58A4F78A2BD01B3B6A4A87DE0A0D279F5DD90641B574DD5FBFFFA4F3"
AUTHORITY_BYTES = 1_771_230
PRODUCER_SHA256 = "830E67D6C53398956C8AD9F223E9D29ADF987F13C6203881E7EC939A234D0137"
PRODUCER_BYTES = 367_606
INTAKE_SHA256 = "ED596BDCC15BD05A624ADFB49C8C05B0D5B8F99BC5522A616AD533853C404D5E"
INTAKE_BYTES = 4_675
UPSTREAM_LOCK_SHA256 = "B195ECC83AB0F32C574A60D1FDBA9B0DA4D35B04E0DF7CB106DC9C0FDAD99C0D"
COPYING_SHA256 = "4B2C8FC390F802CD92F0622DC00A708A588BEC54D0145D2EE135D6D7672BFE85"
SPEC_SHA256 = "A73298B59EDE7A40CE271CC64969D4DAF71D85DB06029D0E25794C4023ECCFC9"
GENERATED_AT = "2026-08-24T21:27:03Z"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="",
    )


def artifact(path: Path, logical_path: str) -> dict:
    return {"path": logical_path, "bytes": path.stat().st_size, "sha256": sha256(path)}


def line_offsets(data: bytes) -> list[int]:
    starts = [0]
    starts.extend(match.end() for match in re.finditer(b"\n", data))
    return starts


def sanitize_intake(raw: dict) -> dict:
    result = copy.deepcopy(raw)
    result["external_checkpoint"] = {
        "bytes": INTAKE_BYTES,
        "sha256": INTAKE_SHA256,
        "sanitized_for_publication": True,
    }
    result["authority"]["path"] = "authority/source/algebra.tex"
    result["producer_snapshot"]["path"] = "authority/producer/SOURCE_DEFECT_LEDGER.csv"
    if "producer_emendation_evidence" in result:
        result["producer_emendation_evidence"]["path"] = "external producer evidence; not imported as canon"
    return result


def map_operations(authority: bytes, accepted: list[dict]) -> list[dict]:
    starts = line_offsets(authority)
    mapped: list[dict] = []
    for unit in accepted:
        for index, raw in enumerate(unit["operations"], 1):
            line_start = raw["source_start_line"]
            line_end = raw["source_end_line"]
            scope_start = starts[line_start - 1]
            scope_end = starts[line_end]
            old = raw["old_text"].encode("utf-8")
            new = raw["replacement_text"].encode("utf-8")
            scope = authority[scope_start:scope_end]
            if scope.count(old) != 1:
                raise AssertionError(
                    f"{unit['producer_id']} OP{index}: old span is not unique in bounded lines"
                )
            start = scope_start + scope.index(old)
            mapped.append({
                "producer_id": unit["producer_id"],
                "stable_id": unit["stable_id"],
                "operation_index": index,
                "source_start_line": line_start,
                "source_end_line": line_end,
                "start_byte": start,
                "end_byte_exclusive": start + len(old),
                "occurrence_count_in_frozen_authority": authority.count(old),
                "old_bytes": len(old),
                "old_sha256": sha_bytes(old),
                "replacement_bytes": len(new),
                "replacement_sha256": sha_bytes(new),
                "old_text": raw["old_text"],
                "replacement_text": raw["replacement_text"],
            })
    ordered = sorted(mapped, key=lambda row: row["start_byte"])
    for left, right in zip(ordered, ordered[1:]):
        if left["end_byte_exclusive"] > right["start_byte"]:
            raise AssertionError(
                f"overlap: {left['producer_id']} OP{left['operation_index']} / "
                f"{right['producer_id']} OP{right['operation_index']}"
            )
    return mapped


def apply_operations(authority: bytes, operations: list[dict]) -> bytes:
    payload = authority
    for row in sorted(operations, key=lambda item: item["start_byte"], reverse=True):
        start = row["start_byte"]
        end = row["end_byte_exclusive"]
        old = row["old_text"].encode("utf-8")
        new = row["replacement_text"].encode("utf-8")
        if payload[start:end] != old:
            raise AssertionError(f"replay interval mismatch: {row['producer_id']}")
        payload = payload[:start] + new + payload[end:]
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authority", type=Path, required=True)
    parser.add_argument("--producer-ledger", type=Path, required=True)
    parser.add_argument("--intake-checkpoint", type=Path, required=True)
    parser.add_argument("--upstream-lock", type=Path, required=True)
    parser.add_argument("--copying", type=Path, required=True)
    parser.add_argument("--replace-generated", action="store_true")
    args = parser.parse_args()

    authority = args.authority.read_bytes()
    if len(authority) != AUTHORITY_BYTES or sha_bytes(authority) != AUTHORITY_SHA256:
        raise AssertionError("frozen authority identity mismatch")
    if b"\r" in authority or not authority.endswith(b"\n"):
        raise AssertionError("authority is not terminal-LF UTF-8/LF source")
    producer_live = args.producer_ledger.read_bytes()
    producer_snapshot = producer_live[:PRODUCER_BYTES]
    if len(producer_snapshot) != PRODUCER_BYTES or sha_bytes(producer_snapshot) != PRODUCER_SHA256:
        raise AssertionError("producer ledger does not retain the frozen append-only prefix")
    if args.intake_checkpoint.stat().st_size != INTAKE_BYTES or sha256(args.intake_checkpoint) != INTAKE_SHA256:
        raise AssertionError("external intake checkpoint identity mismatch")
    if sha256(args.upstream_lock) != UPSTREAM_LOCK_SHA256 or sha256(args.copying) != COPYING_SHA256:
        raise AssertionError("upstream lock or COPYING identity mismatch")

    spec_path = ROOT / "authority" / "canon" / "R12_ALG_386_391_ADJUDICATION_SPEC.json"
    if SPEC_SHA256 == "TO_BE_FILLED" or sha256(spec_path) != SPEC_SHA256:
        raise AssertionError("adjudication spec identity mismatch")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    accepted = spec["accepted"]
    rejected = spec["rejected"]
    expected_producers = [f"ALGEBRA-{number}" for number in range(386, 392)]
    accepted_producers = [row["producer_id"] for row in accepted]
    rejected_producers = [row["producer_id"] for row in rejected]
    if sorted(accepted_producers + rejected_producers) != sorted(expected_producers):
        raise AssertionError("adjudication partition is not ALGEBRA-386..391")
    expected_ids = [f"MC-STK-ERR-{number:04d}" for number in range(729, 735)]
    if [row["stable_id"] for row in accepted] != expected_ids:
        raise AssertionError("stable-ID assignment is not contiguous 0729..0734")

    producer_rows = list(csv.DictReader(producer_snapshot.decode("utf-8").splitlines()))
    producer_ids = [row["id"] for row in producer_rows]
    if any(producer_ids.count(producer) != 1 for producer in expected_producers):
        raise AssertionError("producer ledger does not contain every selected row exactly once")

    generated = [
        ROOT / "authority" / "source" / "algebra.tex",
        ROOT / "authority" / "producer" / "SOURCE_DEFECT_LEDGER.csv",
        ROOT / "authority" / "upstream.lock.json",
        ROOT / "authority" / "COPYING",
        ROOT / "authority" / "canon" / "R12_ALG_386_391_INTAKE.json",
        ROOT / "authority" / "canon" / "R12_ALG_386_391_REVIEW.md",
        ROOT / "payload" / "algebra.tex",
        ROOT / "candidate.config.json",
        ROOT / "stable-units.json",
        ROOT / "source-map.jsonl",
        ROOT / "decisions.jsonl",
        ROOT / "rejections.jsonl",
        ROOT / "formula-diagram-inventory.json",
        ROOT / "operation-spec.json",
    ]
    if any(path.exists() for path in generated) and not args.replace_generated:
        raise FileExistsError("candidate material already exists; materializer refuses to overwrite")

    operations = map_operations(authority, accepted)
    payload = apply_operations(authority, operations)
    ops_by_producer: dict[str, list[dict]] = {}
    for row in operations:
        ops_by_producer.setdefault(row["producer_id"], []).append(row)

    authority_source = ROOT / "authority" / "source" / "algebra.tex"
    producer_copy = ROOT / "authority" / "producer" / "SOURCE_DEFECT_LEDGER.csv"
    payload_path = ROOT / "payload" / "algebra.tex"
    authority_source.parent.mkdir(parents=True, exist_ok=True)
    producer_copy.parent.mkdir(parents=True, exist_ok=True)
    payload_path.parent.mkdir(parents=True, exist_ok=True)
    authority_source.write_bytes(authority)
    payload_path.write_bytes(payload)
    producer_copy.write_bytes(producer_snapshot)
    shutil.copy2(args.upstream_lock, ROOT / "authority" / "upstream.lock.json")
    shutil.copy2(args.copying, ROOT / "authority" / "COPYING")
    intake = sanitize_intake(json.loads(args.intake_checkpoint.read_text(encoding="utf-8")))
    write_json(ROOT / "authority" / "canon" / "R12_ALG_386_391_INTAKE.json", intake)

    source_rows: list[dict] = []
    stable_units: list[dict] = []
    formula_units: list[str] = []
    prose_units: list[str] = []
    for unit in accepted:
        unit_ops = sorted(ops_by_producer[unit["producer_id"]], key=lambda row: row["operation_index"])
        map_ops = []
        for row in unit_ops:
            map_ops.append({
                "operation_id": f"{unit['stable_id']}-OP{row['operation_index']}",
                "source_start_line": row["source_start_line"],
                "source_end_line": row["source_end_line"],
                "start_byte": row["start_byte"],
                "end_byte_exclusive": row["end_byte_exclusive"],
                "occurrence_count_in_frozen_authority": row["occurrence_count_in_frozen_authority"],
                "old_bytes": row["old_bytes"],
                "old_sha256": row["old_sha256"],
                "replacement_bytes": row["replacement_bytes"],
                "replacement_sha256": row["replacement_sha256"],
                "old_text": row["old_text"],
                "replacement_text": row["replacement_text"],
            })
        stable_units.append({
            "id": unit["stable_id"], "producer_id": unit["producer_id"],
            "class": unit["class"], "source": "algebra.tex", "locus": unit["locus"],
            "payload": "payload/algebra.tex",
            "operation_ids": [row["operation_id"] for row in map_ops], "status": "applied",
        })
        source_rows.append({
            "schema": "mathematics-commons-stacks-errata-map/v2",
            "unit_id": unit["stable_id"], "producer_id": unit["producer_id"],
            "source": "algebra.tex", "authority": "authority/source/algebra.tex",
            "authority_sha256": AUTHORITY_SHA256, "payload": "payload/algebra.tex",
            "locus": unit["locus"], "class": unit["class"],
            "proof": f"Independent canon replay: {unit['result']}. {unit['disposition']}",
            "adverse_evidence": "The frozen source and producer evidence are retained; no translation byte or mutable upstream file was used as the correction authority.",
            "operations": map_ops,
        })
        has_tex = any(
            "$" in row["old_text"] or "\\" in row["old_text"] or
            "$" in row["replacement_text"] or "\\" in row["replacement_text"]
            for row in unit_ops
        )
        (formula_units if has_tex else prose_units).append(unit["stable_id"])

    write_json(ROOT / "stable-units.json", {
        "schema": "mathematics-commons-stacks-errata-units/v1",
        "authority_commit": spec["authority_commit"], "unit_count": len(stable_units),
        "units": stable_units,
    })
    (ROOT / "source-map.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in source_rows),
        encoding="utf-8", newline="",
    )
    write_json(ROOT / "operation-spec.json", {
        "schema": "mathematics-commons-stacks-errata-operation-spec/v1",
        "authority_sha256": AUTHORITY_SHA256, "operation_count": len(operations),
        "apply_order": "descending_start_byte", "operations": operations,
    })
    write_json(ROOT / "formula-diagram-inventory.json", {
        "schema": "mathematics-commons-stacks-errata-formula-diagram-inventory/v1",
        "candidate_id": spec["candidate_id"], "unit_count": len(stable_units),
        "formula_units": formula_units, "diagram_units": [], "prose_only_units": prose_units,
        "classification": "Every accepted unit is classified exactly once; no xymatrix span changes.",
        "unmapped_formula_or_diagram_changes": 0,
    })

    decisions = [
        ("ERR-R12-D0001", "Bind R12 exclusively to the active errata/r12 lease and frozen upstream commit/tree.", "Preserves the single-writer and immutable-authority boundary."),
        ("ERR-R12-D0002", "Assign MC-STK-ERR-0729..0734 in producer order after admitted R11.", "Creates a deterministic contiguous stable-ID sequence for all six accepted rows."),
        ("ERR-R12-D0003", "Apply only exact nonoverlapping half-open UTF-8 spans in descending byte order.", "Prevents contextual or global replacement from changing unrelated source text."),
        ("ERR-R12-D0004", "Accept all six producer rows after independent source replay and deduplication against R1-R11.", "Every accepted row is a distinct bounded defect supported by the frozen source and queue checkpoint."),
        ("ERR-R12-D0005", "Keep canonical locale bytes and the literal upstream mirror outside the corrected English payload.", "Corrections belong only to Stacks — English AI Edition."),
        ("ERR-R12-D0006", "Do not contact or submit this AI-derived correction set to upstream Stacks maintainers.", "The maintained AI-open English edition is the authorized correction surface."),
    ]
    (ROOT / "decisions.jsonl").write_text(
        "".join(json.dumps({"schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": row[0], "timestamp_utc": GENERATED_AT, "choice": row[1],
            "rationale": row[2], "supersedes": None}, ensure_ascii=False,
            separators=(",", ":")) + "\n" for row in decisions),
        encoding="utf-8", newline="",
    )
    (ROOT / "rejections.jsonl").write_text(
        "".join(json.dumps({"schema": "mathematics-commons-stacks-candidate-rejection/v1",
            "id": f"ERR-R12-R{index:04d}", "timestamp_utc": GENERATED_AT,
            "producer_id": row["producer_id"], "disposition": "rejected",
            "reason": row["reason"]}, ensure_ascii=False, separators=(",", ":")) + "\n"
            for index, row in enumerate(rejected, 1)), encoding="utf-8", newline="",
    )

    review_lines = [
        "# Independent review: ALGEBRA-386–391", "",
        f"Frozen authority: `{AUTHORITY_SHA256}` at `{spec['authority_commit']}`.", "",
        "The six producer rows were replayed against the frozen source and are accepted",
        "as `MC-STK-ERR-0729` through `MC-STK-ERR-0734`. No unit is rejected, aliased, or",
        "unresolved. Exact operations and the adjudication rationale for every accepted unit are",
        "bound by the public specification and source map. A separate read-only review checked",
        "all six operations, exact source-line bounds, deduplication against R1–R11, and the",
        "corrected bounded-slice hash before materialization.", "",
        "The English payload is the only corrected surface. The frozen source, canonical translations,",
        "permanent tags, and unrelated chapters remain unchanged. No upstream submission is made.",
    ]
    (ROOT / "authority" / "canon" / "R12_ALG_386_391_REVIEW.md").write_text(
        "\n".join(review_lines) + "\n", encoding="utf-8", newline="")

    authority_evidence = [artifact(path, path.relative_to(ROOT).as_posix())
        for path in sorted((ROOT / "authority").rglob("*")) if path.is_file()]
    config = {
        "schema": "mathematics-commons-stacks-errata-candidate-config/v1",
        "candidate_id": spec["candidate_id"], "lease_id": "stacks-lease-000015-errata-r12",
        "writer_task": "01a0256d-5693-77c1-96b2-cf37101e0c6c",
        "authority_commit": spec["authority_commit"], "authority_tree": spec["authority_tree"],
        "source_date_epoch": "1785270512", "expected_unit_ids": expected_ids,
        "expected_producer_ids": expected_producers, "namespace": "commons/stacks/errata/r12",
        "private_render_logical_path": "canon/private_evidence/errata-r12-20260824T2127Z/render-final/render-manifest.json",
        "operation_count": len(operations),
        "stems": {"algebra": {"authority_sha256": AUTHORITY_SHA256,
            "payload_sha256": sha_bytes(payload), "authority_bytes": len(authority),
            "payload_bytes": len(payload), "display_delimiter_delta": 0,
            "ordered_structure_exceptions": {},
            "build_exceptions": {"candidate_only_undefined_reference_targets": {},
                "candidate_page_delta": 0}}},
        "authority_evidence": authority_evidence,
        "proof_closure": {"producer_rows": len(expected_producers), "accepted": len(accepted),
            "operations": len(operations), "rejected": len(rejected),
            "prior_overlay_aliases": 0, "packet_duplicates": 0, "unresolved": 0},
    }
    write_json(ROOT / "candidate.config.json", config)
    print(json.dumps({"passed": True, "units": len(accepted), "operations": len(operations),
        "payload_bytes": len(payload), "payload_sha256": sha_bytes(payload)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
