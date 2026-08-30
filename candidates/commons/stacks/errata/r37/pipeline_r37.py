from __future__ import annotations

import bisect
import csv
import hashlib
import io
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
CANDIDATE = "stacks-errata-a04446e-r37"
LEASE = "stacks-lease-000041-errata-r37"
WRITER = "01a0256d-5693-77c1-96b2-cf37101e0c6c"
STAMP = "2026-08-30T17:15:00Z"
ADMISSION_STAMP = "2026-08-30T17:58:40Z"
SOURCE = "sites-cohomology.tex"
SOURCE_SHA = "5B335CE2C7208A128B3C744B8828D93508063F41A4FABBCE2E921F890928895C"
LIVE_LEDGER_SHA = "087AEE1F16323974C8C95ECDC9596429D83362149214B96313107074F066A977"
AUDIT_SHA = "70A04B1873D1B977713717C06C7EDCCE1B2E45ED1C1A67D61C77FDEA6FFD41B3"
R36_OVERLAYS_SHA = "3835AD948ED6F420584459472E630C2442BC5815232E2FCB26B6ACCDC6F003D2"
R36_LEASES_SHA = "DE5F068855355930821CAFB47725ACFC1C044D74C817F773F9FAFA5B992E29D3"
PACKET_NAME = "SITES_COHOMOLOGY_SOURCE_DEFECT_LEDGER_014_027_029_037.csv"
PACKET_PATH = f"authority/producer/{PACKET_NAME}"
RECEIPT_PATH = "authority/producer/SITES_COHOMOLOGY_R37_PACKET_RECEIPT.json"
AUDIT_PATH = "authority/registrar/STACKS_R37_INDEPENDENT_AUDIT_20260830.json"
PRODUCER_IDS = [
    *[f"SITES-COHOMOLOGY-{number:03d}" for number in range(14, 28)],
    *[f"SITES-COHOMOLOGY-{number:03d}" for number in range(29, 38)],
]
STABLE_IDS = [f"MC-STK-ERR-{number}" for number in range(1313, 1336)]
STABLE_BY_PRODUCER = dict(zip(PRODUCER_IDS, STABLE_IDS, strict=True))
RIGHTS = (
    "The authority and modified payload retain the Stacks Project GNU Free "
    "Documentation License 1.2; metadata and receipts do not relicense upstream "
    "content. This independently maintained AI-produced English correction overlay "
    "has no Stacks Project review, approval, affiliation, or endorsement."
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="",
    )


def dump_registry(path: Path, value: object) -> None:
    """Preserve historical registry insertion and key order."""
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="",
    )


def dump_jsonl(path: Path, values: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n" for value in values
    )
    path.write_text(text, encoding="utf-8", newline="")


def evidence(path: Path) -> dict[str, object]:
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha(path.read_bytes()),
    }


def line_starts(data: bytes) -> list[int]:
    return [0] + [index + 1 for index, value in enumerate(data) if value == 10]


def line_at(starts: list[int], byte_index: int) -> int:
    return bisect.bisect_right(starts, byte_index)


def csv_records(path: Path) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, object]]]:
    data = path.read_bytes()
    rows = list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))
    raw_lines = data.splitlines(keepends=True)
    if len(raw_lines) != len(rows) + 1:
        raise AssertionError(f"CSV rows are not one physical line each: {path.name}")
    if not raw_lines or not raw_lines[-1].endswith(b"\n"):
        raise AssertionError(f"CSV lacks terminal LF: {path.name}")
    by_id: dict[str, dict[str, str]] = {}
    bindings: dict[str, dict[str, object]] = {}
    for index, (row, raw) in enumerate(zip(rows, raw_lines[1:], strict=True), start=1):
        producer_id = row["canonical_defect_id"]
        if producer_id in by_id:
            raise AssertionError(f"duplicate producer ID: {producer_id}")
        by_id[producer_id] = row
        bindings[producer_id] = {
            "data_row_index_1_based": index,
            "row_bytes": len(raw),
            "row_sha256": sha(raw),
        }
    return by_id, bindings


