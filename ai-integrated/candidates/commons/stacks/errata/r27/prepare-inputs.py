from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
GENERATED_AT = "2026-08-28T15:30:00Z"
AUTHORITY_COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
AUTHORITY_TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
AUTHORITY_PATH = "modules.tex"
AUTHORITY_BYTES = 204133
AUTHORITY_SHA256 = "7BD3E9E096717EF6FD458492D8AD91FC9FFE428CFD7DD80E386FAE377BB7CB0D"
PRODUCER_LEDGER_BYTES = 5335
PRODUCER_LEDGER_SHA256 = "FD2098057D005F93EE17480643CF8D177D791AD68F2C219F8EFFAC0983A5B7F8"
PRODUCER_EMENDATIONS_BYTES = 3247
PRODUCER_EMENDATIONS_SHA256 = "420A2629924B044E083170E1DDD28D3518E51A3E784BA8B236478F176220161A"
EXPECTED_IDS = [f"MC-STK-ERR-{number:04d}" for number in range(1202, 1216)]
EXPECTED_PRODUCER_IDS = [
    "MODULES-012", "MODULES-013", "MODULES-014", "MODULES-008",
    "MODULES-009", "MODULES-010", "MODULES-011", "MODULES-001",
    "MODULES-002", "MODULES-003", "MODULES-004", "MODULES-005",
    "MODULES-006", "MODULES-007",
]


OPERATIONS = {
    "MODULES-012": (1131, 1131, "be ringed space.", "be a ringed space."),
    "MODULES-013": (
        1152,
        1153,
        "corresponding to $j \\in J$\ngiven by",
        "corresponding to $j \\in J$\nis given by",
    ),
    "MODULES-014": (
        2169,
        2169,
        "as an $\\Gamma(U, \\mathcal{O}_U)$-module",
        "as a $\\Gamma(U, \\mathcal{O}_U)$-module",
    ),
    "MODULES-008": (4093, 4093, "$U$ an integer", "$U$ of $x$, an integer"),
    "MODULES-009": (
        4182,
        4182,
        "Looking over an open covering trivialization $\\mathcal{L}$",
        "Looking over an open covering trivializing $\\mathcal{L}$",
    ),
    "MODULES-010": (4337, 4337, "U_i", "U_j"),
    "MODULES-011": (4362, 4362, "linebundle", "line bundle"),
    "MODULES-001": (
        4629,
        4629,
        "section of $\\mathcal{O}_X$.",
        "section of $\\mathcal{S}^{-1}\\mathcal{O}_X$.",
    ),
    "MODULES-002": (
        5179,
        5179,
        "is an is an $\\mathcal{O}_1$-linear map",
        "is an $\\mathcal{O}_1$-linear map",
    ),
    "MODULES-003": (5263, 5263, "[m + m' - [m] - [m'],", "[m + m'] - [m] - [m'],"),
    "MODULES-004": (5709, 5709, "a sheaves of sets", "a sheaf of sets"),
    "MODULES-005": (
        5748,
        5748,
        "these maps are quasi-isomorphism",
        "these maps are quasi-isomorphisms",
    ),
    "MODULES-006": (
        5895,
        5895,
        "$(g \\circ g')^*\\NL_{X''/Y''} \\to \\NL_{X/Y}$",
        "$(g \\circ g')^*\\NL_{X/Y} \\to \\NL_{X''/Y''}$",
    ),
    "MODULES-007": (5921, 5921, "maps of sheaves rings", "maps of sheaves of rings"),
}


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


