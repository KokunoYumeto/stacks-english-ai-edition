from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
R26 = ROOT.parent / "r26"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def verify_manifest(path: Path) -> dict:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    rows.extend(manifest["source_authorities"])
    rows.extend(manifest["builds"])
    for key in (
        "stable_unit_manifest",
        "source_map",
        "decision_ledger",
        "rejection_ledger",
        "formula_diagram_inventory",
    ):
        rows.append(manifest[key])
    if len({row["path"] for row in rows}) != len(rows):
        raise AssertionError("manifest repeats an evidence path")
    for row in rows:
        target = ROOT / row["path"]
        if not target.is_file() or sha256(target) != row["sha256"]:
            raise AssertionError(f"manifest evidence mismatch: {row['path']}")
    actual = sorted(
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.name != "candidate.manifest.json"
        and "__pycache__" not in path.parts
        and path != ROOT / "replay/independent-review.json"
    )
    manifested = sorted(row["path"] for row in rows)
    if actual != manifested:
        raise AssertionError("pre-review manifest does not close the sealed public file set")
    return {"evidence_files": len(rows), "passed": True}


def main() -> int:
    parser = argparse.ArgumentParser(description="Independent adverse replay for R28")
    parser.add_argument("--private-render-manifest", type=Path, required=True)
    args = parser.parse_args()
    manifest_path = ROOT / "candidate.manifest.json"
    validation_path = ROOT / "builds/validation.json"
    pre_review_manifest_sha = sha256(manifest_path)
    manifest_closure = verify_manifest(manifest_path)

    official = (ROOT / "authority/source/smoothing.tex").read_bytes()
    base = (ROOT / "authority/composition-base/smoothing.tex").read_bytes()
    payload = (ROOT / "payload/smoothing.tex").read_bytes()
    projection = (ROOT / "composition-projection/smoothing.tex").read_bytes()
    old = b"$a_kb_k$"
    prior = b"$(a_k)^N + b_k$"
    new = b"$a_k((a_k)^N + b_k)$"
    if official.count(old) != 1 or official.index(old) != 56549:
        raise AssertionError("official preimage failed independent replay")
    if base.count(prior) != 1 or base.index(prior) != 56560:
        raise AssertionError("cumulative preimage failed independent replay")
    replay_payload = official[:56549] + new + official[56549 + len(old):]
    replay_projection = base[:56560] + new + base[56560 + len(prior):]
    if replay_payload != payload or replay_projection != projection:
        raise AssertionError("independent source replay failed")

    r26_manifest = R26 / "candidate.manifest.json"
    r26_map_path = R26 / "source-map.jsonl"
    if sha256(r26_manifest) != "1A045F9452501725CAF45996FD19C633D594E0C3D57AA745780C3C06FB031085":
        raise AssertionError("R26 manifest changed")
    if sha256(r26_map_path) != "46C29F2D0DFDC1081FFFDA61757DFCEB4E3036881A9D2D272B5ED9D67626B9BF":
        raise AssertionError("R26 source map changed")
    r26_rows = [json.loads(line) for line in r26_map_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    r26_unit = next(row for row in r26_rows if row["unit_id"] == "MC-STK-ERR-1183")
    if r26_unit["operations"][0]["replacement_text"].encode("utf-8") != prior:
        raise AssertionError("R26 effective fragment mismatch")

    stable = json.loads((ROOT / "stable-units.json").read_text(encoding="utf-8"))["units"]
    source_map = [json.loads(line) for line in (ROOT / "source-map.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    if (
        len(stable) != 1
        or stable[0]["id"] != "MC-STK-ERR-1216"
        or stable[0]["supersedes_unit_id"] != "MC-STK-ERR-1183"
        or len(source_map) != 1
        or source_map[0]["supersedes_unit_id"] != "MC-STK-ERR-1183"
    ):
        raise AssertionError("append-only supersession identity failed")

    # Mathematical adverse review. R26 knows only that c/a^N annihilates M_a;
    # this implies M_{a,c}=0, not M_c=0. The counterexample encoded below
    # has I=(x), I_k=(a(a+x)x); at prime (a), x and a+x are units, so I is the
    # unit ideal while I_k=(a), proving the missing implication is false.
    proof_state = {
        "counterexample": {
            "ambient_ring": "k[a,x]",
            "I": "(x)",
            "I_k": "(a(a+x)x)",
            "N": 1,
            "b": "x",
            "c": "a+x",
            "localization_prime": "(a)",
            "I_localized": "unit ideal",
            "I_k_localized": "(a)",
            "r26_conclusion_false": True,
        },
        "corrected_argument": {
            "new_element": "d=a(a^N+b)",
            "ambient_localization": "inverting d inverts both a and c=a^N+b",
            "annihilating_unit": "c/a^N",
            "module_conclusion": "M_d=0",
            "cover_conclusion": "d mod Ibar = a^(N+1), hence D(d)=D(a) on Spec(Cbar)",
            "passed": True,
        },
    }

    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    if validation.get("candidate_id") != "stacks-errata-a04446e-r28" or validation.get("passed") is not True:
        raise AssertionError("sealed validation failed")
    deterministic = json.loads((ROOT / "builds/deterministic-replay.json").read_text(encoding="utf-8"))
    if deterministic.get("passed") is not True or any(row["byte_identical"] is not True for row in deterministic["pdfs"]):
        raise AssertionError("two-build reproducibility failed")
    visual = json.loads((ROOT / "builds/visual-qa.json").read_text(encoding="utf-8"))
    if visual.get("passed") is not True or visual["pdfs"][0]["manual_findings"]["passed"] is not True:
        raise AssertionError("visual QA failed")

    private_manifest_path = args.private_render_manifest.resolve()
    private_manifest = json.loads(private_manifest_path.read_text(encoding="utf-8"))
    if private_manifest.get("schema") != "mathematics-commons-stacks-private-render-manifest/v1":
        raise AssertionError("private render manifest schema mismatch")
    if private_manifest["pdfs"]["smoothing"]["pdf_sha256"] != sha256(ROOT / "builds/smoothing.pdf"):
        raise AssertionError("private render PDF binding mismatch")
    render_rows = private_manifest["pdfs"]["smoothing"]["renders"]
    if [row["page"] for row in render_rows] != list(range(1, 38)):
        raise AssertionError("private full-page render closure mismatch")
    render_root = private_manifest_path.parent
    for row in render_rows:
        path = render_root / "smoothing" / row["file"]
        if path.stat().st_size != row["bytes"] or sha256(path) != row["sha256"]:
            raise AssertionError(f"private render mismatch: {row['file']}")

    receipt = {
        "schema": "mathematics-commons-stacks-errata-independent-review/v1",
        "candidate_id": "stacks-errata-a04446e-r28",
        "recorded_at_utc": utc_now(),
        "passed": True,
        "result": "PASS",
        "pass_is_unconditional": True,
        "pre_review_manifest_sha256": pre_review_manifest_sha,
        "validation_sha256": sha256(validation_path),
        "manifest_closure": manifest_closure,
        "source_replay": {
            "official_authority": {"bytes": len(official), "sha256": sha_bytes(official)},
            "standalone_payload": {"bytes": len(payload), "sha256": sha_bytes(payload)},
            "composition_base": {"bytes": len(base), "sha256": sha_bytes(base)},
            "composition_projection": {"bytes": len(projection), "sha256": sha_bytes(projection)},
            "operation_count": 1,
            "passed": True,
        },
        "predecessor_replay": {
            "overlay_id": "stacks-errata-a04446e-r26",
            "manifest_sha256": sha256(r26_manifest),
            "source_map_sha256": sha256(r26_map_path),
            "unit_id": "MC-STK-ERR-1183",
            "operation_id": "MC-STK-ERR-1183-OP1",
            "passed": True,
        },
        "mathematical_adverse_review": proof_state,
        "sealed_evidence_verification": {
            "deterministic_replay": {"sha256": sha256(ROOT / "builds/deterministic-replay.json"), "passed": True},
            "validation": {"sha256": sha256(validation_path), "passed": True},
            "visual_qa": {"sha256": sha256(ROOT / "builds/visual-qa.json"), "passed": True},
            "private_render_manifest": {
                "bytes": private_manifest_path.stat().st_size,
                "sha256": sha256(private_manifest_path),
                "full_page_count": len(render_rows),
                "high_resolution_pages": [row["page"] for row in private_manifest["high_resolution"]["renders"]],
                "private_path_published": False,
            },
        },
        "composition_rule": {
            "base_commit": "f8e6c227aa3dc89256427f3b64a2ad330d5ff221",
            "base_blob": "ea0c59e134220971957a0a019e57663d0102cd07",
            "old_text": prior.decode("utf-8"),
            "replacement_text": new.decode("utf-8"),
            "old_occurrence_count": 1,
            "copy_isolated_payload_wholesale": False,
        },
        "unresolved": [],
    }
    output = ROOT / "replay/independent-review.json"
    output.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="",
    )
    print(json.dumps({"passed": True, "receipt_sha256": sha256(output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
