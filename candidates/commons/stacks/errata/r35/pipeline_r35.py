from __future__ import annotations

import bisect
import csv
import hashlib
import io
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
CANDIDATE = "stacks-errata-a04446e-r35"
LEASE = "stacks-lease-000039-errata-r35"
WRITER = "01a0256d-5693-77c1-96b2-cf37101e0c6c"
STAMP = "2026-08-30T15:30:00Z"
SITES_SHA = "5B335CE2C7208A128B3C744B8828D93508063F41A4FABBCE2E921F890928895C"
SITES_LIVE_LEDGER_SHA = "AFD6E4910E2D263E1B25B3715D8C64348A8CF2802AC079D6B9DFEBB13CDE6F6E"
SITES_PACKET_IDS = ["SITES-COHOMOLOGY-012", "SITES-COHOMOLOGY-013", "SITES-COHOMOLOGY-028"]


CASES = [
    {
        "stable_id": "MC-STK-ERR-1309", "producer_id": "SITES-COHOMOLOGY-012",
        "source": "sites-cohomology.tex", "start_line": 11671, "end_line": 11671,
        "old": r"(M^\bullet \otimes_{\mathcal{O}(U)} \mathcal{O}_U)^\#",
        "new": r"(\mathcal{M}^\bullet(U) \otimes_{\mathcal{O}(U)} \mathcal{O}_U)^\#",
        "kind": "mathematical_typing",
        "rationale": "The proof chose the sheaf complex \\mathcal{M}^\\bullet, while assumption (2) applies to the K-flat \\mathcal{O}(U)-complex of sections \\mathcal{M}^\\bullet(U); the identical generic M^\\bullet occurrence at line 11619 remains valid.",
    },
    {
        "stable_id": "MC-STK-ERR-1310", "producer_id": "SITES-COHOMOLOGY-013",
        "source": "sites-cohomology.tex", "start_line": 11933, "end_line": 11933,
        "old": r"\SheafHom_\mathcal{O}(\mathcal{L}^{-q}, \mathcal{I}^p)",
        "new": r"\SheafHom_\mathcal{O}(\mathcal{E}^{-q}, \mathcal{I}^p)",
        "kind": "mathematical_symbol",
        "rationale": "The lemma fixes the strictly perfect source complex \\mathcal{E}^\\bullet; no \\mathcal{L}^\\bullet is introduced, and the comparison complex immediately above uses \\mathcal{E}^{-q}.",
    },
    {
        "stable_id": "MC-STK-ERR-1311", "producer_id": "SITES-COHOMOLOGY-028",
        "source": "sites-cohomology.tex", "start_line": 12001, "end_line": 12001,
        "old": r"(\mathcal{H}')^\bullet \to \mathcal{H}^\bullet",
        "new": r"\mathcal{H}^\bullet \to (\mathcal{H}')^\bullet",
        "kind": "mathematical_arrow_direction",
        "rationale": "The chosen quasi-isomorphism \\mathcal{F}^\\bullet \\to \\mathcal{I}^\\bullet induces the comparison covariantly in the second Hom argument, from the F-based complex \\mathcal{H}^\\bullet to the I-based complex (\\mathcal{H}')^\\bullet.",
    },
]


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
    """Preserve registry insertion order; historical entries must not be re-sorted."""
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


def prefix_through_lf(data: bytes, count: int) -> bytes:
    seen = 0
    for index, value in enumerate(data):
        if value == 10:
            seen += 1
            if seen == count:
                return data[: index + 1]
    raise AssertionError(f"input has fewer than {count} LF-terminated lines")


