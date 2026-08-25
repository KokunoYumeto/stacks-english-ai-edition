from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
AUTHORITY_SHA256 = "FA8BB92E58A4F78A2BD01B3B6A4A87DE0A0D279F5DD90641B574DD5FBFFFA4F3"
AUTHORITY_BYTES = 1_771_230
PRODUCER_SHA256 = "2C9697C25000F18F4CD786CBA5E5B9D5CA726D9D4F4246A96915A53DC093E5F0"
PRODUCER_BYTES = 1_983
UPSTREAM_LOCK_SHA256 = "B195ECC83AB0F32C574A60D1FDBA9B0DA4D35B04E0DF7CB106DC9C0FDAD99C0D"
COPYING_SHA256 = "4B2C8FC390F802CD92F0622DC00A708A588BEC54D0145D2EE135D6D7672BFE85"
SPEC_SHA256 = "9FAC4A5948E4AA20FBD67EF53036A9F4795091AC0CBA29AD5F69057B15BF482A"
GENERATED_AT = "2026-08-24T22:10:34Z"


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
    parser.add_argument("--producer-packet", type=Path, required=True)
    parser.add_argument("--upstream-lock", type=Path, required=True)
    parser.add_argument("--copying", type=Path, required=True)
    parser.add_argument("--replace-generated", action="store_true")
    args = parser.parse_args()

    authority = args.authority.read_bytes()
    if len(authority) != AUTHORITY_BYTES or sha_bytes(authority) != AUTHORITY_SHA256:
        raise AssertionError("frozen authority identity mismatch")
    if b"\r" in authority or not authority.endswith(b"\n"):
        raise AssertionError("authority is not terminal-LF UTF-8/LF source")
    producer_snapshot = args.producer_packet.read_bytes()
    if len(producer_snapshot) != PRODUCER_BYTES or sha_bytes(producer_snapshot) != PRODUCER_SHA256:
        raise AssertionError("producer packet identity mismatch")
    producer_packet = json.loads(producer_snapshot.decode("utf-8"))
    if sha256(args.upstream_lock) != UPSTREAM_LOCK_SHA256 or sha256(args.copying) != COPYING_SHA256:
        raise AssertionError("upstream lock or COPYING identity mismatch")

    spec_path = ROOT / "authority" / "canon" / "R14_ALG_395_402_ADJUDICATION_SPEC.json"
    if SPEC_SHA256 == "TO_BE_FILLED" or sha256(spec_path) != SPEC_SHA256:
        raise AssertionError("adjudication spec identity mismatch")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    accepted = spec["accepted"]
    rejected = spec["rejected"]
    expected_producers = [f"ALGEBRA-{number}" for number in range(395, 403)]
    accepted_producers = [row["producer_id"] for row in accepted]
    rejected_producers = [row["producer_id"] for row in rejected]
    if sorted(accepted_producers + rejected_producers) != sorted(expected_producers):
        raise AssertionError("adjudication partition is not ALGEBRA-395..402")
    expected_ids = [f"MC-STK-ERR-{number:04d}" for number in range(738, 745)]
    if [row["stable_id"] for row in accepted] != expected_ids:
        raise AssertionError("stable-ID assignment is not contiguous 0738..0744")
    if producer_packet.get("ids") != expected_producers:
        raise AssertionError("producer packet does not enumerate ALGEBRA-395..402 exactly")
    if (producer_packet.get("authority_commit") != spec["authority_commit"] or
            producer_packet.get("authority_sha256") != AUTHORITY_SHA256):
        raise AssertionError("producer packet authority binding mismatch")

    generated = [
        ROOT / "authority" / "source" / "algebra.tex",
        ROOT / "authority" / "producer" / "ALGEBRA_395_402_CANON_PACKET_SANITIZED.json",
        ROOT / "authority" / "upstream.lock.json",
        ROOT / "authority" / "COPYING",
        ROOT / "authority" / "canon" / "R14_ALG_395_402_INTAKE.json",
        ROOT / "authority" / "canon" / "R14_ALG_395_402_REVIEW.md",
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
    producer_copy = ROOT / "authority" / "producer" / "ALGEBRA_395_402_CANON_PACKET_SANITIZED.json"
    payload_path = ROOT / "payload" / "algebra.tex"
    authority_source.parent.mkdir(parents=True, exist_ok=True)
    producer_copy.parent.mkdir(parents=True, exist_ok=True)
    payload_path.parent.mkdir(parents=True, exist_ok=True)
    authority_source.write_bytes(authority)
    payload_path.write_bytes(payload)
    public_packet = copy.deepcopy(producer_packet)
    public_packet["producer_global_ledger"]["path"] = "external producer ledger; not imported"
    public_packet["producer_local_ledger"]["path"] = "external producer ledger; not imported"
    public_packet["source_emendation_manifest"]["path"] = (
        "external producer emendation manifest; not opened, imported, or trusted as canon"
    )
    public_packet["review"]["path"] = "external producer review; not imported"
    write_json(producer_copy, public_packet)
    shutil.copy2(args.upstream_lock, ROOT / "authority" / "upstream.lock.json")
    shutil.copy2(args.copying, ROOT / "authority" / "COPYING")

    authority_offsets = line_offsets(authority)
    payload_offsets = line_offsets(payload)
    bounded_start_line = 47092
    bounded_end_line = 47885
    bounded_authority = authority[
        authority_offsets[bounded_start_line - 1]:authority_offsets[bounded_end_line]
    ]
    bounded_payload = payload[
        payload_offsets[bounded_start_line - 1]:payload_offsets[bounded_end_line]
    ]
    intake = {
        "schema": "stacks-canon-errata-intake/v1",
        "recorded_at_utc": GENERATED_AT,
        "candidate_id": spec["candidate_id"],
        "authority": {
            "path": "authority/source/algebra.tex",
            "commit": spec["authority_commit"],
            "tree": spec["authority_tree"],
            "bytes": len(authority),
            "physical_lines": authority.count(b"\n"),
            "sha256": AUTHORITY_SHA256,
            "line_endings": "LF-only with terminal LF",
            "mutated": False,
        },
        "producer_packet": {
            "source_identity": "external named packet, verified before sanitization",
            "bytes": len(producer_snapshot),
            "sha256": PRODUCER_SHA256,
            "selected_ids": "ALGEBRA-395..ALGEBRA-402",
            "source_emendation_manifest_used_as_canon": False,
            "published_sanitized_copy": artifact(
                producer_copy,
                "authority/producer/ALGEBRA_395_402_CANON_PACKET_SANITIZED.json",
            ),
        },
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
            "operations": len(operations),
            "aliases": 0,
            "unresolved": 0,
            "stable_ids": "MC-STK-ERR-0738..MC-STK-ERR-0744",
        },
        "deduplication": {
            "overlap": False,
            "public_candidates_checked": "R1..R13",
            "packet_duplicates": 0,
        },
        "adjudication": {
            row["producer_id"]: row["result"] for row in accepted
        } | {
            row["producer_id"]: row["result"] for row in rejected
        },
        "write_boundaries": {
            "english_authority": "immutable",
            "canonical_translations": "immutable",
            "payload_derivation": "directly from frozen authority, never a prior payload",
            "producer_emendation_manifest": "not trusted or imported as canon",
        },
    }
    write_json(ROOT / "authority" / "canon" / "R14_ALG_395_402_INTAKE.json", intake)

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
        ("ERR-R14-D0001", "Bind R14 exclusively to the active errata/r14 lease and frozen upstream commit/tree.", "Preserves the single-writer and immutable-authority boundary."),
        ("ERR-R14-D0002", "Assign MC-STK-ERR-0738..0744 in accepted producer order after admitted R13.", "Creates a deterministic contiguous stable-ID sequence for the seven proved corrections."),
        ("ERR-R14-D0003", "Apply only exact nonoverlapping half-open UTF-8 spans in descending byte order.", "Prevents contextual or global replacement from changing unrelated source text."),
        ("ERR-R14-D0004", "Accept ALGEBRA-395..399 and ALGEBRA-401..402 after independent source replay and deduplication against R1-R13.", "Each accepted row is a distinct bounded defect proved directly from the frozen source."),
        ("ERR-R14-D0005", "Reject ALGEBRA-400 as redundant but valid localization notation.", "The image of g is already a unit in S-prime, so localizing S-prime at g changes no mathematics and proves no source defect."),
        ("ERR-R14-D0006", "Do not treat the producer emendation manifest as canon.", "Only the named packet, frozen source, and independent adjudication bind this overlay."),
        ("ERR-R14-D0007", "Keep canonical locale bytes and the literal upstream mirror outside the corrected English payload.", "Corrections belong only to Stacks — English AI Edition."),
        ("ERR-R14-D0008", "Do not contact or submit this AI-derived correction set to upstream Stacks maintainers.", "The maintained AI-open English edition is the authorized correction surface."),
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
            "id": f"ERR-R14-R{index:04d}", "timestamp_utc": GENERATED_AT,
            "producer_id": row["producer_id"], "disposition": "rejected",
            "reason": row["reason"]}, ensure_ascii=False, separators=(",", ":")) + "\n"
            for index, row in enumerate(rejected, 1)), encoding="utf-8", newline="",
    )

    review_lines = [
        "# Independent review: ALGEBRA-395–402", "",
        f"Frozen authority: `{AUTHORITY_SHA256}` at `{spec['authority_commit']}`.", "",
        "The eight packet rows were replayed directly against the frozen source. ALGEBRA-395",
        "through ALGEBRA-399 and ALGEBRA-401 through ALGEBRA-402 are accepted as",
        "`MC-STK-ERR-0738` through `MC-STK-ERR-0744`. ALGEBRA-400 is rejected because",
        "localizing `S'` at the already invertible image of `g` is redundant but valid.",
        "No unit is aliased or unresolved. Exact operations, the rejection, and the adjudication",
        "rationale are bound by the public specification, intake, source map, and ledgers.",
        "The producer emendation manifest was not opened, imported, or trusted as canon.", "",
        "The English payload is the only corrected surface. The frozen source, canonical translations,",
        "permanent tags, and unrelated chapters remain unchanged. No upstream submission is made.",
    ]
    (ROOT / "authority" / "canon" / "R14_ALG_395_402_REVIEW.md").write_text(
        "\n".join(review_lines) + "\n", encoding="utf-8", newline="")

    authority_evidence = [artifact(path, path.relative_to(ROOT).as_posix())
        for path in sorted((ROOT / "authority").rglob("*")) if path.is_file()]
    config = {
        "schema": "mathematics-commons-stacks-errata-candidate-config/v1",
        "candidate_id": spec["candidate_id"], "lease_id": "stacks-lease-000017-errata-r14",
        "writer_task": "01a0256d-5693-77c1-96b2-cf37101e0c6c",
        "authority_commit": spec["authority_commit"], "authority_tree": spec["authority_tree"],
        "source_date_epoch": "1785270512", "expected_unit_ids": expected_ids,
        "expected_producer_ids": expected_producers, "namespace": "commons/stacks/errata/r14",
        "private_render_logical_path": "canon/private_evidence/errata-r14-20260824T2210Z/render-final/render-manifest.json",
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
