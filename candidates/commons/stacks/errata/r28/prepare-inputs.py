from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
R26 = ROOT.parent / "r26"

CANDIDATE_ID = "stacks-errata-a04446e-r28"
LEASE_ID = "stacks-lease-000032-errata-r28"
NAMESPACE = "commons/stacks/errata/r28"
WRITER_TASK = "01a0256d-5693-77c1-96b2-cf37101e0c6c"
GENERATED_AT = "2026-08-28T19:43:50Z"
SOURCE_DATE_EPOCH = "1787946230"

UPSTREAM_COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
UPSTREAM_TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
UPSTREAM_SHA256 = "FD28CF874BB7DAD3C5C5FF03314D1C83701613A8A98730A99B9CA7A4BCFE6068"
UPSTREAM_BYTES = 134660

COMPOSITION_COMMIT = "f8e6c227aa3dc89256427f3b64a2ad330d5ff221"
COMPOSITION_TREE = "94112e11f45252b9f9ce01783103e0b925f0cc0d"
COMPOSITION_BLOB = "ea0c59e134220971957a0a019e57663d0102cd07"
COMPOSITION_SHA256 = "85251479BB7D35D73CD5691C194D33B3ADC1BF245BCC248643D969DBBA0E7928"
COMPOSITION_BYTES = 134830

R26_MANIFEST_SHA256 = "1A045F9452501725CAF45996FD19C633D594E0C3D57AA745780C3C06FB031085"
R26_SOURCE_MAP_SHA256 = "46C29F2D0DFDC1081FFFDA61757DFCEB4E3036881A9D2D272B5ED9D67626B9BF"
PRIOR_UNIT = "MC-STK-ERR-1183"
PRIOR_OPERATION = "MC-STK-ERR-1183-OP1"
NEW_UNIT = "MC-STK-ERR-1216"
NEW_OPERATION = "MC-STK-ERR-1216-OP1"
PRODUCER_ID = "SMOOTHING-026"

OFFICIAL_OLD = "$a_kb_k$"
PRIOR_REPLACEMENT = "$(a_k)^N + b_k$"
NEW_REPLACEMENT = "$a_k((a_k)^N + b_k)$"
OFFICIAL_OFFSET = 56549
COMPOSITION_OFFSET = 56560
SOURCE_LINE = 1481


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="",
    )


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
        newline="",
    )


def replace_exact(data: bytes, old_text: str, new_text: str) -> tuple[bytes, int]:
    old = old_text.encode("utf-8")
    new = new_text.encode("utf-8")
    if data.count(old) != 1:
        raise AssertionError(f"expected exactly one preimage: {old_text!r}")
    offset = data.index(old)
    return data[:offset] + new + data[offset + len(old):], offset


