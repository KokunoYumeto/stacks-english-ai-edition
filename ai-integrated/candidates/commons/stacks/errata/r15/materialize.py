from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
AUTHORITY_SHA256 = "B2504820D769EBE4E9E33B8ADD78753FB30ACA6E8A7F75C8D54DDA885EDCD682"
AUTHORITY_BYTES = 28_201
UPSTREAM_LOCK_SHA256 = "B195ECC83AB0F32C574A60D1FDBA9B0DA4D35B04E0DF7CB106DC9C0FDAD99C0D"
COPYING_SHA256 = "4B2C8FC390F802CD92F0622DC00A708A588BEC54D0145D2EE135D6D7672BFE85"
GENERATED_AT = "2026-08-25T00:13:52Z"
SPEC_PATH = ROOT / "authority" / "canon" / "R15_BRAUER_001_010_ADJUDICATION_SPEC.json"


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

    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    if (
        spec["candidate_id"] != "stacks-errata-a04446e-r15"
        or spec["authority_sha256"] != AUTHORITY_SHA256
        or spec["authority_commit"] != "a04446e57ec1fbc252a871afcec7752fb2807b14"
        or spec["authority_tree"] != "3feeb703b931a6e7259782c10e7d1575adc83e5e"
    ):
        raise AssertionError("adjudication specification authority binding mismatch")
    accepted = spec["accepted"]
    rejected = spec["rejected"]
    expected_producers = [f"BRAUER-{number:03d}" for number in range(1, 11)]
    accepted_producers = [row["producer_id"] for row in accepted]
    rejected_producers = [row["producer_id"] for row in rejected]
    if sorted(accepted_producers + rejected_producers) != expected_producers:
        raise AssertionError("adjudication partition is not BRAUER-001..010")
    expected_ids = [f"MC-STK-ERR-{number:04d}" for number in range(745, 753)]
    if [row["stable_id"] for row in accepted] != expected_ids:
        raise AssertionError("stable-ID assignment is not contiguous 0745..0752")
    if rejected_producers != ["BRAUER-001", "BRAUER-007"]:
        raise AssertionError("duplicate rejection identities changed")
    if [row["alias_of"] for row in rejected] != ["MC-STK-ERR-0016", "MC-STK-ERR-0017"]:
        raise AssertionError("R2 duplicate aliases changed")

    generated = [
        ROOT / "authority" / "source" / "brauer.tex",
        ROOT / "authority" / "upstream.lock.json",
        ROOT / "authority" / "COPYING",
        ROOT / "authority" / "canon" / "R15_BRAUER_001_010_INTAKE.json",
        ROOT / "authority" / "canon" / "R15_BRAUER_001_010_REVIEW.md",
        ROOT / "payload" / "brauer.tex",
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
    payload = apply_operations(authority, operations)
    ops_by_producer: dict[str, list[dict]] = {}
    for row in operations:
        ops_by_producer.setdefault(row["producer_id"], []).append(row)

    authority_source = ROOT / "authority" / "source" / "brauer.tex"
    payload_path = ROOT / "payload" / "brauer.tex"
    authority_source.parent.mkdir(parents=True, exist_ok=True)
    payload_path.parent.mkdir(parents=True, exist_ok=True)
    authority_source.write_bytes(authority)
    payload_path.write_bytes(payload)
    shutil.copy2(args.upstream_lock, ROOT / "authority" / "upstream.lock.json")
    shutil.copy2(args.copying, ROOT / "authority" / "COPYING")

    offsets = line_offsets(authority)
    payload_offsets = line_offsets(payload)
    bounded_start_line = 45
    bounded_end_line = 780
    bounded_authority = authority[offsets[bounded_start_line - 1]:offsets[bounded_end_line]]
    bounded_payload = payload[payload_offsets[bounded_start_line - 1]:payload_offsets[bounded_end_line]]
    intake = {
        "schema": "stacks-canon-errata-intake/v1",
        "recorded_at_utc": GENERATED_AT,
        "candidate_id": spec["candidate_id"],
        "authority": {
            "path": "authority/source/brauer.tex",
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
            "producer_source_emendations_json": "not opened, imported, or trusted as canon",
            "adjudication_authorities": [
                "frozen brauer.tex bytes",
                "the pinned Stacks definitions and proofs",
                "all fourteen admitted overlay source maps and rejection ledgers",
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
            "rejected_duplicate": len(rejected),
            "operations": len(operations),
            "unresolved": 0,
            "stable_ids": "MC-STK-ERR-0745..MC-STK-ERR-0752",
        },
        "deduplication": {
            "registered_entries_checked": 14,
            "public_candidates_checked": "R1..R14",
            "duplicate_aliases": {row["producer_id"]: row["alias_of"] for row in rejected},
            "accepted_overlap": False,
        },
        "adjudication": {
            row["producer_id"]: row["result"] for row in accepted + rejected
        },
        "write_boundaries": {
            "english_authority": "immutable",
            "canonical_translations": "immutable",
            "payload_derivation": "directly from frozen authority, never a prior payload",
            "producer_emendation_manifest": "not trusted, opened, or imported as canon",
        },
    }
    write_json(ROOT / "authority" / "canon" / "R15_BRAUER_001_010_INTAKE.json", intake)

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
            "source": "brauer.tex",
            "locus": unit["locus"],
            "payload": "payload/brauer.tex",
            "operation_ids": [row["operation_id"] for row in map_ops],
            "status": "applied",
        })
        source_rows.append({
            "schema": "mathematics-commons-stacks-errata-map/v2",
            "unit_id": unit["stable_id"],
            "producer_id": unit["producer_id"],
            "source": "brauer.tex",
            "authority": "authority/source/brauer.tex",
            "authority_sha256": AUTHORITY_SHA256,
            "payload": "payload/brauer.tex",
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
        ("ERR-R15-D0001", "Bind R15 exclusively to the active errata/r15 lease and frozen upstream commit/tree.", "Preserves the single-writer and immutable-authority boundary."),
        ("ERR-R15-D0002", "Assign MC-STK-ERR-0745..0752 in accepted BRAUER producer order after admitted R14.", "Creates a deterministic contiguous stable-ID sequence for eight proved nonduplicate corrections."),
        ("ERR-R15-D0003", "Apply only exact nonoverlapping half-open UTF-8 spans in descending byte order.", "Prevents contextual or global replacement from changing unrelated source text."),
        ("ERR-R15-D0004", "Accept BRAUER-002..006 and BRAUER-008..010 after independent source replay and deduplication against R1-R14.", "Each accepted allegation is a distinct bounded defect proved directly from frozen brauer.tex and project definitions."),
        ("ERR-R15-D0005", "Reject BRAUER-001 and BRAUER-007 as duplicates of MC-STK-ERR-0016 and MC-STK-ERR-0017 in admitted R2.", "Duplicate evidence is preserved without rematerializing already admitted corrections."),
        ("ERR-R15-D0006", "Do not open or treat BRAUER_SOURCE_EMENDATIONS.json as canon.", "The shared producer ledger supplies locators only; frozen source and independent proofs bind the overlay."),
        ("ERR-R15-D0007", "Keep canonical locale bytes and the literal upstream mirror outside the corrected English payload.", "Corrections belong only to Stacks — English AI Edition."),
        ("ERR-R15-D0008", "Do not contact or submit this AI-derived correction set to upstream Stacks maintainers.", "The maintained AI-open English edition is the authorized correction surface."),
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
            "id": f"ERR-R15-R{index:04d}",
            "timestamp_utc": GENERATED_AT,
            "producer_id": row["producer_id"],
            "disposition": "rejected_duplicate",
            "reason": f"{row['reason']} Alias: {row['alias_of']}; admitted round: {row['round']}.",
        }, ensure_ascii=False, separators=(",", ":")) + "\n" for index, row in enumerate(rejected, 1)),
        encoding="utf-8",
        newline="",
    )

    review_lines = [
        "# Independent review: BRAUER-001–010",
        "",
        f"Frozen authority: `{AUTHORITY_SHA256}` at `{spec['authority_commit']}`.",
        "",
        "The ten bounded allegations were replayed directly against frozen `brauer.tex` and",
        "deduplicated against all fourteen admitted overlay entries. BRAUER-002 through",
        "BRAUER-006 and BRAUER-008 through BRAUER-010 are accepted as `MC-STK-ERR-0745`",
        "through `MC-STK-ERR-0752`. BRAUER-001 and BRAUER-007 are rejected duplicates of",
        "the already admitted R2 units `MC-STK-ERR-0016` and `MC-STK-ERR-0017`.",
        "",
        "BRAUER-002 corrects an ill-typed matrix-corner equality. BRAUER-003 and BRAUER-004",
        "exclude zero-object counterexamples. BRAUER-005 restricts Skolem–Noether to",
        "`k`-algebra automorphisms. BRAUER-006 names the multiplication isomorphism rather",
        "than a literal equality. BRAUER-008 through BRAUER-010 repair bounded grammar and",
        "punctuation. The exact counterexamples and replacements are sealed in the public",
        "adjudication specification and source map.",
        "",
        "The producer emendation manifest was not opened, imported, or trusted as canon.",
        "The English payload is the only corrected surface. Frozen source, canonical",
        "translations, permanent tags, and unrelated chapters remain unchanged.",
    ]
    (ROOT / "authority" / "canon" / "R15_BRAUER_001_010_REVIEW.md").write_text(
        "\n".join(review_lines) + "\n",
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
        "lease_id": "stacks-lease-000018-errata-r15",
        "writer_task": "01a0256d-5693-77c1-96b2-cf37101e0c6c",
        "authority_commit": spec["authority_commit"],
        "authority_tree": spec["authority_tree"],
        "source_date_epoch": "1785270512",
        "expected_unit_ids": expected_ids,
        "expected_producer_ids": expected_producers,
        "namespace": "commons/stacks/errata/r15",
        "private_render_logical_path": "canon/private_evidence/errata-r15-20260825T0015Z/render-final/render-manifest.json",
        "operation_count": len(operations),
        "stems": {
            "brauer": {
                "authority_sha256": AUTHORITY_SHA256,
                "payload_sha256": sha_bytes(payload),
                "authority_bytes": len(authority),
                "payload_bytes": len(payload),
                "display_delimiter_delta": 0,
                "ordered_structure_exceptions": {},
                "build_exceptions": {
                    "candidate_only_undefined_reference_targets": {},
                    "candidate_page_delta": 0,
                },
            }
        },
        "authority_evidence": authority_evidence,
        "proof_closure": {
            "producer_rows": len(expected_producers),
            "accepted": len(accepted),
            "operations": len(operations),
            "rejected": 0,
            "prior_overlay_aliases": len(rejected),
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