def bootstrap(source_root: Path, live_ledger: Path, independent_audit: Path) -> dict[str, object]:
    source_root = source_root.resolve()
    source_data = (source_root / SOURCE).read_bytes()
    if sha(source_data) != SOURCE_SHA:
        raise AssertionError("sites-cohomology authority hash drift")
    target_source = ROOT / "authority/source" / SOURCE
    target_source.parent.mkdir(parents=True, exist_ok=True)
    target_source.write_bytes(source_data)

    copying = source_root / "COPYING"
    if not copying.is_file():
        raise AssertionError("COPYING is absent from source root")
    (ROOT / "authority").mkdir(parents=True, exist_ok=True)
    (ROOT / "authority/COPYING").write_bytes(copying.read_bytes())

    audit_data = independent_audit.resolve().read_bytes()
    if sha(audit_data) != AUDIT_SHA:
        raise AssertionError("independent audit hash drift")
    audit_target = ROOT / AUDIT_PATH
    audit_target.parent.mkdir(parents=True, exist_ok=True)
    audit_target.write_bytes(audit_data)

    live_data = live_ledger.resolve().read_bytes()
    if sha(live_data) != LIVE_LEDGER_SHA:
        raise AssertionError("live corrected producer ledger hash drift")
    raw_lines = live_data.splitlines(keepends=True)
    if not raw_lines or not raw_lines[-1].endswith(b"\n"):
        raise AssertionError("producer ledger lacks terminal LF")
    selected: dict[str, bytes] = {}
    for raw in raw_lines[1:]:
        producer_id = raw.split(b",", 1)[0].decode("utf-8-sig")
        if producer_id in PRODUCER_IDS:
            if producer_id in selected:
                raise AssertionError(f"duplicate selected producer ID: {producer_id}")
            selected[producer_id] = raw
    if list(selected) != PRODUCER_IDS:
        raise AssertionError("selected R37 producer rows are incomplete or out of order")
    packet = raw_lines[0] + b"".join(selected[producer_id] for producer_id in PRODUCER_IDS)
    packet_target = ROOT / PACKET_PATH
    packet_target.parent.mkdir(parents=True, exist_ok=True)
    packet_target.write_bytes(packet)
    packet_rows, _ = csv_records(packet_target)
    if list(packet_rows) != PRODUCER_IDS:
        raise AssertionError("selected R37 packet parse/order failure")
    if packet_rows["SITES-COHOMOLOGY-014"]["proposed_correction"] != "is the {\\it $i$th cohomology group ...}":
        raise AssertionError("producer correction 014 has not landed")
    if packet_rows["SITES-COHOMOLOGY-023"]["proposed_correction"] != "a representative; It preserves; as indicated we denote":
        raise AssertionError("producer correction 023 has not landed")
    dump(
        ROOT / RECEIPT_PATH,
        {
            "schema": "stacks-sites-cohomology-r37-selected-packet-receipt/v1",
            "packet_ids": PRODUCER_IDS,
            "packet_bytes": len(packet),
            "packet_sha256": sha(packet),
            "live_snapshot_bytes": len(live_data),
            "live_snapshot_sha256": sha(live_data),
            "independent_audit_bytes": len(audit_data),
            "independent_audit_sha256": sha(audit_data),
            "producer_corrections_014_and_023_present": True,
            "nonselected_rows_excluded": True,
        },
    )
    return regenerate()


def build_operations() -> tuple[bytes, list[dict[str, object]], dict[str, dict[str, str]]]:
    authority = (ROOT / "authority/source" / SOURCE).read_bytes()
    if sha(authority) != SOURCE_SHA:
        raise AssertionError("candidate authority hash drift")
    audit_path = ROOT / AUDIT_PATH
    if sha(audit_path.read_bytes()) != AUDIT_SHA:
        raise AssertionError("embedded independent audit hash drift")
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if audit.get("status") != "PASS" or audit.get("validation", {}).get("every_preimage_exact_at_declared_position") is not True:
        raise AssertionError("independent audit is not an exact unconditional pass")
    if audit.get("authority", {}).get("sha256") != SOURCE_SHA:
        raise AssertionError("independent audit authority binding drift")
    if audit.get("scope", {}).get("producer_ids") != PRODUCER_IDS:
        raise AssertionError("independent audit producer scope drift")
    if audit.get("scope", {}).get("semantic_units") != 23 or audit.get("scope", {}).get("operations") != 28:
        raise AssertionError("independent audit counts drift")

    packet = ROOT / PACKET_PATH
    rows, bindings = csv_records(packet)
    if list(rows) != PRODUCER_IDS:
        raise AssertionError("producer packet order drift")
    packet_sha = sha(packet.read_bytes())
    starts = line_starts(authority)
    operations: list[dict[str, object]] = []
    audit_units = audit["units"]
    if [unit["producer_id"] for unit in audit_units] != PRODUCER_IDS:
        raise AssertionError("audit unit order drift")
    for unit_index, unit in enumerate(audit_units, start=1):
        producer_id = unit["producer_id"]
        stable_id = STABLE_BY_PRODUCER[producer_id]
        row = rows[producer_id]
        if row["authority_sha256"] != SOURCE_SHA:
            raise AssertionError(f"producer authority hash drift: {producer_id}")
        unit_operations = unit["operations"]
        if len(unit_operations) != unit["operation_count"]:
            raise AssertionError(f"audit operation count drift: {producer_id}")
        for operation_index, audited in enumerate(unit_operations, start=1):
            old = audited["old_text"].encode("utf-8")
            new = audited["replacement_text"].encode("utf-8")
            start = int(audited["start_byte_zero_based"])
            end = int(audited["end_byte_exclusive_zero_based"])
            if end - start != len(old) or authority[start:end] != old:
                raise AssertionError(f"exact audit preimage mismatch: {producer_id}/{operation_index}")
            if sha(old) != audited["old_sha256"] or sha(new) != audited["replacement_sha256"]:
                raise AssertionError(f"audit operation hash drift: {producer_id}/{operation_index}")
            if authority.count(old) != audited["occurrence_count_in_frozen_authority"]:
                raise AssertionError(f"global occurrence count drift: {producer_id}/{operation_index}")
            if line_at(starts, start) != audited["source_start_line"] or line_at(starts, end - 1) != audited["source_end_line"]:
                raise AssertionError(f"line locator drift: {producer_id}/{operation_index}")
            operations.append(
                {
                    "operation_id": f"{stable_id}-OP{operation_index}",
                    "operation_index": operation_index,
                    "stable_id": stable_id,
                    "producer_id": producer_id,
                    "registrar_operation_id": audited["operation_id"],
                    "operation_aliases": [],
                    "source": SOURCE,
                    "source_start_line": audited["source_start_line"],
                    "source_end_line": audited["source_end_line"],
                    "start_byte": start,
                    "end_byte_exclusive": end,
                    "old_text": audited["old_text"],
                    "old_bytes": len(old),
                    "old_sha256": sha(old),
                    "replacement_text": audited["replacement_text"],
                    "replacement_bytes": len(new),
                    "replacement_sha256": sha(new),
                    "occurrence_count_in_frozen_authority": authority.count(old),
                    "declared_line_range_occurrence_count": audited["occurrences_on_declared_start_line"],
                    "rationale": row["rationale"],
                    "class": row["classification"],
                    "independent_disposition": unit["disposition"],
                    "independent_note": unit.get("note"),
                    "producer_source_packet": PACKET_PATH,
                    "producer_source_packet_sha256": packet_sha,
                    "producer_row_binding": bindings[producer_id],
                    "registrar_evidence": AUDIT_PATH,
                    "registrar_evidence_sha256": AUDIT_SHA,
                }
            )
    if len(operations) != 28 or len({op["operation_id"] for op in operations}) != 28:
        raise AssertionError("R37 operation closure failed")
    payload = authority
    for operation in sorted(operations, key=lambda item: int(item["start_byte"]), reverse=True):
        start = int(operation["start_byte"])
        end = int(operation["end_byte_exclusive"])
        old = str(operation["old_text"]).encode("utf-8")
        if payload[start:end] != old:
            raise AssertionError(f"apply preimage mismatch: {operation['operation_id']}")
        payload = payload[:start] + str(operation["replacement_text"]).encode("utf-8") + payload[end:]
    return payload, operations, rows


