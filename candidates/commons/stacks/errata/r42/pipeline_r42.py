"""Materialize the R42 Descent source candidate; never invokes TeX or admits it."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
WORKSPACE = REPO.parent
UPSTREAM = (
    WORKSPACE
    / "03_projects/language_management/cjk/03_working_translations/"
    "stacks_cjk_20260821/upstream/src/"
    "stacks-project-a04446e57ec1fbc252a871afcec7752fb2807b14"
)
PRODUCER = (
    WORKSPACE
    / "03_projects/language_management/romance/03_working_translations/"
    "stacks_fr_20260821"
)
SOURCE = "descent.tex"
AUTH_SHA = "49483B3BCB36427A607A8227F4EA67730FCDDF1EECCB8E992CA61915ACE3B31D"
PAYLOAD_SHA = "D5D48A9B8B22B18985B84529BD8B14483C6682B932912FAFEABEB9FCA07700A7"
AUTH_BYTES = 353760
PAYLOAD_BYTES = 353780
COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
CANDIDATE_ID = "stacks-errata-a04446e-r42"
LEASE_ID = "stacks-lease-000046-errata-r42"
STAMP = "2026-09-05T13:05:21.771Z"
SOURCE_DATE_EPOCH = "1788613521"
PRELEASE_HEAD = "3056e01f8a2dd26f52066434d80ff2c59901dea8"
PRELEASE_OVERLAYS_SHA = "2E6591520F9ADE96B69A0463DB5A5617E319046DD91218170B7DA48DDFFCA14B"
PRELEASE_LEASES_SHA = "4BDEF2CC7327779CA1C6A996E836A59148359CAC835CE146458A7143A46C7F5E"

EVIDENCE_SOURCE = PRODUCER / "p05/evidence/DESCENT_SOURCE_DEFECTS.md"
LEDGER_SOURCE = PRODUCER / "00_control/SOURCE_DEFECT_LEDGER.csv"
EVIDENCE_SHA = "282E9EFFEEA7BD2A102E935052D325BF0E3ACD732D88AAE4CCB5F7479988AB1F"
LEDGER_SHA = "304D51200903ED870D2F72AF8F65C0AB28B314F6075B206C3B34F506B678F8CE"


UNITS = [
    {
        "stable_id": "MC-STK-ERR-1419", "producer_id": "DESCENT-030",
        "class": "editorial_or_notational_clarification", "tags": ["04R7"],
        "proof": "The associated property is defined as mathcal Q at lines 7856--7865 and item (2) of this lemma again names it mathcal Q at line 7904; bare Q is an inconsistent notation.",
        "operations": [{"line": 7896, "end_line": 7896, "old": r"Let $Q$ be the associated property", "new": r"Let $\mathcal{Q}$ be the associated property"}],
    },
    {
        "stable_id": "MC-STK-ERR-1420", "producer_id": "DESCENT-031",
        "class": "source_defect", "tags": ["04NK"],
        "proof": "The vertical etale maps give finite separable residue-field extensions kappa(u')/kappa(u) and kappa(v')/kappa(v), so invariance of transcendence degree compares kappa(u') over kappa(v') with kappa(u) over kappa(v); the unprimed final u is ill-typed for the right-hand base field.",
        "operations": [{"line": 8051, "end_line": 8051, "old": r"$\text{trdeg}_{\kappa(v)} \kappa(u) = \text{trdeg}_{\kappa(v')} \kappa(u)$", "new": r"$\text{trdeg}_{\kappa(v)} \kappa(u) = \text{trdeg}_{\kappa(v')} \kappa(u')$"}],
    },
    {
        "stable_id": "MC-STK-ERR-1421", "producer_id": "DESCENT-032",
        "class": "editorial_or_notational_clarification", "tags": ["023V"],
        "proof": "The sentence lacks its finite copula; inserting 'is' yields the grammatical explanation 'This is because' and changes neither fibre-product identity.",
        "operations": [{"line": 8141, "end_line": 8141, "old": r"This because $X \times_{\Delta, X \times_S X} (V \times_S X) = V$", "new": r"This is because $X \times_{\Delta, X \times_S X} (V \times_S X) = V$"}],
    },
    {
        "stable_id": "MC-STK-ERR-1422", "producer_id": "DESCENT-033",
        "class": "source_defect", "tags": ["02VS"],
        "proof": "Line 8355 defines mathcal V as the family {V_j -> S}; S' is instead the target of the U_i family, so the stated V-family base must be S.",
        "operations": [{"line": 8362, "end_line": 8362, "old": r"family $\{V_j \to S'\}$. The system", "new": r"family $\{V_j \to S\}$. The system"}],
    },
    {
        "stable_id": "MC-STK-ERR-1423", "producer_id": "DESCENT-034",
        "class": "source_defect", "tags": ["02VS"],
        "proof": "The displayed system is indexed by i and obtained by pulling the V-data to U_i via g_i, hence it is descent data relative to mathcal U; keeping mathcal V contradicts the construction and the change-of-base direction.",
        "operations": [{"line": 8370, "end_line": 8370, "old": r"is a descent datum relative to $\mathcal{V}$.", "new": r"is a descent datum relative to $\mathcal{U}$."}],
    },
    {
        "stable_id": "MC-STK-ERR-1424", "producer_id": "DESCENT-035",
        "class": "editorial_or_notational_clarification", "tags": ["023Z"],
        "proof": "English requires 'denote by O this datum'; inserting 'by' is the minimal grammatical repair and changes no mathematical object.",
        "operations": [{"line": 8423, "end_line": 8423, "old": r"denote $(X \times_S U, can)$ this descent datum.", "new": r"denote by $(X \times_S U, can)$ this descent datum."}],
    },
    {
        "stable_id": "MC-STK-ERR-1425", "producer_id": "DESCENT-036",
        "class": "editorial_or_notational_clarification", "tags": ["02VU"],
        "proof": "English requires 'denote this datum by O'; inserting 'by' is the minimal grammatical repair and changes no indexed object.",
        "operations": [{"line": 8453, "end_line": 8453, "old": r"We denote this descent datum $(X_i \times_S U, can)$.", "new": r"We denote this descent datum by $(X_i \times_S U, can)$."}],
    },
    {
        "stable_id": "MC-STK-ERR-1426", "producer_id": "DESCENT-037",
        "class": "editorial_or_notational_clarification", "tags": ["02VV"],
        "proof": "The standard noun corresponding to 'fully faithful' is 'full faithfulness'; 'fully faithfulness' is ungrammatical and the section body immediately states that the functor is fully faithful.",
        "operations": [{"line": 8472, "end_line": 8472, "old": r"\section{Fully faithfulness of the pullback functors}", "new": r"\section{Full faithfulness of the pullback functors}"}],
    },
    {
        "stable_id": "MC-STK-ERR-1427", "producer_id": "DESCENT-038",
        "class": "source_defect", "tags": ["040J", "040K"],
        "proof": "In each factorization X -> X times_S X' -> X', the first arrow is the graph of f and the first projection is its retraction; the graph is a section, but is not thereby a morphism having a section. Both repeated proofs require 'has a retraction' to invoke the equivalence lemma in the correct categorical direction.",
        "operations": [
            {"line": 8708, "end_line": 8708, "old": "The first morphism has a section", "new": "The first morphism has a retraction"},
            {"line": 8727, "end_line": 8727, "old": "The first morphism has a section", "new": "The first morphism has a retraction"},
        ],
    },
    {
        "stable_id": "MC-STK-ERR-1428", "producer_id": "DESCENT-039",
        "class": "source_defect", "tags": ["040K"],
        "proof": "The hypothesis is that X -> S is an fpqc covering. Surjectivity, flatness, and quasi-compactness of the different morphism f:X->X' do not imply that hypothesis, so the parenthetical sufficient condition must refer to X -> S. The full two-line guard avoids changing the valid f-based parenthetical at lines 8565--8566.",
        "operations": [{"line": 8718, "end_line": 8719, "old": "Assume $\\{X \\to S\\}$ is an fpqc covering (for example if $f$ is\nsurjective, flat and quasi-compact).", "new": "Assume $\\{X \\to S\\}$ is an fpqc covering (for example if $X \\to S$ is\nsurjective, flat and quasi-compact)."}],
    },
    {
        "stable_id": "MC-STK-ERR-1429", "producer_id": "DESCENT-040",
        "class": "source_defect", "tags": ["02VZ"],
        "proof": "The family morphisms are g_i:U_i->V_{alpha(i)} indexed by i in I, while alpha(i) lies in J and does not index a g-map; the ith coproduct component is therefore mapped by g_i.",
        "operations": [{"line": 8766, "end_line": 8766, "old": r"via the morphism $g_{\alpha(i)}$", "new": r"via the morphism $g_i$"}],
    },
]


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha_path(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def write_bytes(relative: str, data: bytes) -> None:
    path = (ROOT / relative).resolve()
    assert path.is_relative_to(ROOT)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def dump(relative: str, value: object) -> None:
    write_bytes(relative, (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def write_jsonl(relative: str, rows: list[dict]) -> None:
    write_bytes(relative, ("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)).encode("utf-8"))


def identity(relative: str) -> dict:
    path = ROOT / relative
    return {"path": relative, "bytes": path.stat().st_size, "sha256": sha_path(path)}


def sanitize_text(text: str) -> str:
    return text.replace(str(WORKSPACE), "<WORKSPACE>").replace(WORKSPACE.as_posix(), "<WORKSPACE>")


def exact_occurrences(haystack: bytes, needle: bytes) -> list[int]:
    found: list[int] = []
    cursor = 0
    while True:
        position = haystack.find(needle, cursor)
        if position < 0:
            return found
        found.append(position)
        cursor = position + len(needle)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--materialize", action="store_true")
    args = parser.parse_args()
    if not args.materialize:
        parser.error("Use --materialize for source-only candidate preparation.")
    if (ROOT / "candidate.manifest.json").exists() or list((ROOT / "builds").glob("*.pdf")):
        raise RuntimeError("Refusing to reset a built or sealed candidate.")

    lease = json.loads((ROOT / "LEASE.json").read_text(encoding="utf-8"))
    assert lease["lease_id"] == LEASE_ID and lease["status"] == "active"
    events = json.loads((REPO / "registry/leases.json").read_text(encoding="utf-8"))["events"]
    matches = [event for event in events if event.get("lease_id") == LEASE_ID]
    assert len(matches) == 1 and matches[0]["event"] == "issued" and matches[0]["state"] == "active"
    assert matches[0]["candidate_path"] == "candidates/commons/stacks/errata/r42"
    assert (ROOT / ".gitattributes").read_bytes() == b"* -text\n"

    source = (UPSTREAM / SOURCE).read_bytes()
    assert len(source) == AUTH_BYTES and sha_bytes(source) == AUTH_SHA
    evidence_raw = EVIDENCE_SOURCE.read_bytes()
    ledger_raw = LEDGER_SOURCE.read_bytes()
    assert len(evidence_raw) == 15222 and sha_bytes(evidence_raw) == EVIDENCE_SHA
    assert len(ledger_raw) == 528248 and sha_bytes(ledger_raw) == LEDGER_SHA

    write_bytes("authority/source/descent.tex", source)
    write_bytes("authority/COPYING", (UPSTREAM / "COPYING").read_bytes())
    dump(
        "authority/upstream.lock.json",
        {
            "commit": COMMIT,
            "tree": TREE,
            "source": SOURCE,
            "bytes": len(source),
            "sha256": AUTH_SHA,
            "url": f"https://github.com/stacks/stacks-project/blob/{COMMIT}/{SOURCE}",
        },
    )
    write_bytes("authority/producer/DESCENT_SOURCE_DEFECTS.md", sanitize_text(evidence_raw.decode("utf-8-sig")).encode("utf-8"))
    write_bytes("authority/producer/SOURCE_DEFECT_LEDGER.csv", sanitize_text(ledger_raw.decode("utf-8-sig")).encode("utf-8"))

    operations: list[dict] = []
    units: list[dict] = []
    maps: list[dict] = []
    decisions: list[dict] = []
    for index, declared in enumerate(UNITS, 1):
        group: list[dict] = []
        for operation_index, declared_operation in enumerate(declared["operations"], 1):
            old = declared_operation["old"].encode("utf-8")
            replacement = declared_operation["new"].encode("utf-8")
            positions = exact_occurrences(source, old)
            line_positions = [
                position
                for position in positions
                if source[:position].count(b"\n") + 1 == declared_operation["line"]
            ]
            assert len(line_positions) == 1, (declared["stable_id"], declared_operation["line"], positions)
            start = line_positions[0]
            line = source[:start].count(b"\n") + 1
            operation_id = f'{declared["stable_id"]}-OP{operation_index}'
            producer_operation_id = f'{declared["producer_id"]}-OP{operation_index}'
            operation = {
                "operation_id": operation_id,
                "stable_id": declared["stable_id"],
                "producer_id": declared["producer_id"],
                "producer_operation_id": producer_operation_id,
                "origin": "producer_packet_and_independent_adjudication",
                "class": declared["class"],
                "source": SOURCE,
                "line": line,
                "source_start_line": line,
                "source_end_line": declared_operation["end_line"],
                "start_byte": start,
                "end_byte_exclusive": start + len(old),
                "old_text": declared_operation["old"],
                "old_bytes": len(old),
                "old_sha256": sha_bytes(old),
                "replacement_text": declared_operation["new"],
                "replacement_bytes": len(replacement),
                "replacement_sha256": sha_bytes(replacement),
                "declared_line_occurrences": len(line_positions),
                "file_occurrences": len(positions),
            }
            operations.append(operation)
            group.append(operation)
        locus_lines = list(dict.fromkeys(operation["line"] for operation in group))
        locus = f'{SOURCE}:' + ",".join(str(line) for line in locus_lines)
        unit = {
            "id": declared["stable_id"],
            "source": SOURCE,
            "producer_id": declared["producer_id"],
            "producer_ids": [declared["producer_id"]],
            "producer_aliases": [],
            "class": declared["class"],
            "locus": locus,
            "operation_ids": [operation["operation_id"] for operation in group],
            "payload": "payload/descent.tex",
            "status": "accepted_source_proposal_not_admitted",
        }
        units.append(unit)
        maps.append(
            {
                "schema": "mathematics-commons-stacks-source-map/v2",
                "unit_id": declared["stable_id"],
                "source": SOURCE,
                "authority": "authority/source/descent.tex",
                "authority_sha256": AUTH_SHA,
                "payload": "payload/descent.tex",
                "producer_id": declared["producer_id"],
                "producer_ids": [declared["producer_id"]],
                "producer_aliases": [],
                "class": declared["class"],
                "locus": locus,
                "proof": declared["proof"],
                "operations": group,
                "adverse_evidence": (
                    "Accepted as an editorial or notational source correction, not classified as a false theorem."
                    if declared["class"] == "editorial_or_notational_clarification"
                    else None
                ),
            }
        )
        decisions.append(
            {
                "schema": "mathematics-commons-stacks-decision/v1",
                "id": f"R42-D{index:03d}",
                "timestamp_utc": STAMP,
                "choice": "materialize_source_proposal_not_admission",
                "stable_id": declared["stable_id"],
                "producer_id": declared["producer_id"],
                "rationale": declared["proof"],
                "supersedes": None,
            }
        )

    ordered = sorted(operations, key=lambda item: item["start_byte"])
    assert list(dict.fromkeys(item["stable_id"] for item in ordered)) == [f"MC-STK-ERR-{number}" for number in range(1419, 1430)]
    assert len({item["operation_id"] for item in ordered}) == 12
    assert all(left["end_byte_exclusive"] <= right["start_byte"] for left, right in zip(ordered, ordered[1:]))
    payload = source
    for operation in reversed(ordered):
        payload = (
            payload[: operation["start_byte"]]
            + operation["replacement_text"].encode("utf-8")
            + payload[operation["end_byte_exclusive"] :]
        )
    assert len(payload) == PAYLOAD_BYTES and sha_bytes(payload) == PAYLOAD_SHA
    write_bytes("payload/descent.tex", payload)

    spec = {
        "schema": "mathematics-commons-stacks-operation-spec/v1",
        "source": SOURCE,
        "authority_sha256": AUTH_SHA,
        "apply_order": "descending_start_byte",
        "operation_count": len(operations),
        "operations": operations,
    }
    stable = {
        "schema": "mathematics-commons-stacks-stable-units/v1",
        "authority_commit": COMMIT,
        "unit_count": len(units),
        "units": units,
    }
    for name, value in (("operation-spec", spec), ("stable-units", stable)):
        dump(name + ".json", value)
        dump(name + ".input.json", value)
    for name, rows in (("source-map", maps), ("decisions", decisions), ("rejections", [])):
        write_jsonl(name + ".jsonl", rows)
        write_jsonl(name + ".input.jsonl", rows)

    cursor = 0
    observed = 0
    unchanged = bytearray()
    for operation in ordered:
        span = source[cursor : operation["start_byte"]]
        assert payload[observed : observed + len(span)] == span
        observed += len(span)
        replacement = operation["replacement_text"].encode("utf-8")
        assert payload[observed : observed + len(replacement)] == replacement
        observed += len(replacement)
        unchanged.extend(span)
        cursor = operation["end_byte_exclusive"]
    assert payload[observed:] == source[cursor:]
    unchanged.extend(source[cursor:])

    patterns = {
        "labels": rb"\\label\{[^}]*\}",
        "refs": rb"\\(?:ref|eqref)\{[^}]*\}",
        "environments": rb"\\(?:begin|end)\{[^}]*\}",
        "inputs": rb"\\input\{[^}]*\}",
        "cites": rb"\\cite(?:\[[^]]*\])?\{[^}]*\}",
    }
    structure = {}
    for name, pattern in patterns.items():
        before = re.findall(pattern, source)
        after = re.findall(pattern, payload)
        assert before == after, name
        structure[name] = {"authority": len(before), "candidate": len(after), "ordered_equal": True}

    adjudication_rows = [
        {
            "stable_id": unit["stable_id"],
            "producer_id": unit["producer_id"],
            "line": unit["operations"][0]["line"],
            "lines": [operation["line"] for operation in unit["operations"]],
            "classification": unit["class"],
            "tags": unit["tags"],
            "operations": [
                {
                    "line": operation["line"],
                    "end_line": operation["end_line"],
                    "old": operation["old"],
                    "replacement": operation["new"],
                }
                for operation in unit["operations"]
            ],
            "recommendation": "accept",
            "reason": unit["proof"],
            "exact_line_preimage_occurrences": [1 for operation in unit["operations"]],
        }
        for unit in UNITS
    ]
    adjudication = {
        "schema": "stacks-r42-descent-independent-adjudication/v1",
        "date": "2026-09-05",
        "status": "PASS_ACCEPT_11_NON_DUPLICATIVE_UNITS_12_OPERATIONS",
        "passed": True,
        "authority": {"path": "authority/source/descent.tex", "bytes": AUTH_BYTES, "sha256": AUTH_SHA},
        "producer_evidence_original": {
            "logical_path": "<WORKSPACE>/03_projects/language_management/romance/03_working_translations/stacks_fr_20260821/p05/evidence/DESCENT_SOURCE_DEFECTS.md",
            "bytes": len(evidence_raw),
            "sha256": EVIDENCE_SHA,
            "scope_note": "The append-only producer file also contains later DESCENT-041..047 allegations. They are preserved as adverse/out-of-scope evidence and are not R42 units; the committed R42 lease ends at DESCENT-040.",
        },
        "producer_ledger_original": {
            "logical_path": "<WORKSPACE>/03_projects/language_management/romance/03_working_translations/stacks_fr_20260821/00_control/SOURCE_DEFECT_LEDGER.csv",
            "bytes": len(ledger_raw),
            "sha256": LEDGER_SHA,
            "matching_descent_entries": 0,
        },
        "prelease_registry": {
            "commit": PRELEASE_HEAD,
            "overlays_sha256": PRELEASE_OVERLAYS_SHA,
            "leases_sha256": PRELEASE_LEASES_SHA,
            "registered_rounds_checked_through": 41,
            "source_map_variants_checked": 51,
            "canonical_source_map_files_checked": 41,
            "operation_spec_variants_checked": 46,
            "canonical_operation_spec_files_checked": 36,
            "matching_descent_or_exact_preimage_records": 0,
            "prior_stable_id_max": "MC-STK-ERR-1418",
        },
        "public_checks": {
            "official_commit": COMMIT,
            "official_source_retains_all_preimages": True,
            "official_issue_pr_exact_matches": 0,
            "tags": {"04R7": "Comments (0)", "04NK": "Comments (0)", "023V": "Comments (0)", "02VS": "Comments (0)", "023Z": "Comments (0)", "02VU": "Comments (0)", "02VV": "Comments (0)", "040J": "Comments (0)", "040K": "Comments (0)", "02VZ": "Comments (0)"},
        },
        "rows": adjudication_rows,
        "grouping": {
            "independent_units": 11,
            "exact_operations": 12,
            "authority_order": [unit["stable_id"] for unit in UNITS],
            "similar_but_distinct": [
                "DESCENT-038 is one mathematical defect unit with two required line-bound operations; both are retained under one stable ID.",
                "DESCENT-039 uses a full two-line guard so the valid f-based parenthetical at lines 8565--8566 remains unchanged.",
                "R41 ends at DESCENT-029 and preserves DESCENT-030..040 only as explicitly out-of-scope evidence, not as materialized or admitted operations.",
            ],
        },
        "replay": {"payload_bytes": len(payload), "payload_sha256": sha_bytes(payload), "line_count": payload.count(b"\n")},
        "mutations": "This receipt records adjudication and deduplication only; authority, producer files, generated source, and upstream were not mutated.",
    }
    dump("authority/registrar/DESCENT_R42_INDEPENDENT_ADJUDICATION_20260905.json", adjudication)

    validation = {
        "schema": "stacks-r42-source-validation-v1",
        "passed": True,
        "scope": "Source-only exact replay and structural validation; no build, render, final independent replay, admission, or composition claim.",
        "semantic_units": 11,
        "operations": 12,
        "line_preimages_exact": 12,
        "nonoverlapping": True,
        "unlisted_byte_changes": 0,
        "unchanged_interval_sha256": sha_bytes(bytes(unchanged)),
        "structure": structure,
        "authority": identity("authority/source/descent.tex"),
        "payload": identity("payload/descent.tex"),
        "adjudication": identity("authority/registrar/DESCENT_R42_INDEPENDENT_ADJUDICATION_20260905.json"),
        "deduplication": adjudication["prelease_registry"],
        "build": "NOT_PERFORMED",
        "visual_qa": "NOT_PERFORMED",
        "independent_candidate_replay": "NOT_PERFORMED",
    }
    dump("source-validation.json", validation)
    dump(
        "formula-diagram-inventory.json",
        {
            "schema": "stacks-r42-formula-diagram-inventory-v1",
            "source": SOURCE,
            "structure": structure,
            "operation_bound_changes": True,
            "note": "All mathematical or notational changes are exactly the twelve declared operations in eleven stable units; every unchanged byte interval and ordered structural token list is preserved.",
            "operations": [
                {
                    "id": operation["operation_id"],
                    "line": operation["line"],
                    "class": operation["class"],
                    "old": operation["old_text"],
                    "new": operation["replacement_text"],
                }
                for operation in operations
            ],
        },
    )

    authority_evidence = [
        identity("authority/registrar/DESCENT_R42_INDEPENDENT_ADJUDICATION_20260905.json"),
        identity("authority/producer/DESCENT_SOURCE_DEFECTS.md"),
        identity("authority/producer/SOURCE_DEFECT_LEDGER.csv"),
    ]
    config = {
        "schema": "mathematics-commons-stacks-errata-candidate-config/v1",
        "candidate_id": CANDIDATE_ID,
        "namespace": "commons/stacks/errata/r42",
        "lease_id": LEASE_ID,
        "writer_task": lease["writer_task"],
        "authority_commit": COMMIT,
        "authority_tree": TREE,
        "source_date_epoch": SOURCE_DATE_EPOCH,
        "accepted": 11,
        "rejected": 0,
        "unresolved": 0,
        "operation_count": 12,
        "expected_unit_ids": [unit["stable_id"] for unit in UNITS],
        "expected_producer_ids": [unit["producer_id"] for unit in UNITS],
        "payload_expected_bytes": len(payload),
        "payload_expected_sha256": sha_bytes(payload),
        "stems": {
            "descent": {
                "authority_bytes": len(source),
                "authority_sha256": AUTH_SHA,
                "payload_bytes": len(payload),
                "payload_sha256": sha_bytes(payload),
                "build_exceptions": {},
            }
        },
        "proof_closure": {
            "accepted": 11,
            "operations": 12,
            "producer_rows": 11,
            "source_defect": sum(unit["class"] == "source_defect" for unit in UNITS),
            "editorial_or_notational_clarification": sum(unit["class"] == "editorial_or_notational_clarification" for unit in UNITS),
            "rejected": 0,
            "unresolved": 0,
        },
        "build_render_admission_status": "NOT_PERFORMED",
        "independent_replay": "not_performed",
        "authority_evidence": authority_evidence,
    }
    dump("candidate.config.json", config)
    dump("candidate.config.input.json", config)
    dump(
        "builds/PENDING.json",
        {
            "schema": "stacks-r42-build-ready-state-v1",
            "build": "NOT_PERFORMED",
            "deterministic_pdf_replay": "NOT_PERFORMED",
            "render": "NOT_PERFORMED",
            "visual_inspection": "NOT_PERFORMED",
            "independent_candidate_replay": "NOT_PERFORMED",
            "admission": "NOT_PERFORMED",
            "reason": "Historical source-only preparation state; later additive receipts must preserve it.",
        },
    )
    dump(
        "REGENERATION_RECEIPT.json",
        {
            "schema": "stacks-r42-source-regeneration-v1",
            "status": "SOURCE_REPLAY_PASS_BUILD_PENDING",
            "pipeline": identity("pipeline_r42.py"),
            "source_validation": identity("source-validation.json"),
            "operation_spec": identity("operation-spec.json"),
            "stable_units": identity("stable-units.json"),
            "source_map": identity("source-map.jsonl"),
            "payload": identity("payload/descent.tex"),
            "no_final_manifest": True,
            "next_command": "powershell -File run-builds-with-mutex.ps1 -UpstreamRoot <PINNED_SOURCE_DIRECTORY> -WorkRoot1 <NEW_DIRECTORY> -WorkRoot2 <NEW_DIRECTORY> -PrivateRoot1 <PRIVATE_DIRECTORY> -PrivateRoot2 <PRIVATE_DIRECTORY>",
            "write_scope": "Only the leased R42 candidate; no TeX, admission, composition, or publication was performed.",
        },
    )

    workspace_bytes = str(WORKSPACE).encode("utf-8")
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix in {".json", ".jsonl", ".md", ".csv", ".py", ".ps1"}:
            assert workspace_bytes not in path.read_bytes(), path
    print(json.dumps({"source_pass": True, "units": 11, "operations": 12, "payload_sha256": sha_bytes(payload), "build": "NOT_PERFORMED"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
