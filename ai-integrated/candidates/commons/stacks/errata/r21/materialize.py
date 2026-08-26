from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
AUTHORITY_SHA256 = "187B4CD4F20696BF35EED843528462780CA04ABBBC597AE1045F8404372FDC56"
AUTHORITY_BYTES = 234_898
UPSTREAM_LOCK_SHA256 = "B195ECC83AB0F32C574A60D1FDBA9B0DA4D35B04E0DF7CB106DC9C0FDAD99C0D"
COPYING_SHA256 = "4B2C8FC390F802CD92F0622DC00A708A588BEC54D0145D2EE135D6D7672BFE85"
GENERATED_AT = "2026-08-25T20:33:58Z"
SPEC_PATH = ROOT / "authority" / "canon" / "R21_SIMPLICIAL_001_011_ADJUDICATION_SPEC.json"
SPEC_SHA256 = "77AAB0AB50264240E11AEE565A18F25C35ED50647154587EF38A0D0DE42FB7C2"
REVIEW_PATH = ROOT / "authority" / "canon" / "R21_SIMPLICIAL_001_011_REVIEW.md"
REVIEW_SHA256 = "CE208C8206E4A6D6DCD14B30E27825F9753D30F469392451AB4EB4D11928FFAB"
EXPECTED_PAYLOAD_BYTES = 235_001
EXPECTED_PAYLOAD_SHA256 = "E4FD6748E65633490F8C48D720BEBF7327505DDF25B578868F6739E15BC96E16"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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
            replacement = raw["replacement_text"].encode("utf-8")
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
                "replacement_bytes": len(replacement),
                "replacement_sha256": sha_bytes(replacement),
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
        replacement = row["replacement_text"].encode("utf-8")
        if payload[start:end] != old:
            raise AssertionError(f"replay interval mismatch: {row['producer_id']}")
        payload = payload[:start] + replacement + payload[end:]
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authority", type=Path, required=True)
    parser.add_argument("--upstream-lock", type=Path, required=True)
    parser.add_argument("--copying", type=Path, required=True)
    parser.add_argument("--overwrite-generated", action="store_true")
    args = parser.parse_args()

    authority = args.authority.read_bytes()
    if len(authority) != AUTHORITY_BYTES or sha_bytes(authority) != AUTHORITY_SHA256:
        raise AssertionError("frozen authority identity mismatch")
    if b"\r" in authority or not authority.endswith(b"\n"):
        raise AssertionError("authority is not terminal-LF UTF-8/LF source")
    if sha256(args.upstream_lock) != UPSTREAM_LOCK_SHA256:
        raise AssertionError("upstream lock identity mismatch")
    if sha256(args.copying) != COPYING_SHA256:
        raise AssertionError("COPYING identity mismatch")

    if not SPEC_PATH.is_file() or sha256(SPEC_PATH) != SPEC_SHA256:
        raise AssertionError("adjudication specification identity mismatch")
    if not REVIEW_PATH.is_file() or sha256(REVIEW_PATH) != REVIEW_SHA256:
        raise AssertionError("independent review identity mismatch")
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    if (
        spec["candidate_id"] != "stacks-errata-a04446e-r21"
        or spec["authority_sha256"] != AUTHORITY_SHA256
        or spec["authority_commit"] != "a04446e57ec1fbc252a871afcec7752fb2807b14"
        or spec["authority_tree"] != "3feeb703b931a6e7259782c10e7d1575adc83e5e"
    ):
        raise AssertionError("adjudication specification authority binding mismatch")
    accepted = spec["accepted"]
    rejected = spec["rejected"]
    expected_producers = (
        [f"SIMPLICIAL-{number:03d}" for number in range(1, 7)]
        + ["CANON-SIMPLICIAL-001"]
        + [f"SIMPLICIAL-{number:03d}" for number in range(7, 12)]
    )
    accepted_producers = [row["producer_id"] for row in accepted]
    rejected_producers = [row["producer_id"] for row in rejected]
    if (
        len(set(accepted_producers + rejected_producers)) != len(expected_producers)
        or set(accepted_producers + rejected_producers) != set(expected_producers)
        or rejected_producers != ["SIMPLICIAL-007"]
    ):
        raise AssertionError("adjudication partition is not SIMPLICIAL-001..011 plus CANON-SIMPLICIAL-001 with only 007 rejected")
    expected_ids = [f"MC-STK-ERR-{number:04d}" for number in range(904, 915)]
    if [row["stable_id"] for row in accepted] != expected_ids:
        raise AssertionError("stable-ID assignment is not contiguous 0904..0914")

    generated = [
        ROOT / "authority" / "source" / "simplicial.tex",
        ROOT / "authority" / "upstream.lock.json",
        ROOT / "authority" / "COPYING",
        ROOT / "authority" / "canon" / "R21_SIMPLICIAL_001_011_INTAKE.json",
        ROOT / "payload" / "simplicial.tex",
        ROOT / "candidate.config.json",
        ROOT / "stable-units.json",
        ROOT / "source-map.jsonl",
        ROOT / "decisions.jsonl",
        ROOT / "rejections.jsonl",
        ROOT / "formula-diagram-inventory.json",
        ROOT / "operation-spec.json",
    ]
    if any(path.exists() for path in generated):
        if not args.overwrite_generated:
            raise FileExistsError("candidate material already exists; pass --overwrite-generated for the bounded regenerated set")
        for path in generated:
            if path.is_file():
                path.unlink()

    operations = map_operations(authority, accepted)
    if len(accepted) != 11 or len(operations) != 11 or len(rejected) != 1:
        raise AssertionError("R21 count contract mismatch")
    payload = apply_operations(authority, operations)
    if len(payload) != EXPECTED_PAYLOAD_BYTES or sha_bytes(payload) != EXPECTED_PAYLOAD_SHA256:
        raise AssertionError("R21 deterministic payload identity mismatch")
    ops_by_producer: dict[str, list[dict]] = {}
    for row in operations:
        ops_by_producer.setdefault(row["producer_id"], []).append(row)

    authority_source = ROOT / "authority" / "source" / "simplicial.tex"
    payload_path = ROOT / "payload" / "simplicial.tex"
    authority_source.parent.mkdir(parents=True, exist_ok=True)
    payload_path.parent.mkdir(parents=True, exist_ok=True)
    authority_source.write_bytes(authority)
    payload_path.write_bytes(payload)
    shutil.copy2(args.upstream_lock, ROOT / "authority" / "upstream.lock.json")
    shutil.copy2(args.copying, ROOT / "authority" / "COPYING")

    offsets = line_offsets(authority)
    bounded_start_line = 277
    bounded_end_line = 2762
    bounded_authority = authority[offsets[bounded_start_line - 1]:offsets[bounded_end_line]]
    bounded_start_byte = offsets[bounded_start_line - 1]
    bounded_end_byte = offsets[bounded_end_line]
    bounded_operations = []
    for row in operations:
        if bounded_start_byte <= row["start_byte"] and row["end_byte_exclusive"] <= bounded_end_byte:
            local = dict(row)
            local["start_byte"] -= bounded_start_byte
            local["end_byte_exclusive"] -= bounded_start_byte
            bounded_operations.append(local)
    if len(bounded_operations) != len(operations):
        raise AssertionError("an R21 operation lies outside the declared bounded source")
    bounded_payload = apply_operations(bounded_authority, bounded_operations)
    intake = {
        "schema": "stacks-canon-errata-intake/v1",
        "recorded_at_utc": GENERATED_AT,
        "candidate_id": spec["candidate_id"],
        "authority": {
            "path": "authority/source/simplicial.tex",
            "commit": spec["authority_commit"],
            "tree": spec["authority_tree"],
            "bytes": len(authority),
            "physical_lines": authority.count(b"\n"),
            "sha256": AUTHORITY_SHA256,
            "line_endings": "LF-only with terminal LF",
            "mutated": False,
        },
        "allegation_locator_policy": {
            "shared_producer_ledger": "used only to locate bounded allegations",
            "producer_source_emendations_json": "pinned as bounded allegation evidence only; every row independently replayed against frozen authority",
            "adjudication_authorities": [
                "frozen simplicial.tex bytes",
                "the pinned Stacks definitions and proofs",
                "all twenty admitted overlay source maps and rejection ledgers",
            ],
        },
        "allegation_locators": [
            {"producer_id": row["producer_id"], "locus": row["locus"], "class": row["class"]}
            for row in sorted(accepted + rejected, key=lambda item: item["producer_id"])
        ],
        "bounded_source": {
            "start_line": bounded_start_line,
            "end_line": bounded_end_line,
            "physical_lines": bounded_authority.count(b"\n"),
            "bytes": len(bounded_authority),
            "sha256": sha_bytes(bounded_authority),
        },
        "corrected_bounded_replay": {
            "physical_lines": bounded_payload.count(b"\n"),
            "bytes": len(bounded_payload),
            "sha256": sha_bytes(bounded_payload),
            "old_spans_unique_in_declared_lines": True,
            "operations_nonoverlapping": True,
        },
        "closure": {
            "producer_rows": len(expected_producers),
            "accepted": len(accepted),
            "rejected": len(rejected),
            "rejected_duplicate": 0,
            "operations": len(operations),
            "unresolved": 0,
            "stable_ids": "MC-STK-ERR-0904..MC-STK-ERR-0914",
        },
        "deduplication": {
            "registered_entries_checked": 20,
            "public_candidates_checked": "R1..R20",
            "duplicate_aliases": {},
            "accepted_overlap": False,
        },
        "adjudication": {
            row["producer_id"]: row["result"] for row in accepted + rejected
        },
        "write_boundaries": {
            "english_authority": "immutable",
            "canonical_translations": "immutable",
            "payload_derivation": "directly from frozen authority, never a prior payload",
            "producer_emendation_manifest": "bounded snapshot retained as evidence; independently adjudicated rather than treated as canon",
        },
    }
    write_json(ROOT / "authority" / "canon" / "R21_SIMPLICIAL_001_011_INTAKE.json", intake)

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
            "id": unit["stable_id"],
            "producer_id": unit["producer_id"],
            "class": unit["class"],
            "source": "simplicial.tex",
            "locus": unit["locus"],
            "payload": "payload/simplicial.tex",
            "operation_ids": [row["operation_id"] for row in map_ops],
            "status": "applied",
        })
        source_rows.append({
            "schema": "mathematics-commons-stacks-errata-map/v2",
            "unit_id": unit["stable_id"],
            "producer_id": unit["producer_id"],
            "source": "simplicial.tex",
            "authority": "authority/source/simplicial.tex",
            "authority_sha256": AUTHORITY_SHA256,
            "payload": "payload/simplicial.tex",
            "locus": unit["locus"],
            "class": unit["class"],
            "proof": f"Independent canon replay: {unit['result']}. {unit['disposition']}",
            "adverse_evidence": "The frozen source and admitted overlay evidence are retained; no translation byte, prior payload, or mutable upstream file was used as correction authority.",
            "operations": map_ops,
        })
        has_tex = any(
            "$" in row["old_text"] or "\\" in row["old_text"]
            or "$" in row["replacement_text"] or "\\" in row["replacement_text"]
            for row in unit_ops
        )
        (formula_units if has_tex else prose_units).append(unit["stable_id"])

    write_json(ROOT / "stable-units.json", {
        "schema": "mathematics-commons-stacks-errata-units/v1",
        "authority_commit": spec["authority_commit"],
        "unit_count": len(stable_units),
        "units": stable_units,
    })
    (ROOT / "source-map.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in source_rows),
        encoding="utf-8",
        newline="",
    )
    write_json(ROOT / "operation-spec.json", {
        "schema": "mathematics-commons-stacks-errata-operation-spec/v1",
        "authority_sha256": AUTHORITY_SHA256,
        "operation_count": len(operations),
        "apply_order": "descending_start_byte",
        "operations": operations,
    })
    write_json(ROOT / "formula-diagram-inventory.json", {
        "schema": "mathematics-commons-stacks-errata-formula-diagram-inventory/v1",
        "candidate_id": spec["candidate_id"],
        "unit_count": len(stable_units),
        "formula_units": formula_units,
        "diagram_units": [],
        "prose_only_units": prose_units,
        "classification": "Every accepted unit is classified exactly once; no xymatrix span changes.",
        "unmapped_formula_or_diagram_changes": 0,
    })

    decisions = [
        ("ERR-R21-D0001", "Bind R21 exclusively to the active errata/r21 lease and frozen upstream commit/tree.", "Preserves the single-writer and immutable-authority boundary."),
        ("ERR-R21-D0002", "Assign MC-STK-ERR-0904..0914 to ten accepted SIMPLICIAL producer units and one canon-origin unit after frozen R20.", "Creates a deterministic contiguous stable-ID sequence for eleven proved nonduplicate corrections; the rejected SIMPLICIAL-007 allegation consumes no ID."),
        ("ERR-R21-D0003", "Apply only exact nonoverlapping half-open UTF-8 spans in descending byte order.", "Prevents contextual or global replacement from changing unrelated source text."),
        ("ERR-R21-D0004", "Accept SIMPLICIAL-001..006, SIMPLICIAL-008..011, and CANON-SIMPLICIAL-001; reject SIMPLICIAL-007 after independent source replay and deduplication against R1-R20.", "The accepted units are distinct bounded defects. SIMPLICIAL-007 would delete the parenthesis closing the outer Mor call and is therefore not a defect."),
        ("ERR-R21-D0005", "Freeze R21 at eleven units, eleven operations, and one rejected allegation.", "Prevents later producer or canon growth from moving this round underneath its hashes."),
        ("ERR-R21-D0006", "Use producer evidence only as a bounded allegation packet, not as correction authority.", "Frozen source, independent exact-preimage replay, mathematical typing, and admitted-history deduplication bind the overlay."),
        ("ERR-R21-D0007", "Admit CANON-SIMPLICIAL-001 as a separately attributed canon-origin unit.", "The defect was discovered independently and is mathematically distinct from the producer line-277 allegation."),
        ("ERR-R21-D0008", "Keep canonical locale bytes and the literal upstream mirror outside the corrected English payload.", "Corrections belong only to the Unofficial AI-Integrated Stacks Project."),
        ("ERR-R21-D0009", "Do not contact or submit this AI-derived correction set to upstream Stacks maintainers.", "The maintained AI-open English edition is the authorized correction surface."),
    ]
    (ROOT / "decisions.jsonl").write_text(
        "".join(json.dumps({
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": row[0],
            "timestamp_utc": GENERATED_AT,
            "choice": row[1],
            "rationale": row[2],
            "supersedes": None,
        }, ensure_ascii=False, separators=(",", ":")) + "\n" for row in decisions),
        encoding="utf-8",
        newline="",
    )
    (ROOT / "rejections.jsonl").write_text(
        "".join(json.dumps({
            "schema": "mathematics-commons-stacks-candidate-rejection/v1",
            "id": f"ERR-R21-R{index:04d}",
            "timestamp_utc": GENERATED_AT,
            "producer_id": row["producer_id"],
            "class": row["class"],
            "result": row["result"],
            "disposition": "rejected",
            "reason": row["reason"],
        }, ensure_ascii=False, separators=(",", ":")) + "\n" for index, row in enumerate(rejected, 1)),
        encoding="utf-8",
        newline="",
    )

    authority_evidence = [
        artifact(path, path.relative_to(ROOT).as_posix())
        for path in sorted((ROOT / "authority").rglob("*")) if path.is_file()
    ]
    config = {
        "schema": "mathematics-commons-stacks-errata-candidate-config/v1",
        "candidate_id": spec["candidate_id"],
        "lease_id": "stacks-lease-000024-errata-r21",
        "writer_task": "01a0256d-5693-77c1-96b2-cf37101e0c6c",
        "authority_commit": spec["authority_commit"],
        "authority_tree": spec["authority_tree"],
        "source_date_epoch": "1785274200",
        "expected_unit_ids": expected_ids,
        "expected_producer_ids": expected_producers,
        "namespace": "commons/stacks/errata/r21",
        "private_render_logical_path": "canon/private_evidence/errata-r21-20260825T2045Z/render-final/render-manifest.json",
        "operation_count": len(operations),
        "visual_qa": {
            "high_resolution_pages": {"simplicial": [5, 6, 7, 14, 18, 24, 28]},
            "correction_sensitive_pages": {"simplicial": [5, 6, 7, 14, 18, 24, 28]},
        },
        "stems": {
            "simplicial": {
                "authority_sha256": AUTHORITY_SHA256,
                "payload_sha256": sha_bytes(payload),
                "authority_bytes": len(authority),
                "payload_bytes": len(payload),
                "display_delimiter_delta": 0,
                "ordered_structure_exceptions": {},
                "build_exceptions": {
                    "candidate_page_delta": 0,
                },
            }
        },
        "authority_evidence": authority_evidence,
        "proof_closure": {
            "producer_rows": len(expected_producers),
            "accepted": len(accepted),
            "operations": len(operations),
            "rejected": len(rejected),
            "prior_overlay_aliases": 0,
            "packet_duplicates": 0,
            "unresolved": 0,
        },
    }
    write_json(ROOT / "candidate.config.json", config)
    print(json.dumps({
        "passed": True,
        "units": len(accepted),
        "rejections": len(rejected),
        "operations": len(operations),
        "payload_bytes": len(payload),
        "payload_sha256": sha_bytes(payload),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