def make_units(operations: list[dict[str, object]], rows: dict[str, dict[str, str]]) -> list[dict[str, object]]:
    by_stable: dict[str, list[dict[str, object]]] = {stable_id: [] for stable_id in STABLE_IDS}
    for operation in operations:
        by_stable[str(operation["stable_id"])].append(operation)
    units: list[dict[str, object]] = []
    for producer_id, stable_id in zip(PRODUCER_IDS, STABLE_IDS, strict=True):
        units.append(
            {
                "id": stable_id,
                "producer_id": producer_id,
                "producer_ids": [producer_id],
                "class": "source_defect_correction",
                "status": "accepted_new",
                "source": SOURCE,
                "locus": rows[producer_id]["source_locator"],
                "payload": f"payload/{SOURCE}",
                "operation_ids": [operation["operation_id"] for operation in by_stable[stable_id]],
            }
        )
    return units


def write_metadata(payload: bytes, operations: list[dict[str, object]], rows: dict[str, dict[str, str]]) -> None:
    payload_path = ROOT / "payload" / SOURCE
    payload_path.parent.mkdir(parents=True, exist_ok=True)
    payload_path.write_bytes(payload)
    units = make_units(operations, rows)
    packet = ROOT / PACKET_PATH
    receipt = ROOT / RECEIPT_PATH
    audit = ROOT / AUDIT_PATH

    dump(
        ROOT / "authority/upstream.lock.json",
        {
            "schema": "mathematics-commons-stacks-upstream-lock/v1",
            "repository": "https://github.com/stacks/stacks-project",
            "commit": COMMIT,
            "tree": TREE,
            "source": SOURCE,
            "source_bytes": (ROOT / "authority/source" / SOURCE).stat().st_size,
            "source_sha256": SOURCE_SHA,
            "authority_mutated": False,
        },
    )
    dump(
        ROOT / "LEASE.json",
        {
            "schema": "mathematics-commons-stacks-candidate-lease-pointer/v1",
            "lease_id": LEASE,
            "namespace": "commons/stacks/errata/r37",
            "candidate_path": "candidates/commons/stacks/errata/r37",
            "writer_task": WRITER,
            "upstream_commit": COMMIT,
            "writer_contract": "candidates/CONTRACT.md",
            "state": "active_pending_admission",
        },
    )
    dump(
        ROOT / "operation-spec.json",
        {
            "schema": "mathematics-commons-stacks-errata-operation-spec/v1",
            "authority_commit": COMMIT,
            "apply_order": "descending_start_byte_per_source",
            "operation_count": len(operations),
            "operations": operations,
        },
    )
    dump(
        ROOT / "stable-units.json",
        {
            "schema": "mathematics-commons-stacks-errata-units/v1",
            "authority_commit": COMMIT,
            "unit_count": len(units),
            "units": units,
        },
    )
    source_map: list[dict[str, object]] = []
    operation_by_id = {operation["operation_id"]: operation for operation in operations}
    for unit in units:
        source_map.append(
            {
                "schema": "mathematics-commons-stacks-errata-map/v2",
                "unit_id": unit["id"],
                "producer_id": unit["producer_id"],
                "producer_ids": unit["producer_ids"],
                "class": unit["class"],
                "source": SOURCE,
                "locus": unit["locus"],
                "authority": f"authority/source/{SOURCE}",
                "authority_sha256": SOURCE_SHA,
                "payload": f"payload/{SOURCE}",
                "operation_aliases": [],
                "operations": [operation_by_id[operation_id] for operation_id in unit["operation_ids"]],
                "proof": "accepted_after_independent_exact_preimage_context_math_and_registry_deduplication",
                "adverse_evidence": (
                    "Frozen authority and French target remain provenance. Producer evidence and the "
                    "registrar audit are both preserved; this candidate changes only the future "
                    "AI-open English edition when composed downstream."
                ),
            }
        )
    dump_jsonl(ROOT / "source-map.jsonl", source_map)

    decisions = [
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R37-D0001",
            "timestamp_utc": STAMP,
            "choice": "Bind R37 to the pinned sites-cohomology.tex authority, the exact corrected 23-row producer packet, and the independent registrar audit.",
            "rationale": "The embedded authority, producer packet, packet receipt, and registrar audit are each hash-bound and replay exactly.",
        },
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R37-D0002",
            "timestamp_utc": STAMP,
            "choice": "Allocate MC-STK-ERR-1313..1335 to SITES-COHOMOLOGY-014..027 and 029..037 in producer order.",
            "rationale": "The R36 registry head contains no producer, operation, or stable-ID collision; the independent audit accepts 23 semantic units and 28 exact operations.",
        },
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R37-D0003",
            "timestamp_utc": STAMP,
            "choice": "Use the registrar-corrected exact operations for SITES-COHOMOLOGY-014 and SITES-COHOMOLOGY-023.",
            "rationale": "014 is minimally it the to is the; 023 is a representative, It preserves, and indicate to denote. The live producer packet now records those corrections, and the already-correct French target is unchanged.",
        },
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R37-D0004",
            "timestamp_utc": STAMP,
            "choice": "Keep authority, locale targets, registry files, and generated-source trees unchanged in the candidate-builder lane.",
            "rationale": "Candidate construction, registry admission, and generated-source composition are distinct transactions.",
        },
    ]
    dump_jsonl(ROOT / "decisions.jsonl", decisions)
    (ROOT / "rejections.jsonl").write_bytes(b"")

    formula_units: list[str] = []
    prose_units: list[str] = []
    for unit in units:
        changed = [operation_by_id[operation_id] for operation_id in unit["operation_ids"]]
        if any(("\\" in str(op["old_text"]) or "$" in str(op["old_text"]) or "\\" in str(op["replacement_text"]) or "$" in str(op["replacement_text"])) for op in changed):
            formula_units.append(str(unit["id"]))
        else:
            prose_units.append(str(unit["id"]))
    dump(
        ROOT / "formula-diagram-inventory.json",
        {
            "schema": "mathematics-commons-stacks-errata-formula-diagram-inventory/v1",
            "candidate_id": CANDIDATE,
            "authority_commit": COMMIT,
            "unit_count": len(units),
            "formula_units": formula_units,
            "prose_only_units": prose_units,
            "diagram_units": [],
            "unmapped_formula_or_diagram_changes": 0,
        },
    )
    dump(
        ROOT / "candidate.config.json",
        {
            "$schema": "../../schemas/candidate-manifest.schema.json",
            "schema": "mathematics-commons-stacks-errata-candidate-config/v1",
            "candidate_id": CANDIDATE,
            "lease_id": LEASE,
            "namespace": "commons/stacks/errata/r37",
            "writer_task": WRITER,
            "authority_commit": COMMIT,
            "authority_tree": TREE,
            "accepted": 23,
            "rejected": 0,
            "unresolved": 0,
            "operation_count": 28,
            "composition_performed": False,
            "expected_producer_ids": PRODUCER_IDS,
            "expected_unit_ids": STABLE_IDS,
            "stems": {
                SOURCE: {
                    "authority_bytes": (ROOT / "authority/source" / SOURCE).stat().st_size,
                    "authority_sha256": SOURCE_SHA,
                    "operations": 28,
                    "payload_bytes": len(payload),
                    "payload_sha256": sha(payload),
                }
            },
        },
    )
    dump(
        ROOT / "source-validation.json",
        {
            "schema": "mathematics-commons-stacks-errata-source-validation/v1",
            "candidate_id": CANDIDATE,
            "passed": True,
            "accepted_units": 23,
            "rejected_units": 0,
            "unresolved_units": 0,
            "operation_count": 28,
            "authority_bytes_mutated": False,
            "locale_target_bytes_mutated": False,
            "generated_source_composed": False,
            "authorities": {SOURCE: {"bytes": (ROOT / "authority/source" / SOURCE).stat().st_size, "sha256": SOURCE_SHA}},
            "payloads": {SOURCE: evidence(payload_path)},
            "producer_packets": [evidence(packet), evidence(receipt)],
            "registrar_audit": evidence(audit),
        },
    )
    review = {
        "schema": "mathematics-commons-stacks-errata-independent-review/v1",
        "candidate_id": CANDIDATE,
        "review_kind": "independent_exact_preimage_context_math_deduplication_and_payload_review",
        "recorded_at_utc": STAMP,
        "passed": True,
        "pass_is_unconditional": True,
        "result": "PASS",
        "conclusion": "UNCONDITIONAL PASS",
        "input_bindings": {
            "authority_sha256": SOURCE_SHA,
            "live_ledger_bytes": json.loads(receipt.read_text(encoding="utf-8"))["live_snapshot_bytes"],
            "live_ledger_sha256": LIVE_LEDGER_SHA,
            "selected_packet": evidence(packet),
            "independent_audit": evidence(audit),
        },
        "deduplication": {
            "passed": True,
            "registry_pre_admission_head": "stacks-errata-a04446e-r36",
            "semantic_units": 23,
            "operations": 28,
            "accepted_new_units": PRODUCER_IDS,
            "stable_id_collisions": 0,
            "producer_id_collisions": 0,
            "operation_aliases": {},
        },
        "adverse_observations": [
            "SITES-COHOMOLOGY-014 and 023 required canon repairs to the producer's initial proposals; the live corrected packet and registrar audit now agree.",
            "SITES-COHOMOLOGY-019 is locator-scoped because its old token occurs 22 times file-wide; only the three audited positions are changed.",
            "Already admitted producer rows 001..013 and 028 are excluded from R37.",
            "R37 is registrar-candidate-only; admission, generated-source composition, and publication are excluded from this build.",
        ],
        "closure_checks": {
            "passed": True,
            "authority_files": 1,
            "payload_files": 1,
            "source_map_rows": 23,
            "stable_ids_unique": 23,
            "operation_ids_unique": 28,
        },
        "scratch_replay": {
            "passed": True,
            "apply_order": "descending_start_byte_per_source",
            "stable_units": 23,
            "operations": 28,
            "payload_sha256": {SOURCE: sha(payload)},
        },
        "constraints_observed": {
            "upstream_authority_mutated": False,
            "locale_targets_mutated_by_registrar": False,
            "registry_mutated_by_review": False,
            "generated_source_composed": False,
            "generated_source_pushed": False,
            "nonselected_producer_rows_admitted": False,
        },
    }
    dump(ROOT / "replay/independent-review.json", review)

    (ROOT / "README.md").write_text(
        "# R37: `sites-cohomology.tex`\n\n"
        "Registrar candidate for 23 independently replayed producer units (014--027 and 029--037), "
        "materialized as 28 exact operations and stable IDs MC-STK-ERR-1313..1335. "
        "The corrected producer packet and independent registrar audit are both preserved.\n\n"
        "This candidate does not mutate pinned authority or locale targets, alter registry files, "
        "or compose generated Stacks source.\n",
        encoding="utf-8",
        newline="",
    )
    (ROOT / "BUILD.md").write_text(
        "Run `python pipeline_r37.py regenerate` to deterministically rebuild candidate artifacts, "
        "then `python pipeline_r37.py verify` for exact source, payload, deduplication, and manifest replay. "
        "Use `python pipeline_r37.py rebind-manifest` after a manifested pipeline/documentation-only change. "
        "Registrar admission is the single append-only transaction `python pipeline_r37.py admit`; it does not compose generated source.\n",
        encoding="utf-8",
        newline="",
    )
    dump(
        ROOT / "REGENERATION_RECEIPT.json",
        {
            "schema": "stacks-r37-sites-cohomology-regeneration/v1",
            "candidate_id": CANDIDATE,
            "generated_at_utc": STAMP,
            "semantic_units": 23,
            "operations": 28,
            "stable_id_range": [STABLE_IDS[0], STABLE_IDS[-1]],
            "payloads": {SOURCE: evidence(payload_path)},
            "authority_bytes_mutated": False,
            "locale_target_bytes_mutated": False,
            "registry_files_mutated": False,
            "generated_source_composed": False,
        },
    )


