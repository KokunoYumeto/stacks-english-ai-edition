from __future__ import annotations

import bisect
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
CANDIDATE = "stacks-errata-a04446e-r36"
LEASE = "stacks-lease-000040-errata-r36"
WRITER = "01a0256d-5693-77c1-96b2-cf37101e0c6c"
STAMP = "2026-08-30T16:20:00Z"
SOURCE = "cohomology.tex"
AUTHORITY_SHA = "FA9747D0082AFBF8B09244DCC6C260F8A122E5E3B4A3C69E2273506D76E18A42"
PRODUCER_ID = "CANON-COHOMOLOGY-001"
STABLE_ID = "MC-STK-ERR-1312"
LINE = 11924
OLD = r"(\mathcal{H}')^\bullet \to \mathcal{H}^\bullet"
NEW = r"\mathcal{H}^\bullet \to (\mathcal{H}')^\bullet"


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
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="",
    )


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


def bootstrap(source_root: Path) -> None:
    source_root = source_root.resolve()
    source = source_root / SOURCE
    data = source.read_bytes()
    if sha(data) != AUTHORITY_SHA:
        raise AssertionError("cohomology.tex bootstrap authority hash drift")
    target = ROOT / "authority/source" / SOURCE
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    copying = source_root / "COPYING"
    if copying.is_file():
        (ROOT / "authority/COPYING").write_bytes(copying.read_bytes())
    else:
        prior = ROOT.parent / "r35/authority/COPYING"
        (ROOT / "authority/COPYING").write_bytes(prior.read_bytes())


def build_operation() -> tuple[bytes, dict[str, object]]:
    authority_path = ROOT / "authority/source" / SOURCE
    authority = authority_path.read_bytes()
    if sha(authority) != AUTHORITY_SHA:
        raise AssertionError("candidate authority hash drift")
    old = OLD.encode("utf-8")
    new = NEW.encode("utf-8")
    starts = line_starts(authority)
    positions: list[int] = []
    cursor = 0
    while True:
        position = authority.find(old, cursor)
        if position < 0:
            break
        if line_at(starts, position) == LINE and line_at(starts, position + len(old) - 1) == LINE:
            positions.append(position)
        cursor = position + 1
    if positions != [422290]:
        raise AssertionError(f"unexpected exact preimage positions: {positions}")
    position = positions[0]
    if authority.count(old) != 1:
        raise AssertionError("cohomology mirror preimage is not globally unique")
    operation = {
        "operation_id": f"{STABLE_ID}-OP1",
        "operation_index": 1,
        "stable_id": STABLE_ID,
        "producer_id": PRODUCER_ID,
        "operation_aliases": [],
        "source": SOURCE,
        "source_start_line": LINE,
        "source_end_line": LINE,
        "start_byte": position,
        "end_byte_exclusive": position + len(old),
        "old_text": OLD,
        "old_bytes": len(old),
        "old_sha256": sha(old),
        "replacement_text": NEW,
        "replacement_bytes": len(new),
        "replacement_sha256": sha(new),
        "occurrence_count_in_frozen_authority": 1,
        "declared_line_range_occurrence_count": 1,
        "class": "mathematical_arrow_direction",
        "rationale": (
            "The proof chooses the quasi-isomorphism \\mathcal{F}^\\bullet \\to "
            "\\mathcal{I}^\\bullet. Internal Hom is covariant in its second argument, so "
            "the induced map of total double complexes is \\mathcal{H}^\\bullet \\to "
            "(\\mathcal{H}')^\\bullet, matching the displayed cohomology map at lines "
            "11935--11940; the printed reverse arrow has no source."
        ),
        "registrar_evidence": "authority/registrar/CANON_COHOMOLOGY_001.json",
        "registrar_evidence_sha256": sha((ROOT / "authority/registrar/CANON_COHOMOLOGY_001.json").read_bytes()),
    }
    payload = authority[:position] + new + authority[position + len(old):]
    return payload, operation


