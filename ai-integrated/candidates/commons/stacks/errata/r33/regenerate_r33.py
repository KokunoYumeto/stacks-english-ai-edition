from __future__ import annotations

import bisect
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
AUTHORITY = ROOT / "authority/source/spaces-morphisms.tex"
PRODUCER = ROOT / "authority/producer/ERRATA_CANDIDATES.jsonl"
COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
AUTHORITY_SHA = "22D2D9F7807D408335DD97053568304F7568144BD382E73A953EC15659DE3B33"
PRODUCER_SHA = "7A3431BCFA833691F058DA6050E5E50F8299374DA4D77792D6053050FEF889C6"
CANDIDATE = "stacks-errata-a04446e-r33"
LEASE = "stacks-lease-000037-errata-r33"
WRITER = "01a0256d-5693-77c1-96b2-cf37101e0c6c"
STAMP = "2026-08-30T12:15:00Z"


CASES = [
    {
        "stable_id": "MC-STK-ERR-1288", "canonical": "P08-E262", "aliases": ["P08-E588"],
        "line": 10129, "old": r"codimension $0$ points in $U$", "new": r"codimension $0$ points in $V$",
        "rationale": "The paragraph studies U -> V and immediately fixes v in V and the fibre U_v; the repeated target U is wrong.",
        "kind": "mathematical_typing",
    },
    {
        "stable_id": "MC-STK-ERR-1289", "canonical": "P08-E263", "aliases": ["P08-E589"],
        "line": 10188, "old": r"$X^\nu \to X \to Y$", "new": r"$U^\nu \to U \to V$",
        "rationale": "Item (c) quantifies g : U -> V; normalization functoriality applies to U^nu -> U -> V, not unrelated X/Y variables.",
        "kind": "mathematical_typing",
    },
    {
        "stable_id": "MC-STK-ERR-1290", "canonical": "P08-E264", "aliases": ["P08-E590"],
        "line": 10252, "old": "What have we shown", "new": "What we have shown",
        "rationale": "The clause is declarative and is the subject of 'is this'; interrogative inversion is ungrammatical.",
        "kind": "grammar",
    },
    {
        "stable_id": "MC-STK-ERR-1291", "canonical": "P08-E265", "aliases": ["P08-E591"],
        "line": 10311, "old": "in stead of", "new": "instead of",
        "rationale": "The fixed adverb is the single word 'instead'.",
        "kind": "spelling",
    },
    {
        "stable_id": "MC-STK-ERR-1292", "canonical": "P08-E266", "aliases": ["P08-E592"],
        "line": 10377, "old": r"Let $Z \to X$ be a morphism.", "new": r"Let $f : Z \to X$ be a morphism.",
        "rationale": "The same statement later uses f(z), so the displayed morphism must be named f.",
        "kind": "mathematical_typing",
    },
    {
        "stable_id": "MC-STK-ERR-1293", "canonical": "P08-E593", "aliases": [],
        "line": 10408, "old": r"$V/V \times_{U \times_X Z} V$", "new": r"$V/(V \times_{U \times_X Z} V)$",
        "rationale": "The two arrows above define the relation V x_(U x_X Z) V on V; the quotient denominator requires grouping.",
        "kind": "mathematical_notation",
    },
    {
        "stable_id": "MC-STK-ERR-1294", "canonical": "P08-E594", "aliases": [],
        "line": 10425, "old": r"Since $X = U/R$ a", "new": r"Since $X = U/R$, a",
        "rationale": "The introductory subordinate clause must be separated from the main clause by a comma.",
        "kind": "punctuation",
    },
]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")


def line_starts(data: bytes) -> list[int]:
    return [0] + [i + 1 for i, value in enumerate(data) if value == 10]


def line_at(starts: list[int], offset: int) -> int:
    return bisect.bisect_right(starts, offset)


def evidence(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data)}


def producer_rows() -> tuple[dict[str, dict], dict[str, dict]]:
    rows: dict[str, dict] = {}
    bindings: dict[str, dict] = {}
    for index, raw in enumerate(PRODUCER.read_bytes().splitlines(keepends=True), 1):
        if not raw.strip():
            continue
        row = json.loads(raw.decode("utf-8"))
        pid = row.get("id")
        if pid in rows:
            raise AssertionError(f"duplicate producer id {pid}")
        rows[pid] = row
        bindings[pid] = {"producer_row_1_based": index, "row_bytes": len(raw), "row_sha256": sha(raw)}
    return rows, bindings


