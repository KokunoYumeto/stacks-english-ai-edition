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
PRODUCER_SHA256 = "71C77AD80E68F10107D1295E4DEF985954B315FBAC246F2910AFDECBECE48798"
PRODUCER_BYTES = 341_079
UPSTREAM_LOCK_SHA256 = "B195ECC83AB0F32C574A60D1FDBA9B0DA4D35B04E0DF7CB106DC9C0FDAD99C0D"
COPYING_SHA256 = "4B2C8FC390F802CD92F0622DC00A708A588BEC54D0145D2EE135D6D7672BFE85"
GENERATED_AT = "2026-08-24T06:51:28Z"

CONTROL_EVIDENCE = {
    "DECISION_20260824_R8_ALG_330_341.json": "6761ECF355233007C2D8AD68A3CC5C54F7563B44EE28B082FE14262E58D11CE9",
    "R8_ALG_330_341_INTAKE.json": "048E368684043F24BBCD6F255899D973B7CBECAC63B08CB18106E6770B0AFB3D",
    "R8_ALG_330_341_REPLAY.json": "A993D45F7F2B3E5305733334A9881CB54BF859414AA5931BD08CAC2C4ADA99A1",
    "R8_ALG_330_341_REVIEW.md": "73CE5C616E736E27C243AE6DBAE4F2963B29E9DE1767538F7632F0094F47FB1C",
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
    op(330, 44038, 44040,
       "It follows that $R'/R$ is annihilated by a power of $\\mathfrak m$\n"
       "(Lemma \\ref{lemma-Noetherian-power-ideal-kills-module}).\n"
       "By Lemma \\ref{lemma-hart-serre-loc-thm} this",
       "It follows that $R'/R$ is annihilated by a power of $\\mathfrak m$\n"
       "(Lemma \\ref{lemma-Noetherian-power-ideal-kills-module}).\n"
       "If $x \\in R$, there is nothing to prove, so assume $x \\notin R$.\n"
       "Then $R \\to R'$ is not an isomorphism and has zero kernel.\n"
       "Since $\\text{depth}(R) \\geq 2$, there is a nonzerodivisor\n"
       "$t \\in \\mathfrak m$ on $R$. As $t$ is invertible in $Q(R)$, it\n"
       "is a nonzerodivisor on $R' \\subset Q(R)$. Thus $\\mathfrak m$ is\n"
       "not an associated prime of $R'$, and $R' \\not = 0$.\n"
       "By~Lemma~\\ref{lemma-hart-serre-loc-thm} this"),
    op(331, 44071, 44071,
       "all its associates primes",
       "all its associated primes"),
    op(332, 44078, 44078,
       "(use Lemma \\ref{lemma-depth-in-ses} for example)",
       "(use Lemma \\ref{lemma-depth-in-ses} for example)."),
    op(331, 44108, 44108,
       "the set of associate primes",
       "the set of associated primes"),
    op(333, 44287, 44288,
       "Moreover $K$ is the field of fractions of the domain.\n"
       "$S = K[X_1, \\ldots, X_{r + 1}]/(G)$.",
       "Moreover $K$ is the field of fractions of the domain\n"
       "$S = k[X_1, \\ldots, X_{r + 1}]/(G)$.") ,
    op(334, 44298, 44298,
       "S \\otimes_k \\Omega_k \\oplus",
       "S \\otimes_k \\Omega_{k/\\mathbf{F}_p} \\oplus"),
    op(334, 44314, 44314,
       "K \\otimes_k \\Omega_k \\oplus",
       "K \\otimes_k \\Omega_{k/\\mathbf{F}_p} \\oplus"),
    op(335, 44324, 44324,
       "$K \\otimes_k \\Omega_{k/\\mathbf{F}_p} \\to \\Omega_{S/\\mathbf{F}_p}$",
       "$K \\otimes_k \\Omega_{k/\\mathbf{F}_p} \\to \\Omega_{K/\\mathbf{F}_p}$"),
    op(336, 44389, 44393,
       "Assume $K$ is formally smooth over $k$.\n"
       "By Lemma \\ref{lemma-ses-formally-smooth} we see that\n"
       "$K \\otimes_k \\Omega_{k/\\mathbf{Z}} \\to \\Omega_{K/\\mathbf{Z}}$\n"
       "is injective. Hence $K$ is separable over $k$ by\n"
       "Lemma \\ref{lemma-separable-differentials}.",
       "Assume $K$ is formally smooth over $k$.\n"
       "If $k$ has characteristic zero, then $K/k$ is separable.\n"
       "Thus we may assume that $k$ has characteristic $p > 0$.\n"
       "By Lemma \\ref{lemma-ses-formally-smooth} we see that\n"
       "$K \\otimes_k \\Omega_{k/\\mathbf{F}_p} \\to\n"
       "\\Omega_{K/\\mathbf{F}_p}$\n"
       "is injective. Hence $K$ is separable over $k$ by\n"
       "Lemma \\ref{lemma-separable-differentials}."),
    op(337, 44405, 44405,
       "the fact that a vector spaces is free",
       "the fact that a vector space is free"),
    op(339, 44500, 44504,
       "This is a combination of\n"
       "Lemmas \\ref{lemma-characterize-separable-field-extensions},\n"
       "\\ref{lemma-fields-are-formally-smooth}\n"
       "\\ref{lemma-formally-smooth-implies-separable}, and\n"
       "\\ref{lemma-separable-differentials}.",
       "This is a combination of\n"
       "Lemmas \\ref{lemma-characterize-separable-field-extensions},\n"
       "\\ref{lemma-fields-are-formally-smooth},\n"
       "\\ref{lemma-characterize-formally-smooth-field-extension},\n"
       "\\ref{lemma-formally-smooth-implies-separable}, and\n"
       "\\ref{lemma-separable-differentials}."),
    op(340, 44547, 44547,
       "minimum polynomial",
       "minimal polynomial"),
    op(341, 44549, 44549,
       "$P_1, \\ldots, P_r$ is a regular sequence",
       "$P_1, \\ldots, P_r$ are a regular sequence"),
    op(341, 44550, 44550,
       "$k(x_1, \\ldots, x_r)[Y_1, \\ldots, Y_r]$",
       "$k(x_1, \\ldots, x_d)[Y_1, \\ldots, Y_r]$"),
    op(341, 44551, 44551,
       "$L = k(x_1, \\ldots, x_r)[Y_1, \\ldots, Y_r]/(P_1, \\ldots, P_r)$",
       "$L = k(x_1, \\ldots, x_d)[Y_1, \\ldots, Y_r]/(P_1, \\ldots, P_r)$"),
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
    required = [f"ALGEBRA-{number}" for number in range(330, 342)]
    if any(producer_ids.count(producer) != 1 for producer in required):
        raise AssertionError("producer ledger does not contain each ALGEBRA-330..341 row exactly once")

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
    if len(mapped) != 15:
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

    decision_path = args.control_root / "DECISION_20260824_R8_ALG_330_341.json"
    replay_path = args.control_root / "R8_ALG_330_341_REPLAY.json"
    decision_rows = json.loads(decision_path.read_text(encoding="utf-8"))["accepted"]
    replay_rows = json.loads(replay_path.read_text(encoding="utf-8"))["accepted"]
    accepted_ids = [f"MC-STK-ERR-{number:04d}" for number in range(675, 686)]
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
        "candidate_id": "stacks-errata-a04446e-r8",
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
        ("ERR-R8-D0001", "Bind R8 exclusively to the active errata/r8 lease and frozen upstream commit/tree.", "Preserves the single-writer and immutable-authority boundary."),
        ("ERR-R8-D0002", "Assign MC-STK-ERR-0675..0685 in ascending accepted-producer order after admitted R7.", "Creates a deterministic, globally unique stable-ID sequence without assigning an ID to the rejected row."),
        ("ERR-R8-D0003", "Apply only exact nonoverlapping half-open UTF-8 spans in descending byte order.", "Prevents contextual or global replacement from changing unrelated text."),
        ("ERR-R8-D0004", "Treat ALGEBRA-330 as a proof-gap repair while leaving the theorem statement unchanged.", "The theorem is valid, but the invocation of the four-way lemma omitted required verifications."),
        ("ERR-R8-D0005", "Reject ALGEBRA-338 as no defect and preserve the original characteristic-zero assertion.", "Its enumeration already completes the conditional; replacing it by equivalence changes logical force."),
        ("ERR-R8-D0006", "Keep canonical locale bytes and the literal upstream mirror outside the corrected English payload.", "Corrections belong only to Stacks — English AI Edition."),
        ("ERR-R8-D0007", "Do not contact or submit this AI-derived correction set to upstream Stacks maintainers.", "The maintained AI-open English edition is the authorized correction surface."),
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
    rejection = {
        "schema": "mathematics-commons-stacks-candidate-rejection/v1",
        "id": "ERR-R8-R0001",
        "timestamp_utc": GENERATED_AT,
        "producer_id": "ALGEBRA-338",
        "disposition": "rejected",
        "reason": "The enumerated clauses grammatically complete the preceding If-then assertion and state that all five claims hold; replacing this with an equivalence predicate changes the logical force.",
    }
    (ROOT / "rejections.jsonl").write_text(
        json.dumps(rejection, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="",
    )

    authority_evidence = []
    for path in sorted((ROOT / "authority").rglob("*")):
        if path.is_file():
            authority_evidence.append(evidence(path, path.relative_to(ROOT).as_posix()))
    config = {
        "schema": "mathematics-commons-stacks-errata-candidate-config/v1",
        "candidate_id": "stacks-errata-a04446e-r8",
        "lease_id": "stacks-lease-000011-errata-r8",
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
                "ordered_structure_exceptions": {
                    "references_added": [
                        {
                            "index_0based": 2760,
                            "payload": "\\ref{lemma-characterize-formally-smooth-field-extension}",
                        }
                    ]
                },
                "build_exceptions": {
                    "candidate_only_undefined_reference_targets": {},
                    "candidate_page_delta": 1,
                },
            }
        },
        "authority_evidence": authority_evidence,
        "proof_closure": {
            "producer_rows": 12,
            "accepted": 11,
            "operations": 15,
            "rejected": 1,
            "prior_overlay_aliases": 0,
            "packet_duplicates": 0,
            "unresolved": 0,
        },
    }
    write_json(ROOT / "candidate.config.json", config)
    print(json.dumps({
        "passed": True,
        "units": 11,
        "operations": 15,
        "payload_bytes": len(payload),
        "payload_sha256": sha_bytes(payload),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
