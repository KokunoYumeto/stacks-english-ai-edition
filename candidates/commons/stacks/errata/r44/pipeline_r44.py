"""Materialize the R44 Perfect source candidate; never invokes TeX or admits it."""
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
SOURCE = "perfect.tex"
AUTH_SHA = "83BD632E693848D32B54ACC48EA7D89B0ED024C4B84499486687E31E92BFDCF0"
PAYLOAD_SHA = "31EF572D294E8C79AB31A1AD3A9C8662CE2ACA6E26CF41BD28B541CB2AFA19B7"
AUTH_BYTES = 417503
PAYLOAD_BYTES = 417517
COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
CANDIDATE_ID = "stacks-errata-a04446e-r44"
LEASE_ID = "stacks-lease-000048-errata-r44"
STAMP = "2026-09-05T14:40:34.6572234Z"
SOURCE_DATE_EPOCH = "1788619234"
PRELEASE_HEAD = "c69900fe75119d39025084ed520abc8bb24d507b"
PRELEASE_OVERLAYS_SHA = "05E01334F67E83AD9B226E119A60AEFDEABBB0B1436F4A56297A35010E50A554"
PRELEASE_LEASES_SHA = "BD24F0BBCAD50427B07C3C86F7923328EAD0A983E08D4F82FE9B6563F45C817C"

RECEIPTS = [
    (
        "STACKS_PERFECT_LATE_CHAPTER_INTAKE_20260905_R1.json",
        15942,
        "AB99E12E79DF738D480C1A41A8C1B7C07F431A303D5AC447315343871E8E7B99",
    ),
    (
        "STACKS_PERFECT_LATE_CHAPTER_INTAKE_20260905_R2.json",
        17579,
        "65BAD203F40809C4CBF80E783D70284291D90B3C5902933C62D8F6979ACF27B3",
    ),
    (
        "STACKS_PERFECT_LATE_CHAPTER_INTAKE_20260905_R3.json",
        24696,
        "5A178ECA6CE995A55A3FEB726692A6CD4E83F6D37B0BE699AB3553B5B885B2E6",
    ),
]
HARVEST = (
    "STACKS_PERFECT_FROZEN_HARVEST_20260905.json",
    6906,
    "39A8166112D5BB55E372A95EB6F81E90841D899916EF1764F5B3874EF5A4E8A9",
)
EXPECTED_PRODUCER_IDS = [
    "PERFECT-SRC-046", "PERFECT-SRC-047", "PERFECT-SRC-048", "PERFECT-SRC-049",
    "PERFECT-SRC-050", "PERFECT-SRC-051", "PERFECT-SRC-052", "PERFECT-SRC-054",
    "PERFECT-SRC-055", "PERFECT-SRC-056", "PERFECT-SRC-057", "PERFECT-SRC-058",
    "PERFECT-SRC-059", "PERFECT-SRC-060", "PERFECT-SRC-061", "PERFECT-SRC-064",
    "PERFECT-SRC-065", "PERFECT-SRC-066", "PERFECT-SRC-067", "PERFECT-SRC-068",
    "PERFECT-SRC-069", "PERFECT-SRC-070", "PERFECT-SRC-071", "PERFECT-SRC-072",
]
DEFERRED_PRODUCER_IDS = ["PERFECT-SRC-053", "PERFECT-SRC-062", "PERFECT-SRC-063"]
EXPECTED_STABLE_IDS = [f"MC-STK-ERR-{number}" for number in range(1437, 1461)]
EDITORIAL_CLASSES = {
    "duplicate_word", "number_agreement", "spelling", "duplicated_phrase",
    "duplicated_article", "unidiomatic_redundancy", "article_number_agreement",
    "duplicated_space", "missing_governing_verb",
}


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
    plain = {str(WORKSPACE), WORKSPACE.as_posix(), str(WORKSPACE.parent), WORKSPACE.parent.as_posix()}
    variants = plain | {value.replace("\\", "\\\\") for value in plain}
    for value in sorted(variants, key=len, reverse=True):
        text = text.replace(value, "<WORKSPACE>")
    text = re.sub(r"C:(?:\\|/)Users(?:\\|/)[^\\/\r\n\"']+", "<USER_ROOT>", text, flags=re.IGNORECASE)
    return text


