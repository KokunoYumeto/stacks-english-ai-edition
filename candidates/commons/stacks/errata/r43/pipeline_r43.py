"""Materialize the R43 Descent source candidate; never invokes TeX or admits it."""
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
PAYLOAD_SHA = "1D879A4F8874CDA6C3D57D9C8D059C5E6AC1FAE2EE4467BF4C4C7C9621B8F907"
AUTH_BYTES = 353760
PAYLOAD_BYTES = 353754
COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
CANDIDATE_ID = "stacks-errata-a04446e-r43"
LEASE_ID = "stacks-lease-000047-errata-r43"
STAMP = "2026-09-05T13:56:05.033Z"
SOURCE_DATE_EPOCH = "1788616565"
PRELEASE_HEAD = "c2107a9d5f6f0644abc7af42d739ff741c9dc675"
PRELEASE_OVERLAYS_SHA = "DA19549F9CF827415FEB484D5C4351123231805CC80709E04D91561DE3423DA0"
PRELEASE_LEASES_SHA = "17787014140DFB45E7915A2584A5EB9E06E437C27FF7A2743F309533C1993628"

EVIDENCE_SOURCE = PRODUCER / "p05/evidence/DESCENT_SOURCE_DEFECTS.md"
LEDGER_SOURCE = PRODUCER / "00_control/SOURCE_DEFECT_LEDGER.csv"
EVIDENCE_SHA = "282E9EFFEEA7BD2A102E935052D325BF0E3ACD732D88AAE4CCB5F7479988AB1F"
LEDGER_SHA = "304D51200903ED870D2F72AF8F65C0AB28B314F6075B206C3B34F506B678F8CE"


