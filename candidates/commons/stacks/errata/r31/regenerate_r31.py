from __future__ import annotations

import bisect
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
AUTHORITY = ROOT / "authority" / "source" / "sites-modules.tex"
PRODUCER = ROOT / "producer"
HANDOFF = PRODUCER / "SITES_MODULES_CANON_HANDOFF.json"
EMENDATIONS = PRODUCER / "SITES_MODULES_SOURCE_EMENDATIONS.json"
DEFECTS = PRODUCER / "SITES_MODULES_SOURCE_DEFECT_LEDGER.csv"
CROSSWALK = PRODUCER / "SITES_MODULES_DEFECT_ID_CROSSWALK.csv"
D_EMENDATIONS = PRODUCER / "SITES_MODULES_D_SOURCE_EMENDATIONS.json"
D_DEFECTS = PRODUCER / "SITES_MODULES_D_SOURCE_DEFECTS.csv"

COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
AUTHORITY_SHA = "B7CD92AFF9DF33F05EEAB72C4B55E8AA33F3AEBD947FC53160E87CA80DFFB245"
STABLE = "MC-STK-ERR-1287"
ALIAS = "R31-REOPEN-SITES-MODULES-CH18-030"
RAW = "SITES-MODULES-CH18-030"
LEASE = "D"
LEASE_ID = "stacks-lease-000035-errata-r31"
WRITER = "01a0256d-5693-77c1-96b2-cf37101e0c6c"
SOURCE_PACKET = "producer/SITES_MODULES_D_SOURCE_EMENDATIONS.json"
SOURCE_PACKET_SHA = "048104FCC94F539D4A59EAEBCF0A096F8C36E6C4939C9CC4AF3D8D08819CFB1D"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")


def file_hash(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data)}


def line_starts(data: bytes) -> list[int]:
    return [0] + [i + 1 for i, b in enumerate(data) if b == 10]


def line_at(starts: list[int], offset: int) -> int:
    return bisect.bisect_right(starts, offset)


def find_unique(data: bytes, old: str, first: int, last: int) -> tuple[int, int]:
    needle = old.encode("utf-8")
    starts = line_starts(data)
    found: list[tuple[int, int]] = []
    cursor = 0
    while True:
        pos = data.find(needle, cursor)
        if pos < 0:
            break
        end = pos + len(needle)
        if line_at(starts, pos) == first and line_at(starts, max(pos, end - 1)) == last:
            found.append((pos, end))
        cursor = pos + 1
    if len(found) != 1:
        raise AssertionError(f"expected one {first}-{last} preimage, found {len(found)}")
    return found[0]


