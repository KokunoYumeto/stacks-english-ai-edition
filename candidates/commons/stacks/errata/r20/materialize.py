from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
AUTHORITY_SHA256 = "EFDA4CB361DD40909D1991161EAE716E58B6CF9E79380971502E1DA12396D402"
AUTHORITY_BYTES = 449_677
UPSTREAM_LOCK_SHA256 = "B195ECC83AB0F32C574A60D1FDBA9B0DA4D35B04E0DF7CB106DC9C0FDAD99C0D"
COPYING_SHA256 = "4B2C8FC390F802CD92F0622DC00A708A588BEC54D0145D2EE135D6D7672BFE85"
GENERATED_AT = "2026-08-25T16:00:00Z"
SPEC_PATH = ROOT / "authority" / "canon" / "R20_DERIVED_064_092_ADJUDICATION_SPEC.json"
SPEC_SHA256 = "A7C506D7C84BA31D952816F769EF8C7CA54A3C21E6BBD305DDC411334B0697CC"
REVIEW_PATH = ROOT / "authority" / "canon" / "R20_DERIVED_064_092_REVIEW.md"
REVIEW_SHA256 = "AC3E97546924957EF884A420A224E85BD2EB02B6F46C8B6773ABF083BAD15C41"
EXPECTED_PAYLOAD_BYTES = 449_730
EXPECTED_PAYLOAD_SHA256 = "FEEC32EEEEAF1194899A877208077EF7721B53D937048209FEEC4B9B75E376CD"


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
        spec["candidate_id"] != "stacks-errata-a04446e-r20"
        or spec["authority_sha256"] != AUTHORITY_SHA256
        or spec["authority_commit"] != "a04446e57ec1fbc252a871afcec7752fb2807b14"
        or spec["authority_tree"] != "3feeb703b931a6e7259782c10e7d1575adc83e5e"
    ):
        raise AssertionError("adjudication specification authority binding mismatch")
    accepted = spec["accepted"]
    rejected = spec["rejected"]
    expected_producers = [f"DERIVED-{number:03d}" for number in range(64, 93)]
    accepted_producers = [row["producer_id"] for row in accepted]
    rejected_producers = [row["producer_id"] for row in rejected]
    if sorted(accepted_producers + rejected_producers) != expected_producers:
        raise AssertionError("adjudication partition is not DERIVED-064..092")
    expected_ids = [f"MC-STK-ERR-{number:04d}" for number in range(875, 904)]
    if [row["stable_id"] for row in accepted] != expected_ids:
        raise AssertionError("stable-ID assignment is not contiguous 0875..0903")
    if rejected_producers:
        raise AssertionError("R20 has no rejected producer rows")

    generated = [
        ROOT / "authority" / "source" / "derived.tex",
        ROOT / "authority" / "upstream.lock.json",
        ROOT / "authority" / "COPYING",
        ROOT / "authority" / "canon" / "R20_DERIVED_064_092_INTAKE.json",
        ROOT / "payload" / "derived.tex",
        ROOT / "candidate.config.json",
        ROOT / "stable-units.json",
        ROOT / "source-map.jsonl",
        ROOT / "decisions.jsonl",
        ROOT / "rejections.jsonl",
        ROOT / "formula-diagram-inventory.json",
        ROOT / "operation-spec.json",
    ]
    if any(path.exists() for path in generated):
        raise FileExistsError("candidate material already exists; materializer refuses to overwrite")

    operations = map_operations(authority, accepted)
    if len(accepted) != 29 or len(operations) != 32:
        raise AssertionError("R20 count contract mismatch")
    payload = apply_operations(authority, operations)
    if len(payload) != EXPECTED_PAYLOAD_BYTES or sha_bytes(payload) != EXPECTED_PAYLOAD_SHA256:
        raise AssertionError("R20 deterministic payload identity mismatch")
    ops_by_producer: dict[str, list[dict]] = {}
    for row in operations:
        ops_by_producer.setdefault(row["producer_id"], []).append(row)

    authority_source = ROOT / "authority" / "source" / "derived.tex"
    payload_path = ROOT / "payload" / "derived.tex"
    authority_source.parent.mkdir(parents=True, exist_ok=True)
    payload_path.parent.mkdir(parents=True, exist_ok=True)
    authority_source.write_bytes(authority)
    payload_path.write_bytes(payload)
    shutil.copy2(args.upstream_lock, ROOT / "authority" / "upstream.lock.json")
    shutil.copy2(args.copying, ROOT / "authority" / "COPYING")

    offsets = line_offsets(authority)
    bounded_start_line = 8739
    bounded_end_line = 12560
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
        raise AssertionError("an R20 operation lies outside the declared bounded source")
    bounded_payload = apply_operations(bounded_authority, bounded_operations)
    intake = {
        "schema": "stacks-canon-errata-intake/v1",
        "recorded_at_utc": GENERATED_AT,
        "candidate_id": spec["candidate_id"],
        "authority": {
            "path": "authority/source/derived.tex",
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
                "frozen derived.tex bytes",
                "the pinned Stacks definitions and proofs",
                "all eighteen admitted overlay source maps and rejection ledgers",
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
            "rejected": 0,
            "rejected_duplicate": 0,
            "operations": len(operations),
            "unresolved": 0,
            "stable_ids": "MC-STK-ERR-0875..MC-STK-ERR-0903",
        },
        "deduplication": {
            "registered_entries_checked": 19,
            "public_candidates_checked": "R1..R19",
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
    write_json(ROOT / "authority" / "canon" / "R20_DERIVED_064_092_INTAKE.json", intake)

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
            "source": "derived.tex",
            "locus": unit["locus"],
            "payload": "payload/derived.tex",
            "operation_ids": [row["operation_id"] for row in map_ops],
            "status": "applied",
        })
        source_rows.append({
            "schema": "mathematics-commons-stacks-errata-map/v2",
            "unit_id": unit["stable_id"],
            "producer_id": unit["producer_id"],
            "source": "derived.tex",
            "authority": "authority/source/derived.tex",
            "authority_sha256": AUTHORITY_SHA256,
            "payload": "payload/derived.tex",
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
        ("ERR-R20-D0001", "Bind R20 exclusively to the active errata/r20 lease and frozen upstream commit/tree.", "Preserves the single-writer and immutable-authority boundary."),
        ("ERR-R20-D0002", "Assign MC-STK-ERR-0875..0903 in accepted DERIVED producer order after frozen R19.", "Creates a deterministic contiguous stable-ID sequence for 29 proved nonduplicate corrections."),
        ("ERR-R20-D0003", "Apply only exact nonoverlapping half-open UTF-8 spans in descending byte order.", "Prevents contextual or global replacement from changing unrelated source text."),
        ("ERR-R20-D0004", "Accept DERIVED-064..092 after independent source replay and deduplication against R1-R19.", "Each allegation is a distinct bounded defect proved directly from frozen derived.tex and surrounding project definitions."),
        ("ERR-R20-D0005", "Freeze R20 at 29 units and 32 operations, DERIVED-064..092.", "Prevents later producer growth beginning at DERIVED-093 from moving this round underneath its hashes."),
        ("ERR-R20-D0006", "Use producer evidence only as a bounded allegation packet, not as correction authority.", "Frozen source, independent exact-preimage replay, mathematical typing, and admitted-history deduplication bind the overlay."),
        ("ERR-R20-D0007", "Admit the canon style amendment for DERIVED-071.", "The conditioned product index uses surrounding Stacks spacing while preserving the corrected mathematics."),
        ("ERR-R20-D0008", "Keep canonical locale bytes and the literal upstream mirror outside the corrected English payload.", "Corrections belong only to the Unofficial AI-Integrated Stacks Project."),
        ("ERR-R20-D0009", "Do not contact or submit this AI-derived correction set to upstream Stacks maintainers.", "The maintained AI-open English edition is the authorized correction surface."),
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
            "id": f"ERR-R20-R{index:04d}",
            "timestamp_utc": GENERATED_AT,
            "producer_id": row["producer_id"],
            "disposition": "rejected_duplicate",
            "reason": f"{row['reason']} Alias: {row['alias_of']}; admitted round: {row['round']}.",
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
        "lease_id": "stacks-lease-000023-errata-r20",
        "writer_task": "01a0256d-5693-77c1-96b2-cf37101e0c6c",
        "authority_commit": spec["authority_commit"],
        "authority_tree": spec["authority_tree"],
        "source_date_epoch": "1785274200",
        "expected_unit_ids": expected_ids,
        "expected_producer_ids": expected_producers,
        "namespace": "commons/stacks/errata/r20",
        "private_render_logical_path": "canon/private_evidence/errata-r20-20260825T1600Z/render-final/render-manifest.json",
        "operation_count": len(operations),
        "visual_qa": {
            "high_resolution_pages": {"derived": list(range(1, 130))},
            "correction_sensitive_pages": {"derived": list(range(1, 130))},
        },
        "stems": {
            "derived": {
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
        "duplicate_rejections": len(rejected),
        "operations": len(operations),
        "payload_bytes": len(payload),
        "payload_sha256": sha_bytes(payload),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