def bootstrap(source_root: Path, producer_root: Path) -> None:
    source_root = source_root.resolve()
    producer_root = producer_root.resolve()
    inputs = {
        source_root / "sites-cohomology.tex": (ROOT / "authority/source/sites-cohomology.tex", SITES_SHA),
    }
    for source, (target, expected_sha) in inputs.items():
        data = source.read_bytes()
        if sha(data) != expected_sha:
            raise AssertionError(f"bootstrap input hash drift: {source.name}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    sites_live_path = producer_root / "SITES_COHOMOLOGY_SOURCE_DEFECT_LEDGER.csv"
    sites_live = sites_live_path.read_bytes()
    if sha(sites_live) != SITES_LIVE_LEDGER_SHA:
        raise AssertionError("sites-cohomology live ledger hash drift")
    raw_lines = sites_live.splitlines(keepends=True)
    if not raw_lines or not raw_lines[-1].endswith((b"\n", b"\r")):
        raise AssertionError("sites-cohomology ledger lacks terminal newline")
    selected: dict[str, bytes] = {}
    for raw in raw_lines[1:]:
        row_id = raw.split(b",", 1)[0].decode("utf-8-sig")
        if row_id in SITES_PACKET_IDS:
            if row_id in selected:
                raise AssertionError(f"duplicate selected producer ID: {row_id}")
            selected[row_id] = raw
    if set(selected) != set(SITES_PACKET_IDS):
        raise AssertionError("sites-cohomology R35 packet IDs are incomplete")
    sites_packet = raw_lines[0] + b"".join(selected[row_id] for row_id in SITES_PACKET_IDS)
    sites_target = ROOT / "authority/producer/SITES_COHOMOLOGY_SOURCE_DEFECT_LEDGER_012_013_028.csv"
    sites_target.parent.mkdir(parents=True, exist_ok=True)
    sites_target.write_bytes(sites_packet)
    dump(
        ROOT / "authority/producer/SITES_COHOMOLOGY_R35_PACKET_RECEIPT.json",
        {
            "schema": "stacks-sites-cohomology-selected-packet-receipt/v1",
            "packet_ids": SITES_PACKET_IDS,
            "packet_bytes": len(sites_packet),
            "packet_sha256": sha(sites_packet),
            "live_snapshot_bytes": len(sites_live),
            "live_snapshot_sha256": sha(sites_live),
            "nonselected_rows_excluded": True,
        },
    )
    copying = source_root / "COPYING"
    if copying.is_file():
        (ROOT / "authority/COPYING").write_bytes(copying.read_bytes())
    else:
        prior = ROOT.parent / "r33/authority/COPYING"
        (ROOT / "authority/COPYING").write_bytes(prior.read_bytes())


def line_starts(data: bytes) -> list[int]:
    return [0] + [index + 1 for index, value in enumerate(data) if value == 10]


def line_at(starts: list[int], byte_index: int) -> int:
    return bisect.bisect_right(starts, byte_index)


def csv_records(path: Path) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, object]]]:
    data = path.read_bytes()
    text = data.decode("utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(text)))
    raw_lines = data.splitlines(keepends=True)
    if len(raw_lines) != len(rows) + 1:
        raise AssertionError(f"CSV rows are not one physical line each: {path.name}")
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


def source_packet(case: dict[str, object]) -> str:
    return "authority/producer/SITES_COHOMOLOGY_SOURCE_DEFECT_LEDGER_012_013_028.csv"


def build_operations() -> tuple[dict[str, bytes], list[dict[str, object]], dict[str, dict[str, object]]]:
    authorities = {
        "sites-cohomology.tex": (ROOT / "authority/source/sites-cohomology.tex").read_bytes(),
    }
    expected_hashes = {"sites-cohomology.tex": SITES_SHA}
    for name, data in authorities.items():
        if sha(data) != expected_hashes[name]:
            raise AssertionError(f"candidate authority hash drift: {name}")

    all_rows, all_bindings = csv_records(ROOT / "authority/producer/SITES_COHOMOLOGY_SOURCE_DEFECT_LEDGER_012_013_028.csv")
    operations: list[dict[str, object]] = []
    by_source: dict[str, list[dict[str, object]]] = {name: [] for name in authorities}
    for case in CASES:
        producer_id = str(case["producer_id"])
        if producer_id not in all_rows:
            raise AssertionError(f"producer packet omits {producer_id}")
        if all_rows[producer_id]["authority_sha256"] != expected_hashes[str(case["source"])]:
            raise AssertionError(f"producer authority hash drift: {producer_id}")
        source = str(case["source"])
        authority = authorities[source]
        old = str(case["old"]).encode("utf-8")
        new = str(case["new"]).encode("utf-8")
        starts = line_starts(authority)
        positions: list[int] = []
        cursor = 0
        while True:
            position = authority.find(old, cursor)
            if position < 0:
                break
            if (
                line_at(starts, position) == int(case["start_line"])
                and line_at(starts, position + len(old) - 1) == int(case["end_line"])
            ):
                positions.append(position)
            cursor = position + 1
        if len(positions) != 1:
            raise AssertionError(f"declared preimage is not unique at its locus: {producer_id}")
        position = positions[0]
        packet = ROOT / source_packet(case)
        operation = {
            "operation_id": f"{case['stable_id']}-OP1",
            "operation_index": 1,
            "stable_id": case["stable_id"],
            "producer_id": producer_id,
            "operation_aliases": case.get("operation_aliases", []),
            "source": source,
            "source_start_line": case["start_line"],
            "source_end_line": case["end_line"],
            "start_byte": position,
            "end_byte_exclusive": position + len(old),
            "old_text": case["old"],
            "old_bytes": len(old),
            "old_sha256": sha(old),
            "replacement_text": case["new"],
            "replacement_bytes": len(new),
            "replacement_sha256": sha(new),
            "occurrence_count_in_frozen_authority": authority.count(old),
            "declared_line_range_occurrence_count": 1,
            "rationale": case["rationale"],
            "class": case["kind"],
            "producer_source_packet": source_packet(case),
            "producer_source_packet_sha256": sha(packet.read_bytes()),
            "producer_row_binding": all_bindings[producer_id],
        }
        operations.append(operation)
        by_source[source].append(operation)

    payloads: dict[str, bytes] = {}
    for source, authority in authorities.items():
        payload = authority
        for operation in sorted(by_source[source], key=lambda item: int(item["start_byte"]), reverse=True):
            start = int(operation["start_byte"])
            end = int(operation["end_byte_exclusive"])
            old = str(operation["old_text"]).encode("utf-8")
            if payload[start:end] != old:
                raise AssertionError(f"apply preimage mismatch: {operation['operation_id']}")
            payload = payload[:start] + str(operation["replacement_text"]).encode("utf-8") + payload[end:]
        payloads[source] = payload
    return payloads, operations, all_rows


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
        "namespace": "commons/stacks/errata/r35",
        "writer_task": WRITER,
        "upstream": {"lock": "upstream/stacks.lock.json", "commit": COMMIT, "tree": TREE},
        "source_authorities": [evidence(path) for path in authority_paths],
        "source_closure": {"enumerated": True, "expected_units": 3, "manifested_units": 3, "complete": True},
        **{key: evidence(path) for key, path in singled.items()},
        "builds": [evidence(path) for path in build_paths],
        "rights_state": "The authority and modified payload retain the Stacks Project GNU Free Documentation License 1.2; metadata and receipts do not relicense upstream content. This independently maintained AI-produced English correction overlay has no Stacks Project review, approval, affiliation, or endorsement.",
        "review_state": "performed" if reviewed else "partial",
        "independent_replay": "passed" if reviewed else "not_performed",
        "unresolved_defects": [
            "Only SITES-COHOMOLOGY-012, SITES-COHOMOLOGY-013, and SITES-COHOMOLOGY-028 are included; every other producer row is excluded.",
            "The producer replacement for SITES-COHOMOLOGY-012 is strengthened to the typed expression \\mathcal{M}^\\bullet(U); the original producer row is preserved as adverse evidence.",
            "The mirrored reversed comparison map in cohomology.tex is outside this sites-cohomology-only packet and is queued for a distinct later unit.",
            "This registrar candidate does not compose or push generated Stacks source.",
            "Pinned authority and locale targets remain unmodified.",
        ],
        "stop_conditions": [
            "Do not mutate pinned upstream authority or locale targets.",
            "Do not include producer rows outside the exact selected three-row packet.",
            "Any byte change requires a regenerated manifest and replay.",
        ],
        "generated_at_utc": STAMP,
    }
    dump(ROOT / "candidate.manifest.json", manifest)
    return manifest