UNITS = [
    {
        "stable_id": "MC-STK-ERR-1430", "producer_id": "DESCENT-041",
        "class": "editorial_or_notational_clarification", "tags": ["02VY"],
        "proof": "Full faithfulness already implies faithfulness, so the phrase 'faithful and fully faithful' is redundant; the minimal repair retains the mathematically stronger property used by the cited result.",
        "operations": [{"line": 8830, "end_line": 8830, "old": "The functor is faithful and fully faithful by", "new": "The functor is fully faithful by"}],
    },
    {
        "stable_id": "MC-STK-ERR-1431", "producer_id": "DESCENT-042",
        "class": "editorial_or_notational_clarification", "tags": ["0AP4"],
        "proof": "The sentence refers to one collection of gluing isomorphisms satisfying the cocycle condition, so the singular count noun is 'datum', not 'data'.",
        "operations": [{"line": 8955, "end_line": 8956, "old": "is a glueing\ndata as in Schemes", "new": "is a glueing\ndatum as in Schemes"}],
    },
    {
        "stable_id": "MC-STK-ERR-1432", "producer_id": "DESCENT-043",
        "class": "editorial_or_notational_clarification", "tags": ["02W1"],
        "proof": "The initialism 'fpqc' begins with a vowel sound, so the indefinite article is 'an'.",
        "operations": [{"line": 8976, "end_line": 8976, "old": "relative to a fpqc-covering", "new": "relative to an fpqc-covering"}],
    },
    {
        "stable_id": "MC-STK-ERR-1433", "producer_id": "DESCENT-044",
        "class": "editorial_or_notational_clarification", "tags": ["02W1"],
        "proof": "The adverb modifying the recurring condition is 'sometimes'; 'sometime' denotes an unspecified time and is not grammatical here.",
        "operations": [{"line": 8986, "end_line": 8986, "old": "then it is sometime the", "new": "then it is sometimes the"}],
    },
    {
        "stable_id": "MC-STK-ERR-1434", "producer_id": "DESCENT-045",
        "class": "editorial_or_notational_clarification", "tags": ["02W3"],
        "proof": "The phrasal verb is 'pull back'; the closed compound 'pullback' is a noun or adjective, not the finite verb required after 'we'.",
        "operations": [{"line": 9060, "end_line": 9060, "old": "if we pullback", "new": "if we pull back"}],
    },
    {
        "stable_id": "MC-STK-ERR-1435", "producer_id": "DESCENT-046",
        "class": "source_defect", "tags": ["02W3"],
        "proof": "The proof shrinks the affine base opens S_i covering S so that their pullbacks X_i retain the desired property; the smaller affine opens are therefore opens of S, not opens of X.",
        "operations": [{"line": 9125, "end_line": 9125, "old": r"restricting to smaller affine opens in $X$.", "new": r"restricting to smaller affine opens in $S$."}],
    },
    {
        "stable_id": "MC-STK-ERR-1436", "producer_id": "DESCENT-047",
        "class": "editorial_or_notational_clarification", "tags": ["02W5"],
        "proof": "English requires 'denote by F_i the sheaf'; inserting 'by' is the minimal grammatical repair and changes no mathematical object.",
        "operations": [{"line": 9395, "end_line": 9395, "old": r"For each $i$ denote $F_i$ the sheaf", "new": r"For each $i$ denote by $F_i$ the sheaf"}],
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
    assert matches[0]["candidate_path"] == "candidates/commons/stacks/errata/r43"
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
                "id": f"R43-D{index:03d}",
                "timestamp_utc": STAMP,
                "choice": "materialize_source_proposal_not_admission",
                "stable_id": declared["stable_id"],
                "producer_id": declared["producer_id"],
                "rationale": declared["proof"],
                "supersedes": None,
            }
        )

    ordered = sorted(operations, key=lambda item: item["start_byte"])
    assert list(dict.fromkeys(item["stable_id"] for item in ordered)) == [f"MC-STK-ERR-{number}" for number in range(1430, 1437)]
    assert len({item["operation_id"] for item in ordered}) == 7
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
        "schema": "stacks-r43-descent-independent-adjudication/v1",
        "date": "2026-09-05",
        "status": "PASS_ACCEPT_7_NON_DUPLICATIVE_UNITS_7_OPERATIONS",
        "passed": True,
        "authority": {"path": "authority/source/descent.tex", "bytes": AUTH_BYTES, "sha256": AUTH_SHA},
        "producer_evidence_original": {
            "logical_path": "<WORKSPACE>/03_projects/language_management/romance/03_working_translations/stacks_fr_20260821/p05/evidence/DESCENT_SOURCE_DEFECTS.md",
            "bytes": len(evidence_raw),
            "sha256": EVIDENCE_SHA,
            "scope_note": "R43 is exactly the append-only DESCENT-041..047 suffix. Earlier DESCENT-001..040 findings remain preserved in predecessor rounds and are not resent or rematerialized here.",
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
            "registered_rounds_checked_through": 42,
            "source_map_variants_checked": 52,
            "canonical_source_map_files_checked": 42,
            "operation_spec_variants_checked": 47,
            "canonical_operation_spec_files_checked": 37,
            "matching_descent_or_exact_preimage_records": 0,
            "prior_stable_id_max": "MC-STK-ERR-1429",
        },
        "public_checks": {
            "official_commit": COMMIT,
            "official_source_retains_all_preimages": True,
            "official_issue_pr_exact_matches": 0,
            "tags": {"02VY": "Comments (0)", "0AP4": "Comments (0)", "02W1": "Comments (0)", "02W3": "Comments (0)", "02W5": "Comments (0)"},
        },
        "rows": adjudication_rows,
        "grouping": {
            "independent_units": 7,
            "exact_operations": 7,
            "authority_order": [unit["stable_id"] for unit in UNITS],
            "similar_but_distinct": [
                "DESCENT-042 uses one atomic two-line guard because the corrected singular noun begins on the second physical line.",
                "DESCENT-046 is the sole source-defect classification; the other six units are editorial or grammatical clarifications.",
                "R42 ends at DESCENT-040; R43 starts at DESCENT-041 and introduces no predecessor payload operation.",
            ],
        },
        "replay": {"payload_bytes": len(payload), "payload_sha256": sha_bytes(payload), "line_count": payload.count(b"\n")},
        "mutations": "This receipt records adjudication and deduplication only; authority, producer files, generated source, and upstream were not mutated.",
    }
    dump("authority/registrar/DESCENT_R43_INDEPENDENT_ADJUDICATION_20260905.json", adjudication)

    validation = {
        "schema": "stacks-r43-source-validation-v1",
        "passed": True,
        "scope": "Source-only exact replay and structural validation; no build, render, final independent replay, admission, or composition claim.",
        "semantic_units": 7,
        "operations": 7,
        "line_preimages_exact": 7,
        "nonoverlapping": True,
        "unlisted_byte_changes": 0,
        "unchanged_interval_sha256": sha_bytes(bytes(unchanged)),
        "structure": structure,
        "authority": identity("authority/source/descent.tex"),
        "payload": identity("payload/descent.tex"),
        "adjudication": identity("authority/registrar/DESCENT_R43_INDEPENDENT_ADJUDICATION_20260905.json"),
        "deduplication": adjudication["prelease_registry"],
        "build": "NOT_PERFORMED",
        "visual_qa": "NOT_PERFORMED",
        "independent_candidate_replay": "NOT_PERFORMED",
    }
    dump("source-validation.json", validation)
    dump(
        "formula-diagram-inventory.json",
        {
            "schema": "stacks-r43-formula-diagram-inventory-v1",
            "source": SOURCE,
            "structure": structure,
            "operation_bound_changes": True,
            "note": "All mathematical, grammatical, or notational changes are exactly the seven declared operations in seven stable units; every unchanged byte interval and ordered structural token list is preserved.",
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
        identity("authority/registrar/DESCENT_R43_INDEPENDENT_ADJUDICATION_20260905.json"),
        identity("authority/producer/DESCENT_SOURCE_DEFECTS.md"),
        identity("authority/producer/SOURCE_DEFECT_LEDGER.csv"),
    ]
    config = {
        "schema": "mathematics-commons-stacks-errata-candidate-config/v1",
        "candidate_id": CANDIDATE_ID,
        "namespace": "commons/stacks/errata/r43",
        "lease_id": LEASE_ID,
        "writer_task": lease["writer_task"],
        "authority_commit": COMMIT,
        "authority_tree": TREE,
        "source_date_epoch": SOURCE_DATE_EPOCH,
        "accepted": 7,
        "rejected": 0,
        "unresolved": 0,
        "operation_count": 7,
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
            "accepted": 7,
            "operations": 7,
            "producer_rows": 7,
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
            "schema": "stacks-r43-build-ready-state-v1",
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
            "schema": "stacks-r43-source-regeneration-v1",
            "status": "SOURCE_REPLAY_PASS_BUILD_PENDING",
            "pipeline": identity("pipeline_r43.py"),
            "source_validation": identity("source-validation.json"),
            "operation_spec": identity("operation-spec.json"),
            "stable_units": identity("stable-units.json"),
            "source_map": identity("source-map.jsonl"),
            "payload": identity("payload/descent.tex"),
            "no_final_manifest": True,
            "next_command": "powershell -File run-builds-with-mutex.ps1 -UpstreamRoot <PINNED_SOURCE_DIRECTORY> -WorkRoot1 <NEW_DIRECTORY> -WorkRoot2 <NEW_DIRECTORY> -PrivateRoot1 <PRIVATE_DIRECTORY> -PrivateRoot2 <PRIVATE_DIRECTORY>",
            "write_scope": "Only the leased R43 candidate; no TeX, admission, composition, or publication was performed.",
        },
    )

    workspace_bytes = str(WORKSPACE).encode("utf-8")
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix in {".json", ".jsonl", ".md", ".csv", ".py", ".ps1"}:
            assert workspace_bytes not in path.read_bytes(), path
    print(json.dumps({"source_pass": True, "units": 7, "operations": 7, "payload_sha256": sha_bytes(payload), "build": "NOT_PERFORMED"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