def build_manifest() -> dict[str, object]:
    singled = {
        "stable_unit_manifest": ROOT / "stable-units.json",
        "source_map": ROOT / "source-map.jsonl",
        "decision_ledger": ROOT / "decisions.jsonl",
        "rejection_ledger": ROOT / "rejections.jsonl",
        "formula_diagram_inventory": ROOT / "formula-diagram-inventory.json",
    }
    authority_paths = sorted(path for path in (ROOT / "authority").rglob("*") if path.is_file())
    excluded = {ROOT / "candidate.manifest.json", *authority_paths, *singled.values()}
    build_paths = sorted(
        path for path in ROOT.rglob("*")
        if path.is_file() and path not in excluded and "__pycache__" not in path.parts
    )
    review_path = ROOT / "replay/independent-review.json"
    reviewed = review_path.is_file() and json.loads(review_path.read_text(encoding="utf-8")).get("passed") is True
    manifest = {
        "$schema": "../../../../../schemas/candidate-manifest.schema.json",
        "schema": "mathematics-commons-stacks-candidate-manifest/v1",
        "candidate_id": CANDIDATE,
        "lease_id": LEASE,
        "namespace": "commons/stacks/errata/r36",
        "writer_task": WRITER,
        "upstream": {"lock": "upstream/stacks.lock.json", "commit": COMMIT, "tree": TREE},
        "source_authorities": [evidence(path) for path in authority_paths],
        "source_closure": {"enumerated": True, "expected_units": 1, "manifested_units": 1, "complete": True},
        **{key: evidence(path) for key, path in singled.items()},
        "builds": [evidence(path) for path in build_paths],
        "rights_state": (
            "The authority and modified payload retain the Stacks Project GNU Free Documentation "
            "License 1.2; metadata and receipts do not relicense upstream content. This independently "
            "maintained AI-produced English correction overlay has no Stacks Project review, approval, "
            "affiliation, or endorsement."
        ),
        "review_state": "performed" if reviewed else "partial",
        "independent_replay": "passed" if reviewed else "not_performed",
        "unresolved_defects": [
            "Only the independently discovered cohomology.tex:11924 mirror is included.",
            "The analogous sites-cohomology.tex correction was admitted separately in R35 and is not repeated.",
            "This registrar candidate does not compose or push generated Stacks source.",
            "Pinned authority and locale targets remain unmodified.",
        ],
        "stop_conditions": [
            "Do not mutate pinned upstream authority or locale targets.",
            "Do not reopen or alter R35.",
            "Any byte change requires a regenerated manifest and replay.",
        ],
        "generated_at_utc": STAMP,
    }
    dump(ROOT / "candidate.manifest.json", manifest)
    return manifest


