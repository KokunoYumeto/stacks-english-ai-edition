from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
AUTHORITY_SHA256 = "FA8BB92E58A4F78A2BD01B3B6A4A87DE0A0D279F5DD90641B574DD5FBFFFA4F3"
AUTHORITY_BYTES = 1_771_230
PRODUCER_SHA256 = "ECE134C64FCB7091B665DF5CBDB31168386C9812F94EAFC0A034F80EFFB16143"
PRODUCER_BYTES = 334_819
UPSTREAM_LOCK_SHA256 = "B195ECC83AB0F32C574A60D1FDBA9B0DA4D35B04E0DF7CB106DC9C0FDAD99C0D"
COPYING_SHA256 = "4B2C8FC390F802CD92F0622DC00A708A588BEC54D0145D2EE135D6D7672BFE85"
GENERATED_AT = "2026-08-24T04:09:15Z"

CONTROL_EVIDENCE = {
    "DECISION_20260824_R7_ALG_315_329.json": "27E745BE87C048359C3DB67B771D837571BD51FBF036E08B2F4E71A109780CE6",
    "R7_ALG_315_329_INTAKE.json": "0D7BF0007F2F6CDE9778C4507FD6039A45D584ECC3EDE0D44FF220B1ECF5C9FF",
    "R7_ALG_315_329_REPLAY.json": "2AF67F975E3641636589E5B0A0E98A5F6484259F98E606190F06F4C2E5EA6B04",
    "R7_ALG_315_329_REVIEW.md": "6FF60FA2BB0C684C6AB94ADED199C1A58110C80B1FA2F197A40F63C1105A3242",
}


def op(producer: int, line_start: int, line_end: int, old: str, new: str) -> dict:
    return {
        "producer_id": f"ALGEBRA-{producer}",
        "source_start_line": line_start,
        "source_end_line": line_end,
        "old_text": old,
        "replacement_text": new,
    }


OPERATIONS = [
    op(315, 31171, 31172,
       "Let $R \\to S$ be a finite type ring map.\nLet $\\mathfrak q \\subset S$ be a prime.",
       "Let $R \\to S$ be a finite type ring map.\nLet $\\mathfrak q \\subset S$ be a prime.\n"
       "Let $\\mathfrak p \\subset R$ be the inverse image of $\\mathfrak q$."),
    op(316, 31187, 31187, "\\overline{q}", "\\overline{\\mathfrak q}"),
    op(317, 31203, 31203,
       "\\kappa(\\mathfrak p)[t_1\\ldots, t_n]",
       "\\kappa(\\mathfrak p)[t_1, \\ldots, t_n]"),
    op(318, 31283, 31284,
       "we have $S_{\\mathfrak q} = S'_{\\mathfrak q'}$ for some\n"
       "$\\mathfrak q' \\subset S'$ lying over $\\mathfrak q$.",
       "we have $S_{\\mathfrak q} = S'_{\\mathfrak q'}$, where\n"
       "$\\mathfrak q' = S' \\cap \\mathfrak qS_{\\mathfrak p}$.") ,
    op(319, 31297, 31297, "\\subset", "\\to"),
    op(320, 31368, 31368, "x_n", "x_N"),
    op(320, 31371, 31371, "x_n", "x_N"),
    op(321, 31392, 31392, "\\dim_{\\mathfrak q}(S/k)", "\\dim_{\\mathfrak q}(S/R)"),
    op(321, 31396, 31396, "\\dim_{\\mathfrak q}(S/k)", "\\dim_{\\mathfrak q}(S/R)"),
    op(321, 31397, 31397, "\\dim_{\\mathfrak q}(S/k)", "\\dim_{\\mathfrak q}(S/R)"),
    op(322, 31457, 31457, "$x_{ij}$", "$x_{ji}$"),
    op(323, 31481, 31481, "$f_{ij}$", "$f_{ji}$"),
    op(324, 31659, 31659, "$C$", "$S$"),
    op(325, 31685, 31685, "x_n", "x_m"),
    op(325, 31688, 31688, "x_n", "x_m"),
    op(325, 31692, 31692, "x_n", "x_m"),
    op(326, 31708, 31708,
       "$S'$ of finite presentation over $R$",
       "$S'$ is of finite presentation over $R$"),
    op(326, 31736, 31736,
       "$S'$ of finite presentation over $R$",
       "$S'$ is of finite presentation over $R$"),
    op(327, 31644, 31644,
       "$R[y_1, \\ldots, y_m, y_{m + 1}]$",
       "$R[y_1, \\ldots, y_m]$ by $R[y_1, \\ldots, y_m, y_{m + 1}]$"),
    op(327, 31652, 31652,
       "$R[y_1, \\ldots, y_m, y_{m + 1}]$",
       "$R[y_1, \\ldots, y_m]$ by $R[y_1, \\ldots, y_m, y_{m + 1}]$"),
    op(328, 43650, 43650,
       "at the prime ideal which is the kernel of the map",
       "at the prime ideal $\\mathfrak q'$ which is the kernel of the map"),
    op(328, 43683, 43684,
       "at the prime ideal $\\mathfrak q'$\n"
       "given in the statement of the lemma",
       "at the inverse image of $\\mathfrak q'$ under the canonical map\n"
       "$R_{\\mathfrak p}^{sh} \\otimes_R S \\to\n"
       "R_{\\mathfrak p}^{sh} \\otimes_{R_{\\mathfrak p}} S_{\\mathfrak q}$"),
    op(329, 43832, 43832,
       "filtered colimit commute with tensor products",
       "filtered colimits commute with tensor products"),
]


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def write_json(path: Path, data: object) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="",
    )