def write_manifest(*, admitted: bool) -> None:
    source_authorities = [
        evidence(ROOT / "authority/COPYING"),
        evidence(ROOT / PACKET_PATH),
        evidence(ROOT / RECEIPT_PATH),
        evidence(ROOT / AUDIT_PATH),
        evidence(ROOT / "authority/source" / SOURCE),
        evidence(ROOT / "authority/upstream.lock.json"),
    ]
    build_paths = [
        "BUILD.md",
        "candidate.config.json",
        "LEASE.json",
        "operation-spec.json",
        f"payload/{SOURCE}",
        "pipeline_r37.py",
        "README.md",
        "REGENERATION_RECEIPT.json",
        "replay/independent-review.json",
        "source-validation.json",
    ]
    manifest = {
        "$schema": "../../../../../schemas/candidate-manifest.schema.json",
        "schema": "mathematics-commons-stacks-candidate-manifest/v1",
        "candidate_id": CANDIDATE,
        "lease_id": LEASE,
        "namespace": "commons/stacks/errata/r37",
        "writer_task": WRITER,
        "generated_at_utc": STAMP,
        "review_state": "performed",
        "independent_replay": "passed",
        "rights_state": RIGHTS,
        "upstream": {"commit": COMMIT, "tree": TREE, "lock": "upstream/stacks.lock.json"},
        "source_authorities": source_authorities,
        "decision_ledger": evidence(ROOT / "decisions.jsonl"),
        "rejection_ledger": evidence(ROOT / "rejections.jsonl"),
        "stable_unit_manifest": evidence(ROOT / "stable-units.json"),
        "source_map": evidence(ROOT / "source-map.jsonl"),
        "formula_diagram_inventory": evidence(ROOT / "formula-diagram-inventory.json"),
        "builds": [evidence(ROOT / path) for path in build_paths],
        "source_closure": {"complete": True, "enumerated": True, "expected_units": 23, "manifested_units": 23},
        "stop_conditions": [
            "Do not mutate pinned upstream authority or locale targets.",
            "Do not include producer rows outside 014..027 and 029..037.",
            "Registrar admission may alter only the overlay/lease registries and the R37 admission receipt; do not compose generated source in this lane.",
            "Any byte change requires a regenerated manifest and replay.",
        ],
        "unresolved_defects": [
            "Already admitted producer rows 001..013 and 028 are excluded.",
            "The exact canon repairs for rows 014 and 023 supersede their initial producer proposals; corrected producer evidence and registrar audit are both bound.",
            ("This candidate is admitted to the registry but does not compose or push generated Stacks source."
             if admitted else
             "This candidate is not yet admitted to the registry and does not compose or push generated Stacks source."),
            "Pinned authority and locale targets remain unmodified.",
        ],
    }
    dump(ROOT / "candidate.manifest.json", manifest)