def regenerate() -> dict[str, object]:
    authority = ROOT / "authority/source" / SOURCE
    if not authority.is_file():
        raise AssertionError("bootstrap authority is absent")
    dump(
        ROOT / "authority/registrar/CANON_COHOMOLOGY_001.json",
        {
            "schema": "interlanguage-stacks-registrar-observation/v1",
            "producer_id": PRODUCER_ID,
            "authority_commit": COMMIT,
            "authority_path": SOURCE,
            "authority_bytes": authority.stat().st_size,
            "authority_sha256": AUTHORITY_SHA,
            "source_locator": "cohomology.tex:11924",
            "line_start_byte_zero_based": 422273,
            "preimage_byte_span_zero_based": [422289, 422337],
            "inner_operation_byte_span_zero_based": [422290, 422336],
            "old_text": OLD,
            "replacement_text": NEW,
            "preimage_occurrences_in_authority": 1,
            "math_audit": "PASS",
            "registry_dedup_through": "stacks-errata-a04446e-r35",
            "registry_dedup": "PASS; no existing source-path/locus/operation match",
            "related_distinct_unit": "SITES-COHOMOLOGY-028 / MC-STK-ERR-1311 in R35",
            "related_distinct_unit_repeated": False,
            "authority_mutated": False,
            "locale_target_mutated": False,
            "generated_source_composed": False,
        },
    )
    payload, operation = build_operation()
    payload_path = ROOT / "payload" / SOURCE
    payload_path.parent.mkdir(parents=True, exist_ok=True)
    payload_path.write_bytes(payload)
    source_row = {
        "schema": "mathematics-commons-stacks-errata-map/v2",
        "unit_id": STABLE_ID,
        "class": "source_defect_correction",
        "source": SOURCE,
        "authority": f"authority/source/{SOURCE}",
        "authority_sha256": AUTHORITY_SHA,
        "payload": f"payload/{SOURCE}",
        "locus": "cohomology.tex:11924",
        "producer_id": PRODUCER_ID,
        "producer_ids": [PRODUCER_ID],
        "operation_aliases": [],
        "operations": [operation],
        "proof": "accepted_after_independent_exact_preimage_context_math_and_registry_deduplication",
        "adverse_evidence": (
            "The frozen source remains authority provenance. The same semantic defect in "
            "sites-cohomology.tex was a distinct R35 unit and is not duplicated here."
        ),
    }
    (ROOT / "source-map.jsonl").write_text(
        json.dumps(source_row, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="",
    )
    (ROOT / "rejections.jsonl").write_text("", encoding="utf-8", newline="")
    dump(
        ROOT / "operation-spec.json",
        {
            "schema": "mathematics-commons-stacks-errata-operation-spec/v1",
            "authority_commit": COMMIT,
            "apply_order": "descending_start_byte_per_source",
            "operation_count": 1,
            "operations": [operation],
        },
    )
    dump(
        ROOT / "stable-units.json",
        {
            "schema": "mathematics-commons-stacks-errata-units/v1",
            "authority_commit": COMMIT,
            "unit_count": 1,
            "units": [{
                "id": STABLE_ID,
                "class": "source_defect_correction",
                "source": SOURCE,
                "payload": f"payload/{SOURCE}",
                "locus": "cohomology.tex:11924",
                "operation_ids": [f"{STABLE_ID}-OP1"],
                "producer_id": PRODUCER_ID,
                "producer_ids": [PRODUCER_ID],
                "status": "accepted_new",
            }],
        },
    )
    dump(
        ROOT / "formula-diagram-inventory.json",
        {
            "schema": "mathematics-commons-stacks-errata-formula-diagram-inventory/v1",
            "candidate_id": CANDIDATE,
            "authority_commit": COMMIT,
            "unit_count": 1,
            "formula_units": [STABLE_ID],
            "diagram_units": [],
            "prose_only_units": [],
            "unmapped_formula_or_diagram_changes": 0,
        },
    )
    decisions = [
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R36-D0001",
            "choice": "Admit the independently discovered cohomology.tex:11924 arrow reversal as a distinct source-path unit.",
            "rationale": "The exact preimage occurs once and the proof forces covariance in the second internal-Hom argument.",
            "timestamp_utc": STAMP,
        },
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R36-D0002",
            "choice": "Allocate MC-STK-ERR-1312 and preserve CANON-COHOMOLOGY-001 as its registrar provenance ID.",
            "rationale": "No producer row or admitted unit covers the exact cohomology.tex source path and locus through R35.",
            "timestamp_utc": STAMP,
        },
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R36-D0003",
            "choice": "Keep the analogous sites-cohomology.tex unit in R35 and do not repeat it in R36.",
            "rationale": "The two files have distinct authority bytes and stable units, but each operation must be applied exactly once per source path.",
            "timestamp_utc": STAMP,
        },
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R36-D0004",
            "choice": "Keep authority, locale targets, and generated-source trees unchanged in the registrar lane.",
            "rationale": "Admission and generated-source composition are separate transactions.",
            "timestamp_utc": STAMP,
        },
    ]
    (ROOT / "decisions.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in decisions),
        encoding="utf-8",
        newline="",
    )
    dump(
        ROOT / "authority/upstream.lock.json",
        {
            "schema": "mathematics-commons-stacks-upstream-lock/v1",
            "repository": "https://github.com/stacks/stacks-project",
            "commit": COMMIT,
            "tree": TREE,
            "sources": [{
                "path": f"authority/source/{SOURCE}",
                "bytes": authority.stat().st_size,
                "sha256": AUTHORITY_SHA,
            }],
            "authority_mutated": False,
        },
    )
    registry = json.loads((REPO / "registry/overlays.json").read_text(encoding="utf-8"))
    already_admitted = any(entry.get("id") == CANDIDATE for entry in registry["registered_entries"])
    dump(
        ROOT / "LEASE.json",
        {
            "schema": "mathematics-commons-stacks-candidate-lease-pointer/v1",
            "candidate_path": "candidates/commons/stacks/errata/r36",
            "lease_id": LEASE,
            "namespace": "commons/stacks/errata/r36",
            "state": "released_after_admission" if already_admitted else "active_pending_admission",
            "upstream_commit": COMMIT,
            "writer_contract": "candidates/CONTRACT.md",
            "writer_task": WRITER,
        },
    )
    dump(
        ROOT / "candidate.config.json",
        {
            "$schema": "../../schemas/candidate-manifest.schema.json",
            "schema": "mathematics-commons-stacks-errata-candidate-config/v1",
            "candidate_id": CANDIDATE,
            "namespace": "commons/stacks/errata/r36",
            "lease_id": LEASE,
            "writer_task": WRITER,
            "authority_commit": COMMIT,
            "authority_tree": TREE,
            "accepted": 1,
            "rejected": 0,
            "unresolved": 0,
            "operation_count": 1,
            "expected_unit_ids": [STABLE_ID],
            "expected_producer_ids": [PRODUCER_ID],
            "stems": {SOURCE: {
                "authority_bytes": authority.stat().st_size,
                "authority_sha256": AUTHORITY_SHA,
                "payload_bytes": len(payload),
                "payload_sha256": sha(payload),
                "operations": 1,
            }},
            "composition_performed": False,
        },
    )
    dump(
        ROOT / "source-validation.json",
        {
            "schema": "mathematics-commons-stacks-errata-source-validation/v1",
            "candidate_id": CANDIDATE,
            "passed": True,
            "authorities": {SOURCE: evidence(authority)},
            "registrar_observation": evidence(ROOT / "authority/registrar/CANON_COHOMOLOGY_001.json"),
            "accepted_units": 1,
            "operation_count": 1,
            "rejected_units": 0,
            "unresolved_units": 0,
            "payloads": {SOURCE: evidence(payload_path)},
            "authority_bytes_mutated": False,
            "locale_target_bytes_mutated": False,
            "generated_source_composed": False,
        },
    )
    dump(
        ROOT / "REGENERATION_RECEIPT.json",
        {
            "schema": "stacks-r36-cohomology-mirror-regeneration/v1",
            "candidate_id": CANDIDATE,
            "semantic_units": 1,
            "operations": 1,
            "stable_id_range": [STABLE_ID, STABLE_ID],
            "payloads": {SOURCE: evidence(payload_path)},
            "authority_bytes_mutated": False,
            "generated_source_composed": False,
            "generated_at_utc": STAMP,
        },
    )
    (ROOT / "README.md").write_text(
        "# R36: `cohomology.tex` mirror correction\n\n"
        "Registrar-only admission of the independently discovered reversed natural comparison map at line 11924. "
        "The analogous `sites-cohomology.tex` correction is already the distinct R35 unit MC-STK-ERR-1311.\n\n"
        "This candidate does not mutate pinned authority or locale targets and does not compose generated Stacks source.\n",
        encoding="utf-8",
        newline="",
    )
    (ROOT / "BUILD.md").write_text(
        "Run `python pipeline_r36.py verify` for deterministic source and manifest replay. "
        "Admission requires a passing independent review and runs `python pipeline_r36.py admit`.\n",
        encoding="utf-8",
        newline="",
    )
    build_manifest()
    return {
        "passed": True,
        "candidate_id": CANDIDATE,
        "units": 1,
        "operations": 1,
        "payloads": {SOURCE: sha(payload)},
        "manifest_sha256": sha((ROOT / "candidate.manifest.json").read_bytes()),
    }


