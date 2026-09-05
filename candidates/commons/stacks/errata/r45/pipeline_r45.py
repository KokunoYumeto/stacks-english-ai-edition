"""Materialize the R45 Topologies source candidate; never invokes TeX or admits it."""
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
INTAKE = WORKSPACE / "03_projects/language_management/cjk/00_lane_control"
QA_STATE = (
    WORKSPACE
    / "03_projects/language_management/romance/03_working_translations/"
      "stacks_fr_20260821/p05/evidence/TOPOLOGIES_NATIVE_QA_STATE.json"
)
TEMPLATE = REPO / "candidates/commons/stacks/errata/r44"
SOURCE = "topologies.tex"
AUTH_SHA = "C984C98BCD458A191880433DED32A36AC9035543BBF8C98E191AE022A260F513"
AUTH_BYTES = 166188
PAYLOAD_SHA = "FA88114672E734B6B9677C62378691DFFA761D2376026EAE4340CDEFD053A8A9"
PAYLOAD_BYTES = 166236
COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
CANDIDATE_ID = "stacks-errata-a04446e-r45"
LEASE_ID = "stacks-lease-000049-errata-r45"
STAMP = "2026-09-05T16:57:49.9357746Z"
SOURCE_DATE_EPOCH = "1788627469"
PRELEASE_HEAD = "05d14edf76f2d54e8d6867b09359cbbc4e5ddd00"
PRELEASE_OVERLAYS_SHA = "0A86C8871E2459B7C0B2FB02620FFD696D01F1C175E5EA0F32A7BB589F03AAAD"
INTAKE_NAME = "STACKS_TOPOLOGIES_INDEPENDENT_INTAKE_20260905_R1.json"
INTAKE_BYTES = 36164
INTAKE_SHA = "DCAEB62D9F21D92AE551104AAED8BC9EB5A19F07FC098422F221ACF8F89996D9"
QA_BYTES = 13853
QA_SHA = "595D45784CE9CB7107700A565D3FCA24635DAC0AE4DE4F0BE11DE90099D0ED49"
EXPECTED_STABLE_IDS = [f"MC-STK-ERR-{number}" for number in range(1461, 1480)]
EDITORIAL_CLASSES = {"typographic_macro_defect", "editorial_marker_misplacement"}
GENERIC_TOOLS = [
    "build-receipt.py",
    "check-manifest.py",
    "derive-visual-pages.py",
    "deterministic-replay.py",
    "render-qa.py",
    "replay-build.py",
    "run-builds-with-mutex.ps1",
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
    write_bytes(
        relative,
        (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )


def write_jsonl(relative: str, rows: list[dict]) -> None:
    raw = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
    write_bytes(relative, raw.encode("utf-8"))


def identity(relative: str) -> dict:
    path = ROOT / relative
    return {"path": relative, "bytes": path.stat().st_size, "sha256": sha_path(path)}


def sanitize_text(text: str) -> str:
    values = {str(WORKSPACE), WORKSPACE.as_posix(), str(WORKSPACE.parent), WORKSPACE.parent.as_posix()}
    values |= {value.replace("\\", "\\\\") for value in values}
    for value in sorted(values, key=len, reverse=True):
        text = text.replace(value, "<WORKSPACE>")
    return re.sub(
        r"C:(?:\\|/)Users(?:\\|/)[^\\/\r\n\"']+",
        "<USER_ROOT>",
        text,
        flags=re.IGNORECASE,
    )


def occurrences(haystack: bytes, needle: bytes) -> list[int]:
    found: list[int] = []
    cursor = 0
    while True:
        position = haystack.find(needle, cursor)
        if position < 0:
            return found
        found.append(position)
        cursor = position + len(needle)


def normalized_class(producer_class: str) -> str:
    return (
        "editorial_or_notational_clarification"
        if producer_class in EDITORIAL_CLASSES
        else "source_defect"
    )


def scan_prior_registry(target_operations: list[dict]) -> dict:
    stable_ids = set(EXPECTED_STABLE_IDS)
    overlays_path = REPO / "registry/overlays.json"
    overlays = json.loads(overlays_path.read_text(encoding="utf-8"))["registered_entries"]
    assert sha_path(overlays_path) == PRELEASE_OVERLAYS_SHA
    prior_stable = [stable_id for entry in overlays for stable_id in entry["stable_ids"]]
    assert not stable_ids.intersection(prior_stable)
    prior_max = max(int(value.rsplit("-", 1)[1]) for value in prior_stable if value.startswith("MC-STK-ERR-"))
    assert prior_max == 1460
    producer_ids = {operation["producer_id"] for operation in target_operations}
    exact_old = {operation["old_text"] for operation in target_operations}
    producer_hits = source_operations = interval_overlaps = preimage_hits = 0
    spec_files = map_files = 0
    for path in (REPO / "candidates").rglob("operation-spec*.json"):
        if ROOT in path.resolve().parents:
            continue
        spec_files += 1
        raw = path.read_text(encoding="utf-8")
        producer_hits += sum(raw.count(producer_id) for producer_id in producer_ids)
        for prior in json.loads(raw).get("operations", []):
            if prior.get("source") != SOURCE:
                continue
            source_operations += 1
            preimage_hits += int(prior.get("old_text") in exact_old)
            interval_overlaps += sum(
                not (
                    prior["end_byte_exclusive"] <= target["start_byte"]
                    or target["end_byte_exclusive"] <= prior["start_byte"]
                )
                for target in target_operations
            )
    for path in (REPO / "candidates").rglob("source-map*.jsonl"):
        if ROOT in path.resolve().parents:
            continue
        map_files += 1
        raw = path.read_text(encoding="utf-8")
        producer_hits += sum(raw.count(producer_id) for producer_id in producer_ids)
        for line in raw.splitlines():
            if not line:
                continue
            for prior in json.loads(line).get("operations", []):
                if prior.get("source") != SOURCE:
                    continue
                source_operations += 1
                preimage_hits += int(prior.get("old_text") in exact_old)
                interval_overlaps += sum(
                    not (
                        prior["end_byte_exclusive"] <= target["start_byte"]
                        or target["end_byte_exclusive"] <= prior["start_byte"]
                    )
                    for target in target_operations
                )
    assert producer_hits == source_operations == interval_overlaps == preimage_hits == 0
    return {
        "prelease_commit": PRELEASE_HEAD,
        "overlays_sha256": PRELEASE_OVERLAYS_SHA,
        "registered_entries_checked": len(overlays),
        "registered_errata_rounds_checked_through": 44,
        "operation_spec_variants_checked": spec_files,
        "source_map_variants_checked": map_files,
        "matching_producer_ids": producer_hits,
        "prior_topologies_operations": source_operations,
        "prior_target_interval_overlaps": interval_overlaps,
        "prior_exact_preimage_hits": preimage_hits,
        "prior_stable_id_max": f"MC-STK-ERR-{prior_max:04d}",
    }


def copy_generic_tools() -> None:
    for name in GENERIC_TOOLS:
        raw = (TEMPLATE / name).read_bytes()
        raw = raw.replace(b"stacks-errata-a04446e-r44", b"stacks-errata-a04446e-r45")
        raw = raw.replace(b"stacks-r44", b"stacks-r45")
        raw = raw.replace(b".r44-build-work.json", b".r45-build-work.json")
        write_bytes(name, raw)


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
    assert matches[0]["candidate_path"] == "candidates/commons/stacks/errata/r45"
    assert (ROOT / ".gitattributes").read_bytes() == b"* -text\n"

    source = (UPSTREAM / SOURCE).read_bytes()
    assert len(source) == AUTH_BYTES and sha_bytes(source) == AUTH_SHA
    assert source.count(b"\r") == 0 and source.count(b"\n") == 4512
    intake_path = INTAKE / INTAKE_NAME
    intake_raw = intake_path.read_bytes()
    assert len(intake_raw) == INTAKE_BYTES and sha_bytes(intake_raw) == INTAKE_SHA
    intake = json.loads(intake_raw.decode("utf-8-sig"))
    assert intake["status"] == "independent_preflight_complete_not_registered_not_published"
    assert intake["summary"] == {
        "accepted": 19,
        "deferred": 0,
        "rejected": 0,
        "accepted_operations": 36,
        "stable_ids_allocated": 0,
        "duplicates_against_R1_R44": 0,
        "internal_analogue_policy": "Related patterns at distinct source loci remain separate line-scoped replay operations.",
    }
    qa_raw = QA_STATE.read_bytes()
    assert len(qa_raw) == QA_BYTES and sha_bytes(qa_raw) == QA_SHA
    qa = json.loads(qa_raw.decode("utf-8-sig"))
    assert qa["source_sha256"] == AUTH_SHA and len(qa["source_defects"]) == 19

    write_bytes(f"authority/source/{SOURCE}", source)
    write_bytes("authority/COPYING", (UPSTREAM / "COPYING").read_bytes())
    write_bytes(f"authority/intake/{INTAKE_NAME}", sanitize_text(intake_raw.decode("utf-8-sig")).encode("utf-8"))
    write_bytes("authority/intake/TOPOLOGIES_NATIVE_QA_STATE.json", sanitize_text(qa_raw.decode("utf-8-sig")).encode("utf-8"))
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

    selected = sorted(intake["candidates"], key=lambda item: min(op["start_byte"] for op in item["operations"]))
    assert len(selected) == len(EXPECTED_STABLE_IDS) == 19
    operations: list[dict] = []
    units: list[dict] = []
    maps: list[dict] = []
    decisions: list[dict] = []
    adjudication_rows: list[dict] = []
    for index, (declared, stable_id) in enumerate(zip(selected, EXPECTED_STABLE_IDS), 1):
        producer_id = f"TOPOLOGIES-NATIVE-{declared['ordinal']:03d}"
        classification = normalized_class(declared["class"])
        group: list[dict] = []
        for operation_index, declared_operation in enumerate(declared["operations"], 1):
            old_text = declared_operation["old_text"]
            replacement_text = declared_operation["replacement_text"]
            old = old_text.encode("utf-8")
            replacement = replacement_text.encode("utf-8")
            start = int(declared_operation["start_byte"])
            end = int(declared_operation["end_byte_exclusive"])
            assert sha_bytes(old) == declared_operation["old_sha256"]
            assert source[start:end] == old
            positions = occurrences(source, old)
            assert len(positions) == int(declared_operation["file_occurrences"])
            line = source[:start].count(b"\n") + 1
            operation = {
                "operation_id": f"{stable_id}-OP{operation_index}",
                "stable_id": stable_id,
                "producer_id": producer_id,
                "producer_operation_id": declared_operation["id"],
                "origin": "manager_topologies_independent_intake_r1",
                "class": classification,
                "producer_class": declared["class"],
                "source": SOURCE,
                "line": line,
                "source_start_line": line,
                "source_end_line": line + old.count(b"\n"),
                "declared_lines": declared_operation["lines"],
                "start_byte": start,
                "end_byte_exclusive": end,
                "old_text": old_text,
                "old_bytes": len(old),
                "old_sha256": sha_bytes(old),
                "replacement_text": replacement_text,
                "replacement_bytes": len(replacement),
                "replacement_sha256": sha_bytes(replacement),
                "declared_line_occurrences": sum(
                    source[:position].count(b"\n") + 1 == line for position in positions
                ),
                "file_occurrences": len(positions),
            }
            assert operation["declared_line_occurrences"] == 1
            group.append(operation)
            operations.append(operation)
        lines = [operation["line"] for operation in group]
        locus = f"{SOURCE}:" + ",".join(str(value) for value in lines)
        unit = {
            "id": stable_id,
            "source": SOURCE,
            "producer_id": producer_id,
            "producer_ids": [producer_id],
            "producer_aliases": [f"TOP-{declared['ordinal']:02d}"],
            "class": classification,
            "producer_class": declared["class"],
            "locus": locus,
            "logical_location": declared["location"],
            "operation_ids": [operation["operation_id"] for operation in group],
            "payload": f"payload/{SOURCE}",
            "status": "accepted_source_proposal_not_admitted",
        }
        units.append(unit)
        maps.append(
            {
                "schema": "mathematics-commons-stacks-source-map/v2",
                "unit_id": stable_id,
                "source": SOURCE,
                "authority": f"authority/source/{SOURCE}",
                "authority_sha256": AUTH_SHA,
                "payload": f"payload/{SOURCE}",
                "producer_id": producer_id,
                "producer_ids": [producer_id],
                "producer_aliases": [f"TOP-{declared['ordinal']:02d}"],
                "class": classification,
                "producer_class": declared["class"],
                "locus": locus,
                "logical_location": declared["location"],
                "proof": declared["rationale"],
                "operations": group,
                "adverse_evidence": (
                    "Accepted as an editorial or notational source correction, not classified as a false theorem."
                    if classification != "source_defect"
                    else None
                ),
            }
        )
        decisions.append(
            {
                "schema": "mathematics-commons-stacks-decision/v1",
                "id": f"R45-D{index:03d}",
                "timestamp_utc": STAMP,
                "choice": "materialize_source_proposal_not_admission",
                "stable_id": stable_id,
                "producer_id": producer_id,
                "producer_aliases": [f"TOP-{declared['ordinal']:02d}"],
                "rationale": declared["rationale"],
                "supersedes": None,
            }
        )
        adjudication_rows.append(
            {
                "stable_id": stable_id,
                "producer_id": producer_id,
                "producer_ordinal": declared["ordinal"],
                "source_lines": lines,
                "logical_location": declared["location"],
                "producer_class": declared["class"],
                "classification": classification,
                "operation_count": len(group),
                "recommendation": "accept",
                "reason": declared["rationale"],
                "exact_line_preimage_occurrences": [1] * len(group),
            }
        )

    assert len(operations) == 36
    ordered = sorted(operations, key=lambda item: item["start_byte"])
    assert all(left["end_byte_exclusive"] <= right["start_byte"] for left, right in zip(ordered, ordered[1:]))
    assert len({item["operation_id"] for item in ordered}) == 36
    payload = source
    for operation in reversed(ordered):
        replacement = operation["replacement_text"].encode("utf-8")
        payload = payload[: operation["start_byte"]] + replacement + payload[operation["end_byte_exclusive"] :]
    assert len(payload) == PAYLOAD_BYTES and sha_bytes(payload) == PAYLOAD_SHA
    write_bytes(f"payload/{SOURCE}", payload)

    dedup = scan_prior_registry(operations)
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
        diffs = [index for index, (left, right) in enumerate(zip(before, after)) if left != right]
        assert len(before) == len(after)
        if name == "refs":
            assert len(diffs) == 5
            assert all(before[index] == b"\\ref{sets-lemma-what-is-in-it}" for index in diffs)
            assert all(after[index] == b"\\ref{sets-lemma-coverings-site}" for index in diffs)
        else:
            assert not diffs, name
        structure[name] = {
            "authority": len(before),
            "candidate": len(after),
            "count_equal": True,
            "ordered_equal": not diffs,
            "declared_changed_positions": diffs,
        }

    unchanged = bytearray()
    source_cursor = payload_cursor = 0
    for operation in ordered:
        span = source[source_cursor : operation["start_byte"]]
        assert payload[payload_cursor : payload_cursor + len(span)] == span
        unchanged.extend(span)
        payload_cursor += len(span)
        replacement = operation["replacement_text"].encode("utf-8")
        assert payload[payload_cursor : payload_cursor + len(replacement)] == replacement
        payload_cursor += len(replacement)
        source_cursor = operation["end_byte_exclusive"]
    assert payload[payload_cursor:] == source[source_cursor:]
    unchanged.extend(source[source_cursor:])

    original_bindings = [
        {"logical_path": f"<WORKSPACE>/03_projects/language_management/cjk/00_lane_control/{INTAKE_NAME}", "bytes": INTAKE_BYTES, "sha256": INTAKE_SHA},
        {"logical_path": "<WORKSPACE>/03_projects/language_management/romance/03_working_translations/stacks_fr_20260821/p05/evidence/TOPOLOGIES_NATIVE_QA_STATE.json", "bytes": QA_BYTES, "sha256": QA_SHA},
    ]
    adjudication_path = "authority/registrar/TOPOLOGIES_R45_INDEPENDENT_ADJUDICATION_20260905.json"
    dump(
        adjudication_path,
        {
            "schema": "stacks-r45-topologies-independent-adjudication/v1",
            "date": "2026-09-05",
            "status": "PASS_ACCEPT_19_NON_DUPLICATIVE_UNITS_36_OPERATIONS",
            "passed": True,
            "authority": {"path": f"authority/source/{SOURCE}", "bytes": AUTH_BYTES, "sha256": AUTH_SHA},
            "intake_originals": original_bindings,
            "prelease_registry": dedup,
            "rows": adjudication_rows,
            "grouping": {
                "semantic_units": len(units),
                "exact_operations": len(operations),
                "stable_ids_in_first_locus_authority_order": EXPECTED_STABLE_IDS,
                "multi_operation_units": {row["stable_id"]: row["operation_count"] for row in adjudication_rows if row["operation_count"] > 1},
                "deferred": 0,
                "rejected": 0,
            },
            "classification": {
                "source_defect": sum(unit["class"] == "source_defect" for unit in units),
                "editorial_or_notational_clarification": sum(unit["class"] != "source_defect" for unit in units),
            },
            "replay": {"payload_bytes": len(payload), "payload_sha256": sha_bytes(payload), "physical_lines": payload.count(b"\n")},
            "mutations": "Only the leased R45 candidate is materialized; frozen authority, producer/French/CJK sources, generated source, upstream, and registry admission remain untouched.",
        },
    )
    validation = {
        "schema": "stacks-r45-source-validation-v1",
        "passed": True,
        "scope": "Source-only exact replay, semantic-unit grouping, structural token accounting, and registry dedup validation; no build, render, admission, composition, or publication claim.",
        "semantic_units": 19,
        "operations": 36,
        "line_preimages_exact": 36,
        "nonoverlapping": True,
        "unlisted_byte_changes": 0,
        "unchanged_interval_sha256": sha_bytes(bytes(unchanged)),
        "structure": structure,
        "authority": identity(f"authority/source/{SOURCE}"),
        "payload": identity(f"payload/{SOURCE}"),
        "adjudication": identity(adjudication_path),
        "deduplication": dedup,
        "build": "NOT_PERFORMED",
        "visual_qa": "NOT_PERFORMED",
        "independent_candidate_replay": "NOT_PERFORMED",
    }
    dump("source-validation.json", validation)
    dump(
        "formula-diagram-inventory.json",
        {
            "schema": "stacks-r45-formula-diagram-inventory-v1",
            "source": SOURCE,
            "structure": structure,
            "operation_bound_changes": True,
            "note": "All changes are exactly the 36 declared operations in 19 stable units; every unchanged byte interval is preserved.",
            "operations": [
                {"id": operation["operation_id"], "line": operation["line"], "class": operation["class"], "old": operation["old_text"], "new": operation["replacement_text"]}
                for operation in operations
            ],
        },
    )

    authority_evidence = [
        identity(adjudication_path),
        identity(f"authority/intake/{INTAKE_NAME}"),
        identity("authority/intake/TOPOLOGIES_NATIVE_QA_STATE.json"),
    ]
    config = {
        "schema": "mathematics-commons-stacks-errata-candidate-config/v1",
        "candidate_id": CANDIDATE_ID,
        "namespace": "commons/stacks/errata/r45",
        "lease_id": LEASE_ID,
        "writer_task": lease["writer_task"],
        "authority_commit": COMMIT,
        "authority_tree": TREE,
        "source_date_epoch": SOURCE_DATE_EPOCH,
        "accepted": 19,
        "rejected": 0,
        "unresolved": 0,
        "excluded_deferred": 0,
        "operation_count": 36,
        "expected_unit_ids": EXPECTED_STABLE_IDS,
        "expected_producer_ids": [unit["producer_id"] for unit in units],
        "payload_expected_bytes": len(payload),
        "payload_expected_sha256": sha_bytes(payload),
        "stems": {
            "topologies": {
                "authority_bytes": len(source),
                "authority_sha256": AUTH_SHA,
                "payload_bytes": len(payload),
                "payload_sha256": sha_bytes(payload),
                "build_exceptions": {
                    "candidate_undefined_reference_target_deltas": {
                        "sets-lemma-coverings-site": 5,
                        "sets-lemma-what-is-in-it": -5
                    }
                },
            }
        },
        "proof_closure": {
            "accepted": 19,
            "operations": 36,
            "producer_rows": 19,
            "source_defect": sum(unit["class"] == "source_defect" for unit in units),
            "editorial_or_notational_clarification": sum(unit["class"] != "source_defect" for unit in units),
            "rejected": 0,
            "unresolved": 0,
            "excluded_deferred": 0,
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
            "schema": "stacks-r45-build-ready-state-v1",
            "build": "NOT_PERFORMED",
            "deterministic_pdf_replay": "NOT_PERFORMED",
            "fls_dependency_closure": "NOT_PERFORMED",
            "render": "NOT_PERFORMED",
            "visual_inspection": "NOT_PERFORMED",
            "independent_candidate_replay": "NOT_PERFORMED",
            "admission": "NOT_PERFORMED",
            "reason": "Historical source-only preparation state; later additive receipts must preserve it.",
        },
    )
    copy_generic_tools()
    dump(
        "REGENERATION_RECEIPT.json",
        {
            "schema": "stacks-r45-source-regeneration/v1",
            "status": "SOURCE_REPLAY_PASS_BUILD_PENDING",
            "pipeline": identity("pipeline_r45.py"),
            "source_validation": identity("source-validation.json"),
            "operation_spec": identity("operation-spec.json"),
            "stable_units": identity("stable-units.json"),
            "source_map": identity("source-map.jsonl"),
            "payload": identity(f"payload/{SOURCE}"),
            "no_final_manifest": True,
            "next_command": "powershell -File run-builds-with-mutex.ps1 -UpstreamRoot <PINNED_SOURCE_DIRECTORY> -WorkRoot1 <NEW_DIRECTORY> -WorkRoot2 <NEW_DIRECTORY> -PrivateRoot1 <PRIVATE_DIRECTORY> -PrivateRoot2 <PRIVATE_DIRECTORY>",
            "write_scope": "Only the leased R45 candidate; no TeX, admission, composition, or publication was performed.",
        },
    )

    forbidden_text = {str(WORKSPACE), str(WORKSPACE.parent)}
    forbidden_text |= {value.replace("\\", "\\\\") for value in forbidden_text}
    forbidden = [value.encode("utf-8") for value in forbidden_text]
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix in {".json", ".jsonl", ".md", ".csv", ".py", ".ps1"}:
            raw = path.read_bytes()
            assert not any(value in raw for value in forbidden), path
    print(json.dumps({"source_pass": True, "units": 19, "operations": 36, "payload_sha256": sha_bytes(payload), "build": "NOT_PERFORMED"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