def regenerate() -> dict[str, object]:
    registry = json.loads((REPO / "registry/overlays.json").read_text(encoding="utf-8"))
    if any(entry.get("id") == CANDIDATE for entry in registry["registered_entries"]):
        raise AssertionError("regenerate is forbidden after R37 admission; use verify")
    payload, operations, rows = build_operations()
    write_metadata(payload, operations, rows)
    write_manifest(admitted=False)
    return verify()


def rebind_manifest() -> dict[str, object]:
    registry = json.loads((REPO / "registry/overlays.json").read_text(encoding="utf-8"))
    admitted = any(entry.get("id") == CANDIDATE for entry in registry["registered_entries"])
    write_manifest(admitted=admitted)
    return verify()


def verify_manifest() -> None:
    manifest = json.loads((ROOT / "candidate.manifest.json").read_text(encoding="utf-8"))
    records = [
        *manifest["source_authorities"],
        manifest["decision_ledger"],
        manifest["rejection_ledger"],
        manifest["stable_unit_manifest"],
        manifest["source_map"],
        manifest["formula_diagram_inventory"],
        *manifest["builds"],
    ]
    paths = [record["path"] for record in records]
    if len(paths) != len(set(paths)):
        raise AssertionError("manifest contains duplicate paths")
    for record in records:
        path = ROOT / record["path"]
        if not path.is_file():
            raise AssertionError(f"manifested path is absent: {record['path']}")
        if path.stat().st_size != record["bytes"] or sha(path.read_bytes()) != record["sha256"]:
            raise AssertionError(f"manifest identity mismatch: {record['path']}")