def regenerate() -> dict[str, object]:
    payloads, operations, _ = build_operations()
    for source, payload in payloads.items():
        target = ROOT / "payload" / source
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)

    source_rows = []
    units = []
    for case, operation in zip(CASES, operations, strict=True):
        source = str(case["source"])
        source_rows.append(
            {
                "schema": "mathematics-commons-stacks-errata-map/v2",
                "unit_id": case["stable_id"],
                "class": "source_defect_correction",
                "source": source,
                "authority": f"authority/source/{source}",
                "authority_sha256": SITES_SHA,
                "payload": f"payload/{source}",
                "locus": f"{source}:{case['start_line']}" if case["start_line"] == case["end_line"] else f"{source}:{case['start_line']}-{case['end_line']}",
                "producer_id": case["producer_id"],
                "producer_ids": [case["producer_id"]],
                "operation_aliases": case.get("operation_aliases", []),
                "operations": [operation],
                "proof": "accepted_after_independent_exact_preimage_context_and_registry_deduplication",
                "adverse_evidence": "Frozen authority and French target remain provenance; this overlay changes only the independently maintained AI-open English edition when composed downstream.",
            }
        )
        units.append(
            {
                "id": case["stable_id"],
                "class": "source_defect_correction",
                "source": source,
                "payload": f"payload/{source}",
                "locus": source_rows[-1]["locus"],
                "operation_ids": [operation["operation_id"]],
                "producer_id": case["producer_id"],
                "producer_ids": [case["producer_id"]],
                "status": "accepted_new",
            }
        )
    (ROOT / "source-map.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in source_rows),
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
    formula_units = [case["stable_id"] for case in CASES if str(case["kind"]).startswith("mathematical")]
    prose_units = [case["stable_id"] for case in CASES if case["stable_id"] not in formula_units]
    dump(
        ROOT / "formula-diagram-inventory.json",
        {
            "schema": "mathematics-commons-stacks-errata-formula-diagram-inventory/v1",
            "candidate_id": CANDIDATE,
            "authority_commit": COMMIT,
            "unit_count": len(CASES),
            "formula_units": formula_units,
            "diagram_units": [],
            "prose_only_units": prose_units,
            "unmapped_formula_or_diagram_changes": 0,
        },
    )
    decisions = [
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R35-D0001",
            "choice": "Bind R35 to the pinned sites-cohomology.tex authority and the exact selected producer rows 012, 013, and 028.",
            "rationale": "The full live ledger and the selected three-row packet are separately hash-bound and replay exactly.",
            "timestamp_utc": STAMP,
        },
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R35-D0002",
            "choice": "Admit the three independently checked sites-cohomology corrections as MC-STK-ERR-1309..1311.",
            "rationale": "Every preimage is unique at its declared line, each correction is source-grounded, and no admitted registry map duplicates it.",
            "timestamp_utc": STAMP,
        },
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R35-D0003",
            "choice": "Strengthen the row-012 replacement from \\mathcal{M}^\\bullet to \\mathcal{M}^\\bullet(U).",
            "rationale": "Assumption (2) applies to a K-flat complex of \\mathcal{O}(U)-modules, so the sheaf complex must first be evaluated at U; the identical generic occurrence at line 11619 remains valid.",
            "timestamp_utc": STAMP,
        },
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R35-D0004",
            "choice": "Keep authority, French locale targets, and generated-source trees unchanged in the registrar lane.",
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
            "sources": [
                {"path": "authority/source/sites-cohomology.tex", "bytes": (ROOT / "authority/source/sites-cohomology.tex").stat().st_size, "sha256": SITES_SHA},
            ],
            "authority_mutated": False,
        },
    )
    dump(
        ROOT / "candidate.config.json",
        {
            "$schema": "../../schemas/candidate-manifest.schema.json",
            "schema": "mathematics-commons-stacks-errata-candidate-config/v1",
            "candidate_id": CANDIDATE,
            "namespace": "commons/stacks/errata/r35",
            "lease_id": LEASE,
            "writer_task": WRITER,
            "authority_commit": COMMIT,
            "authority_tree": TREE,
            "accepted": 3,
            "rejected": 0,
            "unresolved": 0,
            "operation_count": 3,
            "expected_unit_ids": [case["stable_id"] for case in CASES],
            "expected_producer_ids": [case["producer_id"] for case in CASES],
            "stems": {
                source: {
                    "authority_bytes": (ROOT / "authority/source" / source).stat().st_size,
                    "authority_sha256": SITES_SHA,
                    "payload_bytes": len(payloads[source]),
                    "payload_sha256": sha(payloads[source]),
                    "operations": sum(1 for case in CASES if case["source"] == source),
                }
                for source in payloads
            },
            "composition_performed": False,
        },
    )
    registry_path = REPO / "registry/overlays.json"
    already_admitted = False
    if registry_path.is_file():
        registered = json.loads(registry_path.read_text(encoding="utf-8")).get("registered_entries", [])
        already_admitted = any(entry.get("id") == CANDIDATE for entry in registered)
    dump(
        ROOT / "LEASE.json",
        {
            "schema": "mathematics-commons-stacks-candidate-lease-pointer/v1",
            "candidate_path": "candidates/commons/stacks/errata/r35",
            "lease_id": LEASE,
            "namespace": "commons/stacks/errata/r35",
            "state": "released_after_admission" if already_admitted else "active_pending_admission",
            "upstream_commit": COMMIT,
            "writer_contract": "candidates/CONTRACT.md",
            "writer_task": WRITER,
        },
    )
    dump(
        ROOT / "source-validation.json",
        {
            "schema": "mathematics-commons-stacks-errata-source-validation/v1",
            "candidate_id": CANDIDATE,
            "passed": True,
            "authorities": {
                source: {"bytes": (ROOT / "authority/source" / source).stat().st_size, "sha256": SITES_SHA}
                for source in payloads
            },
            "producer_packets": [
                evidence(ROOT / "authority/producer/SITES_COHOMOLOGY_SOURCE_DEFECT_LEDGER_012_013_028.csv"),
                evidence(ROOT / "authority/producer/SITES_COHOMOLOGY_R35_PACKET_RECEIPT.json"),
            ],
            "accepted_units": 3,
            "operation_count": 3,
            "rejected_units": 0,
            "unresolved_units": 0,
            "payloads": {source: evidence(ROOT / "payload" / source) for source in payloads},
            "authority_bytes_mutated": False,
            "locale_target_bytes_mutated": False,
            "generated_source_composed": False,
        },
    )
    dump(
        ROOT / "REGENERATION_RECEIPT.json",
        {
            "schema": "stacks-r35-sites-cohomology-regeneration/v1",
            "candidate_id": CANDIDATE,
            "semantic_units": 3,
            "operations": 3,
            "stable_id_range": ["MC-STK-ERR-1309", "MC-STK-ERR-1311"],
            "payloads": {source: evidence(ROOT / "payload" / source) for source in payloads},
            "authority_bytes_mutated": False,
            "generated_source_composed": False,
            "generated_at_utc": STAMP,
        },
    )
    (ROOT / "README.md").write_text(
        "# R35: `sites-cohomology.tex`\n\n"
        "Registrar-only admission of three independently replayed corrections from exact producer rows 012, 013, and 028. "
        "The row-012 correction is strengthened to include evaluation at U; the producer row remains preserved as evidence.\n\n"
        "This candidate does not mutate pinned authority or locale targets and does not compose generated Stacks source.\n",
        encoding="utf-8",
        newline="",
    )
    (ROOT / "BUILD.md").write_text(
        "Run `python pipeline_r35.py verify` for deterministic source and manifest replay. "
        "Admission requires a passing independent review and runs `python pipeline_r35.py admit`.\n",
        encoding="utf-8",
        newline="",
    )
    build_manifest()
    return {
        "passed": True,
        "candidate_id": CANDIDATE,
        "units": 3,
        "operations": 3,
        "payloads": {source: sha(payload) for source, payload in payloads.items()},
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
    payloads, operations, _ = build_operations()
    for source, expected in payloads.items():
        actual = (ROOT / "payload" / source).read_bytes()
        if actual != expected:
            raise AssertionError(f"payload replay mismatch: {source}")
    spec = json.loads((ROOT / "operation-spec.json").read_text(encoding="utf-8"))
    if spec["operation_count"] != 3 or spec["operations"] != operations:
        raise AssertionError("operation-spec replay mismatch")
    units = json.loads((ROOT / "stable-units.json").read_text(encoding="utf-8"))
    stable_ids = [unit["id"] for unit in units["units"]]
    expected_ids = [case["stable_id"] for case in CASES]
    if stable_ids != expected_ids or len(set(stable_ids)) != 3:
        raise AssertionError("stable-unit identity drift")
    registry = json.loads((REPO / "registry/overlays.json").read_text(encoding="utf-8"))
    entries = registry["registered_entries"]
    admitted_r35 = any(entry["id"] == CANDIDATE for entry in entries)
    allowed_head = CANDIDATE if admitted_r35 else "stacks-errata-a04446e-r34"
    if entries[-1]["id"] != allowed_head:
        raise AssertionError(f"registry head drift: {entries[-1]['id']}")
    allocated = {stable for entry in entries if entry["id"] != CANDIDATE for stable in entry["stable_ids"]}
    collisions = sorted(set(expected_ids) & allocated)
    if collisions:
        raise AssertionError(f"stable-ID collision: {collisions}")
    if require_review:
        review = json.loads((ROOT / "replay/independent-review.json").read_text(encoding="utf-8"))
        if review.get("passed") is not True or review.get("pass_is_unconditional") is not True:
            raise AssertionError("independent review is absent or conditional")
    verify_manifest()
    return {
        "candidate_id": CANDIDATE,
        "units": 3,
        "operations": 3,
        "manifest_references": len(json.loads((ROOT / "candidate.manifest.json").read_text(encoding="utf-8"))["source_authorities"])
        + 5
        + len(json.loads((ROOT / "candidate.manifest.json").read_text(encoding="utf-8"))["builds"]),
        "stable_ids": expected_ids,
        "payload_sha256": {source: sha(payload) for source, payload in payloads.items()},
        "passed": True,
    }


def admit() -> dict[str, object]:
    core = verify(require_review=True)
    registry_path = REPO / "registry/overlays.json"
    leases_path = REPO / "registry/leases.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    if registry["registered_entries"][-1]["id"] != "stacks-errata-a04446e-r34":
        raise AssertionError("registry is not at the exact R34 head")
    registry_before = sha(registry_path.read_bytes())
    leases_before = sha(leases_path.read_bytes())
    manifest_sha = sha((ROOT / "candidate.manifest.json").read_bytes())
    stable_ids = [case["stable_id"] for case in CASES]
    registry["registered_entries"].append(
        {
            "id": CANDIDATE,
            "namespace": "commons/stacks/errata/r35",
            "writer": WRITER,
            "source_commit": COMMIT,
            "source_tree": TREE,
            "manifest_sha256": manifest_sha,
            "stable_ids": stable_ids,
            "rights_state": "The authority and modified payload retain the Stacks Project GNU Free Documentation License 1.2; metadata and receipts do not relicense upstream content. This independently maintained AI-produced English correction overlay has no Stacks Project review, approval, affiliation, or endorsement.",
            "review_receipt": "candidates/commons/stacks/errata/r35/replay/independent-review.json",
            "admitted_at_utc": STAMP,
        }
    )
    dump_registry(registry_path, registry)
    leases = json.loads(leases_path.read_text(encoding="utf-8"))
    if leases["events"][-1]["event_id"] != "lease-event-000073":
        raise AssertionError("lease registry is not at the exact R34 head")
    common = {
        "lease_id": LEASE,
        "namespace": "commons/stacks/errata/r35",
        "candidate_path": "candidates/commons/stacks/errata/r35",
        "writer_task": WRITER,
        "upstream_commit": COMMIT,
        "upstream_tree": TREE,
        "issued_at_utc": STAMP,
        "writer_contract": "candidates/CONTRACT.md",
    }
    leases["events"].append({"event_id": "lease-event-000074", "event": "issued", **common, "state": "active", "supersedes_event_id": "lease-event-000073"})
    leases["events"].append({"event_id": "lease-event-000075", "event": "released", **common, "state": "released", "supersedes_event_id": "lease-event-000074"})
    dump_registry(leases_path, leases)
    # The released lease pointer is a manifested candidate byte. Regenerate it
    # after the registry transition, then bind that final manifest in both the
    # registry entry and the admission receipt.
    regenerate()
    manifest_sha = sha((ROOT / "candidate.manifest.json").read_bytes())
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    if registry["registered_entries"][-1]["id"] != CANDIDATE:
        raise AssertionError("R35 registry transition drifted during final regeneration")
    registry["registered_entries"][-1]["manifest_sha256"] = manifest_sha
    dump_registry(registry_path, registry)
    core = verify(require_review=True)
    receipt_path = REPO / "registry/admission-receipts/r35.json"
    receipt = {
        "schema": "mathematics-commons-stacks-registry-admission-receipt/v1",
        "candidate_id": CANDIDATE,
        "admitted_at_utc": STAMP,
        "manifest": evidence(ROOT / "candidate.manifest.json"),
        "source_map": evidence(ROOT / "source-map.jsonl"),
        "stable_ids": stable_ids,
        "stable_id_count": 3,
        "producer_ids": [case["producer_id"] for case in CASES],
        "registry": {"before_sha256": registry_before, "after_sha256": sha(registry_path.read_bytes()), "last_overlay": CANDIDATE},
        "leases": {"before_sha256": leases_before, "after_sha256": sha(leases_path.read_bytes()), "issued_event": "lease-event-000074", "released_event": "lease-event-000075"},
        "fresh_replay": core,
        "constraints": {"authority_mutated": False, "producer_target_mutated": False, "generated_source_composed": False, "generated_source_pushed": False, "published": False},
        "status": "PASS",
    }
    dump(receipt_path, receipt)
    return {
        "passed": True,
        "candidate_id": CANDIDATE,
        "manifest_sha256": manifest_sha,
        "registry_sha256": sha(registry_path.read_bytes()),
        "leases_sha256": sha(leases_path.read_bytes()),
        "receipt_sha256": sha(receipt_path.read_bytes()),
    }


def repair_admission() -> dict[str, object]:
    """Rebind an uncommitted R35 admission to its released final lease byte."""
    registry_path = REPO / "registry/overlays.json"
    leases_path = REPO / "registry/leases.json"
    receipt_path = REPO / "registry/admission-receipts/r35.json"
    previous = json.loads(receipt_path.read_text(encoding="utf-8"))
    registry = json.loads(subprocess.check_output(["git", "show", "HEAD:registry/overlays.json"], cwd=REPO))
    leases = json.loads(subprocess.check_output(["git", "show", "HEAD:registry/leases.json"], cwd=REPO))
    if registry["registered_entries"][-1]["id"] != "stacks-errata-a04446e-r34":
        raise AssertionError("committed registry base is not exact R34")
    if leases["events"][-1]["event_id"] != "lease-event-000073":
        raise AssertionError("committed lease base is not exact R34")
    stable_ids = [case["stable_id"] for case in CASES]
    registry["registered_entries"].append({
        "id": CANDIDATE,
        "namespace": "commons/stacks/errata/r35",
        "writer": WRITER,
        "source_commit": COMMIT,
        "source_tree": TREE,
        "manifest_sha256": sha((ROOT / "candidate.manifest.json").read_bytes()),
        "stable_ids": stable_ids,
        "rights_state": "The authority and modified payload retain the Stacks Project GNU Free Documentation License 1.2; metadata and receipts do not relicense upstream content. This independently maintained AI-produced English correction overlay has no Stacks Project review, approval, affiliation, or endorsement.",
        "review_receipt": "candidates/commons/stacks/errata/r35/replay/independent-review.json",
        "admitted_at_utc": STAMP,
    })
    common = {
        "lease_id": LEASE,
        "namespace": "commons/stacks/errata/r35",
        "candidate_path": "candidates/commons/stacks/errata/r35",
        "writer_task": WRITER,
        "upstream_commit": COMMIT,
        "upstream_tree": TREE,
        "issued_at_utc": STAMP,
        "writer_contract": "candidates/CONTRACT.md",
    }
    leases["events"].append({"event_id": "lease-event-000074", "event": "issued", **common, "state": "active", "supersedes_event_id": "lease-event-000073"})
    leases["events"].append({"event_id": "lease-event-000075", "event": "released", **common, "state": "released", "supersedes_event_id": "lease-event-000074"})
    dump_registry(registry_path, registry)
    dump_registry(leases_path, leases)
    regenerate()
    manifest_sha = sha((ROOT / "candidate.manifest.json").read_bytes())
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["registered_entries"][-1]["manifest_sha256"] = manifest_sha
    dump_registry(registry_path, registry)
    core = verify(require_review=True)
    receipt = {
        "schema": "mathematics-commons-stacks-registry-admission-receipt/v1",
        "candidate_id": CANDIDATE,
        "admitted_at_utc": STAMP,
        "manifest": evidence(ROOT / "candidate.manifest.json"),
        "source_map": evidence(ROOT / "source-map.jsonl"),
        "stable_ids": stable_ids,
        "stable_id_count": 3,
        "producer_ids": [case["producer_id"] for case in CASES],
        "registry": {
            "before_sha256": previous["registry"]["before_sha256"],
            "after_sha256": sha(registry_path.read_bytes()),
            "last_overlay": CANDIDATE,
        },
        "leases": {
            "before_sha256": previous["leases"]["before_sha256"],
            "after_sha256": sha(leases_path.read_bytes()),
            "issued_event": "lease-event-000074",
            "released_event": "lease-event-000075",
        },
        "fresh_replay": core,
        "transport_repair": {
            "reason": "The initial uncommitted admission changed LEASE.json after manifest generation; this receipt binds the regenerated released lease and final manifest.",
            "history_rewritten": False,
            "public_or_committed_predecessor_existed": False,
            "status": "PASS",
        },
        "constraints": {
            "authority_mutated": False,
            "producer_target_mutated": False,
            "generated_source_composed": False,
            "generated_source_pushed": False,
            "published": False,
        },
        "status": "PASS",
    }
    dump(receipt_path, receipt)
    return {
        "passed": True,
        "candidate_id": CANDIDATE,
        "manifest_sha256": manifest_sha,
        "registry_sha256": sha(registry_path.read_bytes()),
        "leases_sha256": sha(leases_path.read_bytes()),
        "receipt_sha256": sha(receipt_path.read_bytes()),
    }


def main() -> int:
    if len(sys.argv) < 2:
        raise SystemExit("usage: pipeline_r35.py bootstrap SOURCE_ROOT PRODUCER_ROOT | regenerate | verify | admit | repair-admission")
    mode = sys.argv[1]
    if mode == "bootstrap":
        if len(sys.argv) != 4:
            raise SystemExit("bootstrap requires SOURCE_ROOT PRODUCER_ROOT")
        bootstrap(Path(sys.argv[2]), Path(sys.argv[3]))
        result = regenerate()
    elif mode == "regenerate":
        result = regenerate()
    elif mode == "verify":
        result = verify(require_review=False)
    elif mode == "admit":
        result = admit()
    elif mode == "repair-admission":
        result = repair_admission()
    else:
        raise SystemExit(f"unknown mode: {mode}")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