def occurrences(haystack: bytes, needle: bytes) -> list[int]:
    found: list[int] = []
    cursor = 0
    while True:
        position = haystack.find(needle, cursor)
        if position < 0:
            return found
        found.append(position)
        cursor = position + len(needle)


def receipt_units(document: dict) -> list[dict]:
    return document.get("operations", document.get("semantic_units", []))


def rationale(unit: dict) -> str:
    if unit.get("independent_rationale"):
        return unit["independent_rationale"]
    derivation = unit.get("independent_derivation", [])
    partial = unit.get("rejected_partial_repairs", [])
    assert derivation
    return " ".join(derivation + ["Rejected partial repair: " + item for item in partial])


def exact_unit_operations(unit: dict) -> list[dict]:
    return unit.get("exact_operations", [unit])


def source_labels(unit: dict) -> list[str]:
    if "source_labels" in unit:
        return list(unit["source_labels"])
    label = unit.get("source_label")
    return [label] if label else []


def normalized_class(unit: dict) -> str:
    return "editorial_or_notational_clarification" if unit["class"] in EDITORIAL_CLASSES else "source_defect"


def scan_prior_registry(target_operations: list[dict]) -> dict:
    producer_ids = {operation["producer_id"] for operation in target_operations}
    exact_old = {operation["old_text"] for operation in target_operations}
    stable_ids = set(EXPECTED_STABLE_IDS)
    overlays = json.loads((REPO / "registry/overlays.json").read_text(encoding="utf-8"))["registered_entries"]
    prior_stable = [stable_id for entry in overlays for stable_id in entry["stable_ids"]]
    assert not stable_ids.intersection(prior_stable)
    producer_hits = 0
    source_operations = 0
    interval_overlaps = 0
    preimage_hits = 0
    spec_files = 0
    map_files = 0
    for path in (REPO / "candidates").rglob("operation-spec*.json"):
        if ROOT in path.resolve().parents:
            continue
        spec_files += 1
        document = json.loads(path.read_text(encoding="utf-8"))
        raw = path.read_text(encoding="utf-8")
        producer_hits += sum(raw.count(producer_id) for producer_id in producer_ids)
        for operation in document.get("operations", []):
            if operation.get("source") != SOURCE:
                continue
            source_operations += 1
            preimage_hits += int(operation.get("old_text") in exact_old)
            interval_overlaps += sum(
                not (
                    operation["end_byte_exclusive"] <= target["start_byte"]
                    or target["end_byte_exclusive"] <= operation["start_byte"]
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
            for operation in json.loads(line).get("operations", []):
                if operation.get("source") != SOURCE:
                    continue
                source_operations += 1
                preimage_hits += int(operation.get("old_text") in exact_old)
                interval_overlaps += sum(
                    not (
                        operation["end_byte_exclusive"] <= target["start_byte"]
                        or target["end_byte_exclusive"] <= operation["start_byte"]
                    )
                    for target in target_operations
                )
    assert producer_hits == source_operations == interval_overlaps == preimage_hits == 0
    return {
        "commit": PRELEASE_HEAD,
        "overlays_sha256": PRELEASE_OVERLAYS_SHA,
        "leases_sha256": PRELEASE_LEASES_SHA,
        "registered_rounds_checked_through": 43,
        "operation_spec_variants_checked": spec_files,
        "source_map_variants_checked": map_files,
        "matching_producer_ids": producer_hits,
        "prior_perfect_operations": source_operations,
        "prior_target_interval_overlaps": interval_overlaps,
        "prior_exact_preimage_hits": preimage_hits,
        "prior_stable_id_max": "MC-STK-ERR-1436",
    }


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
    assert matches[0]["candidate_path"] == "candidates/commons/stacks/errata/r44"
    assert (ROOT / ".gitattributes").read_bytes() == b"* -text\n"

    source = (UPSTREAM / SOURCE).read_bytes()
    assert len(source) == AUTH_BYTES and sha_bytes(source) == AUTH_SHA
    intake_documents: list[tuple[int, str, bytes, dict]] = []
    original_bindings = []
    for round_number, (name, size, digest) in enumerate(RECEIPTS, 1):
        path = INTAKE / name
        raw = path.read_bytes()
        assert len(raw) == size and sha_bytes(raw) == digest
        document = json.loads(raw.decode("utf-8-sig"))
        assert document["authority"]["sha256"] == AUTH_SHA
        intake_documents.append((round_number, name, raw, document))
        original_bindings.append({"logical_path": f"<WORKSPACE>/03_projects/language_management/cjk/00_lane_control/{name}", "bytes": size, "sha256": digest})
        write_bytes(f"authority/intake/{name}", sanitize_text(raw.decode("utf-8-sig")).encode("utf-8"))
    harvest_name, harvest_size, harvest_digest = HARVEST
    harvest_path = INTAKE / harvest_name
    harvest_raw = harvest_path.read_bytes()
    assert len(harvest_raw) == harvest_size and sha_bytes(harvest_raw) == harvest_digest
    harvest_document = json.loads(harvest_raw.decode("utf-8-sig"))
    assert harvest_document["status"] == "EXACT_FROZEN_PASS"
    assert harvest_document["authority"]["sha256"] == AUTH_SHA
    original_bindings.append({"logical_path": f"<WORKSPACE>/03_projects/language_management/cjk/00_lane_control/{harvest_name}", "bytes": harvest_size, "sha256": harvest_digest})
    write_bytes(f"authority/intake/{harvest_name}", sanitize_text(harvest_raw.decode("utf-8-sig")).encode("utf-8"))

    selected: list[tuple[int, dict]] = []
    deferred: list[str] = []
    for round_number, _, _, document in intake_documents:
        for unit in receipt_units(document):
            if "READY_FOR_FORMAL_ADMISSION" in unit.get("intake_disposition", ""):
                selected.append((round_number, unit))
            else:
                deferred.append(unit["producer_id"])
    assert [unit["producer_id"] for _, unit in selected] == EXPECTED_PRODUCER_IDS
    assert deferred == DEFERRED_PRODUCER_IDS
    assert len(selected) == len(EXPECTED_STABLE_IDS) == 24

    write_bytes("authority/source/perfect.tex", source)
    write_bytes("authority/COPYING", (UPSTREAM / "COPYING").read_bytes())
    dump("authority/upstream.lock.json", {"commit": COMMIT, "tree": TREE, "source": SOURCE, "bytes": len(source), "sha256": AUTH_SHA, "url": f"https://github.com/stacks/stacks-project/blob/{COMMIT}/{SOURCE}"})

    operations: list[dict] = []
    units: list[dict] = []
    maps: list[dict] = []
    decisions: list[dict] = []
    adjudication_rows: list[dict] = []
    for index, ((round_number, declared), stable_id) in enumerate(zip(selected, EXPECTED_STABLE_IDS), 1):
        classification = normalized_class(declared)
        group: list[dict] = []
        declared_operations = exact_unit_operations(declared)
        for operation_index, declared_operation in enumerate(declared_operations, 1):
            old_text = declared_operation["old_text"]
            replacement_text = declared_operation["replacement_text"]
            old = old_text.encode("utf-8")
            replacement = replacement_text.encode("utf-8")
            assert sha_bytes(old) == declared_operation["old_sha256"]
            assert sha_bytes(replacement) == declared_operation["replacement_sha256"]
            positions = occurrences(source, old)
            expected_start = int(declared_operation["start_byte_zero_based"])
            expected_end = int(declared_operation["end_byte_exclusive_zero_based"])
            assert source[expected_start:expected_end] == old
            assert len(positions) == int(declared_operation["global_preimage_count"])
            line = source[:expected_start].count(b"\n") + 1
            declared_line = declared_operation.get("source_line")
            if declared_line is not None:
                assert line == int(declared_line)
            line_positions = [position for position in positions if source[:position].count(b"\n") + 1 == line]
            assert len(line_positions) == int(declared_operation["line_preimage_count"]) == 1
            operation_id = f"{stable_id}-OP{operation_index}"
            operation = {
                "operation_id": operation_id,
                "stable_id": stable_id,
                "producer_id": declared["producer_id"],
                "producer_operation_id": f'{declared["producer_id"]}-OP{operation_index}',
                "origin": f"manager_intake_r{round_number}_and_independent_adjudication",
                "class": classification,
                "producer_class": declared["class"],
                "source": SOURCE,
                "line": line,
                "source_start_line": line,
                "source_end_line": line + old.count(b"\n"),
                "start_byte": expected_start,
                "end_byte_exclusive": expected_end,
                "old_text": old_text,
                "old_bytes": len(old),
                "old_sha256": sha_bytes(old),
                "replacement_text": replacement_text,
                "replacement_bytes": len(replacement),
                "replacement_sha256": sha_bytes(replacement),
                "declared_line_occurrences": len(line_positions),
                "file_occurrences": len(positions),
            }
            group.append(operation)
            operations.append(operation)
        lines = list(dict.fromkeys(operation["line"] for operation in group))
        locus = f"{SOURCE}:" + ",".join(str(value) for value in lines)
        unit = {
            "id": stable_id,
            "source": SOURCE,
            "producer_id": declared["producer_id"],
            "producer_ids": [declared["producer_id"]],
            "producer_aliases": [],
            "class": classification,
            "producer_class": declared["class"],
            "locus": locus,
            "operation_ids": [operation["operation_id"] for operation in group],
            "payload": "payload/perfect.tex",
            "status": "accepted_source_proposal_not_admitted",
        }
        proof = rationale(declared)
        units.append(unit)
        maps.append({
            "schema": "mathematics-commons-stacks-source-map/v2",
            "unit_id": stable_id,
            "source": SOURCE,
            "authority": "authority/source/perfect.tex",
            "authority_sha256": AUTH_SHA,
            "payload": "payload/perfect.tex",
            "producer_id": declared["producer_id"],
            "producer_ids": [declared["producer_id"]],
            "producer_aliases": [],
            "class": classification,
            "producer_class": declared["class"],
            "locus": locus,
            "proof": proof,
            "operations": group,
            "adverse_evidence": "Accepted as an editorial or notational source correction, not classified as a false theorem." if classification != "source_defect" else None,
        })
        decisions.append({
            "schema": "mathematics-commons-stacks-decision/v1",
            "id": f"R44-D{index:03d}",
            "timestamp_utc": STAMP,
            "choice": "materialize_source_proposal_not_admission",
            "stable_id": stable_id,
            "producer_id": declared["producer_id"],
            "rationale": proof,
            "supersedes": None,
        })
        adjudication_rows.append({
            "stable_id": stable_id,
            "producer_id": declared["producer_id"],
            "source_lines": lines,
            "source_labels": source_labels(declared),
            "producer_class": declared["class"],
            "classification": classification,
            "intake_round": round_number,
            "operation_count": len(group),
            "recommendation": "accept",
            "reason": proof,
            "exact_line_preimage_occurrences": [1] * len(group),
        })

    assert len(operations) == 32
    ordered = sorted(operations, key=lambda item: item["start_byte"])
    assert all(left["end_byte_exclusive"] <= right["start_byte"] for left, right in zip(ordered, ordered[1:]))
    assert len({item["operation_id"] for item in ordered}) == 32
    assert list(dict.fromkeys(item["stable_id"] for item in ordered)) == EXPECTED_STABLE_IDS
    payload = source
    for operation in reversed(ordered):
        payload = payload[:operation["start_byte"]] + operation["replacement_text"].encode("utf-8") + payload[operation["end_byte_exclusive"]:]
    assert len(payload) == PAYLOAD_BYTES and sha_bytes(payload) == PAYLOAD_SHA
    write_bytes("payload/perfect.tex", payload)

    dedup = scan_prior_registry(operations)
    spec = {"schema": "mathematics-commons-stacks-operation-spec/v1", "source": SOURCE, "authority_sha256": AUTH_SHA, "apply_order": "descending_start_byte", "operation_count": len(operations), "operations": operations}
    stable = {"schema": "mathematics-commons-stacks-stable-units/v1", "authority_commit": COMMIT, "unit_count": len(units), "units": units}
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
        assert before == after, name
        structure[name] = {"authority": len(before), "candidate": len(after), "ordered_equal": True}

    unchanged = bytearray()
    source_cursor = payload_cursor = 0
    for operation in ordered:
        span = source[source_cursor:operation["start_byte"]]
        assert payload[payload_cursor:payload_cursor + len(span)] == span
        unchanged.extend(span)
        payload_cursor += len(span)
        replacement = operation["replacement_text"].encode("utf-8")
        assert payload[payload_cursor:payload_cursor + len(replacement)] == replacement
        payload_cursor += len(replacement)
        source_cursor = operation["end_byte_exclusive"]
    assert payload[payload_cursor:] == source[source_cursor:]
    unchanged.extend(source[source_cursor:])

    adjudication = {
        "schema": "stacks-r44-perfect-independent-adjudication/v1",
        "date": "2026-09-05",
        "status": "PASS_ACCEPT_24_NON_DUPLICATIVE_UNITS_32_OPERATIONS",
        "passed": True,
        "authority": {"path": "authority/source/perfect.tex", "bytes": AUTH_BYTES, "sha256": AUTH_SHA},
        "intake_originals": original_bindings,
        "frozen_french_checkpoint": {"status": harvest_document["status"], "target_sha256": harvest_document["assembled_target"]["sha256"], "pdf_sha256": harvest_document["delivered_pdf"]["sha256"], "visual_status": harvest_document["visual_replay"]["status"], "build_fls_status": harvest_document["build_replay"]["status"]},
        "prelease_registry": dedup,
        "rows": adjudication_rows,
        "grouping": {
            "semantic_units": len(units),
            "exact_operations": len(operations),
            "authority_order": EXPECTED_STABLE_IDS,
            "multi_operation_units": {row["stable_id"]: row["operation_count"] for row in adjudication_rows if row["operation_count"] > 1},
            "excluded_deferred_producer_ids": DEFERRED_PRODUCER_IDS,
            "deferred_disposition": "Not assigned stable IDs, not present in source map, and not applied to payload.",
        },
        "classification": {
            "source_defect": sum(unit["class"] == "source_defect" for unit in units),
            "editorial_or_notational_clarification": sum(unit["class"] != "source_defect" for unit in units),
        },
        "replay": {"payload_bytes": len(payload), "payload_sha256": sha_bytes(payload), "physical_lines": payload.count(b"\n")},
        "mutations": "Only the leased R44 candidate is materialized; frozen authority, producer/French/CJK sources, generated source, upstream, and registry admission remain untouched.",
    }
    dump("authority/registrar/PERFECT_R44_INDEPENDENT_ADJUDICATION_20260905.json", adjudication)

    validation = {
        "schema": "stacks-r44-source-validation-v1",
        "passed": True,
        "scope": "Source-only exact replay, semantic-unit grouping, structural equality, and registry dedup validation; no build, render, admission, or composition claim.",
        "semantic_units": 24,
        "operations": 32,
        "line_preimages_exact": 32,
        "nonoverlapping": True,
        "unlisted_byte_changes": 0,
        "unchanged_interval_sha256": sha_bytes(bytes(unchanged)),
        "structure": structure,
        "authority": identity("authority/source/perfect.tex"),
        "payload": identity("payload/perfect.tex"),
        "adjudication": identity("authority/registrar/PERFECT_R44_INDEPENDENT_ADJUDICATION_20260905.json"),
        "deduplication": dedup,
        "excluded_deferred_producer_ids": DEFERRED_PRODUCER_IDS,
        "build": "NOT_PERFORMED",
        "visual_qa": "NOT_PERFORMED",
        "independent_candidate_replay": "NOT_PERFORMED",
    }
    dump("source-validation.json", validation)
    dump("formula-diagram-inventory.json", {
        "schema": "stacks-r44-formula-diagram-inventory-v1",
        "source": SOURCE,
        "structure": structure,
        "operation_bound_changes": True,
        "note": "All changes are exactly the 32 declared operations in 24 stable units; every unchanged interval and ordered structural token list is preserved.",
        "operations": [{"id": operation["operation_id"], "line": operation["line"], "class": operation["class"], "old": operation["old_text"], "new": operation["replacement_text"]} for operation in operations],
    })

    authority_evidence = [identity("authority/registrar/PERFECT_R44_INDEPENDENT_ADJUDICATION_20260905.json")]
    authority_evidence += [identity(f"authority/intake/{name}") for name, _, _ in RECEIPTS]
    authority_evidence.append(identity(f"authority/intake/{harvest_name}"))
    config = {
        "schema": "mathematics-commons-stacks-errata-candidate-config/v1",
        "candidate_id": CANDIDATE_ID,
        "namespace": "commons/stacks/errata/r44",
        "lease_id": LEASE_ID,
        "writer_task": lease["writer_task"],
        "authority_commit": COMMIT,
        "authority_tree": TREE,
        "source_date_epoch": SOURCE_DATE_EPOCH,
        "accepted": 24,
        "rejected": 0,
        "unresolved": 0,
        "excluded_deferred": 3,
        "operation_count": 32,
        "expected_unit_ids": EXPECTED_STABLE_IDS,
        "expected_producer_ids": EXPECTED_PRODUCER_IDS,
        "payload_expected_bytes": len(payload),
        "payload_expected_sha256": sha_bytes(payload),
        "stems": {"perfect": {"authority_bytes": len(source), "authority_sha256": AUTH_SHA, "payload_bytes": len(payload), "payload_sha256": sha_bytes(payload), "build_exceptions": {}}},
        "proof_closure": {
            "accepted": 24,
            "operations": 32,
            "producer_rows": 24,
            "source_defect": adjudication["classification"]["source_defect"],
            "editorial_or_notational_clarification": adjudication["classification"]["editorial_or_notational_clarification"],
            "rejected": 0,
            "unresolved": 0,
            "excluded_deferred": 3,
        },
        "build_render_admission_status": "NOT_PERFORMED",
        "independent_replay": "not_performed",
        "authority_evidence": authority_evidence,
    }
    dump("candidate.config.json", config)
    dump("candidate.config.input.json", config)
    dump("builds/PENDING.json", {
        "schema": "stacks-r44-build-ready-state-v1",
        "build": "NOT_PERFORMED",
        "deterministic_pdf_replay": "NOT_PERFORMED",
        "fls_dependency_closure": "NOT_PERFORMED",
        "render": "NOT_PERFORMED",
        "visual_inspection": "NOT_PERFORMED",
        "independent_candidate_replay": "NOT_PERFORMED",
        "admission": "NOT_PERFORMED",
        "reason": "Historical source-only preparation state; later additive receipts must preserve it.",
    })
    dump("REGENERATION_RECEIPT.json", {
        "schema": "stacks-r44-source-regeneration/v1",
        "status": "SOURCE_REPLAY_PASS_BUILD_PENDING",
        "pipeline": identity("pipeline_r44.py"),
        "source_validation": identity("source-validation.json"),
        "operation_spec": identity("operation-spec.json"),
        "stable_units": identity("stable-units.json"),
        "source_map": identity("source-map.jsonl"),
        "payload": identity("payload/perfect.tex"),
        "no_final_manifest": True,
        "next_command": "powershell -File run-builds-with-mutex.ps1 -UpstreamRoot <PINNED_SOURCE_DIRECTORY> -WorkRoot1 <NEW_DIRECTORY> -WorkRoot2 <NEW_DIRECTORY> -PrivateRoot1 <PRIVATE_DIRECTORY> -PrivateRoot2 <PRIVATE_DIRECTORY>",
        "write_scope": "Only the leased R44 candidate; no TeX, admission, composition, or publication was performed.",
    })

    forbidden_text = {str(WORKSPACE), str(WORKSPACE.parent)}
    forbidden_text |= {value.replace("\\", "\\\\") for value in forbidden_text}
    forbidden = [value.encode("utf-8") for value in forbidden_text]
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix in {".json", ".jsonl", ".md", ".csv", ".py", ".ps1"}:
            raw = path.read_bytes()
            assert not any(value in raw for value in forbidden), path
    print(json.dumps({"source_pass": True, "units": 24, "operations": 32, "excluded_deferred": DEFERRED_PRODUCER_IDS, "payload_sha256": sha_bytes(payload), "build": "NOT_PERFORMED"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