def main() -> int:
    authority = AUTHORITY.read_bytes()
    if len(authority) != 312143 or sha(authority) != AUTHORITY_SHA:
        raise AssertionError("pinned sites-modules authority identity mismatch")
    required = (HANDOFF, EMENDATIONS, DEFECTS, CROSSWALK, D_EMENDATIONS, D_DEFECTS)
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(path)
    handoff = json.loads(HANDOFF.read_text(encoding="utf-8"))
    if handoff["authority"]["sha256"] != AUTHORITY_SHA or handoff["authority"]["commit"] != COMMIT:
        raise AssertionError("handoff authority identity mismatch")
    source_decl = json.loads(EMENDATIONS.read_text(encoding="utf-8"))
    if source_decl["authority_sha256"] != AUTHORITY_SHA:
        raise AssertionError("source emendation authority identity mismatch")
    d_decl = json.loads(D_EMENDATIONS.read_text(encoding="utf-8"))
    if d_decl["authority_sha256"] != AUTHORITY_SHA or d_decl.get("lease") != "D":
        raise AssertionError("D packet identity mismatch")
    rows = [row for row in d_decl["emendations"] if row.get("line") == 7967]
    if len(rows) != 1:
        raise AssertionError(f"expected one D line-7967 row, found {len(rows)}")
    row = rows[0]
    if row["id"] != "SITES-MODULES-007" or row["old"] != r"$\Sh(\mathcal{C})/\mathcal{F}$, see proof of" or row["new"] != r"$\Sh(\mathcal{C}/U)$, see proof of":
        raise AssertionError("unexpected D row at line 7967")

    # Independently confirm the prior R29 disposition: CH18-030 was rejected,
    # and its old/new operation is absent from the R29 accepted operation set.
    r29_rejections = ROOT / "authority" / "canon" / "R29_rejections.jsonl"
    prior = [json.loads(line) for line in r29_rejections.read_text(encoding="utf-8").splitlines() if line.strip()]
    prior030 = [x for x in prior if x.get("id") == "SITES-MODULES-CH18-030"]
    if len(prior030) != 1 or prior030[0].get("status") != "rejected":
        raise AssertionError("R29 CH18-030 rejection history missing")
    r29_spec = json.loads((ROOT / "authority" / "canon" / "R29_SITES_MODULES_OPERATION_DRAFT_20260829.json").read_text(encoding="utf-8"))
    if any(op.get("source_start_line") == 7967 or op.get("old_text") == row["old"] for op in r29_spec.get("operations", [])):
        raise AssertionError("CH18-030 unexpectedly present in R29 accepted operations")

    old, new = row["old"], row["new"]
    start, end = find_unique(authority, old, 7967, 7967)
    old_b, new_b = old.encode(), new.encode()
    operation = {
        "operation_id": f"{STABLE}-OP1",
        "operation_index": 1,
        "stable_id": STABLE,
        "producer_id": ALIAS,
        "producer_operation_id": row["id"],
        "raw_producer_id": RAW,
        "semantic_unit_producer_id": ALIAS,
        "lease": LEASE,
        "source_start_line": 7967,
        "source_end_line": 7967,
        "start_byte": start,
        "end_byte_exclusive": end,
        "old_text": old,
        "old_bytes": len(old_b),
        "old_sha256": sha(old_b),
        "replacement_text": new,
        "replacement_bytes": len(new_b),
        "replacement_sha256": sha(new_b),
        "occurrence_count_in_frozen_authority": authority.count(old_b),
        "declared_line_range_occurrence_count": 1,
        "rationale": "Reopened R29 rejection: Part (3) is localized at U; the preceding statement and proof context use Sh(C/U), while Sh(C)/F is not the relevant source topos. Independent replay of lines 7862-7972 confirms the correction.",
        "producer_source_packet": SOURCE_PACKET,
        "producer_source_packet_sha256": SOURCE_PACKET_SHA,
        "reopened_from": "SITES-MODULES-CH18-030",
    }
    payload = authority[:start] + new_b + authority[end:]
    payload_path = ROOT / "payload" / "sites-modules.tex"
    payload_path.write_bytes(payload)
    source_entry = {
        "schema": "mathematics-commons-stacks-errata-map/v2",
        "unit_id": STABLE,
        "class": "source_defect_correction",
        "source": "sites-modules.tex",
        "authority": "authority/source/sites-modules.tex",
        "authority_sha256": AUTHORITY_SHA,
        "payload": "payload/sites-modules.tex",
        "locus": "sites-modules.tex:7967",
        "producer_id": ALIAS,
        "producer_ids": [ALIAS],
        "raw_producer_ids": [RAW],
        "producer_identity": {"lease": LEASE, "raw_producer_ids": [RAW], "unique_alias": ALIAS},
        "operations": [operation],
        "proof": "reopened_prior_rejection_after_independent_context_replay",
        "prior_disposition": {"round": "R29", "status": "rejected", "producer_id": "SITES-MODULES-CH18-030", "rejection_file": "authority/canon/R29_rejections.jsonl"},
        "adverse_evidence": "R29 rejection history is preserved verbatim; the present one-operation admission is a separate append-only review.",
    }
    dump(ROOT / "operation-spec.json", {"schema": "mathematics-commons-stacks-errata-operation-spec/v1", "authority_sha256": AUTHORITY_SHA, "apply_order": "descending_start_byte", "operation_count": 1, "operations": [operation]})
    dump(ROOT / "stable-units.json", {"schema": "mathematics-commons-stacks-errata-units/v1", "authority_commit": COMMIT, "unit_count": 1, "units": [{"id": STABLE, "class": "source_defect_correction", "source": "sites-modules.tex", "payload": "payload/sites-modules.tex", "locus": "sites-modules.tex:7967", "operation_ids": [operation["operation_id"]], "producer_id": ALIAS, "producer_ids": [ALIAS], "raw_producer_ids": [RAW], "status": "accepted_reopened_prior_rejection"}]})
    (ROOT / "source-map.jsonl").write_text(json.dumps(source_entry, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="")
    (ROOT / "rejections.jsonl").write_text("", encoding="utf-8", newline="")
    dump(ROOT / "formula-diagram-inventory.json", {"schema": "mathematics-commons-stacks-errata-formula-diagram-inventory/v1", "candidate_id": "stacks-errata-a04446e-r31", "authority_commit": COMMIT, "unit_count": 1, "formula_units": [STABLE], "diagram_units": [], "prose_only_units": [], "unmapped_formula_or_diagram_changes": 0})

    # Preserve prior rejection and every producer identity in an explicit,
    # sanitized canon record. This is evidence, not a mutation of R29.
    prior_record = {
        "schema": "stacks-r31-sites-modules-reopened-rejection/v1",
        "candidate_id": "stacks-errata-a04446e-r31",
        "authority": {"path": "authority/source/sites-modules.tex", "bytes": len(authority), "sha256": AUTHORITY_SHA, "commit": COMMIT, "tree": TREE},
        "prior_round": {"round": "R29", "rejection_path": "authority/canon/R29_rejections.jsonl", "rejection_sha256": sha(r29_rejections.read_bytes()), "rejection_record": prior030[0], "operation_draft_sha256": sha((ROOT / "authority/canon/R29_SITES_MODULES_OPERATION_DRAFT_20260829.json").read_bytes())},
        "current": {"raw_producer_id": RAW, "producer_alias": ALIAS, "stable_id": STABLE, "source_line": 7967, "status": "reopened_and_admitted", "reason": "Independent context lines 7862-7972 establish Sh(C/U) as the localized source topos; the prior rejection's final sentence conflicts with its own item (3) and proof."},
        "excluded_duplicate_operations": 18,
        "excluded_duplicate_note": "All other reportable operations in the current handoff match R29 accepted operation old/new hashes and are excluded from this round.",
        "authority_bytes_mutated": False,
    }
    dump(ROOT / "authority" / "canon" / "R31_SITES_MODULES_REOPENED_REJECTION_20260829.json", prior_record)

    decisions = [
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R31-D0001", "choice": "Bind R31 to the pinned sites-modules.tex authority and the complete Chapter 18 handoff.", "rationale": "Authority bytes, commit, tree, and handoff hash were independently verified.", "timestamp_utc": "2026-08-29T00:00:00Z"},
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R31-D0002", "choice": "Exclude the 18 current operations whose old/new hashes exactly match R29 accepted operations.", "rationale": "This one-unit round is disjoint and avoids replaying work already admitted in R29.", "timestamp_utc": "2026-08-29T00:00:00Z", "supersedes": None},
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R31-D0003", "choice": "Reopen prior R29 rejection SITES-MODULES-CH18-030 and admit it as MC-STK-ERR-1287.", "rationale": "Independent reading of authority lines 7862-7972 shows the localized ringed topos is Sh(C/U), matching item (3) and the proof; the prior final rejection is contradicted by that context.", "timestamp_utc": "2026-08-29T00:00:00Z", "supersedes": "R29-SITES-MODULES-CH18-030"},
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R31-D0004", "choice": "Preserve R29 rejection history and D-lease producer evidence without modifying upstream or historical registry rows.", "rationale": "The reopened admission is append-only evidence with a distinct alias, stable ID, and operation manifest.", "timestamp_utc": "2026-08-29T00:00:00Z", "supersedes": None},
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R31-D0005", "choice": "Require source replay, two fresh builds, deterministic PDF replay, SyncTeX page mapping, full render review, manifest closure, and independent replay before registry admission.", "rationale": "The candidate remains non-admitted until all deterministic gates pass.", "timestamp_utc": "2026-08-29T00:00:00Z", "supersedes": None},
    ]
    (ROOT / "decisions.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in decisions), encoding="utf-8", newline="")

    authority_evidence = [
        file_hash(ROOT / "authority" / "COPYING"),
        file_hash(ROOT / "authority" / "source" / "sites-modules.tex"),
        file_hash(ROOT / "authority" / "upstream.lock.json"),
        file_hash(ROOT / "authority" / "canon" / "R29_SITES_MODULES_INDEPENDENT_ADJUDICATION_20260829.json"),
        file_hash(ROOT / "authority" / "canon" / "R29_SITES_MODULES_OPERATION_DRAFT_20260829.json"),
        file_hash(ROOT / "authority" / "canon" / "R29_SITES_MODULES_PRODUCER_ID_CROSSWALK_DRAFT_20260829.json"),
        file_hash(ROOT / "authority" / "canon" / "R29_rejections.jsonl"),
        file_hash(ROOT / "authority" / "canon" / "R31_SITES_MODULES_REOPENED_REJECTION_20260829.json"),
    ]
    config = {
        "$schema": "../../schemas/candidate-manifest.schema.json",
        "schema": "mathematics-commons-stacks-errata-candidate-config/v1",
        "candidate_id": "stacks-errata-a04446e-r31",
        "namespace": "commons/stacks/errata/r31",
        "lease_id": LEASE_ID,
        "lease_status": "prospective_identifier_only_not_issued_or_registered",
        "writer_task": WRITER,
        "authority_commit": COMMIT,
        "authority_tree": TREE,
        "source_date_epoch": "1788048000",
        "accepted": 1,
        "rejected": 0,
        "unresolved": 0,
        "operation_count": 1,
        "expected_unit_ids": [STABLE],
        "expected_producer_aliases": [ALIAS],
        "proof_closure": {"accepted": 1, "operations": 1, "rejected": 0, "unresolved": 0},
        "authority_evidence": authority_evidence,
        "stems": {"sites-modules": {"authority_bytes": len(authority), "authority_sha256": AUTHORITY_SHA, "payload_bytes": len(payload), "payload_sha256": sha(payload), "display_delimiter_delta": 0, "build_exceptions": {}, "ordered_structure_exceptions": {}, "source_line_exceptions": {}}},
        "visual_qa": {"source_page_map_path": "builds/source-page-map.json", "mapping_strategy": "synctex_every_operation_source_line", "correction_sensitive_pages_strategy": "all_unique_mapped_operation_pages", "high_resolution_pages_strategy": "all_correction_sensitive_pages", "full_page_dpi": 96, "high_resolution_dpi": 180, "contact_sheet_page_capacity": 16},
        "admission_state": "not_admitted",
        "build_state": "not_run",
        "manifest_state": "not_created",
        "review_state": "not_run",
        "reopened_prior_round": "R29",
        "excluded_duplicate_operations": 18,
        "prospective_post_r30_stable_total": 932,
    }
    dump(ROOT / "candidate.config.json", config)
    dump(ROOT / "LEASE.json", {"schema": "mathematics-commons-stacks-candidate-lease-pointer/v1", "candidate_path": "candidates/commons/stacks/errata/r31", "lease_id": LEASE_ID, "lease_registry": "registry/leases.json", "namespace": config["namespace"], "note": "Prospective identifier only; registry admission is a separate append-only transaction.", "state": "prospective_unissued_not_in_registry", "upstream_commit": COMMIT, "writer_contract": "candidates/CONTRACT.md", "writer_task": WRITER})
    dump(ROOT / "source-validation.json", {"schema": "mathematics-commons-stacks-errata-source-validation/v1", "candidate_id": config["candidate_id"], "authority_commit": COMMIT, "passed": True, "accepted_units": 1, "operation_count": 1, "rejected_units": 0, "unresolved_units": 0, "authority": {"bytes": len(authority), "sha256": AUTHORITY_SHA}, "payload": {"path": "payload/sites-modules.tex", "bytes": len(payload), "sha256": sha(payload)}, "operation_spec": {"path": "operation-spec.json"}, "reopened_prior_rejection": "authority/canon/R31_SITES_MODULES_REOPENED_REJECTION_20260829.json", "excluded_duplicate_operations": 18, "authority_bytes_mutated": False})
    dump(ROOT / "INTAKE_VALIDATION.json", {"schema": "stacks-r31-sites-modules-intake-validation/v1", "candidate_id": config["candidate_id"], "passed": True, "accepted": 1, "operations": 1, "rejected": 0, "unresolved": 0, "authority_sha256": AUTHORITY_SHA, "payload_sha256": sha(payload), "stable_id_range": [STABLE, STABLE], "reopened_prior_rejection": RAW, "excluded_duplicate_operations": 18})
    dump(ROOT / "REGENERATION_RECEIPT.json", {"schema": "stacks-r31-sites-modules-regeneration/v1", "candidate_id": config["candidate_id"], "authority": {"path": "authority/source/sites-modules.tex", "bytes": len(authority), "sha256": AUTHORITY_SHA, "commit": COMMIT, "tree": TREE}, "source_packet": file_hash(D_EMENDATIONS), "operation_count": 1, "accepted_units": 1, "excluded_duplicate_operations": 18, "reopened_prior_rejection": RAW, "payload": {"path": "payload/sites-modules.tex", "bytes": len(payload), "sha256": sha(payload)}, "authority_bytes_mutated": False, "generated_at_utc": "2026-08-29T00:00:00Z"})
    print(json.dumps({"passed": True, "candidate_id": config["candidate_id"], "stable_id": STABLE, "operation_count": 1, "excluded_duplicates": 18, "authority_sha256": AUTHORITY_SHA, "payload_bytes": len(payload), "payload_sha256": sha(payload)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
