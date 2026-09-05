"""Independent exact-byte review of the already materialized R42 source stage."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
AUTH_SHA = "49483B3BCB36427A607A8227F4EA67730FCDDF1EECCB8E992CA61915ACE3B31D"
PAYLOAD_SHA = "D5D48A9B8B22B18985B84529BD8B14483C6682B932912FAFEABEB9FCA07700A7"
EXPECTED_IDS = [f"MC-STK-ERR-{number}" for number in range(1419, 1430)]
EXPECTED_PRODUCER_IDS = [f"DESCENT-{number:03d}" for number in range(30, 41)]


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
    authority = (ROOT / "authority/source/descent.tex").read_bytes()
    payload = (ROOT / "payload/descent.tex").read_bytes()
    assert len(authority) == 353760 and sha_bytes(authority) == AUTH_SHA
    assert len(payload) == 353780 and sha_bytes(payload) == PAYLOAD_SHA

    spec = load(ROOT / "operation-spec.json")
    stable = load(ROOT / "stable-units.json")
    maps = [json.loads(line) for line in (ROOT / "source-map.jsonl").read_text(encoding="utf-8").splitlines() if line]
    decisions = [json.loads(line) for line in (ROOT / "decisions.jsonl").read_text(encoding="utf-8").splitlines() if line]
    adjudication = load(ROOT / "authority/registrar/DESCENT_R42_INDEPENDENT_ADJUDICATION_20260905.json")
    assert spec["authority_sha256"] == AUTH_SHA and spec["operation_count"] == 12
    assert stable["unit_count"] == 11
    assert [unit["id"] for unit in stable["units"]] == EXPECTED_IDS
    assert [unit["producer_id"] for unit in stable["units"]] == EXPECTED_PRODUCER_IDS
    assert [row["unit_id"] for row in maps] == EXPECTED_IDS
    assert [row["stable_id"] for row in decisions] == EXPECTED_IDS
    assert [row["stable_id"] for row in adjudication["rows"]] == EXPECTED_IDS

    operations = sorted(spec["operations"], key=lambda row: row["start_byte"])
    assert list(dict.fromkeys(row["stable_id"] for row in operations)) == EXPECTED_IDS
    assert len({row["operation_id"] for row in operations}) == 12
    for left, right in zip(operations, operations[1:]):
        assert left["end_byte_exclusive"] <= right["start_byte"]
    units_by_id = {unit["id"]: unit for unit in stable["units"]}
    maps_by_id = {source_map["unit_id"]: source_map for source_map in maps}
    assert len(units_by_id) == len(maps_by_id) == 11
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
        assert any(mapped["operation_id"] == operation["operation_id"] and mapped == operation for mapped in source_map["operations"])
        assert source_map["authority_sha256"] == AUTH_SHA
        assert source_map["producer_id"] == unit["producer_id"]
    for unit in stable["units"]:
        source_map = maps_by_id[unit["id"]]
        assert unit["operation_ids"] == [operation["operation_id"] for operation in source_map["operations"]]
        assert all(operation["stable_id"] == unit["id"] for operation in source_map["operations"])

    replay = authority
    for operation in reversed(operations):
        replay = (
            replay[: operation["start_byte"]]
            + operation["replacement_text"].encode("utf-8")
            + replay[operation["end_byte_exclusive"] :]
        )
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
    prior_descent_operations = 0
    prior_interval_overlaps = 0
    prior_preimage_hits = 0
    exact_old = {operation["old_text"] for operation in operations}
    checked_operation_specs = 0
    checked_source_maps = 0
    for path in (REPO / "candidates").rglob("operation-spec*.json"):
        if ROOT in path.resolve().parents:
            continue
        checked_operation_specs += 1
        document = load(path)
        text = path.read_text(encoding="utf-8")
        for operation in document.get("operations", []):
            if operation.get("source") == "descent.tex":
                prior_descent_operations += 1
                prior_interval_overlaps += sum(
                    not (
                        operation["end_byte_exclusive"] <= target["start_byte"]
                        or target["end_byte_exclusive"] <= operation["start_byte"]
                    )
                    for target in operations
                )
        prior_preimage_hits += sum(text.count(old) for old in exact_old)
    for path in (REPO / "candidates").rglob("source-map*.jsonl"):
        if ROOT in path.resolve().parents:
            continue
        checked_source_maps += 1
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            if not line:
                continue
            for operation in json.loads(line).get("operations", []):
                if operation.get("source") == "descent.tex":
                    prior_descent_operations += 1
                    prior_interval_overlaps += sum(
                        not (
                            operation["end_byte_exclusive"] <= target["start_byte"]
                            or target["end_byte_exclusive"] <= operation["start_byte"]
                        )
                        for target in operations
                    )
        prior_preimage_hits += sum(text.count(old) for old in exact_old)
    assert prior_descent_operations > 0
    assert prior_interval_overlaps == 0 and prior_preimage_hits == 0

    producer = (ROOT / "authority/producer/DESCENT_SOURCE_DEFECTS.md").read_text(encoding="utf-8")
    listed = [int(value) for value in re.findall(r"(?m)^([0-9]+)\.", producer)]
    assert all(number in listed for number in range(30, 41))
    assert all(number in listed for number in range(41, 48))
    assert b"descent.tex" not in (ROOT / "authority/producer/SOURCE_DEFECT_LEDGER.csv").read_bytes().lower()

    observed = [
        evidence(relative)
        for relative in (
            "candidate.config.json",
            "candidate.config.input.json",
            "operation-spec.json",
            "operation-spec.input.json",
            "stable-units.json",
            "stable-units.input.json",
            "source-map.jsonl",
            "source-map.input.jsonl",
            "decisions.jsonl",
            "decisions.input.jsonl",
            "rejections.jsonl",
            "rejections.input.jsonl",
            "source-validation.json",
            "formula-diagram-inventory.json",
            "REGENERATION_RECEIPT.json",
            "authority/registrar/DESCENT_R42_INDEPENDENT_ADJUDICATION_20260905.json",
            "authority/producer/DESCENT_SOURCE_DEFECTS.md",
            "authority/producer/SOURCE_DEFECT_LEDGER.csv",
            "authority/source/descent.tex",
            "payload/descent.tex",
        )
    ]
    report = {
        "schema": "stacks-r42-independent-source-validation/v1",
        "reviewer": "independent_exact_byte_validator",
        "date": "2026-09-05",
        "status": "PASS_SOURCE_ONLY",
        "passed": True,
        "scope": "Independent source replay, identity, structure, and local-registry dedup validation only; no build, visual, admission, composition, or publication claim.",
        "authority": evidence("authority/source/descent.tex"),
        "payload": evidence("payload/descent.tex"),
        "checks": {
            "exact_authority_hash": True,
            "operations": 12,
            "unique_operation_ids": 12,
            "exact_byte_preimages_lengths_hashes_and_line_numbers": 12,
            "exact_replacement_lengths_hashes": 12,
            "nonoverlapping": True,
            "descending_replay_equals_payload_byte_for_byte": True,
            "stable_units": 11,
            "stable_ids": "MC-STK-ERR-1419..MC-STK-ERR-1429",
            "source_map_unit_operation_producer_identity_equality": True,
            "structure_counts_and_order_equal": structure,
            "prior_operation_specs_checked": checked_operation_specs,
            "prior_source_maps_checked": checked_source_maps,
            "prior_descent_operations_observed": prior_descent_operations,
            "prior_target_interval_overlaps": prior_interval_overlaps,
            "prior_exact_preimage_hits": prior_preimage_hits,
            "global_stable_id_collisions": 0,
            "input_output_stage_pairs_byte_equal": 6,
        },
        "classification": {
            "source_defect": sum(unit["class"] == "source_defect" for unit in stable["units"]),
            "editorial_or_notational_clarification": sum(unit["class"] == "editorial_or_notational_clarification" for unit in stable["units"]),
        },
        "producer_scope": {
            "r42_rows": "DESCENT-030..040",
            "preserved_out_of_scope_rows": "DESCENT-041..047 reserved for a later append-only round",
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
    print(json.dumps({"passed": True, "units": 11, "operations": 12, "payload_sha256": PAYLOAD_SHA, "receipt_sha256": sha_path(output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
