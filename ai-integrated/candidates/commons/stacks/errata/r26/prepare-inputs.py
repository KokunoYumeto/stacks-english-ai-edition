from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
GENERATED_AT = "2026-08-28T10:45:00Z"
AUTHORITY_COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
AUTHORITY_TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
AUTHORITY_PATH = "smoothing.tex"
AUTHORITY_BYTES = 134660
AUTHORITY_SHA256 = "FD28CF874BB7DAD3C5C5FF03314D1C83701613A8A98730A99B9CA7A4BCFE6068"
PRODUCER_LEDGER_BYTES = 13069
PRODUCER_LEDGER_SHA256 = "7E8204DF53B8D8704400149E38DB2C263103956A9AA7F5E9797081EA1A8E2A9E"
PRODUCER_EMENDATIONS_BYTES = 14346
PRODUCER_EMENDATIONS_SHA256 = "992AC09EF5F3F344739390F7369984A894171C12F0218611F616E2B292C8E398"
REJECTED_IDS = ["SMOOTHING-010"]
DUPLICATE_ALIASES = {
    "SMOOTHING-002": "MC-STK-ERR-0002",
    "SMOOTHING-003": "MC-STK-ERR-0005",
    "SMOOTHING-004": "MC-STK-ERR-0006",
}
MERGE_GROUPS = [
    ["SMOOTHING-005", "SMOOTHING-031"],
    ["SMOOTHING-008", "SMOOTHING-012", "SMOOTHING-013", "SMOOTHING-014"],
    ["SMOOTHING-016", "SMOOTHING-018"],
    ["SMOOTHING-017", "SMOOTHING-019"],
]
EXPECTED_PRODUCER_IDS = [f"SMOOTHING-{number:03d}" for number in range(1, 36)]
EXPECTED_IDS = [f"MC-STK-ERR-{number:04d}" for number in range(1177, 1202)]


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="",
    )


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n"
            for row in rows
        ),
        encoding="utf-8",
        newline="",
    )


def base_id(operation_id: str) -> str:
    match = re.fullmatch(r"(SMOOTHING-\d{3})(?:[A-Z])?", operation_id)
    if not match:
        raise AssertionError(f"invalid producer emendation ID: {operation_id}")
    return match.group(1)


def bounded_offset(authority: bytes, operation: dict) -> tuple[int, int, int, int]:
    start_line = operation["source_start_line"]
    end_line = operation["source_end_line"]
    starts = [0]
    starts.extend(index + 1 for index, byte in enumerate(authority) if byte == 10)
    region_start = starts[start_line - 1]
    region_end = starts[end_line] if end_line < len(starts) else len(authority)
    old = operation["old_text"].encode("utf-8")
    region = authority[region_start:region_end]
    positions: list[int] = []
    cursor = 0
    while True:
        position = region.find(old, cursor)
        if position < 0:
            break
        positions.append(position)
        cursor = position + 1
    if len(positions) != 1:
        raise AssertionError(
            f"{operation['producer_id']}: preimage count on lines {start_line}-{end_line} "
            f"is {len(positions)} for {operation['old_text']!r}"
        )
    start = region_start + positions[0]
    end = start + len(old)
    actual_start_line = authority[:start].count(b"\n") + 1
    actual_end_line = authority[: max(start, end - 1)].count(b"\n") + 1
    return start, end, actual_start_line, actual_end_line


