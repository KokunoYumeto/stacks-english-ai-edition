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
CANDIDATE = "stacks-errata-a04446e-r34"
LEASE = "stacks-lease-000038-errata-r34"
WRITER = "01a0256d-5693-77c1-96b2-cf37101e0c6c"
STAMP = "2026-08-30T14:30:00Z"
COHOMOLOGY_SHA = "FA9747D0082AFBF8B09244DCC6C260F8A122E5E3B4A3C69E2273506D76E18A42"
SITES_SHA = "5B335CE2C7208A128B3C744B8828D93508063F41A4FABBCE2E921F890928895C"
COHOMOLOGY_LEDGER_SHA = "7AA50ACD644F21BE569022B10D30790271B4EB36572D1B594B7FBED61B9455CC"
COHOMOLOGY_EMENDATIONS_SHA = "1D9EE84946783C1716E73733E201741558B67B762B42BF3C93E0EE5900152B01"
SITES_PACKET_SHA = "73CEE46DD7AD6C334FD7E584A0F8279B0BD5670F98CD3BC4EFE5ED1CF88CFD2B"


CASES = [
    {
        "stable_id": "MC-STK-ERR-1295", "producer_id": "COHOMOLOGY-CH20-D001",
        "source": "cohomology.tex", "start_line": 2582, "end_line": 2582,
        "old": r"making (\ref{equation-choice}) commutes.",
        "new": r"making (\ref{equation-choice}) commute.",
        "kind": "grammar",
        "rationale": "The causative construction 'making ...' requires the bare infinitive 'commute'.",
    },
    {
        "stable_id": "MC-STK-ERR-1296", "producer_id": "COHOMOLOGY-CH20-D002",
        "source": "cohomology.tex", "start_line": 2718, "end_line": 2718,
        "old": r"$X$ is hausdorff and quasi-compact",
        "new": r"$X$ is Hausdorff and quasi-compact",
        "kind": "capitalization",
        "rationale": "Hausdorff is a proper mathematical adjective and is capitalized throughout the surrounding section.",
    },
    {
        "stable_id": "MC-STK-ERR-1297", "producer_id": "COHOMOLOGY-CH20-D003",
        "operation_aliases": ["COHOMOLOGY-CH20-OP001"],
        "source": "cohomology.tex", "start_line": 12907, "end_line": 12908,
        "old": r"R\SheafHom(R\SheafHom(K_2, L), M)" + "\n" + r"R\SheafHom(R\SheafHom(K_3, L), M)",
        "new": r"R\SheafHom(R\SheafHom(K_2, L), M) \to" + "\n" + r"R\SheafHom(R\SheafHom(K_3, L), M)",
        "kind": "mathematical_omission",
        "rationale": "The displayed row is declared a distinguished triangle; the arrow between its second and third terms is required and is present in the parallel triangle.",
    },
    {
        "stable_id": "MC-STK-ERR-1298", "producer_id": "SITES-COHOMOLOGY-001",
        "source": "sites-cohomology.tex", "start_line": 10957, "end_line": 10957,
        "old": r"Since $\text{Map}(-, A)$ is a contravariant functor, implies that",
        "new": r"Since $\text{Map}(-, A)$ is a contravariant functor, it follows that",
        "kind": "grammar",
        "rationale": "The finite clause lacks a subject; 'it follows that' supplies the intended implication.",
    },
    {
        "stable_id": "MC-STK-ERR-1299", "producer_id": "SITES-COHOMOLOGY-002",
        "source": "sites-cohomology.tex", "start_line": 10967, "end_line": 10968,
        "old": r"computes the left derived functors" + "\n" + r"$H^n(\mathcal{C}, -)$ of $H^0(\mathcal{C}, -)$",
        "new": r"computes the right derived functors" + "\n" + r"$H^n(\mathcal{C}, -)$ of $H^0(\mathcal{C}, -)$",
        "kind": "mathematical_typing",
        "rationale": "Cohomology is the right-derived delta functor of H^0, as stated by the cited lemma.",
    },
    {
        "stable_id": "MC-STK-ERR-1300", "producer_id": "SITES-COHOMOLOGY-003",
        "source": "sites-cohomology.tex", "start_line": 11047, "end_line": 11047,
        "old": r"\Hom(\prod j_{U_i!}\mathcal{O}_{U_i}, p_{U, *}A)",
        "new": r"\Hom(\bigoplus j_{U_i!}\mathcal{O}_{U_i}, p_{U, *}A)",
        "kind": "mathematical_typing",
        "rationale": "The source object in the preceding short exact sequence is the direct sum; contravariant Hom does not replace that object by a product inside Hom.",
    },
    {
        "stable_id": "MC-STK-ERR-1301", "producer_id": "SITES-COHOMOLOGY-004",
        "source": "sites-cohomology.tex", "start_line": 11066, "end_line": 11067,
        "old": "constant simplicial\nset on a singleton $\\{*\\}$",
        "new": r"constant simplicial" + "\n" + r"set $\Mor_\mathcal{C}(U, U')$",
        "kind": "mathematical_statement",
        "rationale": "Composition augments the factorization simplicial set to the discrete set Mor_C(U,U'); each fibre is contractible, but the whole set need not be a singleton.",
    },
    {
        "stable_id": "MC-STK-ERR-1302", "producer_id": "SITES-COHOMOLOGY-005",
        "source": "sites-cohomology.tex", "start_line": 11149, "end_line": 11149,
        "old": r"H^p(M)(V) \otimes_{\mathcal{O}(V)} \mathcal{O}(U) \to H^b(M)(U)",
        "new": r"H^b(M)(V) \otimes_{\mathcal{O}(V)} \mathcal{O}(U) \to H^b(M)(U)",
        "kind": "mathematical_index",
        "rationale": "The lemma fixes the top nonzero degree b; p is unbound and both sides of the base-change map are degree b.",
    },
    {
        "stable_id": "MC-STK-ERR-1303", "producer_id": "SITES-COHOMOLOGY-006",
        "source": "sites-cohomology.tex", "start_line": 11278, "end_line": 11278,
        "old": r"For ever $U$ and $i$ let", "new": r"For every $U$ and $i$ let",
        "kind": "spelling", "rationale": "The quantifier is 'for every'; the final y is missing.",
    },
    {
        "stable_id": "MC-STK-ERR-1304", "producer_id": "SITES-COHOMOLOGY-007",
        "source": "sites-cohomology.tex", "start_line": 11286, "end_line": 11286,
        "old": r"$|\Omega^i_U| \leq |K|$",
        "new": r"$|\Omega^i_U| \leq \max(\kappa, |K|)$",
        "kind": "mathematical_bound",
        "rationale": "The induction bounds S_n by max(kappa,|K|), not by |K| alone, and Omega injects onto a subset of S_n.",
    },
    {
        "stable_id": "MC-STK-ERR-1305", "producer_id": "SITES-COHOMOLOGY-008",
        "source": "sites-cohomology.tex", "start_line": 11290, "end_line": 11290,
        "old": r"\mathcal{S}^i(U) \cup \Omega^i_U \subset \mathcal{F}^i(U)",
        "new": r"\mathcal{S}_n^i(U) \cup \Omega^i_U \subset \mathcal{F}^i(U)",
        "kind": "mathematical_index",
        "rationale": "Although the initial unsubscripted S is defined earlier, this induction must feed S_n into the next step so that S_{n+1} contains S_n and the announced increasing chain is preserved.",
    },
    {
        "stable_id": "MC-STK-ERR-1306", "producer_id": "SITES-COHOMOLOGY-009",
        "source": "sites-cohomology.tex", "start_line": 11447, "end_line": 11447,
        "old": "with containing those subsets and such that",
        "new": "containing those subsets and such that",
        "kind": "grammar", "rationale": "The stray preposition cannot govern the participial phrase.",
    },
    {
        "stable_id": "MC-STK-ERR-1307", "producer_id": "SITES-COHOMOLOGY-010",
        "source": "sites-cohomology.tex", "start_line": 11600, "end_line": 11600,
        "old": r"$H^i(M)(U) \to H^i(M)(V) \otimes_{\mathcal{O}(V)} \mathcal{O}(U)$",
        "new": r"$H^i(M)(V) \otimes_{\mathcal{O}(V)} \mathcal{O}(U) \to H^i(M)(U)$",
        "kind": "mathematical_arrow_direction",
        "rationale": "Restriction V to U and quasi-coherence produce the tensor base-change map from the V-section module to the U-section module.",
    },
    {
        "stable_id": "MC-STK-ERR-1308", "producer_id": "SITES-COHOMOLOGY-011",
        "source": "sites-cohomology.tex", "start_line": 11601, "end_line": 11602,
        "old": r"R\Gamma(V, K) \otimes_{\mathcal{O}(V)}^\mathbf{L} \mathcal{O}(U)" + "\n" + r"\to R\Gamma(U, K)",
        "new": r"R\Gamma(V, M) \otimes_{\mathcal{O}(V)}^\mathbf{L} \mathcal{O}(U)" + "\n" + r"\to R\Gamma(U, M)",
        "kind": "mathematical_symbol",
        "rationale": "The converse fixes M and introduces no K; both derived-section occurrences must use M.",
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
        source_root / "cohomology.tex": (ROOT / "authority/source/cohomology.tex", COHOMOLOGY_SHA),
        source_root / "sites-cohomology.tex": (ROOT / "authority/source/sites-cohomology.tex", SITES_SHA),
        producer_root / "COHOMOLOGY_SOURCE_DEFECT_LEDGER.csv": (
            ROOT / "authority/producer/COHOMOLOGY_SOURCE_DEFECT_LEDGER.csv", COHOMOLOGY_LEDGER_SHA
        ),
        producer_root / "COHOMOLOGY_SOURCE_EMENDATIONS.json": (
            ROOT / "authority/producer/COHOMOLOGY_SOURCE_EMENDATIONS.json", COHOMOLOGY_EMENDATIONS_SHA
        ),
    }
    for source, (target, expected_sha) in inputs.items():
        data = source.read_bytes()
        if sha(data) != expected_sha:
            raise AssertionError(f"bootstrap input hash drift: {source.name}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    sites_live = (producer_root / "SITES_COHOMOLOGY_SOURCE_DEFECT_LEDGER.csv").read_bytes()
    sites_prefix = prefix_through_lf(sites_live, 12)
    if len(sites_prefix) != 5756 or sha(sites_prefix) != SITES_PACKET_SHA:
        raise AssertionError("sites-cohomology 001..011 packet prefix drift")
    sites_target = ROOT / "authority/producer/SITES_COHOMOLOGY_SOURCE_DEFECT_LEDGER_001_011.csv"
    sites_target.parent.mkdir(parents=True, exist_ok=True)
    sites_target.write_bytes(sites_prefix)
    dump(
        ROOT / "authority/producer/SITES_COHOMOLOGY_PACKET_PREFIX_RECEIPT.json",
        {
            "schema": "stacks-sites-cohomology-packet-prefix-receipt/v1",
            "packet_ids": [f"SITES-COHOMOLOGY-{number:03d}" for number in range(1, 12)],
            "prefix_bytes": len(sites_prefix),
            "prefix_sha256": sha(sites_prefix),
            "live_snapshot_bytes": len(sites_live),
            "live_snapshot_sha256": sha(sites_live),
            "append_only_suffix_excluded": True,
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
    return (
        "authority/producer/COHOMOLOGY_SOURCE_DEFECT_LEDGER.csv"
        if case["source"] == "cohomology.tex"
        else "authority/producer/SITES_COHOMOLOGY_SOURCE_DEFECT_LEDGER_001_011.csv"
    )


def build_operations() -> tuple[dict[str, bytes], list[dict[str, object]], dict[str, dict[str, object]]]:
    authorities = {
        "cohomology.tex": (ROOT / "authority/source/cohomology.tex").read_bytes(),
        "sites-cohomology.tex": (ROOT / "authority/source/sites-cohomology.tex").read_bytes(),
    }
    expected_hashes = {"cohomology.tex": COHOMOLOGY_SHA, "sites-cohomology.tex": SITES_SHA}
    for name, data in authorities.items():
        if sha(data) != expected_hashes[name]:
            raise AssertionError(f"candidate authority hash drift: {name}")

    coho_rows, coho_bindings = csv_records(ROOT / "authority/producer/COHOMOLOGY_SOURCE_DEFECT_LEDGER.csv")
    sites_rows, sites_bindings = csv_records(ROOT / "authority/producer/SITES_COHOMOLOGY_SOURCE_DEFECT_LEDGER_001_011.csv")
    all_rows = {**coho_rows, **sites_rows}
    all_bindings = {**coho_bindings, **sites_bindings}
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
        "namespace": "commons/stacks/errata/r34",
        "writer_task": WRITER,
        "upstream": {"lock": "upstream/stacks.lock.json", "commit": COMMIT, "tree": TREE},
        "source_authorities": [evidence(path) for path in authority_paths],
        "source_closure": {"enumerated": True, "expected_units": 14, "manifested_units": 14, "complete": True},
        **{key: evidence(path) for key, path in singled.items()},
        "builds": [evidence(path) for path in build_paths],
        "rights_state": "The authority and modified payload retain the Stacks Project GNU Free Documentation License 1.2; metadata and receipts do not relicense upstream content. This independently maintained AI-produced English correction overlay has no Stacks Project review, approval, affiliation, or endorsement.",
        "review_state": "performed" if reviewed else "partial",
        "independent_replay": "passed" if reviewed else "not_performed",
        "unresolved_defects": [
            "Only the exact handed-off COHOMOLOGY-CH20-D001..D003 and SITES-COHOMOLOGY-001..011 packets are included; later append-only producer suffix rows are excluded.",
            "This registrar candidate does not compose or push generated Stacks source.",
            "Pinned authority and locale targets remain unmodified.",
        ],
        "stop_conditions": [
            "Do not mutate pinned upstream authority or locale targets.",
            "Do not include producer suffix rows outside the exact handed-off packet.",
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
                "authority_sha256": COHOMOLOGY_SHA if source == "cohomology.tex" else SITES_SHA,
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
            "id": "ERR-R34-D0001",
            "choice": "Bind R34 to the pinned cohomology.tex and sites-cohomology.tex authorities and exact handed-off producer packets.",
            "rationale": "All authority and producer packet hashes, including the append-only sites-cohomology prefix, replay exactly.",
            "timestamp_utc": STAMP,
        },
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R34-D0002",
            "choice": "Admit all fourteen independently checked corrections as MC-STK-ERR-1295..1308.",
            "rationale": "Every preimage is unique at its declared locus, each correction is source-grounded, and no admitted registry map duplicates it.",
            "timestamp_utc": STAMP,
        },
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R34-D0003",
            "choice": "Exclude all later append-only sites-cohomology producer suffix rows from R34.",
            "rationale": "They were not part of the exact eleven-row handoff and must be adjudicated in a later bounded packet.",
            "timestamp_utc": STAMP,
        },
        {
            "schema": "mathematics-commons-stacks-candidate-decision/v1",
            "id": "ERR-R34-D0004",
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
                {"path": "authority/source/cohomology.tex", "bytes": (ROOT / "authority/source/cohomology.tex").stat().st_size, "sha256": COHOMOLOGY_SHA},
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
            "namespace": "commons/stacks/errata/r34",
            "lease_id": LEASE,
            "writer_task": WRITER,
            "authority_commit": COMMIT,
            "authority_tree": TREE,
            "accepted": 14,
            "rejected": 0,
            "unresolved": 0,
            "operation_count": 14,
            "expected_unit_ids": [case["stable_id"] for case in CASES],
            "expected_producer_ids": [case["producer_id"] for case in CASES],
            "stems": {
                source: {
                    "authority_bytes": (ROOT / "authority/source" / source).stat().st_size,
                    "authority_sha256": COHOMOLOGY_SHA if source == "cohomology.tex" else SITES_SHA,
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
            "candidate_path": "candidates/commons/stacks/errata/r34",
            "lease_id": LEASE,
            "namespace": "commons/stacks/errata/r34",
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
                source: {"bytes": (ROOT / "authority/source" / source).stat().st_size, "sha256": COHOMOLOGY_SHA if source == "cohomology.tex" else SITES_SHA}
                for source in payloads
            },
            "producer_packets": [
                evidence(ROOT / "authority/producer/COHOMOLOGY_SOURCE_DEFECT_LEDGER.csv"),
                evidence(ROOT / "authority/producer/COHOMOLOGY_SOURCE_EMENDATIONS.json"),
                evidence(ROOT / "authority/producer/SITES_COHOMOLOGY_SOURCE_DEFECT_LEDGER_001_011.csv"),
                evidence(ROOT / "authority/producer/SITES_COHOMOLOGY_PACKET_PREFIX_RECEIPT.json"),
            ],
            "accepted_units": 14,
            "operation_count": 14,
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
            "schema": "stacks-r34-cohomology-sites-cohomology-regeneration/v1",
            "candidate_id": CANDIDATE,
            "semantic_units": 14,
            "operations": 14,
            "stable_id_range": ["MC-STK-ERR-1295", "MC-STK-ERR-1308"],
            "payloads": {source: evidence(ROOT / "payload" / source) for source in payloads},
            "authority_bytes_mutated": False,
            "generated_source_composed": False,
            "generated_at_utc": STAMP,
        },
    )
    (ROOT / "README.md").write_text(
        "# R34: `cohomology.tex` and `sites-cohomology.tex`\n\n"
        "Registrar-only admission of fourteen independently replayed corrections from the exact French-producer handoffs. "
        "The sites-cohomology packet is bound to its eleven-row append-only prefix; later producer suffix rows are excluded.\n\n"
        "This candidate does not mutate pinned authority or locale targets and does not compose generated Stacks source.\n",
        encoding="utf-8",
        newline="",
    )
    (ROOT / "BUILD.md").write_text(
        "Run `python pipeline_r34.py verify` for deterministic source and manifest replay. "
        "Admission requires a passing independent review and runs `python pipeline_r34.py admit`.\n",
        encoding="utf-8",
        newline="",
    )
    build_manifest()
    return {
        "passed": True,
        "candidate_id": CANDIDATE,
        "units": 14,
        "operations": 14,
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
    if spec["operation_count"] != 14 or spec["operations"] != operations:
        raise AssertionError("operation-spec replay mismatch")
    units = json.loads((ROOT / "stable-units.json").read_text(encoding="utf-8"))
    stable_ids = [unit["id"] for unit in units["units"]]
    expected_ids = [case["stable_id"] for case in CASES]
    if stable_ids != expected_ids or len(set(stable_ids)) != 14:
        raise AssertionError("stable-unit identity drift")
    registry = json.loads((REPO / "registry/overlays.json").read_text(encoding="utf-8"))
    entries = registry["registered_entries"]
    admitted_r34 = any(entry["id"] == CANDIDATE for entry in entries)
    allowed_head = CANDIDATE if admitted_r34 else "stacks-errata-a04446e-r33"
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
        "units": 14,
        "operations": 14,
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
    if registry["registered_entries"][-1]["id"] != "stacks-errata-a04446e-r33":
        raise AssertionError("registry is not at the exact R33 head")
    registry_before = sha(registry_path.read_bytes())
    leases_before = sha(leases_path.read_bytes())
    manifest_sha = sha((ROOT / "candidate.manifest.json").read_bytes())
    stable_ids = [case["stable_id"] for case in CASES]
    registry["registered_entries"].append(
        {
            "id": CANDIDATE,
            "namespace": "commons/stacks/errata/r34",
            "writer": WRITER,
            "source_commit": COMMIT,
            "source_tree": TREE,
            "manifest_sha256": manifest_sha,
            "stable_ids": stable_ids,
            "rights_state": "The authority and modified payload retain the Stacks Project GNU Free Documentation License 1.2; metadata and receipts do not relicense upstream content. This independently maintained AI-produced English correction overlay has no Stacks Project review, approval, affiliation, or endorsement.",
            "review_receipt": "candidates/commons/stacks/errata/r34/replay/independent-review.json",
            "admitted_at_utc": STAMP,
        }
    )
    dump_registry(registry_path, registry)
    leases = json.loads(leases_path.read_text(encoding="utf-8"))
    if leases["events"][-1]["event_id"] != "lease-event-000071":
        raise AssertionError("lease registry is not at the exact R33 head")
    common = {
        "lease_id": LEASE,
        "namespace": "commons/stacks/errata/r34",
        "candidate_path": "candidates/commons/stacks/errata/r34",
        "writer_task": WRITER,
        "upstream_commit": COMMIT,
        "upstream_tree": TREE,
        "issued_at_utc": STAMP,
        "writer_contract": "candidates/CONTRACT.md",
    }
    leases["events"].append({"event_id": "lease-event-000072", "event": "issued", **common, "state": "active", "supersedes_event_id": "lease-event-000071"})
    leases["events"].append({"event_id": "lease-event-000073", "event": "released", **common, "state": "released", "supersedes_event_id": "lease-event-000072"})
    dump_registry(leases_path, leases)
    # The released lease pointer is a manifested candidate byte. Regenerate it
    # after the registry transition, then bind that final manifest in both the
    # registry entry and the admission receipt.
    regenerate()
    manifest_sha = sha((ROOT / "candidate.manifest.json").read_bytes())
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    if registry["registered_entries"][-1]["id"] != CANDIDATE:
        raise AssertionError("R34 registry transition drifted during final regeneration")
    registry["registered_entries"][-1]["manifest_sha256"] = manifest_sha
    dump_registry(registry_path, registry)
    core = verify(require_review=True)
    receipt_path = REPO / "registry/admission-receipts/r34.json"
    receipt = {
        "schema": "mathematics-commons-stacks-registry-admission-receipt/v1",
        "candidate_id": CANDIDATE,
        "admitted_at_utc": STAMP,
        "manifest": evidence(ROOT / "candidate.manifest.json"),
        "source_map": evidence(ROOT / "source-map.jsonl"),
        "stable_ids": stable_ids,
        "stable_id_count": 14,
        "producer_ids": [case["producer_id"] for case in CASES],
        "registry": {"before_sha256": registry_before, "after_sha256": sha(registry_path.read_bytes()), "last_overlay": CANDIDATE},
        "leases": {"before_sha256": leases_before, "after_sha256": sha(leases_path.read_bytes()), "issued_event": "lease-event-000072", "released_event": "lease-event-000073"},
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
    """Rebind the uncommitted R34 admission to its released final lease byte."""
    registry_path = REPO / "registry/overlays.json"
    leases_path = REPO / "registry/leases.json"
    receipt_path = REPO / "registry/admission-receipts/r34.json"
    previous = json.loads(receipt_path.read_text(encoding="utf-8"))
    registry = json.loads(subprocess.check_output(["git", "show", "HEAD:registry/overlays.json"], cwd=REPO))
    leases = json.loads(subprocess.check_output(["git", "show", "HEAD:registry/leases.json"], cwd=REPO))
    if registry["registered_entries"][-1]["id"] != "stacks-errata-a04446e-r33":
        raise AssertionError("committed registry base is not exact R33")
    if leases["events"][-1]["event_id"] != "lease-event-000071":
        raise AssertionError("committed lease base is not exact R33")
    stable_ids = [case["stable_id"] for case in CASES]
    registry["registered_entries"].append({
        "id": CANDIDATE,
        "namespace": "commons/stacks/errata/r34",
        "writer": WRITER,
        "source_commit": COMMIT,
        "source_tree": TREE,
        "manifest_sha256": sha((ROOT / "candidate.manifest.json").read_bytes()),
        "stable_ids": stable_ids,
        "rights_state": "The authority and modified payload retain the Stacks Project GNU Free Documentation License 1.2; metadata and receipts do not relicense upstream content. This independently maintained AI-produced English correction overlay has no Stacks Project review, approval, affiliation, or endorsement.",
        "review_receipt": "candidates/commons/stacks/errata/r34/replay/independent-review.json",
        "admitted_at_utc": STAMP,
    })
    common = {
        "lease_id": LEASE,
        "namespace": "commons/stacks/errata/r34",
        "candidate_path": "candidates/commons/stacks/errata/r34",
        "writer_task": WRITER,
        "upstream_commit": COMMIT,
        "upstream_tree": TREE,
        "issued_at_utc": STAMP,
        "writer_contract": "candidates/CONTRACT.md",
    }
    leases["events"].append({"event_id": "lease-event-000072", "event": "issued", **common, "state": "active", "supersedes_event_id": "lease-event-000071"})
    leases["events"].append({"event_id": "lease-event-000073", "event": "released", **common, "state": "released", "supersedes_event_id": "lease-event-000072"})
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
        "stable_id_count": 14,
        "producer_ids": [case["producer_id"] for case in CASES],
        "registry": {
            "before_sha256": previous["registry"]["before_sha256"],
            "after_sha256": sha(registry_path.read_bytes()),
            "last_overlay": CANDIDATE,
        },
        "leases": {
            "before_sha256": previous["leases"]["before_sha256"],
            "after_sha256": sha(leases_path.read_bytes()),
            "issued_event": "lease-event-000072",
            "released_event": "lease-event-000073",
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
        raise SystemExit("usage: pipeline_r34.py bootstrap SOURCE_ROOT PRODUCER_ROOT | regenerate | verify | admit | repair-admission")
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
