from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SPEC_INPUT = ROOT / "R24_SPACES_DUALITY_ADJUDICATION_SPEC.input.json"
GENERATED_AT = "2026-08-27T17:53:29Z"
EXPECTED_IDS = [f"MC-STK-ERR-{number:04d}" for number in range(1008, 1046)]
EXPECTED_MERGES = [
    ["P10-E0255", "P10-E0256"],
    ["P10-E0257", "P10-E0258"],
    ["P10-E0260", "P10-E0268"],
    ["P10-E0265", "P10-E0266"],
    ["P10-E0278", "P10-E0281", "P10-E0284"],
    ["P10-E0285", "P10-E0287"],
]


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def file_sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="",
    )


def write_jsonl(path: Path, rows: list[dict]) -> None:
    content = "".join(
        json.dumps(row, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n"
        for row in rows
    )
    path.write_text(content, encoding="utf-8", newline="")


def bounded_offset(authority: bytes, operation: dict) -> tuple[int, int, int, int]:
    start_line = operation["source_start_line"]
    end_line = operation["source_end_line"]
    if not isinstance(start_line, int) or not isinstance(end_line, int) or start_line < 1 or end_line < start_line:
        raise AssertionError("invalid declared source line interval")

    starts = [0]
    starts.extend(index + 1 for index, byte in enumerate(authority) if byte == 10)
    line_count = authority.count(b"\n")
    if not authority.endswith(b"\n"):
        line_count += 1
    if end_line > line_count:
        raise AssertionError(f"declared line {end_line} exceeds authority line count {line_count}")
    region_start = starts[start_line - 1]
    region_end = starts[end_line] if end_line < len(starts) else len(authority)
    old = operation["old_text"].encode("utf-8")
    if not old:
        raise AssertionError("empty operation preimage")

    positions: list[int] = []
    cursor = 0
    region = authority[region_start:region_end]
    while True:
        position = region.find(old, cursor)
        if position < 0:
            break
        positions.append(position)
        cursor = position + 1
    if len(positions) != 1:
        raise AssertionError(
            f"preimage must occur exactly once on declared lines {start_line}-{end_line}: "
            f"{operation['old_text']!r}; observed={len(positions)}"
        )
    start = region_start + positions[0]
    end = start + len(old)
    actual_start_line = authority[:start].count(b"\n") + 1
    actual_end_line = authority[: max(start, end - 1)].count(b"\n") + 1
    if actual_start_line < start_line or actual_end_line > end_line:
        raise AssertionError(
            f"exact preimage escapes declared line interval for {operation['old_text']!r}: "
            f"declared={start_line}-{end_line}, actual={actual_start_line}-{actual_end_line}"
        )
    return start, end, actual_start_line, actual_end_line


def main() -> int:
    parser = argparse.ArgumentParser(description="Derive the bounded deterministic R24 source-intake inputs.")
    parser.add_argument("--authority", type=Path, required=True)
    args = parser.parse_args()

    authority = args.authority.read_bytes()
    spec_bytes = SPEC_INPUT.read_bytes()
    spec = json.loads(spec_bytes.decode("utf-8"))
    if spec["schema"] != "mathematics-commons-stacks-r24-adjudication-spec/v1":
        raise AssertionError("unexpected R24 adjudication schema")
    if len(authority) != spec["authority_bytes"] or sha_bytes(authority) != spec["authority_sha256"]:
        raise AssertionError("frozen spaces-duality.tex authority mismatch")
    if b"\r" in authority or not authority.endswith(b"\n"):
        raise AssertionError("authority must be LF-only UTF-8 with terminal LF")
    if (
        spec["candidate_id"] != "stacks-errata-a04446e-r24"
        or spec["authority_commit"] != "a04446e57ec1fbc252a871afcec7752fb2807b14"
        or spec["authority_path"] != "spaces-duality.tex"
        or spec["semantic_unit_count"] != 38
        or spec["operation_count"] != 57
        or spec["accepted_producer_row_count"] != 45
        or spec["rejected_producer_row_count"] != 0
        or spec["unresolved"]
        or spec["rejected"]
    ):
        raise AssertionError("R24 adjudication closure mismatch")

    accepted = spec["accepted"]
    if [unit["stable_id"] for unit in accepted] != EXPECTED_IDS:
        raise AssertionError("R24 stable IDs are not contiguous MC-STK-ERR-1008..1045")
    if spec["stable_id_range"] != [EXPECTED_IDS[0], EXPECTED_IDS[-1]]:
        raise AssertionError("R24 stable-ID range metadata mismatch")

    flattened_producers = [producer for unit in accepted for producer in unit["producer_ids"]]
    if len(flattened_producers) != 45 or len(set(flattened_producers)) != 45:
        raise AssertionError("accepted producer IDs must close exactly once")
    if any(not producer.startswith("P10-E") for producer in flattened_producers):
        raise AssertionError("unexpected producer namespace")
    merged_groups = [unit["producer_ids"] for unit in accepted if len(unit["producer_ids"]) > 1]
    if merged_groups != EXPECTED_MERGES:
        raise AssertionError("semantic-unit merge groups differ from frozen adjudication")

    operation_spec_rows: list[dict] = []
    source_map_rows: list[dict] = []
    stable_rows: list[dict] = []
    first_offsets: list[int] = []
    all_intervals: list[tuple[int, int, str]] = []
    line_metadata_normalizations: list[dict] = []

    for unit in accepted:
        stable_id = unit["stable_id"]
        producer_ids = unit["producer_ids"]
        mapped_operations: list[dict] = []
        for operation_index, operation in enumerate(unit["operations"], 1):
            if operation["producer_id"] not in producer_ids:
                raise AssertionError(f"operation producer is outside {stable_id}")
            start, end, actual_start_line, actual_end_line = bounded_offset(authority, operation)
            if (actual_start_line, actual_end_line) != (
                operation["source_start_line"],
                operation["source_end_line"],
            ):
                line_metadata_normalizations.append({
                    "stable_id": stable_id,
                    "producer_id": operation["producer_id"],
                    "semantic_unit_locus": unit["locus"],
                    "declared_operation_start_line": operation["source_start_line"],
                    "declared_operation_end_line": operation["source_end_line"],
                    "exact_operation_start_line": actual_start_line,
                    "exact_operation_end_line": actual_end_line,
                    "rationale": "The frozen semantic-unit locus spans the following sentence line, while the exact old/new replacement preimage is wholly on the first line.",
                })
            old = operation["old_text"].encode("utf-8")
            replacement = operation["replacement_text"].encode("utf-8")
            operation_id = f"{stable_id}-OP{operation_index}"
            mapped = {
                "producer_id": operation["producer_id"],
                "source_start_line": actual_start_line,
                "source_end_line": actual_end_line,
                "old_text": operation["old_text"],
                "replacement_text": operation["replacement_text"],
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
        if not mapped_operations:
            raise AssertionError(f"{stable_id} has no operations")
        first_offsets.append(min(row["start_byte"] for row in mapped_operations))
        operation_ids = [row["operation_id"] for row in mapped_operations]
        stable_rows.append({
            "class": unit["class"],
            "id": stable_id,
            "locus": unit["locus"],
            "operation_ids": operation_ids,
            "payload": "payload/spaces-duality.tex",
            "producer_id": producer_ids[0],
            "producer_ids": producer_ids,
            "source": "spaces-duality.tex",
            "status": "provisional_accepted_not_materialized",
        })
        source_map_rows.append({
            "schema": "mathematics-commons-stacks-errata-map/v2",
            "unit_id": stable_id,
            "producer_id": producer_ids[0],
            "producer_ids": producer_ids,
            "source": "spaces-duality.tex",
            "authority": "authority/source/spaces-duality.tex",
            "authority_sha256": spec["authority_sha256"],
            "payload": "payload/spaces-duality.tex",
            "locus": unit["locus"],
            "class": unit["class"],
            "proof": "accepted_after_independent_frozen_authority_replay",
            "prior_aliases": [],
            "adverse_evidence": "Producer rows are allegation evidence only; the frozen authority, exact bounded preimages, and independent adjudication are controlling.",
            "operations": mapped_operations,
        })

    if len(operation_spec_rows) != 57:
        raise AssertionError("R24 operation count is not 57")
    expected_line_normalizations = [{
        "stable_id": "MC-STK-ERR-1040",
        "producer_id": "P10-E0283",
        "semantic_unit_locus": "spaces-duality.tex:1998-1999",
        "declared_operation_start_line": 1998,
        "declared_operation_end_line": 1999,
        "exact_operation_start_line": 1998,
        "exact_operation_end_line": 1998,
        "rationale": "The frozen semantic-unit locus spans the following sentence line, while the exact old/new replacement preimage is wholly on the first line.",
    }]
    if line_metadata_normalizations != expected_line_normalizations:
        raise AssertionError(
            f"unexpected declared/actual operation line differences: {line_metadata_normalizations!r}"
        )
    if first_offsets != sorted(first_offsets) or len(first_offsets) != len(set(first_offsets)):
        raise AssertionError("stable units are not ordered by first physical source locus")
    ascending = sorted(all_intervals)
    for left, right in zip(ascending, ascending[1:]):
        if left[1] > right[0]:
            raise AssertionError(f"overlapping operations: {left[2]} / {right[2]}")

    payload = authority
    for start, end, operation_id in sorted(all_intervals, reverse=True):
        operation = next(row for row in operation_spec_rows if row["operation_id"] == operation_id)
        old = operation["old_text"].encode("utf-8")
        replacement = operation["replacement_text"].encode("utf-8")
        if payload[start:end] != old:
            raise AssertionError(f"descending replay mismatch: {operation_id}")
        payload = payload[:start] + replacement + payload[end:]

    lease = json.loads((ROOT / "LEASE.json").read_text(encoding="utf-8"))
    config_input = {
        "schema": "mathematics-commons-stacks-errata-candidate-config-input/v1",
        "candidate_id": spec["candidate_id"],
        "authority_commit": spec["authority_commit"],
        "authority_tree": spec["authority_tree"],
        "namespace": lease["namespace"],
        "writer_task": lease["writer_task"],
        "lease_id": lease["lease_id"],
        "accepted": len(accepted),
        "rejected": 0,
        "unresolved": 0,
        "operation_count": len(operation_spec_rows),
        "expected_unit_ids": EXPECTED_IDS,
        "expected_producer_ids": [unit["producer_ids"][0] for unit in accepted],
        "expected_all_producer_ids": flattened_producers,
        "intentionally_absent_producer_ids": [],
        "payload_expected_bytes": len(payload),
        "payload_expected_sha256": sha_bytes(payload),
        "build_render_admission_status": "not_run_by_intake_skeleton",
    }
    operation_spec = {
        "schema": "mathematics-commons-stacks-errata-operation-spec/v1",
        "authority_sha256": spec["authority_sha256"],
        "operations": operation_spec_rows,
    }
    stable_units = {
        "schema": "mathematics-commons-stacks-errata-units/v1",
        "authority_commit": spec["authority_commit"],
        "unit_count": len(stable_rows),
        "units": stable_rows,
    }

    decisions = [
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R24-D0001",
            "timestamp_utc": GENERATED_AT,
            "choice": "Bind R24 to frozen spaces-duality.tex at commit a04446e57ec1fbc252a871afcec7752fb2807b14 without changing R23.",
            "rationale": "Preserves immutable authority and the completed MC-STK-ERR-0998..1007 assignment.",
            "supersedes": None,
        },
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R24-D0002",
            "timestamp_utc": GENERATED_AT,
            "choice": "Assign MC-STK-ERR-1008..1045 to 38 accepted semantic units in first-locus physical source order.",
            "rationale": "The range begins immediately after R23 and contains no reused or skipped stable ID.",
            "supersedes": None,
        },
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R24-D0003",
            "timestamp_utc": GENERATED_AT,
            "choice": "Merge the six linked producer groups sealed in the R24 adjudication specification.",
            "rationale": "Each group records repeated or jointly typed loci of one bounded semantic defect and consumes one canon ID.",
            "supersedes": None,
        },
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R24-D0004",
            "timestamp_utc": GENERATED_AT,
            "choice": "Accept all 45 P10 producer identities; reject none and leave none unresolved.",
            "rationale": "Every allegation replays against its exact frozen-authority locus and is absent from the 640 admitted predecessor units.",
            "supersedes": None,
        },
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R24-D0005",
            "timestamp_utc": GENERATED_AT,
            "choice": "Use only the exact old/new operations sealed in R24_SPACES_DUALITY_ADJUDICATION_SPEC.input.json.",
            "rationale": "This retains the corrected three-use definition repair and explicit local-adjoint definition without broad replacement.",
            "supersedes": None,
        },
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R24-D0006",
            "timestamp_utc": GENERATED_AT,
            "choice": "Materialize and statically replay the source candidate only; leave build, render, admission, registry, Git, publication, and generated-source transitions unexecuted.",
            "rationale": "This produces the bounded deterministic candidate requested for the later build and admission gates.",
            "supersedes": None,
        },
    ]

    validation = {
        "schema": "mathematics-commons-stacks-r24-intake-validation/v1",
        "status": "PASS",
        "authority_bytes": len(authority),
        "authority_sha256": sha_bytes(authority),
        "adjudication_spec_bytes": len(spec_bytes),
        "adjudication_spec_sha256": sha_bytes(spec_bytes),
        "semantic_units": len(stable_rows),
        "operations": len(operation_spec_rows),
        "accepted_producer_ids": len(flattened_producers),
        "rejected_producer_ids": 0,
        "unresolved": 0,
        "stable_id_first": EXPECTED_IDS[0],
        "stable_id_last": EXPECTED_IDS[-1],
        "r23_predecessor_stable_id_last": "MC-STK-ERR-1007",
        "stable_ids_unique_and_contiguous": True,
        "stable_ids_follow_first_physical_source_locus": True,
        "bounded_preimages_unique_on_declared_lines": True,
        "exact_operation_line_metadata": True,
        "adjudication_line_metadata_normalizations": line_metadata_normalizations,
        "operations_nonoverlapping": True,
        "payload_preview_bytes": len(payload),
        "payload_preview_sha256": sha_bytes(payload),
        "merged_producer_groups": EXPECTED_MERGES,
        "closure": {
            "all_expected_producer_ids_accounted_for_exactly_once": True,
            "operation_ids_equal_stable_unit_operation_ids": True,
            "source_map_units_equal_stable_units": True,
            "accepted_rejected_and_unresolved_disjoint": True,
        },
        "r23_touched": False,
        "prohibited_transitions_executed": [],
    }

    review = """# R24 Spaces Duality intake review

This source-only intake binds 38 accepted semantic units and 57 exact operations to frozen `spaces-duality.tex` at commit `a04446e57ec1fbc252a871afcec7752fb2807b14`. The stable range is contiguous from `MC-STK-ERR-1008` through `MC-STK-ERR-1045` in first-locus physical source order.

All 45 P10 producer identities are accepted exactly once. Six linked groups are merged as recorded in the adjudication specification, so 45 producer rows consume 38 stable IDs. No producer row is rejected or unresolved, and no prior admitted unit names `spaces-duality.tex`.

Every old-text preimage occurs exactly once on its declared authority line interval. The resulting 57 UTF-8 byte intervals are pairwise nonoverlapping and replay deterministically in descending byte order. The broad semantic-unit locus for `MC-STK-ERR-1040` remains lines 1998–1999, while its exact replacement preimage is normalized from the spec's 1998–1999 operation metadata to line 1998 alone; the frozen spec bytes are unchanged.

No TeX build, render, registry admission, root-registry mutation, Git operation, publication, or generated-source composition is performed by this intake stage.
"""

    write_json(ROOT / "candidate.config.input.json", config_input)
    write_json(ROOT / "operation-spec.input.json", operation_spec)
    write_json(ROOT / "stable-units.input.json", stable_units)
    write_jsonl(ROOT / "source-map.input.jsonl", source_map_rows)
    write_jsonl(ROOT / "decisions.input.jsonl", decisions)
    write_jsonl(ROOT / "rejections.input.jsonl", [])
    write_json(ROOT / "INTAKE_VALIDATION.json", validation)
    (ROOT / "R24_SPACES_DUALITY_REVIEW.md").write_text(review, encoding="utf-8", newline="")

    print(json.dumps({
        "passed": True,
        "units": len(stable_rows),
        "operations": len(operation_spec_rows),
        "producer_ids": len(flattened_producers),
        "payload_bytes": len(payload),
        "payload_sha256": sha_bytes(payload),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
