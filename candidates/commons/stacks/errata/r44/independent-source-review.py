"""Independent exact-byte review of the already materialized R44 source stage."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
AUTH_SHA = "83BD632E693848D32B54ACC48EA7D89B0ED024C4B84499486687E31E92BFDCF0"
PAYLOAD_SHA = "31EF572D294E8C79AB31A1AD3A9C8662CE2ACA6E26CF41BD28B541CB2AFA19B7"
EXPECTED_IDS = [f"MC-STK-ERR-{number}" for number in range(1437, 1461)]
EXPECTED_PRODUCER_IDS = [
    "PERFECT-SRC-046", "PERFECT-SRC-047", "PERFECT-SRC-048", "PERFECT-SRC-049",
    "PERFECT-SRC-050", "PERFECT-SRC-051", "PERFECT-SRC-052", "PERFECT-SRC-054",
    "PERFECT-SRC-055", "PERFECT-SRC-056", "PERFECT-SRC-057", "PERFECT-SRC-058",
    "PERFECT-SRC-059", "PERFECT-SRC-060", "PERFECT-SRC-061", "PERFECT-SRC-064",
    "PERFECT-SRC-065", "PERFECT-SRC-066", "PERFECT-SRC-067", "PERFECT-SRC-068",
    "PERFECT-SRC-069", "PERFECT-SRC-070", "PERFECT-SRC-071", "PERFECT-SRC-072",
]
DEFERRED = {"PERFECT-SRC-053", "PERFECT-SRC-062", "PERFECT-SRC-063"}


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha_path(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def evidence(relative: str) -> dict:
    path = ROOT / relative
    return {"path": relative, "bytes": path.stat().st_size, "sha256": sha_path(path)}


def main() -> int:
    authority = (ROOT / "authority/source/perfect.tex").read_bytes()
    payload = (ROOT / "payload/perfect.tex").read_bytes()
    assert len(authority) == 417503 and sha_bytes(authority) == AUTH_SHA
    assert len(payload) == 417517 and sha_bytes(payload) == PAYLOAD_SHA

    spec = load(ROOT / "operation-spec.json")
    stable = load(ROOT / "stable-units.json")
    maps = [json.loads(line) for line in (ROOT / "source-map.jsonl").read_text(encoding="utf-8").splitlines() if line]
    decisions = [json.loads(line) for line in (ROOT / "decisions.jsonl").read_text(encoding="utf-8").splitlines() if line]
    adjudication = load(ROOT / "authority/registrar/PERFECT_R44_INDEPENDENT_ADJUDICATION_20260905.json")
    assert spec["authority_sha256"] == AUTH_SHA and spec["operation_count"] == 32
    assert stable["unit_count"] == 24
    assert [unit["id"] for unit in stable["units"]] == EXPECTED_IDS
    assert [unit["producer_id"] for unit in stable["units"]] == EXPECTED_PRODUCER_IDS
    assert [row["unit_id"] for row in maps] == EXPECTED_IDS
    assert [row["stable_id"] for row in decisions] == EXPECTED_IDS
    assert [row["stable_id"] for row in adjudication["rows"]] == EXPECTED_IDS
    assert adjudication["grouping"]["excluded_deferred_producer_ids"] == ["PERFECT-SRC-053", "PERFECT-SRC-062", "PERFECT-SRC-063"]

    operations = sorted(spec["operations"], key=lambda row: row["start_byte"])
    assert len(operations) == len({row["operation_id"] for row in operations}) == 32
    assert list(dict.fromkeys(row["stable_id"] for row in operations)) == EXPECTED_IDS
    assert not DEFERRED.intersection(row["producer_id"] for row in operations)
    for left, right in zip(operations, operations[1:]):
        assert left["end_byte_exclusive"] <= right["start_byte"]
    units_by_id = {unit["id"]: unit for unit in stable["units"]}
    maps_by_id = {source_map["unit_id"]: source_map for source_map in maps}
    assert len(units_by_id) == len(maps_by_id) == 24
    for operation in operations:
        unit = units_by_id[operation["stable_id"]]
        source_map = maps_by_id[operation["stable_id"]]
        old = operation["old_text"].encode("utf-8")
        replacement = operation["replacement_text"].encode("utf-8")
        start = operation["start_byte"]
        end = operation["end_byte_exclusive"]
        assert authority[start:end] == old
        assert authority.count(old) == operation["file_occurrences"]
        assert len(old) == operation["old_bytes"] and sha_bytes(old) == operation["old_sha256"]
        assert len(replacement) == operation["replacement_bytes"] and sha_bytes(replacement) == operation["replacement_sha256"]
        assert authority[:start].count(b"\n") + 1 == operation["source_start_line"] == operation["line"]
        assert operation["source_end_line"] == operation["source_start_line"] + old.count(b"\n")
        positions = []
        cursor = 0
        while True:
            position = authority.find(old, cursor)
            if position < 0:
                break
            positions.append(position)
            cursor = position + len(old)
        line_positions = [position for position in positions if authority[:position].count(b"\n") + 1 == operation["line"]]
        assert len(line_positions) == operation["declared_line_occurrences"] == 1
        assert operation["operation_id"] in unit["operation_ids"]
        assert any(mapped == operation for mapped in source_map["operations"])
        assert source_map["authority_sha256"] == AUTH_SHA
        assert source_map["producer_id"] == unit["producer_id"] == operation["producer_id"]
    for unit in stable["units"]:
        source_map = maps_by_id[unit["id"]]
        assert unit["operation_ids"] == [operation["operation_id"] for operation in source_map["operations"]]

    replay = authority
    for operation in reversed(operations):
        replay = replay[:operation["start_byte"]] + operation["replacement_text"].encode("utf-8") + replay[operation["end_byte_exclusive"]:]
    assert replay == payload

    for left, right in (
        ("operation-spec.json", "operation-spec.input.json"),
        ("stable-units.json", "stable-units.input.json"),
        ("source-map.jsonl", "source-map.input.jsonl"),
        ("decisions.jsonl", "decisions.input.jsonl"),
        ("rejections.jsonl", "rejections.input.jsonl"),
        ("candidate.config.json", "candidate.config.input.json"),
    ):
        assert (ROOT / left).read_bytes() == (ROOT / right).read_bytes(), (left, right)

    patterns = {
        "labels": rb"\\label\{[^}]*\}",
        "refs": rb"\\(?:ref|eqref)\{[^}]*\}",
        "environments": rb"\\(?:begin|end)\{[^}]*\}",
        "inputs": rb"\\input\{[^}]*\}",
        "cites": rb"\\cite(?:\[[^]]*\])?\{[^}]*\}",
    }
    structure = {}
    for name, pattern in patterns.items():
        before = re.findall(pattern, authority)
        after = re.findall(pattern, payload)
        assert before == after
        structure[name] = len(before)

    overlays = load(REPO / "registry/overlays.json")["registered_entries"]
    prior_ids = [stable_id for entry in overlays for stable_id in entry["stable_ids"]]
    assert not set(EXPECTED_IDS).intersection(prior_ids)
    producer_hits = perfect_operations = overlaps = 0
    checked_specs = checked_maps = 0
    target_intervals = [(row["start_byte"], row["end_byte_exclusive"]) for row in operations]
    for path in (REPO / "candidates").rglob("operation-spec*.json"):
        if ROOT in path.resolve().parents:
            continue
        checked_specs += 1
        raw = path.read_text(encoding="utf-8")
        producer_hits += sum(raw.count(producer_id) for producer_id in EXPECTED_PRODUCER_IDS)
        for prior in json.loads(raw).get("operations", []):
            if prior.get("source") != "perfect.tex":
                continue
            perfect_operations += 1
            overlaps += sum(not (prior["end_byte_exclusive"] <= start or end <= prior["start_byte"]) for start, end in target_intervals)
    for path in (REPO / "candidates").rglob("source-map*.jsonl"):
        if ROOT in path.resolve().parents:
            continue
        checked_maps += 1
        raw = path.read_text(encoding="utf-8")
        producer_hits += sum(raw.count(producer_id) for producer_id in EXPECTED_PRODUCER_IDS)
        for line in raw.splitlines():
            if not line:
                continue
            for prior in json.loads(line).get("operations", []):
                if prior.get("source") != "perfect.tex":
                    continue
                perfect_operations += 1
                overlaps += sum(not (prior["end_byte_exclusive"] <= start or end <= prior["start_byte"]) for start, end in target_intervals)
    assert producer_hits == perfect_operations == overlaps == 0

    for relative in (
        "authority/intake/STACKS_PERFECT_LATE_CHAPTER_INTAKE_20260905_R1.json",
        "authority/intake/STACKS_PERFECT_LATE_CHAPTER_INTAKE_20260905_R2.json",
        "authority/intake/STACKS_PERFECT_LATE_CHAPTER_INTAKE_20260905_R3.json",
        "authority/intake/STACKS_PERFECT_FROZEN_HARVEST_20260905.json",
    ):
        document = load(ROOT / relative)
        assert document
    assert load(ROOT / "authority/intake/STACKS_PERFECT_FROZEN_HARVEST_20260905.json")["status"] == "EXACT_FROZEN_PASS"

    observed = [
        evidence(relative)
        for relative in (
            "candidate.config.json", "candidate.config.input.json",
            "operation-spec.json", "operation-spec.input.json",
            "stable-units.json", "stable-units.input.json",
            "source-map.jsonl", "source-map.input.jsonl",
            "decisions.jsonl", "decisions.input.jsonl",
            "rejections.jsonl", "rejections.input.jsonl",
            "source-validation.json", "formula-diagram-inventory.json",
            "REGENERATION_RECEIPT.json",
            "authority/registrar/PERFECT_R44_INDEPENDENT_ADJUDICATION_20260905.json",
            "authority/intake/STACKS_PERFECT_LATE_CHAPTER_INTAKE_20260905_R1.json",
            "authority/intake/STACKS_PERFECT_LATE_CHAPTER_INTAKE_20260905_R2.json",
            "authority/intake/STACKS_PERFECT_LATE_CHAPTER_INTAKE_20260905_R3.json",
            "authority/intake/STACKS_PERFECT_FROZEN_HARVEST_20260905.json",
            "authority/source/perfect.tex", "payload/perfect.tex",
        )
    ]
    report = {
        "schema": "stacks-r44-independent-source-validation/v1",
        "reviewer": "independent_exact_byte_validator",
        "date": "2026-09-05",
        "status": "PASS_SOURCE_ONLY",
        "passed": True,
        "scope": "Independent source replay, identity, semantic grouping, structure, intake binding, and registry dedup validation only; no build, visual, admission, composition, or publication claim.",
        "authority": evidence("authority/source/perfect.tex"),
        "payload": evidence("payload/perfect.tex"),
        "checks": {
            "exact_authority_hash": True,
            "operations": 32,
            "unique_operation_ids": 32,
            "exact_byte_preimages_lengths_hashes_and_line_numbers": 32,
            "exact_replacement_lengths_hashes": 32,
            "nonoverlapping": True,
            "descending_replay_equals_payload_byte_for_byte": True,
            "stable_units": 24,
            "stable_ids": "MC-STK-ERR-1437..MC-STK-ERR-1460",
            "source_map_unit_operation_producer_identity_equality": True,
            "structure_counts_and_order_equal": structure,
            "prior_operation_specs_checked": checked_specs,
            "prior_source_maps_checked": checked_maps,
            "prior_perfect_operations_observed": perfect_operations,
            "prior_target_interval_overlaps": overlaps,
            "prior_producer_id_hits": producer_hits,
            "global_stable_id_collisions": 0,
            "input_output_stage_pairs_byte_equal": 6,
            "deferred_ids_absent_from_candidate": sorted(DEFERRED),
        },
        "classification": {
            "source_defect": sum(unit["class"] == "source_defect" for unit in stable["units"]),
            "editorial_or_notational_clarification": sum(unit["class"] != "source_defect" for unit in stable["units"]),
        },
        "observed_files": observed,
        "blockers": [],
        "build": "NOT_REVIEWED_BY_THIS_RECEIPT",
        "visual": "NOT_REVIEWED_BY_THIS_RECEIPT",
        "full_admission": "NOT_PERFORMED",
        "mutations": "Only this new review receipt; no source, registry, build, generated-source, Git, or publication mutation.",
    }
    output = ROOT / "replay/SOURCE_INDEPENDENT_VALIDATION.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")
    print(json.dumps({"passed": True, "units": 24, "operations": 32, "payload_sha256": PAYLOAD_SHA, "receipt_sha256": sha_path(output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