def verify_manifest() -> None:
    manifest = json.loads((ROOT / "candidate.manifest.json").read_text(encoding="utf-8"))
    references = list(manifest["source_authorities"])
    for key in ("stable_unit_manifest", "source_map", "decision_ledger", "rejection_ledger", "formula_diagram_inventory"):
        references.append(manifest[key])
    references.extend(manifest["builds"])
    seen: set[str] = set()
    for row in references:
        path_text = str(row["path"])
        if path_text in seen:
            raise AssertionError(f"duplicate manifest reference: {path_text}")
        seen.add(path_text)
        path = ROOT / path_text
        if not path.is_file() or path.stat().st_size != row["bytes"] or sha(path.read_bytes()) != row["sha256"]:
            raise AssertionError(f"manifest reference mismatch: {path_text}")


def verify(require_review: bool = False) -> dict[str, object]:
    expected_payload, expected_operation = build_operation()
    payload_path = ROOT / "payload" / SOURCE
    if payload_path.read_bytes() != expected_payload:
        raise AssertionError("payload replay mismatch")
    spec = json.loads((ROOT / "operation-spec.json").read_text(encoding="utf-8"))
    if spec["operation_count"] != 1 or spec["operations"] != [expected_operation]:
        raise AssertionError("operation-spec replay mismatch")
    units = json.loads((ROOT / "stable-units.json").read_text(encoding="utf-8"))
    if units["unit_count"] != 1 or [unit["id"] for unit in units["units"]] != [STABLE_ID]:
        raise AssertionError("stable-unit identity drift")
    registry = json.loads((REPO / "registry/overlays.json").read_text(encoding="utf-8"))
    entries = registry["registered_entries"]
    admitted = any(entry["id"] == CANDIDATE for entry in entries)
    allowed_head = CANDIDATE if admitted else "stacks-errata-a04446e-r35"
    if entries[-1]["id"] != allowed_head:
        raise AssertionError(f"registry head drift: {entries[-1]['id']}")
    allocated = {stable for entry in entries if entry["id"] != CANDIDATE for stable in entry["stable_ids"]}
    if STABLE_ID in allocated:
        raise AssertionError("stable-ID collision")
    for entry in entries:
        if entry["id"] == CANDIDATE:
            continue
        source_map = REPO / "candidates/commons/stacks/errata" / entry["id"].rsplit("r", 1)[-1]
        del source_map
    source_maps = list((REPO / "candidates/commons/stacks/errata").glob("r*/source-map.jsonl"))
    exact_matches = []
    for source_map in source_maps:
        if source_map.parent == ROOT:
            continue
        for raw in source_map.read_text(encoding="utf-8").splitlines():
            if not raw.strip():
                continue
            row = json.loads(raw)
            if row.get("source") == SOURCE and row.get("locus") == "cohomology.tex:11924":
                exact_matches.append((source_map.as_posix(), row.get("unit_id")))
    if exact_matches:
        raise AssertionError(f"registry duplicate at exact source locus: {exact_matches}")
    if require_review:
        review = json.loads((ROOT / "replay/independent-review.json").read_text(encoding="utf-8"))
        if review.get("passed") is not True or review.get("pass_is_unconditional") is not True:
            raise AssertionError("independent review is absent or conditional")
    verify_manifest()
    manifest = json.loads((ROOT / "candidate.manifest.json").read_text(encoding="utf-8"))
    return {
        "candidate_id": CANDIDATE,
        "manifest_references": len(manifest["source_authorities"]) + 5 + len(manifest["builds"]),
        "operations": 1,
        "passed": True,
        "payload_sha256": {SOURCE: sha(expected_payload)},
        "stable_ids": [STABLE_ID],
        "units": 1,
    }