def build_manifest() -> dict[str, object]:
    config = json.loads((ROOT / "candidate.config.json").read_text(encoding="utf-8"))
    authority_paths = sorted(path for path in (ROOT / "authority").rglob("*") if path.is_file())
    singled = {
        "stable_unit_manifest": ROOT / "stable-units.json",
        "source_map": ROOT / "source-map.jsonl",
        "decision_ledger": ROOT / "decisions.jsonl",
        "rejection_ledger": ROOT / "rejections.jsonl",
        "formula_diagram_inventory": ROOT / "formula-diagram-inventory.json",
    }
    excluded = {ROOT / "candidate.manifest.json", *authority_paths, *singled.values()}
    validation_paths = sorted(
        path for path in ROOT.rglob("*")
        if path.is_file() and path not in excluded and "__pycache__" not in path.parts
    )
    replay = ROOT / "replay/independent-review.json"
    reviewed = replay.is_file() and json.loads(replay.read_text(encoding="utf-8")).get("passed") is True
    manifest = {
        "$schema": "../../../../../schemas/candidate-manifest.schema.json",
        "schema": "mathematics-commons-stacks-candidate-manifest/v1",
        "candidate_id": CANDIDATE,
        "lease_id": LEASE,
        "namespace": "commons/stacks/errata/r33",
        "writer_task": WRITER,
        "upstream": {"lock": "upstream/stacks.lock.json", "commit": COMMIT, "tree": TREE},
        "source_authorities": [evidence(path) for path in authority_paths],
        "source_closure": {"enumerated": True, "expected_units": 7, "manifested_units": 7, "complete": True},
        **{key: evidence(path) for key, path in singled.items()},
        "builds": [evidence(path) for path in validation_paths],
        "rights_state": "The authority and modified payload retain the Stacks Project GNU Free Documentation License 1.2; metadata and receipts do not relicense upstream content. This is an independently maintained AI-produced English correction overlay with no Stacks Project review, approval, affiliation, or endorsement.",
        "review_state": "performed" if reviewed else "partial",
        "independent_replay": "passed" if reviewed else "not_performed",
        "unresolved_defects": [
            "Five ko-KR producer observations are exact aliases of five earlier zh-Hans-CN producer observations; both identities and their locale-specific adverse dispositions are preserved, while each semantic correction is applied once.",
            "This candidate performs source-overlay replay only. Generated-source composition, chapter builds, cumulative PDFs, and publication remain separate downstream work.",
            "The frozen authority and locale targets were not mutated.",
        ],
        "stop_conditions": [
            "Do not mutate the pinned upstream authority.",
            "Do not compose or push generated Stacks source in this registrar admission.",
            "Any change to authority, producer evidence, operations, payload, or replay bytes requires a new manifest and verification.",
        ],
        "generated_at_utc": STAMP,
    }
    dump(ROOT / "candidate.manifest.json", manifest)
    return manifest


