from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
R26 = ROOT.parent / "r26"
UNIT = "MC-STK-ERR-1216"
PRIOR_UNIT = "MC-STK-ERR-1183"
OFFICIAL_OLD = b"$a_kb_k$"
PRIOR = b"$(a_k)^N + b_k$"
NEW = b"$a_k((a_k)^N + b_k)$"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def structure(data: bytes) -> dict[str, int]:
    patterns = {
        "labels": rb"\\label\{[^{}]+\}",
        "refs": rb"\\(?:ref|eqref)\{[^{}]+\}",
        "cites": rb"\\cite(?:\[[^\]]*\])?\{[^{}]+\}",
        "begins": rb"\\begin\{[^{}]+\}",
        "ends": rb"\\end\{[^{}]+\}",
        "items": rb"\\item(?:\[[^\]]*\])?",
        "inputs": rb"\\input\{[^{}]+\}",
        "xymatrix": rb"\\xymatrix",
        "control_words": rb"\\[A-Za-z@]+",
    }
    return {name: len(re.findall(pattern, data)) for name, pattern in patterns.items()} | {
        "display_delimiters": data.count(b"$$"),
        "open_braces": data.count(b"{"),
        "close_braces": data.count(b"}"),
    }


def main() -> int:
    config = json.loads((ROOT / "candidate.config.json").read_text(encoding="utf-8"))
    operation_spec = json.loads((ROOT / "operation-spec.json").read_text(encoding="utf-8"))
    stable = json.loads((ROOT / "stable-units.json").read_text(encoding="utf-8"))
    source_map = jsonl(ROOT / "source-map.jsonl")
    decisions = jsonl(ROOT / "decisions.jsonl")
    official = (ROOT / "authority/source/smoothing.tex").read_bytes()
    base = (ROOT / "authority/composition-base/smoothing.tex").read_bytes()
    payload = (ROOT / "payload/smoothing.tex").read_bytes()
    projection = (ROOT / "composition-projection/smoothing.tex").read_bytes()

    if config["candidate_id"] != "stacks-errata-a04446e-r28":
        raise AssertionError("wrong candidate identity")
    if config["expected_unit_ids"] != [UNIT] or config["accepted"] != 1 or config["operation_count"] != 1:
        raise AssertionError("wrong sealed unit/count configuration")
    if len(stable["units"]) != 1 or stable["units"][0]["id"] != UNIT:
        raise AssertionError("stable-unit closure mismatch")
    if stable["units"][0].get("supersedes_unit_id") != PRIOR_UNIT:
        raise AssertionError("stable-unit supersession missing")
    if len(source_map) != 1 or source_map[0]["unit_id"] != UNIT or source_map[0].get("supersedes_unit_id") != PRIOR_UNIT:
        raise AssertionError("source-map supersession missing")
    if len({row["id"] for row in decisions}) != len(decisions) or len(decisions) != 3:
        raise AssertionError("decision ledger identity failure")
    if (ROOT / "rejections.jsonl").read_bytes() != b"":
        raise AssertionError("R28 has unexpected rejections")

    if len(official) != 134660 or sha_bytes(official) != "FD28CF874BB7DAD3C5C5FF03314D1C83701613A8A98730A99B9CA7A4BCFE6068":
        raise AssertionError("official authority mismatch")
    if len(base) != 134830 or sha_bytes(base) != "85251479BB7D35D73CD5691C194D33B3ADC1BF245BCC248643D969DBBA0E7928":
        raise AssertionError("public composition base mismatch")
    if official.count(OFFICIAL_OLD) != 1 or official.index(OFFICIAL_OLD) != 56549:
        raise AssertionError("official preimage mismatch")
    if base.count(PRIOR) != 1 or base.index(PRIOR) != 56560:
        raise AssertionError("cumulative preimage mismatch")

    expected_payload = official[:56549] + NEW + official[56549 + len(OFFICIAL_OLD):]
    expected_projection = base[:56560] + NEW + base[56560 + len(PRIOR):]
    if payload != expected_payload or len(payload) != 134672 or sha_bytes(payload) != "7C475ABEFC3CF2F3F2534F0CA69B8D8BB726BF88195CB50FE849DF99B7D0CD4A":
        raise AssertionError("standalone payload does not replay exactly")
    if projection != expected_projection or len(projection) != 134835 or sha_bytes(projection) != "85A37C95D5591632D11E7BE6775039638B6F5200B44729ABCEA1A644D9F5B056":
        raise AssertionError("cumulative composition projection does not replay exactly")

    operation = operation_spec["operations"][0]
    if (
        operation_spec["operation_count"] != 1
        or operation["stable_id"] != UNIT
        or operation["supersedes_operation_id"] != "MC-STK-ERR-1183-OP1"
        or operation["old_sha256"] != sha_bytes(OFFICIAL_OLD)
        or operation["replacement_sha256"] != sha_bytes(NEW)
        or operation["start_byte"] != 56549
        or operation["end_byte_exclusive"] != 56557
    ):
        raise AssertionError("operation specification mismatch")

    r26_manifest = R26 / "candidate.manifest.json"
    r26_map = R26 / "source-map.jsonl"
    if sha_file(r26_manifest) != "1A045F9452501725CAF45996FD19C633D594E0C3D57AA745780C3C06FB031085":
        raise AssertionError("R26 manifest changed")
    if sha_file(r26_map) != "46C29F2D0DFDC1081FFFDA61757DFCEB4E3036881A9D2D272B5ED9D67626B9BF":
        raise AssertionError("R26 source map changed")
    prior_row = next(row for row in jsonl(r26_map) if row["unit_id"] == PRIOR_UNIT)
    if prior_row["operations"][0]["replacement_text"].encode("utf-8") != PRIOR:
        raise AssertionError("R26 prior replacement changed")

    official_structure = structure(official)
    payload_structure = structure(payload)
    base_structure = structure(base)
    projection_structure = structure(projection)
    if official_structure != payload_structure:
        raise AssertionError("standalone TeX topology changed outside the inline replacement")
    if base_structure != projection_structure:
        raise AssertionError("cumulative TeX topology changed outside the inline replacement")
    if official_structure["open_braces"] != official_structure["close_braces"]:
        raise AssertionError("official braces are not balanced")
    if payload_structure["open_braces"] != payload_structure["close_braces"]:
        raise AssertionError("payload braces are not balanced")

    for name in ("R28_PREDECESSOR_BINDING.json", "R28_SMOOTHING_SUPERSESSION_SPEC.json", "INTAKE_VALIDATION.json"):
        if (ROOT / name).read_bytes() != (ROOT / "authority/canon" / name).read_bytes():
            raise AssertionError(f"canon evidence copy differs: {name}")
    proof = (ROOT / "R28_SMOOTHING_PROOF.md").read_text(encoding="utf-8")
    for required in ("counterexample", "M_d=0", "must not be copied wholesale"):
        if required not in proof:
            raise AssertionError(f"proof closure text missing: {required}")

    report = {
        "schema": "mathematics-commons-stacks-r28-source-validation/v1",
        "candidate_id": config["candidate_id"],
        "passed": True,
        "checks": {
            "composition_projection_replay": {
                "base_bytes": len(base),
                "base_sha256": sha_bytes(base),
                "output_bytes": len(projection),
                "output_sha256": sha_bytes(projection),
                "preimage_count": base.count(PRIOR),
            },
            "official_projection_replay": {
                "authority_bytes": len(official),
                "authority_sha256": sha_bytes(official),
                "output_bytes": len(payload),
                "output_sha256": sha_bytes(payload),
                "preimage_count": official.count(OFFICIAL_OLD),
            },
            "predecessor_binding": {
                "manifest_sha256": sha_file(r26_manifest),
                "source_map_sha256": sha_file(r26_map),
                "unit_id": PRIOR_UNIT,
            },
            "structure": {
                "official": official_structure,
                "payload": payload_structure,
                "composition_base": base_structure,
                "composition_projection": projection_structure,
            },
            "supersession": {"new_unit_id": UNIT, "prior_unit_id": PRIOR_UNIT, "passed": True},
        },
    }
    (ROOT / "source-validation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="",
    )
    print(json.dumps({"passed": True, "report_sha256": sha_file(ROOT / "source-validation.json")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