def admit() -> dict[str, object]:
    core = verify(require_review=True)
    registry_path = REPO / "registry/overlays.json"
    leases_path = REPO / "registry/leases.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    if registry["registered_entries"][-1]["id"] != "stacks-errata-a04446e-r35":
        raise AssertionError("registry is not at exact R35 head")
    registry_before = sha(registry_path.read_bytes())
    leases_before = sha(leases_path.read_bytes())
    registry["registered_entries"].append({
        "id": CANDIDATE,
        "namespace": "commons/stacks/errata/r36",
        "writer": WRITER,
        "source_commit": COMMIT,
        "source_tree": TREE,
        "manifest_sha256": sha((ROOT / "candidate.manifest.json").read_bytes()),
        "stable_ids": [STABLE_ID],
        "rights_state": (
            "The authority and modified payload retain the Stacks Project GNU Free Documentation "
            "License 1.2; metadata and receipts do not relicense upstream content. This independently "
            "maintained AI-produced English correction overlay has no Stacks Project review, approval, "
            "affiliation, or endorsement."
        ),
        "review_receipt": "candidates/commons/stacks/errata/r36/replay/independent-review.json",
        "admitted_at_utc": STAMP,
    })
    dump_registry(registry_path, registry)
    leases = json.loads(leases_path.read_text(encoding="utf-8"))
    if leases["events"][-1]["event_id"] != "lease-event-000075":
        raise AssertionError("lease registry is not at exact R35 head")
    common = {
        "lease_id": LEASE,
        "namespace": "commons/stacks/errata/r36",
        "candidate_path": "candidates/commons/stacks/errata/r36",
        "writer_task": WRITER,
        "upstream_commit": COMMIT,
        "upstream_tree": TREE,
        "issued_at_utc": STAMP,
        "writer_contract": "candidates/CONTRACT.md",
    }
    leases["events"].append({"event_id": "lease-event-000076", "event": "issued", **common, "state": "active", "supersedes_event_id": "lease-event-000075"})
    leases["events"].append({"event_id": "lease-event-000077", "event": "released", **common, "state": "released", "supersedes_event_id": "lease-event-000076"})
    dump_registry(leases_path, leases)
    regenerate()
    manifest_sha = sha((ROOT / "candidate.manifest.json").read_bytes())
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    if registry["registered_entries"][-1]["id"] != CANDIDATE:
        raise AssertionError("R36 registry transition drifted")
    registry["registered_entries"][-1]["manifest_sha256"] = manifest_sha
    dump_registry(registry_path, registry)
    core = verify(require_review=True)
    receipt_path = REPO / "registry/admission-receipts/r36.json"
    receipt = {
        "schema": "mathematics-commons-stacks-registry-admission-receipt/v1",
        "candidate_id": CANDIDATE,
        "admitted_at_utc": STAMP,
        "manifest": evidence(ROOT / "candidate.manifest.json"),
        "source_map": evidence(ROOT / "source-map.jsonl"),
        "stable_ids": [STABLE_ID],
        "stable_id_count": 1,
        "producer_ids": [PRODUCER_ID],
        "registry": {"before_sha256": registry_before, "after_sha256": sha(registry_path.read_bytes()), "last_overlay": CANDIDATE},
        "leases": {"before_sha256": leases_before, "after_sha256": sha(leases_path.read_bytes()), "issued_event": "lease-event-000076", "released_event": "lease-event-000077"},
        "fresh_replay": core,
        "constraints": {"authority_mutated": False, "producer_target_mutated": False, "generated_source_composed": False, "generated_source_pushed": False, "published": False},
        "status": "PASS",
    }
    dump(receipt_path, receipt)
    return {
        "candidate_id": CANDIDATE,
        "leases_sha256": sha(leases_path.read_bytes()),
        "manifest_sha256": manifest_sha,
        "passed": True,
        "receipt_sha256": sha(receipt_path.read_bytes()),
        "registry_sha256": sha(registry_path.read_bytes()),
    }


def main() -> int:
    if len(sys.argv) < 2:
        raise SystemExit("usage: pipeline_r36.py bootstrap SOURCE_ROOT | regenerate | verify | admit")
    mode = sys.argv[1]
    if mode == "bootstrap":
        if len(sys.argv) != 3:
            raise SystemExit("bootstrap requires SOURCE_ROOT")
        bootstrap(Path(sys.argv[2]))
        result = regenerate()
    elif mode == "regenerate":
        result = regenerate()
    elif mode == "verify":
        result = verify(require_review=False)
    elif mode == "admit":
        result = admit()
    else:
        raise SystemExit(f"unknown mode: {mode}")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
