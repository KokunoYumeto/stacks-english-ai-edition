"""Materialize the R40 Descent source candidate; never invokes TeX or admits it."""
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
PAYLOAD_SHA = "AA18A14DBBC153BD8F8D75C27EAE5D410BE7C0D52B54962AEFCDB59F75827BDA"
AUTH_BYTES = 353760
PAYLOAD_BYTES = 353794
COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
CANDIDATE_ID = "stacks-errata-a04446e-r40"
LEASE_ID = "stacks-lease-000044-errata-r40"
STAMP = "2026-09-05T11:15:31.908Z"
SOURCE_DATE_EPOCH = "1788606931"
PRELEASE_HEAD = "bf472632906dcfbc032620f8ce203fa687e929e5"
PRELEASE_OVERLAYS_SHA = "A259CAA4DBB502B35B7F0F0759D093CF59811D1590228B93AFD4D1714DC14FF0"
PRELEASE_LEASES_SHA = "BCDFF849CACF5C14657B76BE7BD43B5F147857ACE77621888CB3C2E4B9E7BD2A"

EVIDENCE_SOURCE = PRODUCER / "p05/evidence/DESCENT_SOURCE_DEFECTS.md"
LEDGER_SOURCE = PRODUCER / "00_control/SOURCE_DEFECT_LEDGER.csv"
EVIDENCE_SHA = "279C1FBF5732A56A192AE75C72FDFA46285381815CBE6536E178205BC86373A2"
LEDGER_SHA = "304D51200903ED870D2F72AF8F65C0AB28B314F6075B206C3B34F506B678F8CE"


