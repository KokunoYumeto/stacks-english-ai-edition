"""Materialize the R46 Groupoids source candidate; never invokes TeX or admits it."""
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
PRODUCER_PACKET = (
    WORKSPACE
    / "03_projects/language_management/romance/03_working_translations/"
      "stacks_fr_20260821/p06/evidence/GROUPOIDS_SOURCE_DEFECT_PACKET.json"
)
TEMPLATE = REPO / "candidates/commons/stacks/errata/r45"
SOURCE = "groupoids.tex"
AUTH_SHA = "157CC1C792F41465B8249582FEE0F6DFF266AC4224F06B05E936C66C65DB043A"
AUTH_BYTES = 189166
PAYLOAD_SHA = "6ED98A884E9F4AD6C3EF6720AE538F1FEFEED24E09E60111B1F9D825CF1A7C04"
PAYLOAD_BYTES = 189152
COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
CANDIDATE_ID = "stacks-errata-a04446e-r46"
LEASE_ID = "stacks-lease-000050-errata-r46"
STAMP = "2026-09-05T17:52:38.3487552Z"
SOURCE_DATE_EPOCH = "1788630758"
PRELEASE_HEAD = "34d2d62ca3d99f3a99ea5b59ad2e2a75bd813aee"
PRELEASE_OVERLAYS_SHA = "382D67696118D59BC601B7360EC9DC11DD883C4FA445357818CE89BA6564F70D"
INTAKE_NAME = "STACKS_GROUPOIDS_INDEPENDENT_INTAKE_20260905_R1.json"
INTAKE_BYTES = 60278
INTAKE_SHA = "83000418E293CE4C9D841C7F40AC8114F716BDF506F9A573227060075EF29243"
PACKET_NAME = "GROUPOIDS_SOURCE_DEFECT_PACKET.json"
PACKET_BYTES = 63431
PACKET_SHA = "C16B9AC06CE172FA71EB50E99379D8DF18B8A4F459D75F82A2E5AE201332E34B"
EXPECTED_STABLE_IDS = [f"MC-STK-ERR-{number}" for number in range(1480, 1523)]
EDITORIAL_CLASSES = {
    "editorial_reference_placeholder",
    "editorial_reference_placeholders",
    "editorial_residue",
}
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
    assert prior_max == 1479
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
        "registered_errata_rounds_checked_through": 45,
        "operation_spec_variants_checked": spec_files,
        "source_map_variants_checked": map_files,
        "matching_producer_ids": producer_hits,
        "prior_groupoids_operations": source_operations,
        "prior_target_interval_overlaps": interval_overlaps,
        "prior_exact_preimage_hits": preimage_hits,
        "prior_stable_id_max": f"MC-STK-ERR-{prior_max:04d}",
    }