def canonical_operations(producer: dict) -> dict[str, list[dict]]:
    operations: dict[str, list[dict]] = {}
    for row in producer["emendations"]:
        producer_id = base_id(row["id"])
        if producer_id in REJECTED_IDS or producer_id in DUPLICATE_ALIASES:
            continue
        operation = {
            "producer_id": producer_id,
            "producer_operation_id": row["id"],
            "source_start_line": int(row["line"]),
            "source_end_line": int(row["line"]),
            "old_text": row["old"],
            "replacement_text": row["new"],
        }
        operations.setdefault(producer_id, []).append(operation)

    # Independent authority review refines two malformed solution clauses.
    for producer_id, line, field, terminator in (
        ("SMOOTHING-017", 3191, "R", "."),
        ("SMOOTHING-019", 3270, "R'", ""),
    ):
        operations[producer_id] = [{
            "producer_id": producer_id,
            "producer_operation_id": producer_id,
            "source_start_line": line,
            "source_end_line": line,
            "old_text": f"Suppose that we can show that $g_j$ as a solution $(b_{{i, l}})$ in ${field}${terminator}",
            "replacement_text": (
                "Suppose that we can show that the system of equations $g_j = 0$ "
                f"has a solution $(b_{{i, l}})$ in ${field}${terminator}"
            ),
        }]

    # The current proof does not bind \kappa; name its explicit base field.
    operations["SMOOTHING-023"][0]["replacement_text"] = "over $R/\\pi R$"

    # Independent review found the same ill-typed B-prime at the next use.
    operations["SMOOTHING-022"].append({
        "producer_id": "SMOOTHING-022",
        "producer_operation_id": "SMOOTHING-022B",
        "source_start_line": 1170,
        "source_end_line": 1170,
        "old_text": "$g_j \\in \\mathfrak p^2$",
        "replacement_text": "$g_j \\in \\mathfrak p_B^2$",
    })
    return operations


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare deterministic R26 Smoothing source-intake inputs.")
    parser.add_argument("--authority", type=Path, required=True)
    parser.add_argument("--producer-ledger", type=Path, required=True)
    parser.add_argument("--producer-emendations", type=Path, required=True)
    args = parser.parse_args()

    authority = args.authority.read_bytes()
    ledger_bytes = args.producer_ledger.read_bytes()
    emendation_bytes = args.producer_emendations.read_bytes()
    if len(authority) != AUTHORITY_BYTES or sha_bytes(authority) != AUTHORITY_SHA256:
        raise AssertionError("frozen smoothing.tex authority mismatch")
    if b"\r" in authority or not authority.endswith(b"\n"):
        raise AssertionError("authority must be LF-only UTF-8 with terminal LF")
    if len(ledger_bytes) != PRODUCER_LEDGER_BYTES or sha_bytes(ledger_bytes) != PRODUCER_LEDGER_SHA256:
        raise AssertionError("frozen Smoothing producer ledger mismatch")
    if (
        len(emendation_bytes) != PRODUCER_EMENDATIONS_BYTES
        or sha_bytes(emendation_bytes) != PRODUCER_EMENDATIONS_SHA256
    ):
        raise AssertionError("frozen Smoothing producer emendations mismatch")

    producer_rows = list(csv.DictReader(ledger_bytes.decode("utf-8-sig").splitlines()))
    if [row["id"] for row in producer_rows] != EXPECTED_PRODUCER_IDS:
        raise AssertionError("producer packet is not exact contiguous SMOOTHING-001..035")
    if any(row["authority_sha256"] != AUTHORITY_SHA256 for row in producer_rows):
        raise AssertionError("producer source identity mismatch")
    producer = json.loads(emendation_bytes.decode("utf-8"))
    if (
        producer.get("authority_bytes") != AUTHORITY_BYTES
        or producer.get("authority_sha256") != AUTHORITY_SHA256
        or producer.get("emendation_count") != 42
        or len(producer.get("emendations", [])) != 42
    ):
        raise AssertionError("producer emendation declaration closure mismatch")
    sanitized_producer = dict(producer)
    sanitized_producer["authority_path"] = "smoothing.tex"
    sanitized_emendation_bytes = (
        json.dumps(sanitized_producer, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")

    operations_by_producer = canonical_operations(producer)
    accepted_ids = [
        producer_id
        for producer_id in EXPECTED_PRODUCER_IDS
        if producer_id not in REJECTED_IDS and producer_id not in DUPLICATE_ALIASES
    ]
    if set(operations_by_producer) != set(accepted_ids):
        raise AssertionError("accepted producer-operation closure mismatch")
    if sum(map(len, operations_by_producer.values())) != 39:
        raise AssertionError("expected 39 independently adjudicated operations")

    merged_members = {member for group in MERGE_GROUPS for member in group}
    groups: list[list[str]] = []
    for producer_id in accepted_ids:
        if producer_id in merged_members:
            group = next(group for group in MERGE_GROUPS if producer_id in group)
            if group not in groups:
                groups.append(group)
        else:
            groups.append([producer_id])

    def first_line(group: list[str]) -> int:
        return min(
            operation["source_start_line"]
            for producer_id in group
            for operation in operations_by_producer[producer_id]
        )

    groups.sort(key=lambda group: (first_line(group), group[0]))
    if len(groups) != 25:
        raise AssertionError(f"expected 25 semantic units, observed {len(groups)}")

    row_by_id = {row["id"]: row for row in producer_rows}
    accepted: list[dict] = []
    operation_spec_rows: list[dict] = []
    source_map_rows: list[dict] = []
    stable_rows: list[dict] = []
    all_intervals: list[tuple[int, int, str]] = []
    for stable_id, producer_ids in zip(EXPECTED_IDS, groups):
        flat_operations = [
            operation
            for producer_id in producer_ids
            for operation in operations_by_producer[producer_id]
        ]
        mapped_operations: list[dict] = []
        for operation_index, operation in enumerate(flat_operations, 1):
            start, end, actual_start_line, actual_end_line = bounded_offset(authority, operation)
            if (actual_start_line, actual_end_line) != (
                operation["source_start_line"], operation["source_end_line"]
            ):
                raise AssertionError(f"{operation['producer_id']}: exact line metadata mismatch")
            old = operation["old_text"].encode("utf-8")
            replacement = operation["replacement_text"].encode("utf-8")
            operation_id = f"{stable_id}-OP{operation_index}"
            mapped = {
                **operation,
                "operation_id": operation_id,
                "start_byte": start,
                "end_byte_exclusive": end,
                "occurrence_count_in_frozen_authority": authority.count(old),
                "old_bytes": len(old),
                "old_sha256": sha_bytes(old),
                "replacement_bytes": len(replacement),
                "replacement_sha256": sha_bytes(replacement),
            }
            mapped_operations.append(mapped)
            operation_spec_rows.append({
                "stable_id": stable_id,
                "semantic_unit_producer_id": producer_ids[0],
                "operation_index": operation_index,
                **mapped,
            })
            all_intervals.append((start, end, operation_id))

        loci = sorted({
            line
            for operation in flat_operations
            for line in (operation["source_start_line"], operation["source_end_line"])
        })
        locus = f"smoothing.tex:{loci[0]}" if loci[0] == loci[-1] else f"smoothing.tex:{loci[0]}-{loci[-1]}"
        rationale = " ".join(row_by_id[producer_id]["observation"] for producer_id in producer_ids)
        unit = {
            "stable_id": stable_id,
            "producer_ids": producer_ids,
            "class": "source_defect_correction",
            "locus": locus,
            "operations": flat_operations,
            "rationale": rationale,
        }
        accepted.append(unit)
        operation_ids = [operation["operation_id"] for operation in mapped_operations]
        stable_rows.append({
            "class": unit["class"],
            "id": stable_id,
            "locus": locus,
            "operation_ids": operation_ids,
            "payload": "payload/smoothing.tex",
            "producer_id": producer_ids[0],
            "producer_ids": producer_ids,
            "source": "smoothing.tex",
            "status": "provisional_accepted_not_admitted",
        })
        source_map_rows.append({
            "schema": "mathematics-commons-stacks-errata-map/v2",
            "unit_id": stable_id,
            "producer_id": producer_ids[0],
            "producer_ids": producer_ids,
            "source": "smoothing.tex",
            "authority": "authority/source/smoothing.tex",
            "authority_sha256": AUTHORITY_SHA256,
            "payload": "payload/smoothing.tex",
            "locus": locus,
            "class": unit["class"],
            "proof": "accepted_after_independent_frozen_authority_replay",
            "prior_aliases": [],
            "adverse_evidence": "Producer rows are allegation evidence only; frozen authority, bounded preimages, and independent adjudication control.",
            "operations": mapped_operations,
        })

    ascending = sorted(all_intervals)
    for left, right in zip(ascending, ascending[1:]):
        if left[1] > right[0]:
            raise AssertionError(f"overlapping operations: {left[2]} / {right[2]}")
    first_offsets = [min(operation["start_byte"] for operation in row["operations"]) for row in source_map_rows]
    if first_offsets != sorted(first_offsets):
        raise AssertionError("stable units do not follow first physical source locus")

    operation_by_id = {row["operation_id"]: row for row in operation_spec_rows}
    payload = authority
    for start, end, operation_id in sorted(all_intervals, reverse=True):
        operation = operation_by_id[operation_id]
        old = operation["old_text"].encode("utf-8")
        replacement = operation["replacement_text"].encode("utf-8")
        if payload[start:end] != old:
            raise AssertionError(f"descending replay mismatch: {operation_id}")
        payload = payload[:start] + replacement + payload[end:]

    rejected_proposal = {
        "producer_id": "SMOOTHING-010",
        "source_start_line": 2958,
        "source_end_line": 2958,
        "old_text": "this trivial",
        "replacement_text": "this is trivial",
    }
    start, end, _, _ = bounded_offset(authority, rejected_proposal)
    old = rejected_proposal["old_text"].encode("utf-8")
    replacement = rejected_proposal["replacement_text"].encode("utf-8")
    rejected_rows = [{
        "schema": "mathematics-commons-stacks-errata-rejection/v1",
        "producer_id": "SMOOTHING-010",
        "producer_ids": ["SMOOTHING-010"],
        "source": "smoothing.tex",
        "locus": "smoothing.tex:2958-2959",
        "class": "grammatical_original_not_source_defect",
        "result": "rejected_after_independent_authority_review",
        "rationale": "The noun phrase 'this trivial but key observation' is the grammatical subject of 'will ensure'; adding 'is' would make the sentence malformed.",
        "prior_aliases": [],
        "proposed_operation": {
            "source_start_line": 2958,
            "source_end_line": 2958,
            "old_text": rejected_proposal["old_text"],
            "replacement_text": rejected_proposal["replacement_text"],
            "start_byte": start,
            "end_byte_exclusive": end,
            "old_bytes": len(old),
            "old_sha256": sha_bytes(old),
            "replacement_bytes": len(replacement),
            "replacement_sha256": sha_bytes(replacement),
            "applied": False,
        },
    }]

    spec = {
        "schema": "mathematics-commons-stacks-r26-adjudication-spec/v1",
        "candidate_id": "stacks-errata-a04446e-r26",
        "authority_commit": AUTHORITY_COMMIT,
        "authority_tree": AUTHORITY_TREE,
        "authority_path": AUTHORITY_PATH,
        "authority_bytes": len(authority),
        "authority_sha256": sha_bytes(authority),
        "producer_sources": [
            "SMOOTHING_SOURCE_DEFECT_LEDGER.input.csv",
            "SMOOTHING_SOURCE_EMENDATIONS.input.json",
        ],
        "producer_ledger_bytes": len(ledger_bytes),
        "producer_ledger_sha256": sha_bytes(ledger_bytes),
        "producer_emendations_bytes": len(emendation_bytes),
        "producer_emendations_sha256": sha_bytes(emendation_bytes),
        "producer_emendations_sanitized_bytes": len(sanitized_emendation_bytes),
        "producer_emendations_sanitized_sha256": sha_bytes(sanitized_emendation_bytes),
        "producer_row_count": 35,
        "accepted_producer_row_count": 31,
        "rejected_producer_row_count": 1,
        "prior_alias_producer_row_count": 3,
        "semantic_unit_count": len(accepted),
        "operation_count": len(operation_spec_rows),
        "stable_id_range": [EXPECTED_IDS[0], EXPECTED_IDS[-1]],
        "deduplication": {
            "admitted_units_reviewed": 809,
            "prior_rounds": "root/R1 and R2-R25",
            "prior_smoothing_units_reviewed": 5,
            "matching_smoothing_units": 3,
            "result": "accepted_units_new; three exact R1 duplicates aliased; one grammatical false positive rejected",
        },
        "prior_aliases": [
            {
                "producer_id": producer_id,
                "stable_id": stable_id,
                "result": "exact_duplicate_of_admitted_r1_unit",
            }
            for producer_id, stable_id in DUPLICATE_ALIASES.items()
        ],
        "accepted": accepted,
        "rejected": rejected_rows,
        "unresolved": [],
    }
    spec_path = ROOT / "R26_SMOOTHING_ADJUDICATION_SPEC.input.json"
    write_json(spec_path, spec)
    spec_bytes = spec_path.read_bytes()

    lease = json.loads((ROOT / "LEASE.json").read_text(encoding="utf-8"))
    flattened_producers = [producer_id for unit in accepted for producer_id in unit["producer_ids"]]
    config_input = {
        "schema": "mathematics-commons-stacks-errata-candidate-config-input/v1",
        "candidate_id": spec["candidate_id"],
        "authority_commit": AUTHORITY_COMMIT,
        "authority_tree": AUTHORITY_TREE,
        "namespace": lease["namespace"],
        "writer_task": lease["writer_task"],
        "lease_id": lease["lease_id"],
        "accepted": 25,
        "rejected": 1,
        "unresolved": 0,
        "operation_count": len(operation_spec_rows),
        "expected_unit_ids": EXPECTED_IDS,
        "expected_producer_ids": [unit["producer_ids"][0] for unit in accepted],
        "expected_all_producer_ids": flattened_producers,
        "rejected_producer_ids": REJECTED_IDS,
        "prior_alias_producer_ids": list(DUPLICATE_ALIASES),
        "intentionally_absent_producer_ids": [],
        "payload_expected_bytes": len(payload),
        "payload_expected_sha256": sha_bytes(payload),
        "build_render_admission_status": "not_run_by_source_materialization",
    }
    operation_spec = {
        "schema": "mathematics-commons-stacks-errata-operation-spec/v1",
        "authority_sha256": AUTHORITY_SHA256,
        "operations": operation_spec_rows,
    }
    stable_units = {
        "schema": "mathematics-commons-stacks-errata-units/v1",
        "authority_commit": AUTHORITY_COMMIT,
        "unit_count": len(stable_rows),
        "units": stable_rows,
    }
    decisions = [
        {"schema":"mathematics-commons-stacks-candidate-decision/v1","id":"ERR-R26-D0001","timestamp_utc":GENERATED_AT,"choice":"Bind R26 to frozen smoothing.tex at commit a04446e57ec1fbc252a871afcec7752fb2807b14 without changing R25.","rationale":"Preserves immutable authority and the completed MC-STK-ERR-1046..1176 assignment.","supersedes":None},
        {"schema":"mathematics-commons-stacks-candidate-decision/v1","id":"ERR-R26-D0002","timestamp_utc":GENERATED_AT,"choice":"Assign MC-STK-ERR-1177..1201 to 25 accepted semantic units in first-locus physical source order.","rationale":"The range begins immediately after R25 and contains no reused or skipped stable ID.","supersedes":None},
        {"schema":"mathematics-commons-stacks-candidate-decision/v1","id":"ERR-R26-D0003","timestamp_utc":GENERATED_AT,"choice":"Merge four repeated producer groups and retain every physical operation under the resulting stable unit.","rationale":"Each group is a cloned or repeated instance of one bounded semantic defect.","supersedes":None},
        {"schema":"mathematics-commons-stacks-candidate-decision/v1","id":"ERR-R26-D0004","timestamp_utc":GENERATED_AT,"choice":"Accept 31 new producer identities, bind SMOOTHING-002/003/004 as exact R1 aliases, reject SMOOTHING-010, and leave none unresolved.","rationale":"The three aliases already exist as MC-STK-ERR-0002/0005/0006; the rejected wording is grammatical and its proposed insertion would be malformed.","supersedes":None},
        {"schema":"mathematics-commons-stacks-candidate-decision/v1","id":"ERR-R26-D0005","timestamp_utc":GENERATED_AT,"choice":"Refine the two malformed solution clauses, name R/pi R explicitly, and add the independently found p_B occurrence at line 1170.","rationale":"These exact bounded operations preserve typing and make the intended mathematics explicit without broad rewriting.","supersedes":None},
        {"schema":"mathematics-commons-stacks-candidate-decision/v1","id":"ERR-R26-D0006","timestamp_utc":GENERATED_AT,"choice":"Materialize and replay the source candidate before build, render, admission, registry, and publication transitions.","rationale":"Maintains a deterministic finite gate sequence.","supersedes":None},
    ]
    validation = {
        "schema": "mathematics-commons-stacks-r26-intake-validation/v1",
        "status": "PASS",
        "authority_bytes": len(authority),
        "authority_sha256": sha_bytes(authority),
        "producer_ledger_bytes": len(ledger_bytes),
        "producer_ledger_sha256": sha_bytes(ledger_bytes),
        "producer_emendations_bytes": len(emendation_bytes),
        "producer_emendations_sha256": sha_bytes(emendation_bytes),
        "adjudication_spec_bytes": len(spec_bytes),
        "adjudication_spec_sha256": sha_bytes(spec_bytes),
        "semantic_units": len(stable_rows),
        "operations": len(operation_spec_rows),
        "accepted_producer_ids": len(flattened_producers),
        "rejected_producer_ids": len(REJECTED_IDS),
        "prior_alias_producer_ids": len(DUPLICATE_ALIASES),
        "unresolved": 0,
        "stable_id_first": EXPECTED_IDS[0],
        "stable_id_last": EXPECTED_IDS[-1],
        "r25_predecessor_stable_id_last": "MC-STK-ERR-1176",
        "stable_ids_unique_and_contiguous": True,
        "stable_ids_follow_first_physical_source_locus": True,
        "bounded_preimages_unique_on_declared_lines": True,
        "operations_nonoverlapping": True,
        "payload_preview_bytes": len(payload),
        "payload_preview_sha256": sha_bytes(payload),
        "merged_producer_groups": MERGE_GROUPS,
        "rejected_ids": REJECTED_IDS,
        "prior_aliases": DUPLICATE_ALIASES,
        "independent_additional_operation": "SMOOTHING-022B at smoothing.tex:1170",
        "closure": {
            "all_35_producer_ids_accounted_for_as_new_alias_or_rejected": True,
            "operation_ids_equal_stable_unit_operation_ids": True,
            "source_map_units_equal_stable_units": True,
            "accepted_rejected_and_unresolved_disjoint": True,
        },
        "r25_touched": False,
        "prohibited_transitions_executed": [],
    }
    review = f"""# R26 Smoothing intake review

This source-only intake binds 25 accepted semantic units and {len(operation_spec_rows)} exact operations to frozen `smoothing.tex` at commit `{AUTHORITY_COMMIT}`. The stable range is contiguous from `MC-STK-ERR-1177` through `MC-STK-ERR-1201` in first-locus physical source order.

The packet contains exactly 35 producer identities `SMOOTHING-001` through `SMOOTHING-035`. Independent review accepts 31 new identities, binds `SMOOTHING-002`, `SMOOTHING-003`, and `SMOOTHING-004` as exact aliases of admitted R1 units `MC-STK-ERR-0002`, `MC-STK-ERR-0005`, and `MC-STK-ERR-0006`, rejects `SMOOTHING-010` because the original noun phrase is already grammatical, merges four sets of cloned or repeated defects, and leaves none unresolved. Five R1 units already touch `smoothing.tex`; the remaining two are different loci.

Every accepted old-text preimage occurs exactly once on its declared authority line interval. The producer emendation input contains 42 declared UTF-8 byte operations; after predecessor deduplication, rejection, grouping, and independent refinement, the admitted specification contains 39 pairwise nonoverlapping operations that replay deterministically in descending byte order. Independent review expands the two malformed solution clauses into statements about the system `g_j = 0`, names `R/\\pi R` instead of importing a proof-local symbol, and repairs the second ill-typed use of `\\mathfrak p` for an element of `B` at line 1170.

No predecessor overlay is changed by this source-materialization stage. Build, render, admission, registry, Git publication, and generated-source composition remain later deterministic gates.
"""

    (ROOT / "SMOOTHING_SOURCE_DEFECT_LEDGER.input.csv").write_bytes(ledger_bytes)
    (ROOT / "SMOOTHING_SOURCE_EMENDATIONS.input.json").write_bytes(sanitized_emendation_bytes)
    write_json(ROOT / "candidate.config.input.json", config_input)
    write_json(ROOT / "operation-spec.input.json", operation_spec)
    write_json(ROOT / "stable-units.input.json", stable_units)
    write_jsonl(ROOT / "source-map.input.jsonl", source_map_rows)
    write_jsonl(ROOT / "decisions.input.jsonl", decisions)
    write_jsonl(ROOT / "rejections.input.jsonl", rejected_rows)
    write_json(ROOT / "INTAKE_VALIDATION.json", validation)
    (ROOT / "R26_SMOOTHING_REVIEW.md").write_text(review, encoding="utf-8", newline="")

    print(json.dumps({
        "passed": True,
        "units": len(stable_rows),
        "operations": len(operation_spec_rows),
        "accepted_producer_ids": len(flattened_producers),
        "rejected_producer_ids": len(REJECTED_IDS),
        "payload_bytes": len(payload),
        "payload_sha256": sha_bytes(payload),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