UNITS = [
    {
        "stable_id": "MC-STK-ERR-1402",
        "producer_id": "DESCENT-013",
        "line": 6663,
        "class": "source_defect",
        "old": r"resp.\ \'etale, resp.\ an open immersion, the composition",
        "new": r"resp.\ smooth, resp.\ \'etale, resp.\ an open immersion, the composition",
        "tag": "04QV",
        "proof": "The statement lists six topologies in order but only five corresponding precomposition classes; smooth is the missing fourth class between syntomic and etale.",
    },
    {
        "stable_id": "MC-STK-ERR-1403",
        "producer_id": "DESCENT-014",
        "line": 6790,
        "class": "editorial_or_notational_clarification",
        "old": "Then property",
        "new": "The property",
        "tag": "036L",
        "proof": "The sentence introducing the displayed predicate requires the definite article; no mathematical token changes.",
    },
    {
        "stable_id": "MC-STK-ERR-1404",
        "producer_id": "DESCENT-015",
        "line": 6876,
        "class": "source_defect",
        "old": r"Denote $f_i : X_i \to X$ the compositions.",
        "new": r"Denote by $f_i : X_i \to Y$ the compositions.",
        "tag": "036Q",
        "proof": "For f:X->Y and Xi->X, the named compositions are Xi->X->Y. The proof compares their universal openness as maps to Y; the preferred full-line repair also supplies the missing English 'by'.",
    },
    {
        "stable_id": "MC-STK-ERR-1405",
        "producer_id": "DESCENT-016",
        "line": 7081,
        "class": "source_defect",
        "old": r"Assume $\mathcal{P}(f)$. Let $f(x_i) \leadsto y_i$",
        "new": r"Assume $\mathcal{P}(f)$. Let $f_i(x_i) \leadsto y_i$",
        "tag": "04QY",
        "proof": "Here xi lies in Xi and fi:Xi->Yi is the base change; f has domain X. The next line uses gi(fi(xi))=f(hi(xi)).",
    },
    {
        "stable_id": "MC-STK-ERR-1406",
        "producer_id": "DESCENT-017",
        "line": 7105,
        "class": "source_defect",
        "old": r"$f(x_i) \leadsto y$ be a specialization. Then $f(h_i(x_i)) \leadsto y$ so",
        "new": r"$f_i(x_i) \leadsto y$ be a specialization. Then $f(h_i(x_i)) \leadsto y$ so",
        "tag": "04QY",
        "proof": "Since fi=f composed with hi has domain Xi, the specialization of xi must start at fi(xi), as confirmed by the following f(hi(xi)).",
    },
    {
        "stable_id": "MC-STK-ERR-1407",
        "producer_id": "DESCENT-018",
        "line": 7132,
        "class": "editorial_or_notational_clarification",
        "old": r"$V = X \amalg Y$, let $a, b$ the obvious map, and let $h : U \to V$",
        "new": r"$V = X \amalg Y$, let $a, b$ be the obvious maps, and let $h : U \to V$",
        "tag": "04QY",
        "proof": "The construction introduces two evident morphisms a and b, so the copula and plural agreement are both required.",
    },
    {
        "stable_id": "MC-STK-ERR-1408",
        "producer_id": "DESCENT-019",
        "line": 7292,
        "class": "editorial_or_notational_clarification",
        "old": "(a) equivalent to (g).",
        "new": "(a) is equivalent to (g).",
        "tag": "04R1",
        "proof": "The copula is missing. Condition (g) combines the target-cover and source-cover reductions already proved equivalent to (a).",
    },
    {
        "stable_id": "MC-STK-ERR-1409",
        "producer_id": "DESCENT-020",
        "line": 7481,
        "class": "source_defect",
        "old": r"$\{X \to X \times_Z Y, X' \to X \times_Y Z\}$ is an \'etale covering,",
        "new": r"$\{X \to X \times_Z Y, X' \to X \times_Z Y\}$ is an \'etale covering,",
        "tag": "04R2",
        "proof": "The diagram identifies X and X'=f_Y^{-1}(Y') as the two pieces covering X times_Z Y. X times_Y Z is not defined because no map Z->Y is given.",
    },
    {
        "stable_id": "MC-STK-ERR-1410",
        "producer_id": "DESCENT-021",
        "line": 7511,
        "class": "editorial_or_notational_clarification",
        "old": r"\item locally finite type, see",
        "new": r"\item locally of finite type, see",
        "tag": "04R3",
        "proof": "The standard property, and the cited lemma name immediately below it, are 'locally of finite type'. The existing public comment on this tag concerns adding surjective and is unrelated.",
    },
    {
        "stable_id": "MC-STK-ERR-1411",
        "producer_id": "DESCENT-022",
        "line": 7609,
        "class": "editorial_or_notational_clarification",
        "old": r"we conclude that $f'_{U'} : U' \to Y'$ has $\mathcal{P}$.",
        "new": r"we conclude that $f'|_{U'} : U' \to Y'$ has $\mathcal{P}$.",
        "tag": "0CEZ",
        "proof": "Line 7606 already names the restriction f'|_{U'}:U'->V'; after composition with V'->Y', the same restricted morphism to Y' is meant. The subscripted f'_{U'} is undefined here.",
    },
    {
        "stable_id": "MC-STK-ERR-1412",
        "producer_id": "DESCENT-023",
        "line": 7622,
        "class": "editorial_or_notational_clarification",
        "old": r"morphism $g'|_U' : U' \to X$. Then $\{U' \to U\}$",
        "new": r"morphism $g'|_{U'} : U' \to X$. Then $\{U' \to U\}$",
        "tag": "0CEZ",
        "proof": "The restriction is to the open U' in X'. Braces are required so the prime belongs to the subscript; the same restriction is written correctly at lines 7602, 7603, and 7615.",
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
    assert matches[0]["candidate_path"] == "candidates/commons/stacks/errata/r40"
    assert (ROOT / ".gitattributes").read_bytes() == b"* -text\n"

    source = (UPSTREAM / SOURCE).read_bytes()
    assert len(source) == AUTH_BYTES and sha_bytes(source) == AUTH_SHA
    evidence_raw = EVIDENCE_SOURCE.read_bytes()
    ledger_raw = LEDGER_SOURCE.read_bytes()
    assert len(evidence_raw) == 9699 and sha_bytes(evidence_raw) == EVIDENCE_SHA
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
        old = declared["old"].encode("utf-8")
        replacement = declared["new"].encode("utf-8")
        positions = exact_occurrences(source, old)
        assert len(positions) == 1, (declared["stable_id"], positions)
        start = positions[0]
        line = source[:start].count(b"\n") + 1
        assert line == declared["line"], (declared["stable_id"], line)
        operation_id = declared["stable_id"] + "-OP1"
        producer_operation_id = declared["producer_id"] + "-OP1"
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
            "source_end_line": line,
            "start_byte": start,
            "end_byte_exclusive": start + len(old),
            "old_text": declared["old"],
            "old_bytes": len(old),
            "old_sha256": sha_bytes(old),
            "replacement_text": declared["new"],
            "replacement_bytes": len(replacement),
            "replacement_sha256": sha_bytes(replacement),
            "declared_line_occurrences": 1,
            "file_occurrences": 1,
        }
        operations.append(operation)
        unit = {
            "id": declared["stable_id"],
            "source": SOURCE,
            "producer_id": declared["producer_id"],
            "producer_ids": [declared["producer_id"]],
            "producer_aliases": [],
            "class": declared["class"],
            "locus": f"{SOURCE}:{line}",
            "operation_ids": [operation_id],
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
                "locus": f"{SOURCE}:{line}",
                "proof": declared["proof"],
                "operations": [operation],
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
                "id": f"R40-D{index:03d}",
                "timestamp_utc": STAMP,
                "choice": "materialize_source_proposal_not_admission",
                "stable_id": declared["stable_id"],
                "producer_id": declared["producer_id"],
                "rationale": declared["proof"],
                "supersedes": None,
            }
        )

    ordered = sorted(operations, key=lambda item: item["start_byte"])
    assert [item["stable_id"] for item in ordered] == [f"MC-STK-ERR-{number}" for number in range(1402, 1413)]
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
            "line": unit["line"],
            "classification": unit["class"],
            "tag": unit["tag"],
            "old": unit["old"],
            "replacement": unit["new"],
            "recommendation": "accept",
            "reason": unit["proof"],
            "exact_preimage_occurrences": 1,
        }
        for unit in UNITS
    ]
    adjudication = {
        "schema": "stacks-r40-descent-independent-adjudication/v1",
        "date": "2026-09-05",
        "status": "PASS_ACCEPT_11_NON_DUPLICATIVE_UNITS",
        "passed": True,
        "authority": {"path": "authority/source/descent.tex", "bytes": AUTH_BYTES, "sha256": AUTH_SHA},
        "producer_evidence_original": {
            "logical_path": "<WORKSPACE>/03_projects/language_management/romance/03_working_translations/stacks_fr_20260821/p05/evidence/DESCENT_SOURCE_DEFECTS.md",
            "bytes": len(evidence_raw),
            "sha256": EVIDENCE_SHA,
            "scope_note": "The append-only producer file also contains later DESCENT-024..029 allegations. They are preserved as adverse/out-of-scope evidence and are not R40 units; the committed R40 lease ends at DESCENT-023.",
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
            "registered_rounds_checked_through": 39,
            "source_map_files_checked": 47,
            "operation_spec_files_checked": 42,
            "matching_descent_or_exact_preimage_records": 0,
            "prior_stable_id_max": "MC-STK-ERR-1401",
        },
        "public_checks": {
            "official_commit": COMMIT,
            "official_source_retains_all_preimages": True,
            "official_issue_pr_exact_matches": 0,
            "tags": {
                "04QV": "Comments (0)",
                "036L": "Comments (0)",
                "036Q": "Comments (0)",
                "04QY": "Comments (0)",
                "04R1": "Comments (0)",
                "04R2": "Comments (0)",
                "04R3": "One unrelated comment about adding surjective; no matching correction",
                "0CEZ": "Comments (0)",
            },
        },
        "rows": adjudication_rows,
        "grouping": {
            "independent_units": 11,
            "authority_order": [unit["stable_id"] for unit in UNITS],
            "similar_but_distinct": [
                "DESCENT-013 is a distinct occurrence from the earlier smooth-case omission at lines 5337--5343.",
                "DESCENT-016 and DESCENT-017 are separate proof halves with independent exact guards.",
            ],
        },
        "replay": {"payload_bytes": len(payload), "payload_sha256": sha_bytes(payload), "line_count": payload.count(b"\n")},
        "mutations": "This receipt records adjudication and deduplication only; authority, producer files, generated source, and upstream were not mutated.",
    }
    dump("authority/registrar/DESCENT_R40_INDEPENDENT_ADJUDICATION_20260905.json", adjudication)

    validation = {
        "schema": "stacks-r40-source-validation-v1",
        "passed": True,
        "scope": "Source-only exact replay and structural validation; no build, render, final independent replay, admission, or composition claim.",
        "semantic_units": 11,
        "operations": 11,
        "line_preimages_exact": 11,
        "nonoverlapping": True,
        "unlisted_byte_changes": 0,
        "unchanged_interval_sha256": sha_bytes(bytes(unchanged)),
        "structure": structure,
        "authority": identity("authority/source/descent.tex"),
        "payload": identity("payload/descent.tex"),
        "adjudication": identity("authority/registrar/DESCENT_R40_INDEPENDENT_ADJUDICATION_20260905.json"),
        "deduplication": adjudication["prelease_registry"],
        "build": "NOT_PERFORMED",
        "visual_qa": "NOT_PERFORMED",
        "independent_candidate_replay": "NOT_PERFORMED",
    }
    dump("source-validation.json", validation)
    dump(
        "formula-diagram-inventory.json",
        {
            "schema": "stacks-r40-formula-diagram-inventory-v1",
            "source": SOURCE,
            "structure": structure,
            "operation_bound_changes": True,
            "note": "All mathematical or notational changes are exactly the eleven declared operations; every unchanged byte interval and ordered structural token list is preserved.",
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
        identity("authority/registrar/DESCENT_R40_INDEPENDENT_ADJUDICATION_20260905.json"),
        identity("authority/producer/DESCENT_SOURCE_DEFECTS.md"),
        identity("authority/producer/SOURCE_DEFECT_LEDGER.csv"),
    ]
    config = {
        "schema": "mathematics-commons-stacks-errata-candidate-config/v1",
        "candidate_id": CANDIDATE_ID,
        "namespace": "commons/stacks/errata/r40",
        "lease_id": LEASE_ID,
        "writer_task": lease["writer_task"],
        "authority_commit": COMMIT,
        "authority_tree": TREE,
        "source_date_epoch": SOURCE_DATE_EPOCH,
        "accepted": 11,
        "rejected": 0,
        "unresolved": 0,
        "operation_count": 11,
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
            "operations": 11,
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
            "schema": "stacks-r40-build-ready-state-v1",
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
            "schema": "stacks-r40-source-regeneration-v1",
            "status": "SOURCE_REPLAY_PASS_BUILD_PENDING",
            "pipeline": identity("pipeline_r40.py"),
            "source_validation": identity("source-validation.json"),
            "operation_spec": identity("operation-spec.json"),
            "stable_units": identity("stable-units.json"),
            "source_map": identity("source-map.jsonl"),
            "payload": identity("payload/descent.tex"),
            "no_final_manifest": True,
            "next_command": "powershell -File run-builds-with-mutex.ps1 -UpstreamRoot <PINNED_SOURCE_DIRECTORY> -WorkRoot1 <NEW_DIRECTORY> -WorkRoot2 <NEW_DIRECTORY> -PrivateRoot1 <PRIVATE_DIRECTORY> -PrivateRoot2 <PRIVATE_DIRECTORY>",
            "write_scope": "Only the leased R40 candidate; no TeX, admission, composition, or publication was performed.",
        },
    )

    workspace_bytes = str(WORKSPACE).encode("utf-8")
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix in {".json", ".jsonl", ".md", ".csv", ".py", ".ps1"}:
            assert workspace_bytes not in path.read_bytes(), path
    print(json.dumps({"source_pass": True, "units": 11, "operations": 11, "payload_sha256": sha_bytes(payload), "build": "NOT_PERFORMED"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