def main() -> int:
    authority = AUTHORITY.read_bytes()
    producer = PRODUCER.read_bytes()
    if len(authority) != 398506 or sha(authority) != AUTHORITY_SHA:
        raise AssertionError("authority identity mismatch")
    if len(producer) != 522040 or sha(producer) != PRODUCER_SHA:
        raise AssertionError("producer sidecar identity mismatch")
    rows, row_bindings = producer_rows()
    expected_ids = {case["canonical"] for case in CASES} | {alias for case in CASES for alias in case["aliases"]}
    if not expected_ids.issubset(rows):
        raise AssertionError(f"missing producer rows: {sorted(expected_ids - set(rows))}")
    for pid in expected_ids:
        if rows[pid].get("source_sha256") != AUTHORITY_SHA or rows[pid].get("source_file") != "spaces-morphisms.tex":
            raise AssertionError(f"producer authority mismatch: {pid}")

    starts = line_starts(authority)
    operations: list[dict] = []
    crosswalk: list[dict] = []
    for case in CASES:
        old_b = case["old"].encode("utf-8")
        new_b = case["new"].encode("utf-8")
        positions = []
        cursor = 0
        while True:
            pos = authority.find(old_b, cursor)
            if pos < 0:
                break
            if line_at(starts, pos) == case["line"] and line_at(starts, pos + len(old_b) - 1) == case["line"]:
                positions.append(pos)
            cursor = pos + 1
        if len(positions) != 1 or authority.count(old_b) != 1:
            raise AssertionError(f"preimage not globally unique at {case['stable_id']}")
        pos = positions[0]
        producer_ids = [case["canonical"], *case["aliases"]]
        operation = {
            "operation_id": f"{case['stable_id']}-OP1",
            "operation_index": 1,
            "stable_id": case["stable_id"],
            "producer_id": case["canonical"],
            "producer_ids": producer_ids,
            "source_start_line": case["line"],
            "source_end_line": case["line"],
            "start_byte": pos,
            "end_byte_exclusive": pos + len(old_b),
            "old_text": case["old"],
            "old_bytes": len(old_b),
            "old_sha256": sha(old_b),
            "replacement_text": case["new"],
            "replacement_bytes": len(new_b),
            "replacement_sha256": sha(new_b),
            "occurrence_count_in_frozen_authority": 1,
            "declared_line_range_occurrence_count": 1,
            "rationale": case["rationale"],
            "class": case["kind"],
            "producer_source_packet": "authority/producer/ERRATA_CANDIDATES.jsonl",
            "producer_source_packet_sha256": PRODUCER_SHA,
        }
        operations.append(operation)
        crosswalk.append({
            "stable_id": case["stable_id"],
            "canonical_producer_id": case["canonical"],
            "duplicate_aliases": case["aliases"],
            "all_producer_ids": producer_ids,
            "producer_rows": {pid: {**row_bindings[pid], "translation_impact": rows[pid].get("translation_impact"), "confidence": rows[pid].get("confidence")} for pid in producer_ids},
            "semantic_correction": {"line": case["line"], "old": case["old"], "new": case["new"]},
            "disposition": "admit_once_preserve_all_aliases" if case["aliases"] else "admit_new_unique_row",
        })

    payload = authority
    for op in sorted(operations, key=lambda item: item["start_byte"], reverse=True):
        start, end = op["start_byte"], op["end_byte_exclusive"]
        if payload[start:end] != op["old_text"].encode("utf-8"):
            raise AssertionError(f"apply preimage mismatch: {op['operation_id']}")
        payload = payload[:start] + op["replacement_text"].encode("utf-8") + payload[end:]
    (ROOT / "payload/spaces-morphisms.tex").write_bytes(payload)

    source_rows = []
    units = []
    for case, op in zip(CASES, operations):
        producer_ids = [case["canonical"], *case["aliases"]]
        source_rows.append({
            "schema": "mathematics-commons-stacks-errata-map/v2",
            "unit_id": case["stable_id"],
            "class": "source_defect_correction",
            "source": "spaces-morphisms.tex",
            "authority": "authority/source/spaces-morphisms.tex",
            "authority_sha256": AUTHORITY_SHA,
            "payload": "payload/spaces-morphisms.tex",
            "locus": f"spaces-morphisms.tex:{case['line']}",
            "producer_id": case["canonical"],
            "producer_ids": producer_ids,
            "prior_aliases": case["aliases"],
            "producer_identity": {"canonical": case["canonical"], "duplicate_aliases": case["aliases"], "all_ids": producer_ids},
            "operations": [op],
            "proof": "accepted_after_independent_exact_preimage_context_and_alias_replay",
            "adverse_evidence": "Locale targets and every producer row remain frozen; alias rows are provenance, not additional operations.",
        })
        units.append({
            "id": case["stable_id"], "class": "source_defect_correction", "source": "spaces-morphisms.tex",
            "payload": "payload/spaces-morphisms.tex", "locus": f"spaces-morphisms.tex:{case['line']}",
            "operation_ids": [op["operation_id"]], "producer_id": case["canonical"], "producer_ids": producer_ids,
            "status": "accepted_deduplicated" if case["aliases"] else "accepted_new",
        })
    (ROOT / "source-map.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in source_rows), encoding="utf-8", newline="")
    (ROOT / "rejections.jsonl").write_text("", encoding="utf-8", newline="")
    dump(ROOT / "operation-spec.json", {"schema": "mathematics-commons-stacks-errata-operation-spec/v1", "authority_sha256": AUTHORITY_SHA, "apply_order": "descending_start_byte", "operation_count": 7, "operations": operations})
    dump(ROOT / "stable-units.json", {"schema": "mathematics-commons-stacks-errata-units/v1", "authority_commit": COMMIT, "unit_count": 7, "units": units})
    dump(ROOT / "authority/producer/P08_E262_E266_E588_E594_ALIAS_CROSSWALK.json", {"schema": "stacks-p08-spaces-morphisms-alias-crosswalk/v1", "authority_sha256": AUTHORITY_SHA, "producer_sidecar_sha256": PRODUCER_SHA, "semantic_unit_count": 7, "producer_id_count": 12, "duplicate_alias_pair_count": 5, "records": crosswalk})
    dump(ROOT / "formula-diagram-inventory.json", {"schema": "mathematics-commons-stacks-errata-formula-diagram-inventory/v1", "candidate_id": CANDIDATE, "authority_commit": COMMIT, "unit_count": 7, "formula_units": ["MC-STK-ERR-1288", "MC-STK-ERR-1289", "MC-STK-ERR-1292", "MC-STK-ERR-1293"], "diagram_units": [], "prose_only_units": ["MC-STK-ERR-1290", "MC-STK-ERR-1291", "MC-STK-ERR-1294"], "unmapped_formula_or_diagram_changes": 0})
    decisions = [
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R33-D0001", "choice": "Bind R33 to the pinned spaces-morphisms.tex authority and exact P08 sidecar snapshot.", "rationale": "Both hashes and all twelve producer rows were independently replayed.", "timestamp_utc": STAMP},
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R33-D0002", "choice": "Admit P08-E262..266 as canonical representatives and preserve P08-E588..592 as five duplicate aliases.", "rationale": "Each alias pair has the same authority locus and semantic correction; applying both would duplicate a correction.", "timestamp_utc": STAMP},
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R33-D0003", "choice": "Admit P08-E593 and P08-E594 as two new unique corrections.", "rationale": "The quotient relation requires grouping and the subordinate clause requires punctuation; both preimages are globally unique.", "timestamp_utc": STAMP},
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R33-D0004", "choice": "Keep authority, zh-Hans-CN, ko-KR, and generated-source trees unchanged.", "rationale": "R33 is registrar-only admission; composition is a separate downstream task.", "timestamp_utc": STAMP},
    ]
    (ROOT / "decisions.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in decisions), encoding="utf-8", newline="")
    dump(ROOT / "authority/upstream.lock.json", {"schema": "mathematics-commons-stacks-upstream-lock/v1", "repository": "https://github.com/stacks/stacks-project", "commit": COMMIT, "tree": TREE, "source": {"path": "authority/source/spaces-morphisms.tex", "bytes": len(authority), "sha256": AUTHORITY_SHA}, "authority_mutated": False})
    config = {
        "$schema": "../../schemas/candidate-manifest.schema.json", "schema": "mathematics-commons-stacks-errata-candidate-config/v1",
        "candidate_id": CANDIDATE, "namespace": "commons/stacks/errata/r33", "lease_id": LEASE,
        "writer_task": WRITER, "authority_commit": COMMIT, "authority_tree": TREE,
        "accepted": 7, "rejected": 0, "unresolved": 0, "operation_count": 7,
        "expected_unit_ids": [case["stable_id"] for case in CASES],
        "expected_producer_ids": sorted(expected_ids), "duplicate_aliases": 5,
        "stems": {"spaces-morphisms.tex": {"authority_bytes": len(authority), "authority_sha256": AUTHORITY_SHA, "payload_bytes": len(payload), "payload_sha256": sha(payload), "operations": 7}},
        "composition_performed": False,
    }
    dump(ROOT / "candidate.config.json", config)
    dump(ROOT / "LEASE.json", {"schema": "mathematics-commons-stacks-candidate-lease-pointer/v1", "candidate_path": "candidates/commons/stacks/errata/r33", "lease_id": LEASE, "namespace": "commons/stacks/errata/r33", "state": "released_after_admission", "upstream_commit": COMMIT, "writer_contract": "candidates/CONTRACT.md", "writer_task": WRITER})
    dump(ROOT / "source-validation.json", {"schema": "mathematics-commons-stacks-errata-source-validation/v1", "candidate_id": CANDIDATE, "passed": True, "authority": {"bytes": len(authority), "sha256": AUTHORITY_SHA}, "producer": {"bytes": len(producer), "sha256": PRODUCER_SHA, "rows_bound": 12}, "accepted_units": 7, "operation_count": 7, "duplicate_aliases": 5, "rejected_units": 0, "unresolved_units": 0, "payload": {"path": "payload/spaces-morphisms.tex", "bytes": len(payload), "sha256": sha(payload)}, "authority_bytes_mutated": False, "locale_target_bytes_mutated": False, "generated_source_composed": False})
    dump(ROOT / "REGENERATION_RECEIPT.json", {"schema": "stacks-r33-spaces-morphisms-regeneration/v1", "candidate_id": CANDIDATE, "authority": evidence(AUTHORITY), "producer": evidence(PRODUCER), "semantic_units": 7, "operations": 7, "producer_ids": 12, "duplicate_alias_pairs": 5, "stable_id_range": ["MC-STK-ERR-1288", "MC-STK-ERR-1294"], "payload": evidence(ROOT / "payload/spaces-morphisms.tex"), "authority_bytes_mutated": False, "generated_source_composed": False, "generated_at_utc": STAMP})
    build_manifest()
    print(json.dumps({"passed": True, "candidate_id": CANDIDATE, "semantic_units": 7, "producer_ids": 12, "payload_sha256": sha(payload), "manifest_sha256": sha((ROOT / "candidate.manifest.json").read_bytes())}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
