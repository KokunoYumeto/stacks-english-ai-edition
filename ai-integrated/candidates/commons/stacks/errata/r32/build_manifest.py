from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STAMP = "2026-08-29T20:50:00Z"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def evidence(path: str) -> dict[str, str]:
    return {"path": path, "sha256": sha(ROOT / path)}


def dump(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")


def main() -> int:
    config = json.loads((ROOT / "candidate.config.json").read_text(encoding="utf-8"))
    review = json.loads((ROOT / "replay" / "independent-review.json").read_text(encoding="utf-8"))
    validation = json.loads((ROOT / "source-validation.json").read_text(encoding="utf-8"))
    assert review["passed"] is True and review["pass_is_unconditional"] is True
    assert validation["passed"] is True
    assert config["accepted"] == 103 and config["operation_count"] == 125

    receipt = {
        "schema": "mathematics-commons-stacks-errata-materialization-receipt/v1",
        "candidate_id": config["candidate_id"],
        "recorded_at_utc": STAMP,
        "result": "PASS",
        "passed": True,
        "scope": "materialization_of_prior_accepted_unmaterialized_units",
        "stable_units": {
            "count": 103,
            "ids": config["expected_unit_ids"],
            "historical_ranges": [
                "MC-STK-ERR-0338..MC-STK-ERR-0345",
                "MC-STK-ERR-0396",
                "MC-STK-ERR-0399..MC-STK-ERR-0492",
            ],
        },
        "operations": {
            "count": 125,
            "apply_order": "descending_start_byte_per_source",
            "operation_spec": evidence("operation-spec.json"),
        },
        "stems": config["stems"],
        "independent_review": evidence("replay/independent-review.json"),
        "source_validation": evidence("source-validation.json"),
        "stable_unit_manifest": evidence("stable-units.json"),
        "source_map": evidence("source-map.jsonl"),
        "generator": evidence("regenerate_r32.py"),
        "verifier": evidence("verify_r32.py"),
        "registry_pre_admission": review["registry_pre_admission"],
        "constraints": {
            "authority_bytes_mutated": False,
            "generated_source_composed": False,
            "generated_source_pushed": False,
            "registry_admission_recorded_here": False,
        },
        "excluded": [
            "Rejected ALGEBRA-007 is not present.",
            "No new semantic adjudication is claimed.",
            "No generated Stacks source branch was composed or pushed.",
        ],
    }
    dump(ROOT / "MATERIALIZATION_RECEIPT.json", receipt)

    authority_paths = [
        "authority/COPYING",
        "authority/upstream.lock.json",
        "authority/source/fields.tex",
        "authority/source/categories.tex",
        "authority/source/algebra.tex",
        "authority/producer/accepted-unmaterialized.csv",
        "authority/producer/FIELDS_SOURCE_EMENDATIONS.json",
        "authority/producer/CATEGORIES_SOURCE_EMENDATIONS.json",
    ]
    build_paths = [
        "candidate.config.json",
        "LEASE.json",
        "operation-spec.json",
        "payload/fields.tex",
        "payload/categories.tex",
        "payload/algebra.tex",
        "source-validation.json",
        "regenerate_r32.py",
        "verify_r32.py",
        "build_manifest.py",
        "check-manifest.py",
        "replay/independent-review.json",
        "MATERIALIZATION_RECEIPT.json",
    ]
    manifest = {
        "$schema": "../../../../../schemas/candidate-manifest.schema.json",
        "schema": "mathematics-commons-stacks-candidate-manifest/v1",
        "candidate_id": config["candidate_id"],
        "lease_id": config["lease_id"],
        "namespace": config["namespace"],
        "writer_task": config["writer_task"],
        "upstream": {
            "lock": "upstream/stacks.lock.json",
            "commit": config["authority_commit"],
            "tree": config["authority_tree"],
        },
        "source_authorities": [evidence(path) for path in authority_paths],
        "source_closure": {
            "enumerated": True,
            "expected_units": 103,
            "manifested_units": 103,
            "complete": True,
        },
        "stable_unit_manifest": evidence("stable-units.json"),
        "source_map": evidence("source-map.jsonl"),
        "decision_ledger": evidence("decisions.jsonl"),
        "rejection_ledger": evidence("rejections.jsonl"),
        "formula_diagram_inventory": evidence("formula-diagram-inventory.json"),
        "builds": [evidence(path) for path in build_paths],
        "rights_state": "The authority and modified payload retain the Stacks Project GNU Free Documentation License 1.2; metadata and receipts do not relicense upstream content. This is an independently maintained AI-produced English correction overlay with no Stacks Project review, approval, affiliation, or endorsement. Legal certification was not performed.",
        "review_state": "performed",
        "independent_replay": "passed",
        "unresolved_defects": [
            "R32 closes a registry materialization gap for 103 already-accepted historical stable IDs; it performs no new adjudication and preserves their nonconsecutive numbering.",
            "Cumulative English-source composition and affected-chapter build validation are intentionally outside this overlay transaction and remain assigned to the separate composer.",
            "Canonical translations preserve their pinned authority unless a locale-side emendation is separately bound; this corrected English overlay is not silently copied into them.",
        ],
        "stop_conditions": [
            "Do not mutate the literal stacks-project master mirror.",
            "Do not apply these corrections silently to canonical translation source or PDFs.",
            "Do not compose or push the generated Stacks source branch from this registry materialization lane.",
            "Any change to reviewed authority, stable units, operation specification, payload, or independent replay bytes invalidates this manifest and requires a fresh deterministic replay.",
        ],
        "generated_at_utc": STAMP,
    }
    dump(ROOT / "candidate.manifest.json", manifest)
    print(json.dumps({
        "candidate_id": config["candidate_id"],
        "manifest_bytes": (ROOT / "candidate.manifest.json").stat().st_size,
        "manifest_sha256": sha(ROOT / "candidate.manifest.json"),
        "materialization_receipt_sha256": sha(ROOT / "MATERIALIZATION_RECEIPT.json"),
        "passed": True,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
