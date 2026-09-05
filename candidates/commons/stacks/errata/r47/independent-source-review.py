"""Independent exact-byte replay of the already materialized R47 source stage."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
SOURCE = "more-groupoids.tex"
AUTH_SHA = "F2D59ED504EC35DDA72BF2906F579312EAC2593CE952B84688ACE59B3CF87199"
PAYLOAD_SHA = "039BA96AEA5ED3BA59A7CB0EECB5D8F7491CCF1C2FCEB49211BA7CECF1C0BDDF"
INTAKE_SHA = "E6C73AB66A0C1F182B727B38DA7B53876ED0321CAC8DD006B778A9E044CEE2F5"
EXPECTED_IDS = [f"MC-STK-ERR-{number}" for number in range(1523, 1545)]


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def evidence(relative: str) -> dict:
    path = ROOT / relative
    return {"path": relative, "bytes": path.stat().st_size, "sha256": sha(path)}


def json_lines(path: Path) -> list[dict]:
    return [json.loads(row) for row in path.read_text(encoding="utf-8").splitlines() if row]


def all_occurrences(data: bytes, needle: bytes) -> list[int]:
    result: list[int] = []
    cursor = 0
    while True:
        found = data.find(needle, cursor)
        if found < 0:
            return result
        result.append(found)
        cursor = found + len(needle)


def main() -> int:
    authority = (ROOT / f"authority/source/{SOURCE}").read_bytes()
    payload = (ROOT / f"payload/{SOURCE}").read_bytes()
    assert len(authority) == 121107 and sha_bytes(authority) == AUTH_SHA
    assert len(payload) == 121125 and sha_bytes(payload) == PAYLOAD_SHA

    lease = load(ROOT / "LEASE.json")
    assert lease["lease_id"] == "stacks-lease-000051-errata-r47"
    assert lease["status"] == "active" and lease["admission_status"] == "not_admitted"
    events = load(REPO / "registry/leases.json")["events"]
    matched = [row for row in events if row["lease_id"] == lease["lease_id"]]
    assert len(matched) == 1 and matched[0]["event"] == "issued" and matched[0]["state"] == "active"

    intake = load(ROOT / "authority/intake/STACKS_MORE_GROUPOIDS_INDEPENDENT_INTAKE_20260905_R1.json")
    assert intake["summary"]["accepted_semantic_units"] == 22
    assert intake["summary"]["accepted_producer_rows"] == 23
    assert intake["summary"]["accepted_operations"] == 27
    assert intake["summary"]["rejected"] == intake["summary"]["deferred"] == 0
    assert intake["summary"]["duplicates_against_R1_R46"] == 0
    adjudication_path = "authority/registrar/MORE_GROUPOIDS_R47_INDEPENDENT_ADJUDICATION_20260905.json"
    adjudication = load(ROOT / adjudication_path)
    assert adjudication["passed"] is True and len(adjudication["rows"]) == 22
    assert any(row["sha256"] == INTAKE_SHA and row["bytes"] == 35737 for row in adjudication["intake_originals"])

    spec = load(ROOT / "operation-spec.json")
    stable = load(ROOT / "stable-units.json")
    source_map = json_lines(ROOT / "source-map.jsonl")
    decisions = json_lines(ROOT / "decisions.jsonl")
    assert spec == load(ROOT / "operation-spec.input.json")
    assert stable == load(ROOT / "stable-units.input.json")
    assert source_map == json_lines(ROOT / "source-map.input.jsonl")
    assert decisions == json_lines(ROOT / "decisions.input.jsonl")
    assert not json_lines(ROOT / "rejections.jsonl") and not json_lines(ROOT / "rejections.input.jsonl")
    assert spec["operation_count"] == len(spec["operations"]) == 27
    assert stable["unit_count"] == len(stable["units"]) == 22
    assert [row["id"] for row in stable["units"]] == EXPECTED_IDS
    assert [row["unit_id"] for row in source_map] == EXPECTED_IDS
    assert [row["stable_id"] for row in decisions] == EXPECTED_IDS
    assert all(row["choice"] == "materialize_source_proposal_not_admission" for row in decisions)
    flattened = [producer_id for row in stable["units"] for producer_id in row["producer_ids"]]
    assert len(flattened) == len(set(flattened)) == 23

    operations = spec["operations"]
    assert len({row["operation_id"] for row in operations}) == 27
    assert len({row["producer_operation_id"] for row in operations}) == 27
    ordered = sorted(operations, key=lambda row: row["start_byte"])
    assert all(left["end_byte_exclusive"] <= right["start_byte"] for left, right in zip(ordered, ordered[1:]))
    first_locus = {row["id"]: min(op["start_byte"] for op in operations if op["stable_id"] == row["id"]) for row in stable["units"]}
    assert [first_locus[key] for key in EXPECTED_IDS] == sorted(first_locus.values())

    replay = authority
    unchanged_parts: list[bytes] = []
    cursor = 0
    for operation in ordered:
        old = operation["old_text"].encode("utf-8")
        replacement = operation["replacement_text"].encode("utf-8")
        start = operation["start_byte"]
        end = operation["end_byte_exclusive"]
        assert authority[start:end] == old
        assert len(old) == operation["old_bytes"] and sha_bytes(old) == operation["old_sha256"]
        assert len(replacement) == operation["replacement_bytes"] and sha_bytes(replacement) == operation["replacement_sha256"]
        found = all_occurrences(authority, old)
        assert len(found) == operation["file_occurrences"]
        actual_line = authority[:start].count(b"\n") + 1
        assert actual_line == operation["line"] == operation["source_start_line"]
        assert sum(authority[:value].count(b"\n") + 1 == actual_line for value in found) == 1
        unchanged_parts.append(authority[cursor:start])
        cursor = end
    unchanged_parts.append(authority[cursor:])
    for operation in reversed(ordered):
        replay = replay[:operation["start_byte"]] + operation["replacement_text"].encode("utf-8") + replay[operation["end_byte_exclusive"]:]
    assert replay == payload

    by_stable = {row["id"]: row for row in stable["units"]}
    by_map = {row["unit_id"]: row for row in source_map}
    for stable_id in EXPECTED_IDS:
        unit = by_stable[stable_id]
        mapped = by_map[stable_id]
        expected_ops = [row for row in operations if row["stable_id"] == stable_id]
        assert unit["operation_ids"] == [row["operation_id"] for row in expected_ops]
        assert mapped["operations"] == expected_ops
        assert mapped["authority_sha256"] == AUTH_SHA
        assert unit["producer_ids"] == mapped["producer_ids"]
        assert unit["class"] == mapped["class"]

    patterns = {
        "labels": rb"\\label\{[^}]*\}",
        "refs": rb"\\(?:ref|eqref)\{[^}]*\}",
        "environments": rb"\\(?:begin|end)\{[^}]*\}",
        "inputs": rb"\\input\{[^}]*\}",
        "cites": rb"\\cite(?:\[[^]]*\])?\{[^}]*\}",
    }
    structure = {}
    for key, pattern in patterns.items():
        before = re.findall(pattern, authority)
        after = re.findall(pattern, payload)
        assert before == after
        structure[key] = {"authority": len(before), "candidate": len(after), "count_equal": True, "ordered_equal": True, "declared_changed_positions": []}
    assert authority.count(b"$") == payload.count(b"$")
    structure["dollar_delimiters"] = {"authority": authority.count(b"$"), "candidate": payload.count(b"$"), "count_equal": True}

    prior_source = overlaps = preimage_hits = stable_collisions = 0
    target_intervals = [(row["start_byte"], row["end_byte_exclusive"]) for row in operations]
    target_preimages = {row["old_text"] for row in operations}
    for path in (REPO / "candidates").rglob("source-map.jsonl"):
        if ROOT in path.resolve().parents:
            continue
        for row in json_lines(path):
            stable_collisions += int(row.get("unit_id") in EXPECTED_IDS)
            for prior in row.get("operations", []):
                if prior.get("source") != SOURCE:
                    continue
                prior_source += 1
                preimage_hits += int(prior.get("old_text") in target_preimages)
                overlaps += sum(not (prior["end_byte_exclusive"] <= start or end <= prior["start_byte"]) for start, end in target_intervals)
    assert prior_source == overlaps == preimage_hits == stable_collisions == 0

    validation = load(ROOT / "source-validation.json")
    assert validation["passed"] is True
    assert validation["authority"]["sha256"] == AUTH_SHA
    assert validation["payload"]["sha256"] == PAYLOAD_SHA
    assert validation["unchanged_interval_sha256"] == sha_bytes(b"".join(unchanged_parts))
    assert validation["structure"] == structure

    result = {
        "schema": "stacks-r47-independent-source-validation/v1",
        "candidate_id": "stacks-errata-a04446e-r47",
        "status": "PASS_SOURCE_ONLY",
        "passed": True,
        "scope": "Independent read-only reconstruction of the R47 source stage before any build or admission.",
        "authority": evidence(f"authority/source/{SOURCE}"),
        "payload": evidence(f"payload/{SOURCE}"),
        "operation_spec": evidence("operation-spec.json"),
        "stable_units": evidence("stable-units.json"),
        "source_map": evidence("source-map.jsonl"),
        "decisions": evidence("decisions.jsonl"),
        "adjudication": evidence(adjudication_path),
        "source_validation": evidence("source-validation.json"),
        "replay": {
            "semantic_units": 22,
            "producer_rows": 23,
            "exact_operations": 27,
            "exact_preimages": 27,
            "nonoverlap": True,
            "payload_byte_exact": True,
            "unlisted_byte_changes": 0,
            "unchanged_interval_sha256": sha_bytes(b"".join(unchanged_parts)),
            "stable_ids_first_locus_ordered": True,
            "structure": structure,
        },
        "deduplication": {
            "registered_rounds_checked_through": 46,
            "prior_more_groupoids_operations": prior_source,
            "interval_overlaps": overlaps,
            "exact_preimage_hits": preimage_hits,
            "stable_id_collisions": stable_collisions,
        },
        "build": "NOT_PERFORMED",
        "admission": "NOT_PERFORMED",
        "composition": "NOT_PERFORMED",
    }
    output = ROOT / "replay/SOURCE_INDEPENDENT_VALIDATION.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")
    print(json.dumps({"passed": True, "units": 22, "producer_rows": 23, "operations": 27, "rejected": 0, "payload_sha256": PAYLOAD_SHA}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