def copy_generic_tools() -> None:
    for name in GENERIC_TOOLS:
        raw = (TEMPLATE / name).read_bytes()
        raw = raw.replace(b"stacks-errata-a04446e-r45", b"stacks-errata-a04446e-r46")
        raw = raw.replace(b"stacks-r45", b"stacks-r46")
        raw = raw.replace(b".r45-build-work.json", b".r46-build-work.json")
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
    assert matches[0]["candidate_path"] == "candidates/commons/stacks/errata/r46"
    assert (ROOT / ".gitattributes").read_bytes() == b"* -text\n"

    source = (UPSTREAM / SOURCE).read_bytes()
    assert len(source) == AUTH_BYTES and sha_bytes(source) == AUTH_SHA
    assert source.count(b"\r") == 0 and source.count(b"\n") == 5124
    intake_path = INTAKE / INTAKE_NAME
    intake_raw = intake_path.read_bytes()
    assert len(intake_raw) == INTAKE_BYTES and sha_bytes(intake_raw) == INTAKE_SHA
    intake = json.loads(intake_raw.decode("utf-8-sig"))
    assert intake["status"] == "independent_preflight_complete_not_registered_not_published"
    assert intake["summary"] == {
        "accepted": 43,
        "deferred": 0,
        "rejected": 4,
        "accepted_operations": 46,
        "stable_ids_allocated": 0,
        "duplicates_against_R1_R45": 0,
        "rejected_producer_ids": [
            "FR-GROUPOIDS-005",
            "FR-GROUPOIDS-007",
            "FR-GROUPOIDS-009",
            "FR-GROUPOIDS-015",
        ],
    }
    packet_raw = PRODUCER_PACKET.read_bytes()
    assert len(packet_raw) == PACKET_BYTES and sha_bytes(packet_raw) == PACKET_SHA
    packet = json.loads(packet_raw.decode("utf-8-sig"))
    assert packet["authority"]["sha256"] == AUTH_SHA and len(packet["units"]) == 47

    write_bytes(f"authority/source/{SOURCE}", source)
    write_bytes("authority/COPYING", (UPSTREAM / "COPYING").read_bytes())
    write_bytes(f"authority/intake/{INTAKE_NAME}", sanitize_text(intake_raw.decode("utf-8-sig")).encode("utf-8"))
    write_bytes(f"authority/intake/{PACKET_NAME}", sanitize_text(packet_raw.decode("utf-8-sig")).encode("utf-8"))
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

    selected = sorted(
        (item for item in intake["candidates"] if item["decision"] == "accepted"),
        key=lambda item: min(op["start_byte"] for op in item["operations"]),
    )
    rejected = [item for item in intake["candidates"] if item["decision"] == "rejected"]
    assert len(selected) == len(EXPECTED_STABLE_IDS) == 43
    assert len(rejected) == 4
    operations: list[dict] = []
    units: list[dict] = []
    maps: list[dict] = []
    decisions: list[dict] = []
    adjudication_rows: list[dict] = []
    for index, (declared, stable_id) in enumerate(zip(selected, EXPECTED_STABLE_IDS), 1):
        producer_id = declared["producer_id"]
        producer_alias = f"GRP-{declared['ordinal']:03d}"
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
                "origin": "manager_groupoids_independent_intake_r1",
                "class": classification,
                "producer_class": declared["class"],
                "source": SOURCE,
                "line": line,
                "source_start_line": int(declared_operation["source_start_line"]),
                "source_end_line": int(declared_operation["source_end_line"]),
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
            assert operation["source_start_line"] == line
            assert operation["source_end_line"] in {
                line + old.count(b"\n"),
                line + old.count(b"\n") - int(old.endswith(b"\n")),
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
            "producer_aliases": [producer_alias],
            "class": classification,
            "producer_class": declared["class"],
            "locus": locus,
            "logical_location": f"{producer_id} at {locus}",
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
                "producer_aliases": [producer_alias],
                "class": classification,
                "producer_class": declared["class"],
                "locus": locus,
                "logical_location": f"{producer_id} at {locus}",
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
                "id": f"R46-D{index:03d}",
                "timestamp_utc": STAMP,
                "choice": "materialize_source_proposal_not_admission",
                "stable_id": stable_id,
                "producer_id": producer_id,
                "producer_aliases": [producer_alias],
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
                "logical_location": f"{producer_id} at {locus}",
                "producer_class": declared["class"],
                "classification": classification,
                "operation_count": len(group),
                "recommendation": "accept",
                "reason": declared["rationale"],
                "exact_line_preimage_occurrences": [1] * len(group),
            }
        )

    assert len(operations) == 46
    ordered = sorted(operations, key=lambda item: item["start_byte"])
    assert all(left["end_byte_exclusive"] <= right["start_byte"] for left, right in zip(ordered, ordered[1:]))
    assert len({item["operation_id"] for item in ordered}) == 46
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
    rejection_rows = []
    for rejection_index, declared in enumerate(rejected, len(decisions) + 1):
        rejection_rows.append(
            {
                "schema": "mathematics-commons-stacks-rejection/v1",
                "producer_id": declared["producer_id"],
                "producer_aliases": [f"GRP-{declared['ordinal']:03d}"],
                "source": SOURCE,
                "class": declared["class"],
                "status": "rejected_not_a_reportable_source_erratum",
                "rationale": declared["rationale"],
                "stable_id": None,
            }
        )
        decisions.append(
            {
                "schema": "mathematics-commons-stacks-decision/v1",
                "id": f"R46-D{rejection_index:03d}",
                "timestamp_utc": STAMP,
                "choice": "reject_producer_proposal",
                "stable_id": None,
                "producer_id": declared["producer_id"],
                "producer_aliases": [f"GRP-{declared['ordinal']:03d}"],
                "rationale": declared["rationale"],
                "supersedes": None,
            }
        )
    assert len(decisions) == 47 and len(rejection_rows) == 4
    for name, value in (("operation-spec", spec), ("stable-units", stable)):
        dump(name + ".json", value)
        dump(name + ".input.json", value)
    for name, rows in (("source-map", maps), ("decisions", decisions), ("rejections", rejection_rows)):
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
        {"logical_path": f"<WORKSPACE>/03_projects/language_management/romance/03_working_translations/stacks_fr_20260821/p06/evidence/{PACKET_NAME}", "bytes": PACKET_BYTES, "sha256": PACKET_SHA},
    ]
    adjudication_path = "authority/registrar/GROUPOIDS_R46_INDEPENDENT_ADJUDICATION_20260905.json"
    dump(
        adjudication_path,
        {
            "schema": "stacks-r46-groupoids-independent-adjudication/v1",
            "date": "2026-09-05",
            "status": "PASS_ACCEPT_43_NON_DUPLICATIVE_UNITS_46_OPERATIONS_REJECT_4",
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
                "rejected": len(rejection_rows),
                "rejected_producer_ids": [row["producer_id"] for row in rejection_rows],
            },
            "classification": {
                "source_defect": sum(unit["class"] == "source_defect" for unit in units),
                "editorial_or_notational_clarification": sum(unit["class"] != "source_defect" for unit in units),
            },
            "replay": {"payload_bytes": len(payload), "payload_sha256": sha_bytes(payload), "physical_lines": payload.count(b"\n")},
            "mutations": "Only the leased R46 candidate is materialized; frozen authority, producer/French/CJK sources, generated source, upstream, and registry admission remain untouched.",
        },
    )
    validation = {
        "schema": "stacks-r46-source-validation-v1",
        "passed": True,
        "scope": "Source-only exact replay, semantic-unit grouping, structural token accounting, and registry dedup validation; no build, render, admission, composition, or publication claim.",
        "semantic_units": 43,
        "operations": 46,
        "line_preimages_exact": 46,
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
            "schema": "stacks-r46-formula-diagram-inventory-v1",
            "source": SOURCE,
            "structure": structure,
            "operation_bound_changes": True,
            "note": "All changes are exactly the 46 declared operations in 43 stable units; every unchanged byte interval is preserved. The ten added dollar delimiters are operation-bound clarifications of previously malformed inline mathematics.",
            "operations": [
                {"id": operation["operation_id"], "line": operation["line"], "class": operation["class"], "old": operation["old_text"], "new": operation["replacement_text"]}
                for operation in operations
            ],
        },
    )

    authority_evidence = [
        identity(adjudication_path),
        identity(f"authority/intake/{INTAKE_NAME}"),
        identity(f"authority/intake/{PACKET_NAME}"),
    ]
    config = {
        "schema": "mathematics-commons-stacks-errata-candidate-config/v1",
        "candidate_id": CANDIDATE_ID,
        "namespace": "commons/stacks/errata/r46",
        "lease_id": LEASE_ID,
        "writer_task": lease["writer_task"],
        "authority_commit": COMMIT,
        "authority_tree": TREE,
        "source_date_epoch": SOURCE_DATE_EPOCH,
        "accepted": 43,
        "rejected": 4,
        "unresolved": 0,
        "excluded_deferred": 0,
        "operation_count": 46,
        "expected_unit_ids": EXPECTED_STABLE_IDS,
        "expected_producer_ids": [unit["producer_id"] for unit in units],
        "payload_expected_bytes": len(payload),
        "payload_expected_sha256": sha_bytes(payload),
        "stems": {
            "groupoids": {
                "authority_bytes": len(source),
                "authority_sha256": AUTH_SHA,
                "payload_bytes": len(payload),
                "payload_sha256": sha_bytes(payload),
                "build_exceptions": {
                    "candidate_undefined_reference_target_deltas": {}
                },
            }
        },
        "proof_closure": {
            "accepted": 43,
            "operations": 46,
            "producer_rows": 47,
            "source_defect": sum(unit["class"] == "source_defect" for unit in units),
            "editorial_or_notational_clarification": sum(unit["class"] != "source_defect" for unit in units),
            "rejected": 4,
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
            "schema": "stacks-r46-build-ready-state-v1",
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
            "schema": "stacks-r46-source-regeneration/v1",
            "status": "SOURCE_REPLAY_PASS_BUILD_PENDING",
            "pipeline": identity("pipeline_r46.py"),
            "source_validation": identity("source-validation.json"),
            "operation_spec": identity("operation-spec.json"),
            "stable_units": identity("stable-units.json"),
            "source_map": identity("source-map.jsonl"),
            "payload": identity(f"payload/{SOURCE}"),
            "no_final_manifest": True,
            "next_command": "powershell -File run-builds-with-mutex.ps1 -UpstreamRoot <PINNED_SOURCE_DIRECTORY> -WorkRoot1 <NEW_DIRECTORY> -WorkRoot2 <NEW_DIRECTORY> -PrivateRoot1 <PRIVATE_DIRECTORY> -PrivateRoot2 <PRIVATE_DIRECTORY>",
            "write_scope": "Only the leased R46 candidate; no TeX, admission, composition, or publication was performed.",
        },
    )

    forbidden_text = {str(WORKSPACE), str(WORKSPACE.parent)}
    forbidden_text |= {value.replace("\\", "\\\\") for value in forbidden_text}
    forbidden = [value.encode("utf-8") for value in forbidden_text]
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix in {".json", ".jsonl", ".md", ".csv", ".py", ".ps1"}:
            raw = path.read_bytes()
            assert not any(value in raw for value in forbidden), path
    print(json.dumps({"source_pass": True, "units": 43, "operations": 46, "rejected": 4, "payload_sha256": sha_bytes(payload), "build": "NOT_PERFORMED"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