def main() -> int:
    official_path = ROOT / "authority/source/smoothing.tex"
    composition_path = ROOT / "authority/composition-base/smoothing.tex"
    official = official_path.read_bytes()
    composition = composition_path.read_bytes()
    if len(official) != UPSTREAM_BYTES or sha_bytes(official) != UPSTREAM_SHA256:
        raise AssertionError("official frozen smoothing.tex identity mismatch")
    if len(composition) != COMPOSITION_BYTES or sha_bytes(composition) != COMPOSITION_SHA256:
        raise AssertionError("public cumulative smoothing.tex identity mismatch")

    payload, official_offset = replace_exact(official, OFFICIAL_OLD, NEW_REPLACEMENT)
    projection, composition_offset = replace_exact(composition, PRIOR_REPLACEMENT, NEW_REPLACEMENT)
    if official_offset != OFFICIAL_OFFSET or composition_offset != COMPOSITION_OFFSET:
        raise AssertionError("sealed byte offset changed")
    if len(payload) != 134672 or sha_bytes(payload) != "7C475ABEFC3CF2F3F2534F0CA69B8D8BB726BF88195CB50FE849DF99B7D0CD4A":
        raise AssertionError("standalone payload identity mismatch")
    if len(projection) != 134835 or sha_bytes(projection) != "85A37C95D5591632D11E7BE6775039638B6F5200B44729ABCEA1A644D9F5B056":
        raise AssertionError("cumulative composition projection identity mismatch")
    (ROOT / "payload/smoothing.tex").write_bytes(payload)
    (ROOT / "composition-projection/smoothing.tex").write_bytes(projection)

    r26_manifest = R26 / "candidate.manifest.json"
    r26_map = R26 / "source-map.jsonl"
    if sha_file(r26_manifest) != R26_MANIFEST_SHA256 or sha_file(r26_map) != R26_SOURCE_MAP_SHA256:
        raise AssertionError("R26 predecessor evidence mismatch")
    predecessor_rows = [
        json.loads(line)
        for line in r26_map.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    predecessor = next((row for row in predecessor_rows if row["unit_id"] == PRIOR_UNIT), None)
    if predecessor is None or len(predecessor["operations"]) != 1:
        raise AssertionError("R26 predecessor unit missing or ambiguous")
    predecessor_op = predecessor["operations"][0]
    if (
        predecessor_op["operation_id"] != PRIOR_OPERATION
        or predecessor_op["old_text"] != OFFICIAL_OLD
        or predecessor_op["replacement_text"] != PRIOR_REPLACEMENT
        or predecessor_op["start_byte"] != OFFICIAL_OFFSET
    ):
        raise AssertionError("R26 predecessor operation mismatch")

    official_old = OFFICIAL_OLD.encode("utf-8")
    prior = PRIOR_REPLACEMENT.encode("utf-8")
    replacement = NEW_REPLACEMENT.encode("utf-8")
    operation = {
        "end_byte_exclusive": OFFICIAL_OFFSET + len(official_old),
        "occurrence_count_in_frozen_authority": 1,
        "old_bytes": len(official_old),
        "old_sha256": sha_bytes(official_old),
        "old_text": OFFICIAL_OLD,
        "operation_id": NEW_OPERATION,
        "operation_index": 1,
        "producer_id": PRODUCER_ID,
        "producer_operation_id": PRODUCER_ID,
        "replacement_bytes": len(replacement),
        "replacement_sha256": sha_bytes(replacement),
        "replacement_text": NEW_REPLACEMENT,
        "semantic_unit_producer_id": PRODUCER_ID,
        "source_end_line": SOURCE_LINE,
        "source_start_line": SOURCE_LINE,
        "stable_id": NEW_UNIT,
        "start_byte": OFFICIAL_OFFSET,
        "supersedes_operation_id": PRIOR_OPERATION,
    }
    composition_operation = {
        "base_blob": COMPOSITION_BLOB,
        "base_commit": COMPOSITION_COMMIT,
        "base_end_byte_exclusive": COMPOSITION_OFFSET + len(prior),
        "base_occurrence_count": 1,
        "base_old_bytes": len(prior),
        "base_old_sha256": sha_bytes(prior),
        "base_old_text": PRIOR_REPLACEMENT,
        "base_sha256": COMPOSITION_SHA256,
        "base_start_byte": COMPOSITION_OFFSET,
        "base_tree": COMPOSITION_TREE,
        "output_bytes": len(projection),
        "output_sha256": sha_bytes(projection),
        "replacement_bytes": len(replacement),
        "replacement_sha256": sha_bytes(replacement),
        "replacement_text": NEW_REPLACEMENT,
    }

    predecessor_binding = {
        "schema": "mathematics-commons-stacks-errata-predecessor-binding/v1",
        "candidate_id": CANDIDATE_ID,
        "composition_base": {
            "blob": COMPOSITION_BLOB,
            "bytes": COMPOSITION_BYTES,
            "commit": COMPOSITION_COMMIT,
            "path": "authority/composition-base/smoothing.tex",
            "sha256": COMPOSITION_SHA256,
            "tree": COMPOSITION_TREE,
        },
        "predecessor": {
            "manifest_sha256": R26_MANIFEST_SHA256,
            "operation_id": PRIOR_OPERATION,
            "overlay_id": "stacks-errata-a04446e-r26",
            "replacement_sha256": sha_bytes(prior),
            "replacement_text": PRIOR_REPLACEMENT,
            "source_map_sha256": R26_SOURCE_MAP_SHA256,
            "unit_id": PRIOR_UNIT,
        },
        "projection": {
            "bytes": len(projection),
            "path": "composition-projection/smoothing.tex",
            "sha256": sha_bytes(projection),
        },
        "superseding_operation": composition_operation,
    }
    write_json(ROOT / "R28_PREDECESSOR_BINDING.json", predecessor_binding)

    spec = {
        "schema": "mathematics-commons-stacks-r28-smoothing-supersession-spec/v1",
        "candidate_id": CANDIDATE_ID,
        "accepted": [{
            "class": "source_defect_correction_supersession",
            "composition_operation": composition_operation,
            "locus": "smoothing.tex:1481",
            "operations": [operation],
            "producer_ids": [PRODUCER_ID],
            "rationale": (
                "The R26 replacement c=a_k^N+b_k preserves the principal open only on Spec(Cbar), "
                "but the proof requires the ambient localization equality (Ibar_k)_c=(Ibar)_c. "
                "Replacing by a_k c makes both a_k and c invertible, so c/a_k^N is an annihilating unit; "
                "modulo Ibar the new element is a_k^(N+1), preserving the same cover."
            ),
            "stable_id": NEW_UNIT,
            "supersedes_unit_id": PRIOR_UNIT,
        }],
        "accepted_count": 1,
        "operation_count": 1,
        "predecessor_binding": "R28_PREDECESSOR_BINDING.json",
        "rejected": [],
        "rejected_count": 0,
        "unresolved": [],
        "unresolved_count": 0,
    }
    write_json(ROOT / "R28_SMOOTHING_SUPERSESSION_SPEC.json", spec)

    operation_spec = {
        "authority_bytes": len(official),
        "authority_sha256": sha_bytes(official),
        "candidate_id": CANDIDATE_ID,
        "composition_base_bytes": len(composition),
        "composition_base_sha256": sha_bytes(composition),
        "composition_operation": composition_operation,
        "operation_count": 1,
        "operations": [operation],
        "schema": "mathematics-commons-stacks-errata-operation-spec/v1",
    }
    write_json(ROOT / "operation-spec.json", operation_spec)

    source_map = [{
        "adverse_evidence": (
            "R26 remains immutable. This new unit corrects its insufficient replacement and must be composed "
            "last-wins only at the explicitly bound overlapping locus."
        ),
        "authority": "authority/source/smoothing.tex",
        "authority_sha256": sha_bytes(official),
        "class": "source_defect_correction_supersession",
        "composition_base": "authority/composition-base/smoothing.tex",
        "composition_projection": "composition-projection/smoothing.tex",
        "locus": "smoothing.tex:1481",
        "operations": [operation],
        "payload": "payload/smoothing.tex",
        "predecessor_manifest_sha256": R26_MANIFEST_SHA256,
        "predecessor_operation_id": PRIOR_OPERATION,
        "predecessor_overlay_id": "stacks-errata-a04446e-r26",
        "producer_id": PRODUCER_ID,
        "producer_ids": [PRODUCER_ID],
        "proof": "accepted_after_independent_counterexample_and_localization_reproof",
        "schema": "mathematics-commons-stacks-errata-map/v2",
        "source": "smoothing.tex",
        "supersedes_unit_id": PRIOR_UNIT,
        "unit_id": NEW_UNIT,
    }]
    write_jsonl(ROOT / "source-map.jsonl", source_map)
    stable = {
        "candidate_id": CANDIDATE_ID,
        "schema": "mathematics-commons-stacks-stable-unit-manifest/v1",
        "units": [{
            "class": "source_defect_correction_supersession",
            "id": NEW_UNIT,
            "locus": "smoothing.tex:1481",
            "operation_ids": [NEW_OPERATION],
            "payload": "payload/smoothing.tex",
            "predecessor_manifest_sha256": R26_MANIFEST_SHA256,
            "predecessor_operation_id": PRIOR_OPERATION,
            "predecessor_overlay_id": "stacks-errata-a04446e-r26",
            "producer_id": PRODUCER_ID,
            "producer_ids": [PRODUCER_ID],
            "source": "smoothing.tex",
            "status": "provisional_accepted_not_admitted",
            "supersedes_unit_id": PRIOR_UNIT,
        }],
    }
    write_json(ROOT / "stable-units.json", stable)
    decisions = [
        {
            "choice": f"Allocate {NEW_UNIT} as an append-only supersession of {PRIOR_UNIT}; never mutate or reuse the R26 stable unit.",
            "id": "ERR-R28-D0001",
            "rationale": "Global stable IDs are unique and the prior admitted record remains provenance; an explicit new unit preserves both histories.",
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "supersedes": None,
            "timestamp_utc": GENERATED_AT,
        },
        {
            "choice": f"Replace {OFFICIAL_OLD} by {NEW_REPLACEMENT} in the standalone authority projection and replace the R26 effective text {PRIOR_REPLACEMENT} by the same correction in cumulative composition.",
            "id": "ERR-R28-D0002",
            "rationale": "The extra a_k factor makes both a_k and a_k^N+b_k invertible while preserving the same principal-open cover modulo Ibar.",
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "supersedes": "ERR-R26-D0005",
            "timestamp_utc": GENERATED_AT,
        },
        {
            "choice": f"Bind composition to public main {COMPOSITION_COMMIT} and exact blob {COMPOSITION_BLOB}; never copy the isolated R28 payload wholesale into the cumulative tree.",
            "id": "ERR-R28-D0003",
            "rationale": "The public base contains R1-R27 and later Illusie work that must remain intact; only the manifest-bound overlapping fragment may change.",
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "supersedes": None,
            "timestamp_utc": GENERATED_AT,
        },
    ]
    write_jsonl(ROOT / "decisions.jsonl", decisions)
    (ROOT / "rejections.jsonl").write_bytes(b"")
    write_json(ROOT / "formula-diagram-inventory.json", {
        "candidate_id": CANDIDATE_ID,
        "classification": "The sole superseding unit changes one inline formula and no diagram source.",
        "diagram_units": [],
        "formula_units": [NEW_UNIT],
        "prose_only_units": [],
        "schema": "mathematics-commons-stacks-errata-formula-diagram-inventory/v1",
        "unit_count": 1,
        "unmapped_formula_or_diagram_changes": 0,
    })

    intake = {
        "schema": "mathematics-commons-stacks-r28-intake-validation/v1",
        "candidate_id": CANDIDATE_ID,
        "generated_at_utc": GENERATED_AT,
        "passed": True,
        "proof_closure": {"accepted": 1, "operations": 1, "rejected": 0, "unresolved": 0},
        "r26_predecessor": predecessor_binding["predecessor"],
        "source_preimages": {
            "composition_base_count": composition.count(prior),
            "composition_base_offset": COMPOSITION_OFFSET,
            "official_authority_count": official.count(official_old),
            "official_authority_offset": OFFICIAL_OFFSET,
        },
        "standalone_payload": {"bytes": len(payload), "sha256": sha_bytes(payload)},
        "composition_projection": {"bytes": len(projection), "sha256": sha_bytes(projection)},
    }
    write_json(ROOT / "INTAKE_VALIDATION.json", intake)

    page_map_path = ROOT / "builds/source-page-map.json"
    if page_map_path.is_file():
        page_map = json.loads(page_map_path.read_text(encoding="utf-8"))
        visual_pages = page_map["unique_pages"]
        page_map_evidence = {
            "bytes": page_map_path.stat().st_size,
            "path": "builds/source-page-map.json",
            "sha256": sha_file(page_map_path),
        }
    else:
        visual_pages = [1]
        page_map_evidence = None
    config = {
        "accepted": 1,
        "authority_commit": UPSTREAM_COMMIT,
        "authority_tree": UPSTREAM_TREE,
        "candidate_id": CANDIDATE_ID,
        "expected_unit_ids": [NEW_UNIT],
        "lease_id": LEASE_ID,
        "namespace": NAMESPACE,
        "operation_count": 1,
        "private_render_logical_path": "canon/private_evidence/errata-r28-20260828T194350Z/render",
        "proof_closure": {"accepted": 1, "operations": 1, "rejected": 0, "unresolved": 0},
        "rejected": 0,
        "schema": "mathematics-commons-stacks-errata-candidate-config/v1",
        "source_date_epoch": SOURCE_DATE_EPOCH,
        "stems": {
            "smoothing": {
                "authority_bytes": len(official),
                "authority_sha256": sha_bytes(official),
                "build_exceptions": {},
                "display_delimiter_delta": payload.count(b"$$") - official.count(b"$$"),
                "ordered_structure_exceptions": {},
                "payload_bytes": len(payload),
                "payload_sha256": sha_bytes(payload),
                "source_line_exceptions": {},
            }
        },
        "unresolved": 0,
        "visual_qa": {
            "correction_sensitive_pages": {"smoothing": visual_pages},
            "high_resolution_pages": {"smoothing": visual_pages},
            "source_page_map": page_map_evidence,
        },
        "writer_task": WRITER_TASK,
    }
    write_json(ROOT / "candidate.config.json", config)
    write_json(ROOT / "LEASE.json", {
        "candidate_path": "candidates/commons/stacks/errata/r28",
        "lease_id": LEASE_ID,
        "namespace": NAMESPACE,
        "schema": "mathematics-commons-stacks-lease/v1",
        "state": "active",
        "upstream_commit": UPSTREAM_COMMIT,
        "upstream_tree": UPSTREAM_TREE,
        "writer_task": WRITER_TASK,
    })

    canon = ROOT / "authority/canon"
    canon.mkdir(parents=True, exist_ok=True)
    for name in (
        "R28_PREDECESSOR_BINDING.json",
        "R28_SMOOTHING_SUPERSESSION_SPEC.json",
        "INTAKE_VALIDATION.json",
    ):
        shutil.copy2(ROOT / name, canon / name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