def verify() -> dict[str, object]:
    payload, operations, rows = build_operations()
    if (ROOT / "payload" / SOURCE).read_bytes() != payload:
        raise AssertionError("payload does not replay exactly")
    if json.loads((ROOT / "operation-spec.json").read_text(encoding="utf-8"))["operations"] != operations:
        raise AssertionError("operation specification drift")
    units = json.loads((ROOT / "stable-units.json").read_text(encoding="utf-8"))["units"]
    if [unit["id"] for unit in units] != STABLE_IDS or [unit["producer_id"] for unit in units] != PRODUCER_IDS:
        raise AssertionError("stable unit order/identity drift")
    source_map = [json.loads(line) for line in (ROOT / "source-map.jsonl").read_text(encoding="utf-8").splitlines()]
    if [row["unit_id"] for row in source_map] != STABLE_IDS:
        raise AssertionError("source map closure drift")
    review = json.loads((ROOT / "replay/independent-review.json").read_text(encoding="utf-8"))
    if review.get("passed") is not True or review.get("pass_is_unconditional") is not True:
        raise AssertionError("independent review is absent or conditional")
    registry = json.loads((REPO / "registry/overlays.json").read_text(encoding="utf-8"))
    leases = json.loads((REPO / "registry/leases.json").read_text(encoding="utf-8"))
    entries = registry["registered_entries"]
    r37_entries = [entry for entry in entries if entry.get("id") == CANDIDATE]
    if len(r37_entries) > 1:
        raise AssertionError("registry contains duplicate R37 entries")
    admitted = len(r37_entries) == 1
    expected_head = CANDIDATE if admitted else "stacks-errata-a04446e-r36"
    if entries[-1]["id"] != expected_head:
        raise AssertionError(f"registry head is not {expected_head}")
    if any(entry.get("namespace") == "commons/stacks/errata/r37" for entry in entries[:-1]):
        raise AssertionError("R37 namespace is duplicated or out of order")
    allocated = {
        stable_id
        for entry in entries
        if entry.get("id") != CANDIDATE
        for stable_id in entry.get("stable_ids", [])
    }
    collisions = sorted(set(STABLE_IDS) & allocated)
    if collisions:
        raise AssertionError(f"stable-ID collision: {collisions}")
    if list(rows) != PRODUCER_IDS:
        raise AssertionError("producer packet scope drift")
    verify_manifest()
    manifest = json.loads((ROOT / "candidate.manifest.json").read_text(encoding="utf-8"))
    manifest_sha = sha((ROOT / "candidate.manifest.json").read_bytes())
    lease_pointer = json.loads((ROOT / "LEASE.json").read_text(encoding="utf-8"))
    r37_events = [event for event in leases["events"] if event.get("lease_id") == LEASE]
    if admitted:
        expected_entry = {
            "id": CANDIDATE,
            "namespace": "commons/stacks/errata/r37",
            "writer": WRITER,
            "source_commit": COMMIT,
            "source_tree": TREE,
            "manifest_sha256": manifest_sha,
            "stable_ids": STABLE_IDS,
            "rights_state": RIGHTS,
            "review_receipt": "candidates/commons/stacks/errata/r37/replay/independent-review.json",
            "admitted_at_utc": ADMISSION_STAMP,
        }
        if r37_entries[0] != expected_entry:
            raise AssertionError("R37 registry entry does not bind the final candidate")
        if lease_pointer.get("state") != "released_after_admission":
            raise AssertionError("candidate lease pointer is not released after admission")
        expected_events = [
            {
                "event_id": "lease-event-000078",
                "event": "issued",
                "lease_id": LEASE,
                "namespace": "commons/stacks/errata/r37",
                "candidate_path": "candidates/commons/stacks/errata/r37",
                "writer_task": WRITER,
                "upstream_commit": COMMIT,
                "upstream_tree": TREE,
                "issued_at_utc": ADMISSION_STAMP,
                "writer_contract": "candidates/CONTRACT.md",
                "state": "active",
                "supersedes_event_id": "lease-event-000077",
            },
            {
                "event_id": "lease-event-000079",
                "event": "released",
                "lease_id": LEASE,
                "namespace": "commons/stacks/errata/r37",
                "candidate_path": "candidates/commons/stacks/errata/r37",
                "writer_task": WRITER,
                "upstream_commit": COMMIT,
                "upstream_tree": TREE,
                "issued_at_utc": ADMISSION_STAMP,
                "writer_contract": "candidates/CONTRACT.md",
                "state": "released",
                "supersedes_event_id": "lease-event-000078",
            },
        ]
        if r37_events != expected_events or leases["events"][-2:] != expected_events:
            raise AssertionError("R37 lease event chain does not match the admitted overlay")
        if not any(
            item.startswith("This candidate is admitted to the registry")
            for item in manifest["unresolved_defects"]
        ):
            raise AssertionError("manifest does not record admitted state")
    else:
        if lease_pointer.get("state") != "active_pending_admission":
            raise AssertionError("pre-admission lease pointer is not active")
        if r37_events:
            raise AssertionError("pre-admission lease registry already contains R37 events")
        if leases["events"][-1]["event_id"] != "lease-event-000077":
            raise AssertionError("pre-admission lease head is not event 000077")
        if not any(
            item.startswith("This candidate is not yet admitted to the registry")
            for item in manifest["unresolved_defects"]
        ):
            raise AssertionError("manifest does not record pre-admission state")
    manifested = len(manifest["source_authorities"]) + 5 + len(manifest["builds"])
    return {
        "passed": True,
        "candidate_id": CANDIDATE,
        "units": 23,
        "operations": 28,
        "stable_ids": STABLE_IDS,
        "producer_ids": PRODUCER_IDS,
        "payload_sha256": {SOURCE: sha(payload)},
        "manifest_references": manifested,
        "registry_head": expected_head,
        "registry_mutated": admitted,
        "generated_source_composed": False,
    }


