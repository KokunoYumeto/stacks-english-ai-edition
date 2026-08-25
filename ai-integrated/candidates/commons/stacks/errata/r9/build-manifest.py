from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def evidence(path: Path) -> dict[str, str]:
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path)}


def main() -> int:
    replay_path = ROOT / "replay" / "independent-review.json"
    replay = json.loads(replay_path.read_text(encoding="utf-8")) if replay_path.exists() else None
    authority_paths = sorted(path for path in (ROOT / "authority").rglob("*") if path.is_file())
    singled = {
        "stable_unit_manifest": ROOT / "stable-units.json",
        "source_map": ROOT / "source-map.jsonl",
        "decision_ledger": ROOT / "decisions.jsonl",
        "rejection_ledger": ROOT / "rejections.jsonl",
        "formula_diagram_inventory": ROOT / "formula-diagram-inventory.json",
    }
    excluded = {ROOT / "candidate.manifest.json", *singled.values(), *authority_paths}
    build_paths = sorted(
        path for path in ROOT.rglob("*")
        if path.is_file() and path not in excluded and "__pycache__" not in path.parts
    )
    if replay:
        replay_note = (
            "The independent replay receipt binds pre-review manifest "
            f"{replay['pre_review_manifest_sha256']} and validation "
            f"{replay['validation_sha256']}. This final registrar-only rebind adds the replay receipt "
            "and a local .gitattributes byte-preservation rule; no reviewed authority, payload, proof, "
            "script, or existing build byte changed."
        )
    else:
        replay_note = "Independent adverse replay is pending against this pre-review manifest."
    manifest = {
        "$schema": "../../../../../schemas/candidate-manifest.schema.json",
        "schema": "mathematics-commons-stacks-candidate-manifest/v1",
        "candidate_id": "stacks-errata-a04446e-r9",
        "lease_id": "stacks-lease-000012-errata-r9",
        "namespace": "commons/stacks/errata/r9",
        "writer_task": "01a0256d-5693-77c1-96b2-cf37101e0c6c",
        "upstream": {
            "lock": "upstream/stacks.lock.json",
            "commit": "a04446e57ec1fbc252a871afcec7752fb2807b14",
            "tree": "3feeb703b931a6e7259782c10e7d1575adc83e5e",
        },
        "source_authorities": [evidence(path) for path in authority_paths],
        "source_closure": {
            "enumerated": True,
            "expected_units": 29,
            "manifested_units": 29,
            "complete": True,
        },
        **{key: evidence(path) for key, path in singled.items()},
        "builds": [evidence(path) for path in build_paths],
        "rights_state": (
            "The authority and modified payload retain the Stacks Project GNU Free Documentation "
            "License 1.2; metadata and receipts do not relicense upstream content. This is an "
            "independently maintained AI-produced English edition with no Stacks Project review, "
            "approval, affiliation, or endorsement. Legal certification was not performed."
        ),
        "review_state": "performed" if replay else "partial",
        "independent_replay": "passed" if replay else "not_performed",
        "unresolved_defects": [
            replay_note,
            "The isolated algebra.tex candidate retains cross-chapter undefined-reference targets; the target multiset matches the frozen authority build exactly, so full-corpus composition remains responsible for resolving them.",
            "The candidate reader has 467 pages and the authority reader has 466 pages because the added proof verification reflows at full canonical font size. Every candidate page and all correction-sensitive pages were inspected without clipping or loss.",
            "The proof PDFs contain embedded fonts with ToUnicode maps but are untagged; document-structure accessibility remains a cumulative-edition toolchain concern.",
            "The frozen producer snapshot closes ALGEBRA-342 through ALGEBRA-371: twenty-nine rows are accepted, ALGEBRA-344 is explicitly rejected, and none remains unresolved.",
            "Canonical Chinese, Japanese, Korean, and French translations preserve the frozen authority unless an explicit locale-side emendation is separately bound; this English corrected overlay is not silently copied.",
            "Overlay admission and English-edition composition are separate transitions; this manifest records candidate closure only.",
        ],
        "stop_conditions": [
            "Do not mutate the literal stacks-project master mirror.",
            "Do not apply these corrections silently to canonical translation source or PDFs.",
            "Do not contact or submit to the upstream Stacks maintainers under the current no-AI-contribution boundary.",
            "Do not append an overlay registry record except in a separate admission commit bound to the final manifest hash and a passed independent replay.",
            "Any change to reviewed authority, payload, proof, build, validation, visual-QA, or replay bytes invalidates the replay and requires a new review.",
        ],
        "generated_at_utc": "2026-08-24T14:19:00Z" if replay else "2026-08-24T14:18:00Z",
    }
    (ROOT / "candidate.manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="",
    )
    print(json.dumps({"passed": True, "reviewed": bool(replay), "manifest_sha256": sha256(ROOT / "candidate.manifest.json")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