def evidence(path: Path, relative: str) -> dict:
    return {"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)}


def line_offsets(data: bytes) -> list[int]:
    starts = [0]
    for match in re.finditer(b"\n", data):
        starts.append(match.end())
    return starts


def exact_operations(authority: bytes) -> list[dict]:
    starts = line_offsets(authority)
    mapped = []
    per_producer: dict[str, int] = {}
    for row in OPERATIONS:
        producer = row["producer_id"]
        per_producer[producer] = per_producer.get(producer, 0) + 1
        scope_start = starts[row["source_start_line"] - 1]
        scope_end = starts[row["source_end_line"]]
        old = row["old_text"].encode("utf-8")
        new = row["replacement_text"].encode("utf-8")
        scope = authority[scope_start:scope_end]
        if scope.count(old) != 1:
            raise AssertionError(f"{producer}: old span is not unique in bounded lines")
        start = scope_start + scope.index(old)
        end = start + len(old)
        mapped.append({
            **row,
            "operation_index": per_producer[producer],
            "start_byte": start,
            "end_byte_exclusive": end,
            "occurrence_count_in_frozen_authority": authority.count(old),
            "old_bytes": len(old),
            "old_sha256": sha_bytes(old),
            "replacement_bytes": len(new),
            "replacement_sha256": sha_bytes(new),
        })
    ordered = sorted(mapped, key=lambda row: row["start_byte"])
    for left, right in zip(ordered, ordered[1:]):
        if left["end_byte_exclusive"] > right["start_byte"]:
            raise AssertionError(f"overlap: {left['producer_id']} / {right['producer_id']}")
    return mapped


def apply_operations(authority: bytes, mapped: list[dict]) -> bytes:
    payload = authority
    for row in sorted(mapped, key=lambda item: item["start_byte"], reverse=True):
        start, end = row["start_byte"], row["end_byte_exclusive"]
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
    parser.add_argument("--control-root", type=Path, required=True)
    parser.add_argument("--upstream-lock", type=Path, required=True)
    parser.add_argument("--copying", type=Path, required=True)
    args = parser.parse_args()

    authority = args.authority.read_bytes()
    if len(authority) != AUTHORITY_BYTES or sha_bytes(authority) != AUTHORITY_SHA256:
        raise AssertionError("frozen authority identity mismatch")
    if b"\r" in authority or not authority.endswith(b"\n"):
        raise AssertionError("authority is not terminal-LF UTF-8/LF source")
    if args.producer_ledger.stat().st_size != PRODUCER_BYTES or sha256(args.producer_ledger) != PRODUCER_SHA256:
        raise AssertionError("producer ledger identity mismatch")
    if sha256(args.upstream_lock) != UPSTREAM_LOCK_SHA256 or sha256(args.copying) != COPYING_SHA256:
        raise AssertionError("upstream lock or COPYING identity mismatch")
    for name, expected in CONTROL_EVIDENCE.items():
        if sha256(args.control_root / name) != expected:
            raise AssertionError(f"control evidence mismatch: {name}")

    producer_rows = list(csv.DictReader(args.producer_ledger.read_text(encoding="utf-8").splitlines()))
    producer_ids = [row["id"] for row in producer_rows]
    required = [f"ALGEBRA-{number}" for number in range(315, 330)]
    if any(producer_ids.count(producer) != 1 for producer in required):
        raise AssertionError("producer ledger does not contain each ALGEBRA-315..329 row exactly once")

    generated = [
        ROOT / "authority" / "source" / "algebra.tex",
        ROOT / "authority" / "producer" / "SOURCE_DEFECT_LEDGER.csv",
        ROOT / "authority" / "upstream.lock.json",
        ROOT / "authority" / "COPYING",
        ROOT / "payload" / "algebra.tex",
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

    mapped = exact_operations(authority)
    if len(mapped) != 23:
        raise AssertionError("operation closure mismatch")
    payload = apply_operations(authority, mapped)

    authority_source = ROOT / "authority" / "source" / "algebra.tex"
    producer_copy = ROOT / "authority" / "producer" / "SOURCE_DEFECT_LEDGER.csv"
    payload_path = ROOT / "payload" / "algebra.tex"
    authority_source.parent.mkdir(parents=True)
    producer_copy.parent.mkdir(parents=True)
    payload_path.parent.mkdir(parents=True)
    authority_source.write_bytes(authority)
    payload_path.write_bytes(payload)
    shutil.copy2(args.producer_ledger, producer_copy)
    shutil.copy2(args.upstream_lock, ROOT / "authority" / "upstream.lock.json")
    shutil.copy2(args.copying, ROOT / "authority" / "COPYING")

    decision_path = args.control_root / "DECISION_20260824_R7_ALG_315_329.json"
    replay_path = args.control_root / "R7_ALG_315_329_REPLAY.json"
    decision_rows = json.loads(decision_path.read_text(encoding="utf-8"))["accepted"]
    replay_rows = json.loads(replay_path.read_text(encoding="utf-8"))["accepted"]
    accepted_ids = [f"MC-STK-ERR-{number:04d}" for number in range(660, 675)]
    if [row["canon_id"] for row in decision_rows] != accepted_ids:
        raise AssertionError("stable-ID assignment differs from bounded decision")
    replay_by_producer = {row["producer_id"]: row for row in replay_rows}

    ops_by_producer: dict[str, list[dict]] = {}
    for row in mapped:
        ops_by_producer.setdefault(row["producer_id"], []).append(row)
    stable_units = []
    source_rows = []
    formula_units, prose_units = [], []
    for decision in decision_rows:
        producer = decision["producer_id"]
        stable_id = decision["canon_id"]
        operations = sorted(ops_by_producer[producer], key=lambda row: row["operation_index"])
        if len(operations) != decision["operation_count"]:
            raise AssertionError(f"operation count differs from decision: {producer}")
        operation_rows = []
        for row in operations:
            operation_rows.append({
                "operation_id": f"{stable_id}-OP{row['operation_index']}",
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
        locus = "algebra.tex:" + decision["locus"]
        stable_units.append({
            "id": stable_id,
            "producer_id": producer,
            "class": decision["classification"],
            "source": "algebra.tex",
            "locus": locus,
            "payload": "payload/algebra.tex",
            "operation_ids": [row["operation_id"] for row in operation_rows],
            "status": "applied",
        })
        replay = replay_by_producer[producer]
        source_rows.append({
            "schema": "mathematics-commons-stacks-errata-map/v2",
            "unit_id": stable_id,
            "producer_id": producer,
            "source": "algebra.tex",
            "authority": "authority/source/algebra.tex",
            "authority_sha256": AUTHORITY_SHA256,
            "payload": "payload/algebra.tex",
            "locus": locus,
            "class": decision["classification"],
            "proof": f"Independent replay result: {replay['result']}. {replay['smallest_correction']}",
            "adverse_evidence": "Exact frozen-source and independent mathematical review evidence is bound under authority/canon; no translation or authority byte was used as the corrected payload.",
            "operations": operation_rows,
        })
        has_tex = any(
            "$" in row["old_text"] or "\\" in row["old_text"] or
            "$" in row["replacement_text"] or "\\" in row["replacement_text"]
            for row in operations
        )
        (formula_units if has_tex else prose_units).append(stable_id)

    write_json(ROOT / "stable-units.json", {
        "schema": "mathematics-commons-stacks-errata-units/v1",
        "authority_commit": "a04446e57ec1fbc252a871afcec7752fb2807b14",
        "unit_count": len(stable_units),
        "units": stable_units,
    })
    (ROOT / "source-map.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in source_rows),
        encoding="utf-8",
        newline="",
    )
    write_json(ROOT / "formula-diagram-inventory.json", {
        "schema": "mathematics-commons-stacks-errata-formula-diagram-inventory/v1",
        "candidate_id": "stacks-errata-a04446e-r7",
        "unit_count": len(stable_units),
        "formula_units": formula_units,
        "diagram_units": [],
        "prose_only_units": prose_units,
        "classification": "Each mapped unit is classified exactly once from its corrected span; no xymatrix span is changed.",
        "unmapped_formula_or_diagram_changes": 0,
    })
    write_json(ROOT / "operation-spec.json", {
        "schema": "mathematics-commons-stacks-errata-operation-spec/v1",
        "authority_sha256": AUTHORITY_SHA256,
        "operation_count": len(mapped),
        "apply_order": "descending_start_byte",
        "operations": mapped,
    })

    decisions = [
        ("ERR-R7-D0001", "Bind R7 exclusively to the active errata/r7 lease and frozen upstream commit/tree.", "Preserves the single-writer and immutable-authority boundary."),
        ("ERR-R7-D0002", "Assign MC-STK-ERR-0660..0674 in ascending producer order after admitted R6.", "Creates a deterministic, globally unique stable-ID sequence."),
        ("ERR-R7-D0003", "Apply only exact nonoverlapping half-open UTF-8 spans in descending byte order.", "Prevents contextual or global replacement from changing unrelated text."),
        ("ERR-R7-D0004", "Classify ALGEBRA-326 only as an editorial parallelism copy-edit.", "Does not inflate a grammatical repair into a mathematical defect."),
        ("ERR-R7-D0005", "Keep canonical locale bytes and the literal upstream mirror outside the corrected English payload.", "Corrections belong only to Stacks — English AI Edition."),
        ("ERR-R7-D0006", "Do not contact or submit this AI-derived correction set to upstream Stacks maintainers.", "The maintained AI-open English edition is the authorized correction surface."),
    ]
    (ROOT / "decisions.jsonl").write_text("".join(
        json.dumps({
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": row[0],
            "timestamp_utc": GENERATED_AT,
            "choice": row[1],
            "rationale": row[2],
            "supersedes": None,
        }, separators=(",", ":")) + "\n" for row in decisions
    ), encoding="utf-8", newline="")
    (ROOT / "rejections.jsonl").write_text("", encoding="utf-8", newline="")

    authority_evidence = []
    for path in sorted((ROOT / "authority").rglob("*")):
        if path.is_file():
            authority_evidence.append(evidence(path, path.relative_to(ROOT).as_posix()))
    config = {
        "schema": "mathematics-commons-stacks-errata-candidate-config/v1",
        "candidate_id": "stacks-errata-a04446e-r7",
        "lease_id": "stacks-lease-000010-errata-r7",
        "writer_task": "01a0256d-5693-77c1-96b2-cf37101e0c6c",
        "authority_commit": "a04446e57ec1fbc252a871afcec7752fb2807b14",
        "authority_tree": "3feeb703b931a6e7259782c10e7d1575adc83e5e",
        "source_date_epoch": "1785270512",
        "expected_unit_ids": accepted_ids,
        "operation_count": len(mapped),
        "stems": {
            "algebra": {
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
            "producer_rows": 15,
            "accepted": 15,
            "operations": 23,
            "rejected": 0,
            "prior_overlay_aliases": 0,
            "packet_duplicates": 0,
            "unresolved": 0,
        },
    }
    write_json(ROOT / "candidate.config.json", config)
    print(json.dumps({
        "passed": True,
        "units": 15,
        "operations": 23,
        "payload_bytes": len(payload),
        "payload_sha256": sha_bytes(payload),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