def admit() -> dict[str, object]:
    preflight = verify()
    if preflight["registry_head"] != "stacks-errata-a04446e-r36":
        raise AssertionError("R37 admission requires the exact R36 pre-admission head")
    registry_path = REPO / "registry/overlays.json"
    leases_path = REPO / "registry/leases.json"
    receipt_path = REPO / "registry/admission-receipts/r37.json"
    if receipt_path.exists():
        raise AssertionError("R37 admission receipt already exists")
    registry_before = registry_path.read_bytes()
    leases_before = leases_path.read_bytes()
    if sha(registry_before) != R36_OVERLAYS_SHA:
        raise AssertionError("overlay registry bytes do not match the exact reviewed R36 head")
    if sha(leases_before) != R36_LEASES_SHA:
        raise AssertionError("lease registry bytes do not match the exact reviewed R36 head")
    registry = json.loads(registry_before.decode("utf-8"))
    leases = json.loads(leases_before.decode("utf-8"))
    if registry["registered_entries"][-1]["id"] != "stacks-errata-a04446e-r36":
        raise AssertionError("overlay registry changed after preflight")
    if leases["events"][-1]["event_id"] != "lease-event-000077":
        raise AssertionError("lease registry changed after preflight")

    lease_pointer = json.loads((ROOT / "LEASE.json").read_text(encoding="utf-8"))
    lease_pointer["state"] = "released_after_admission"
    dump(ROOT / "LEASE.json", lease_pointer)
    write_manifest(admitted=True)
    manifest_sha = sha((ROOT / "candidate.manifest.json").read_bytes())

    overlay_entry = {
        "id": CANDIDATE,
        "namespace": "commons/stacks/errata/r37",
        "writer": WRITER,
        "source_commit": COMMIT,
        "source_tree": TREE,
        "manifest_sha256": manifest_sha,
        "stable_ids": STABLE_IDS,
        "rights_state": RIGHTS,
        "review_receipt": "candidates/commons/stacks/errata/r37/replay/independent-review.json",
        "admitted_at_utc": ADMISSION_STAMP,
    }
    issued_event = {
        "event_id": "lease-event-000078",
        "event": "issued",
        "lease_id": LEASE,
        "namespace": "commons/stacks/errata/r37",
        "candidate_path": "candidates/commons/stacks/errata/r37",
        "writer_task": WRITER,
        "upstream_commit": COMMIT,
        "upstream_tree": TREE,
        "issued_at_utc": ADMISSION_STAMP,
        "writer_contract": "candidates/CONTRACT.md",
        "state": "active",
        "supersedes_event_id": "lease-event-000077",
    }
    released_event = {
        **issued_event,
        "event_id": "lease-event-000079",
        "event": "released",
        "state": "released",
        "supersedes_event_id": "lease-event-000078",
    }
    registry["registered_entries"].append(overlay_entry)
    leases["events"].extend([issued_event, released_event])
    dump_registry(registry_path, registry)
    dump_registry(leases_path, leases)
    postflight = verify()

    receipt = {
        "admitted_at_utc": ADMISSION_STAMP,
        "candidate_id": CANDIDATE,
        "constraints": {
            "authority_mutated": False,
            "generated_source_composed": False,
            "generated_source_pushed": False,
            "producer_target_mutated": False,
            "published": False,
        },
        "fresh_replay": postflight,
        "leases": {
            "after_sha256": sha(leases_path.read_bytes()),
            "before_sha256": sha(leases_before),
            "issued_event": "lease-event-000078",
            "released_event": "lease-event-000079",
        },
        "manifest": evidence(ROOT / "candidate.manifest.json"),
        "producer_ids": PRODUCER_IDS,
        "registry": {
            "after_sha256": sha(registry_path.read_bytes()),
            "before_sha256": sha(registry_before),
            "last_overlay": CANDIDATE,
        },
        "schema": "mathematics-commons-stacks-registry-admission-receipt/v1",
        "source_map": evidence(ROOT / "source-map.jsonl"),
        "stable_id_count": len(STABLE_IDS),
        "stable_ids": STABLE_IDS,
        "status": "PASS",
    }
    dump(receipt_path, receipt)
    return {
        **postflight,
        "admission_receipt_sha256": sha(receipt_path.read_bytes()),
        "manifest_sha256": manifest_sha,
        "overlays_sha256": sha(registry_path.read_bytes()),
        "leases_sha256": sha(leases_path.read_bytes()),
    }


def main() -> int:
    if len(sys.argv) < 2:
        raise SystemExit(
            "usage: pipeline_r37.py bootstrap SOURCE_ROOT LIVE_LEDGER INDEPENDENT_AUDIT | regenerate | rebind-manifest | verify | admit"
        )
    mode = sys.argv[1]
    if mode == "bootstrap":
        if len(sys.argv) != 5:
            raise SystemExit("bootstrap requires SOURCE_ROOT LIVE_LEDGER INDEPENDENT_AUDIT")
        result = bootstrap(Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))
    elif mode == "regenerate":
        result = regenerate()
    elif mode == "rebind-manifest":
        result = rebind_manifest()
    elif mode == "verify":
        result = verify()
    elif mode == "admit":
        result = admit()
    else:
        raise SystemExit(f"unknown mode: {mode}")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