def bounded_offset(
    authority: bytes, producer_id: str, start_line: int, end_line: int, old_text: str
) -> tuple[int, int, int, int]:
    starts = [0]
    starts.extend(index + 1 for index, byte in enumerate(authority) if byte == 10)
    region_start = starts[start_line - 1]
    region_end = starts[end_line] if end_line < len(starts) else len(authority)
    old = old_text.encode("utf-8")
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
            f"{producer_id}: preimage count on lines {start_line}-{end_line} is "
            f"{len(positions)} for {old_text!r}"
        )
    start = region_start + positions[0]
    end = start + len(old)
    actual_start_line = authority[:start].count(b"\n") + 1
    actual_end_line = authority[: max(start, end - 1)].count(b"\n") + 1
    return start, end, actual_start_line, actual_end_line


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare deterministic R27 Modules source-intake inputs.")
    parser.add_argument("--authority", type=Path, required=True)
    parser.add_argument("--producer-ledger", type=Path, required=True)
    parser.add_argument("--producer-emendations", type=Path, required=True)
    args = parser.parse_args()

    authority = args.authority.read_bytes()
    ledger_bytes = args.producer_ledger.read_bytes()
    emendation_bytes = args.producer_emendations.read_bytes()
    if len(authority) != AUTHORITY_BYTES or sha_bytes(authority) != AUTHORITY_SHA256:
        raise AssertionError("frozen modules.tex authority mismatch")
    if b"\r" in authority or not authority.endswith(b"\n"):
        raise AssertionError("authority must be LF-only UTF-8 with terminal LF")
    if len(ledger_bytes) != PRODUCER_LEDGER_BYTES or sha_bytes(ledger_bytes) != PRODUCER_LEDGER_SHA256:
        raise AssertionError("frozen Modules producer ledger mismatch")
    if len(emendation_bytes) != PRODUCER_EMENDATIONS_BYTES or sha_bytes(emendation_bytes) != PRODUCER_EMENDATIONS_SHA256:
        raise AssertionError("frozen Modules producer emendations mismatch")

    producer_rows = list(csv.DictReader(ledger_bytes.decode("utf-8-sig").splitlines()))
    row_by_id = {row["defect_id"]: row for row in producer_rows}
    if len(producer_rows) != 14 or set(row_by_id) != set(EXPECTED_PRODUCER_IDS):
        raise AssertionError("producer packet is not the exact 14-row MODULES-001..014 set")
    if any(row["authority_sha256"] != AUTHORITY_SHA256 for row in producer_rows):
        raise AssertionError("producer source identity mismatch")
    producer = json.loads(emendation_bytes.decode("utf-8"))
    if (
        producer.get("authority_sha256") != AUTHORITY_SHA256
        or producer.get("source_file") != "modules.tex"
        or len(producer.get("emendations", [])) != 7
    ):
        raise AssertionError("producer emendation declaration closure mismatch")

    accepted: list[dict] = []
    operation_spec_rows: list[dict] = []
    source_map_rows: list[dict] = []
    stable_rows: list[dict] = []
    all_intervals: list[tuple[int, int, str]] = []
    for stable_id, producer_id in zip(EXPECTED_IDS, EXPECTED_PRODUCER_IDS):
        start_line, end_line, old_text, replacement_text = OPERATIONS[producer_id]
        start, end, actual_start_line, actual_end_line = bounded_offset(
            authority, producer_id, start_line, end_line, old_text
        )
        if (actual_start_line, actual_end_line) != (start_line, end_line):
            raise AssertionError(f"{producer_id}: exact line metadata mismatch")
        old = old_text.encode("utf-8")
        replacement = replacement_text.encode("utf-8")
        operation_id = f"{stable_id}-OP1"
        mapped = {
            "producer_id": producer_id,
            "producer_operation_id": producer_id,
            "source_start_line": start_line,
            "source_end_line": end_line,
            "old_text": old_text,
            "replacement_text": replacement_text,
            "operation_id": operation_id,
            "start_byte": start,
            "end_byte_exclusive": end,
            "occurrence_count_in_frozen_authority": authority.count(old),
            "old_bytes": len(old),
            "old_sha256": sha_bytes(old),
            "replacement_bytes": len(replacement),
            "replacement_sha256": sha_bytes(replacement),
        }
        operation_spec_rows.append({
            "stable_id": stable_id,
            "semantic_unit_producer_id": producer_id,
            "operation_index": 1,
            **mapped,
        })
        all_intervals.append((start, end, operation_id))
        locus = f"modules.tex:{start_line}" if start_line == end_line else f"modules.tex:{start_line}-{end_line}"
        rationale = row_by_id[producer_id]["note"]
        if producer_id == "MODULES-014":
            rationale = (
                "The pronunciation-governed article before Gamma is 'a'. The narrower repair "
                "preserves the singular module phrase and changes no mathematical content."
            )
        unit = {
            "stable_id": stable_id,
            "producer_ids": [producer_id],
            "class": "source_defect_correction",
            "locus": locus,
            "operations": [{
                "producer_id": producer_id,
                "producer_operation_id": producer_id,
                "source_start_line": start_line,
                "source_end_line": end_line,
                "old_text": old_text,
                "replacement_text": replacement_text,
            }],
            "rationale": rationale,
        }
        accepted.append(unit)
        stable_rows.append({
            "class": unit["class"],
            "id": stable_id,
            "locus": locus,
            "operation_ids": [operation_id],
            "payload": "payload/modules.tex",
            "producer_id": producer_id,
            "producer_ids": [producer_id],
            "source": "modules.tex",
            "status": "provisional_accepted_not_admitted",
        })
        source_map_rows.append({
            "schema": "mathematics-commons-stacks-errata-map/v2",
            "unit_id": stable_id,
            "producer_id": producer_id,
            "producer_ids": [producer_id],
            "source": "modules.tex",
            "authority": "authority/source/modules.tex",
            "authority_sha256": AUTHORITY_SHA256,
            "payload": "payload/modules.tex",
            "locus": locus,
            "class": unit["class"],
            "proof": "accepted_after_independent_frozen_authority_replay",
            "prior_aliases": [],
            "adverse_evidence": (
                "Producer rows are allegation evidence only; frozen authority, bounded preimages, "
                "three independent reviews, and deterministic replay control admission."
            ),
            "operations": [mapped],
        })

    ascending = sorted(all_intervals)
    for left, right in zip(ascending, ascending[1:]):
        if left[1] > right[0]:
            raise AssertionError(f"overlapping operations: {left[2]} / {right[2]}")
    if [row["start_byte"] for row in operation_spec_rows] != sorted(row["start_byte"] for row in operation_spec_rows):
        raise AssertionError("stable units do not follow first physical source locus")

    payload = authority
    by_operation_id = {row["operation_id"]: row for row in operation_spec_rows}
    for start, end, operation_id in sorted(all_intervals, reverse=True):
        operation = by_operation_id[operation_id]
        old = operation["old_text"].encode("utf-8")
        replacement = operation["replacement_text"].encode("utf-8")
        if payload[start:end] != old:
            raise AssertionError(f"descending replay mismatch: {operation_id}")
        payload = payload[:start] + replacement + payload[end:]

    spec = {
        "schema": "mathematics-commons-stacks-r27-adjudication-spec/v1",
        "candidate_id": "stacks-errata-a04446e-r27",
        "authority_commit": AUTHORITY_COMMIT,
        "authority_tree": AUTHORITY_TREE,
        "authority_path": AUTHORITY_PATH,
        "authority_bytes": len(authority),
        "authority_sha256": sha_bytes(authority),
        "producer_sources": [
            "MODULES_SOURCE_DEFECT_LEDGER.input.csv",
            "MODULES_SOURCE_EMENDATIONS.input.json",
        ],
        "producer_ledger_bytes": len(ledger_bytes),
        "producer_ledger_sha256": sha_bytes(ledger_bytes),
        "producer_emendations_bytes": len(emendation_bytes),
        "producer_emendations_sha256": sha_bytes(emendation_bytes),
        "producer_emendations_sanitized_bytes": len(emendation_bytes),
        "producer_emendations_sanitized_sha256": sha_bytes(emendation_bytes),
        "producer_row_count": 14,
        "accepted_producer_row_count": 14,
        "rejected_producer_row_count": 0,
        "prior_alias_producer_row_count": 0,
        "semantic_unit_count": 14,
        "operation_count": 14,
        "stable_id_range": [EXPECTED_IDS[0], EXPECTED_IDS[-1]],
        "deduplication": {
            "admitted_stacks_errata_units_reviewed": 834,
            "admitted_stacks_errata_operations_reviewed": 947,
            "prior_rounds": "R1-R26",
            "prior_modules_units_reviewed": 0,
            "matching_modules_units": 0,
            "result": "all 14 units are new; no aliases, rejects, or unresolved proposals",
        },
        "prior_aliases": [],
        "accepted": accepted,
        "rejected": [],
        "unresolved": [],
    }
    spec_path = ROOT / "R27_MODULES_ADJUDICATION_SPEC.input.json"
    write_json(spec_path, spec)
    spec_bytes = spec_path.read_bytes()

    lease = json.loads((ROOT / "LEASE.json").read_text(encoding="utf-8"))
    config_input = {
        "schema": "mathematics-commons-stacks-errata-candidate-config-input/v1",
        "candidate_id": spec["candidate_id"],
        "authority_commit": AUTHORITY_COMMIT,
        "authority_tree": AUTHORITY_TREE,
        "namespace": lease["namespace"],
        "writer_task": lease["writer_task"],
        "lease_id": lease["lease_id"],
        "accepted": 14,
        "rejected": 0,
        "unresolved": 0,
        "operation_count": 14,
        "expected_unit_ids": EXPECTED_IDS,
        "expected_producer_ids": EXPECTED_PRODUCER_IDS,
        "expected_all_producer_ids": EXPECTED_PRODUCER_IDS,
        "rejected_producer_ids": [],
        "prior_alias_producer_ids": [],
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
        "unit_count": 14,
        "units": stable_rows,
    }
    decisions = [
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R27-D0001",
            "timestamp_utc": GENERATED_AT,
            "choice": "Bind R27 to frozen modules.tex without changing R26.",
            "rationale": "Preserves immutable authority and the completed MC-STK-ERR-1177..1201 assignment.",
            "supersedes": None,
        },
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R27-D0002",
            "timestamp_utc": GENERATED_AT,
            "choice": "Accept MODULES-001..014 as 14 new semantic units and assign MC-STK-ERR-1202..1215 in first-locus source order.",
            "rationale": "Three independent reviews found all units genuine and absent from R1-R26.",
            "supersedes": None,
        },
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R27-D0003",
            "timestamp_utc": GENERATED_AT,
            "choice": "Narrow MODULES-014 to the forced article correction 'as an' to 'as a'.",
            "rationale": "The article error is certain; preserving the singular module phrase is the smallest non-semantic repair.",
            "supersedes": None,
        },
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R27-D0004",
            "timestamp_utc": GENERATED_AT,
            "choice": "Materialize and replay the source candidate before build, render, admission, composition, and publication.",
            "rationale": "Maintains the deterministic finite gate sequence.",
            "supersedes": None,
        },
    ]
    validation = {
        "schema": "mathematics-commons-stacks-r27-intake-validation/v1",
        "status": "PASS",
        "authority_bytes": len(authority),
        "authority_sha256": sha_bytes(authority),
        "producer_ledger_bytes": len(ledger_bytes),
        "producer_ledger_sha256": sha_bytes(ledger_bytes),
        "producer_emendations_bytes": len(emendation_bytes),
        "producer_emendations_sha256": sha_bytes(emendation_bytes),
        "adjudication_spec_bytes": len(spec_bytes),
        "adjudication_spec_sha256": sha_bytes(spec_bytes),
        "semantic_units": 14,
        "operations": 14,
        "accepted_producer_ids": 14,
        "rejected_producer_ids": 0,
        "prior_alias_producer_ids": 0,
        "unresolved": 0,
        "stable_id_first": EXPECTED_IDS[0],
        "stable_id_last": EXPECTED_IDS[-1],
        "r26_predecessor_stable_id_last": "MC-STK-ERR-1201",
        "stable_ids_unique_and_contiguous": True,
        "stable_ids_follow_first_physical_source_locus": True,
        "bounded_preimages_unique_on_declared_lines": True,
        "operations_nonoverlapping": True,
        "payload_preview_bytes": len(payload),
        "payload_preview_sha256": sha_bytes(payload),
        "merged_producer_groups": [],
        "rejected_ids": [],
        "prior_aliases": {},
        "independent_additional_operation": None,
        "closure": {
            "all_14_producer_ids_accounted_for_as_new": True,
            "operation_ids_equal_stable_unit_operation_ids": True,
            "source_map_units_equal_stable_units": True,
            "accepted_rejected_and_unresolved_disjoint": True,
        },
        "r26_touched": False,
        "prohibited_transitions_executed": [],
    }
    review = f"""# R27 Modules intake review

This source-only intake binds 14 accepted semantic units and 14 exact operations to frozen `modules.tex` at commit `{AUTHORITY_COMMIT}`. Stable IDs are contiguous from `MC-STK-ERR-1202` through `MC-STK-ERR-1215` in first-locus physical source order.

The packet contains exactly 14 producer identities `MODULES-001` through `MODULES-014`. Three independent authority reviews accept all 14, find no duplicate or alias in R1-R26, and leave no rejection or unresolved proposal. `MODULES-014` is narrowed to the forced article-only repair, preserving the source's singular module phrasing.

Every accepted preimage occurs exactly once on its declared authority line interval. The 14 pairwise nonoverlapping operations replay deterministically in descending byte order. No predecessor overlay is changed by source materialization; build, render, admission, composition, and publication remain later deterministic gates.
"""

    (ROOT / "MODULES_SOURCE_DEFECT_LEDGER.input.csv").write_bytes(ledger_bytes)
    (ROOT / "MODULES_SOURCE_EMENDATIONS.input.json").write_bytes(emendation_bytes)
    write_json(ROOT / "candidate.config.input.json", config_input)
    write_json(ROOT / "operation-spec.input.json", operation_spec)
    write_json(ROOT / "stable-units.input.json", stable_units)
    write_jsonl(ROOT / "source-map.input.jsonl", source_map_rows)
    write_jsonl(ROOT / "decisions.input.jsonl", decisions)
    write_jsonl(ROOT / "rejections.input.jsonl", [])
    write_json(ROOT / "INTAKE_VALIDATION.json", validation)
    (ROOT / "R27_MODULES_REVIEW.md").write_text(review, encoding="utf-8", newline="")

    print(json.dumps({
        "passed": True,
        "units": 14,
        "operations": 14,
        "accepted_producer_ids": 14,
        "rejected_producer_ids": 0,
        "payload_bytes": len(payload),
        "payload_sha256": sha_bytes(payload),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
