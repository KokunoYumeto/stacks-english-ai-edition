#!/usr/bin/env python3
"""Map all R34--R38 byte edits and the proved historical no-op to fresh SyncTeX.

This is a deterministic mapping check, not visual QA. It never invokes TeX,
renders a PDF, edits source, or creates an inspection ledger. The separate
instrumentation receipt must establish that each SyncTeX sidecar was generated
after the fixed-point build without changing its PDF or fixed-point artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from compose_overlay_projection import (
    OFFICIAL_BASELINE,
    apply_operations,
    collect_projection,
    load_semantic_dispositions,
    rebase_operations,
    verify_semantic_disposition_consumption,
)


ROOT = Path(__file__).resolve().parents[1]
STEMS = ("cohomology", "sites-cohomology", "more-algebra")
EXPECTED_APPLIED = {"cohomology": 3, "sites-cohomology": 42, "more-algebra": 31}
NOOP_ID = "MC-STK-ERR-1296-OP1"
COMPOSITION_BASE = "72d10f3135c6007a38fa20a1aee4273fc4cb5693"
COMPOSITION_SOURCE = "1242d514b71e60b4fe11b4c867f7de660f9a3b77"
INSTRUMENTATION_SCHEMA = "unofficial-ai-integrated-stacks-synctex-instrumentation/v1"
ENVIRONMENT = {
    "SOURCE_DATE_EPOCH": "1785270512",
    "FORCE_SOURCE_DATE": "1",
    "TZ": "UTC",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def identity(path: Path) -> dict[str, object]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            size += len(chunk)
            digest.update(chunk)
    return {"bytes": size, "sha256": digest.hexdigest().upper()}


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return value


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def relative_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError:
        return str(resolved)


def git(*arguments: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *arguments], check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="strict",
    ).stdout.strip()


def git_blob(revision: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "blob", f"{revision}:{path}"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout


def require_identity(value: object, expected: dict, label: str) -> None:
    if not isinstance(value, dict) or any(value.get(key) != expected[key] for key in ("bytes", "sha256")):
        raise ValueError(f"identity mismatch: {label}")


def load_build(path: Path) -> tuple[dict, dict[str, dict]]:
    build = load_json(path)
    if build.get("schema") != "unofficial-ai-integrated-stacks-fixed-point-build/v1" or build.get("status") != "PASS":
        raise ValueError("a successful fixed-point build receipt is required")
    source = build.get("source")
    if not isinstance(source, dict) or not isinstance(source.get("commit"), str):
        raise ValueError("build receipt lacks a source commit")
    commit = source["commit"]
    if git("rev-parse", f"{commit}^{{commit}}") != commit or source.get("tree") != git("rev-parse", f"{commit}^{{tree}}"):
        raise ValueError("build source commit/tree binding mismatch")
    composition = build.get("composition", {})
    if (composition.get("composition_base_commit") != COMPOSITION_BASE
            or composition.get("composition_source_commit") != COMPOSITION_SOURCE
            or set(composition.get("affected_source_stems", [])) != set(STEMS)):
        raise ValueError("build does not describe the fixed R34--R38 composition")
    sweep = build.get("build", {}).get("global_fixed_point_sweep")
    if not isinstance(sweep, int) or isinstance(sweep, bool) or sweep < 1:
        raise ValueError("build lacks a successful global fixed-point sweep")
    artifacts: dict[str, dict] = {}
    for row in build.get("artifacts", []):
        if not isinstance(row, dict) or not isinstance(row.get("stem"), str) or row["stem"] in artifacts:
            raise ValueError("build artifact inventory is malformed or duplicated")
        artifacts[row["stem"]] = row
    for stem in STEMS:
        row = artifacts.get(stem, {})
        if (not isinstance(row.get("pages"), int) or isinstance(row.get("pages"), bool)
                or row["pages"] < 1 or not isinstance(row.get("bytes"), int)
                or not re.fullmatch(r"[0-9A-F]{64}", str(row.get("sha256", "")))):
            raise ValueError(f"invalid build artifact: {stem}")
    return build, artifacts


def frozen_input(path: Path, revision: str) -> dict:
    name = path.relative_to(ROOT).as_posix()
    live = path.read_bytes()
    if live != git_blob(revision, name):
        raise ValueError(f"mapping input differs from frozen build commit: {name}")
    return {"path": name, "bytes": len(live), "sha256": sha256(live)}


def check_instrumentation(path: Path, build_path: Path, build: dict,
                          artifacts: dict[str, dict], synctex_root: Path) -> dict:
    """Require run evidence; an old sidecar's mere existence is insufficient.

    Each artifact row must capture sidecar_absent_before=true and its generated
    sidecar's modification time inside the instrumented run interval. All
    timestamps use the same filesystem/clock domain. The instrumentation owner
    captures these facts; this mapper verifies every resulting byte hash.
    """
    receipt = load_json(path)
    if receipt.get("schema") != INSTRUMENTATION_SCHEMA or receipt.get("status") != "PASS" or receipt.get("source") != build["source"]:
        raise ValueError("SyncTeX instrumentation receipt is missing or not source-bound")
    binding = {"path": relative_path(build_path), **identity(build_path)}
    if receipt.get("build_receipt") != binding or receipt.get("environment") != ENVIRONMENT:
        raise ValueError("SyncTeX instrumentation build/environment binding mismatch")
    rows = receipt.get("artifacts")
    if not isinstance(rows, list) or len(rows) != len(STEMS):
        raise ValueError("SyncTeX instrumentation must contain exactly three artifacts")
    by_stem = {row.get("stem"): row for row in rows if isinstance(row, dict)}
    if set(by_stem) != set(STEMS):
        raise ValueError("SyncTeX instrumentation stem inventory mismatch")
    for stem in STEMS:
        row = by_stem[stem]
        command = row.get("command")
        if (row.get("exit_code") != 0 or row.get("synctex_regenerated") is not True
                or not isinstance(command, list) or "-synctex=1" not in command):
            raise ValueError(f"no successful instrumented run for {stem}")
        times = [row.get(key) for key in ("started_ns", "synctex_mtime_ns", "completed_ns")]
        fresh = (row.get("sidecar_absent_before") is True
                 and all(isinstance(value, int) and not isinstance(value, bool) for value in times))
        if fresh:
            started, mtime, completed = times
            fresh = 0 < started <= mtime <= completed
        if not fresh:
            raise ValueError(f"SyncTeX sidecar regeneration was not evidenced: {stem}")
        pdf = synctex_root / f"{stem}.pdf"
        sidecar = synctex_root / f"{stem}.synctex.gz"
        expected_pdf = {key: artifacts[stem][key] for key in ("bytes", "sha256")}
        require_identity(row.get("pdf_before"), expected_pdf, f"{stem} before instrumentation")
        require_identity(row.get("pdf_after"), expected_pdf, f"{stem} after instrumentation")
        require_identity(identity(pdf), expected_pdf, f"{stem} live PDF")
        require_identity(row.get("synctex"), identity(sidecar), f"{stem} fresh sidecar")
        before = row.get("fixed_point_artifacts_before")
        after = row.get("fixed_point_artifacts_after")
        if not isinstance(before, dict) or not before or before != after:
            raise ValueError(f"instrumentation changed or omitted fixed-point artifacts: {stem}")
        if f"{stem}.aux" not in before:
            raise ValueError(f"instrumentation lacks the chapter AUX identity: {stem}")
        suffixes = (".aux", ".bbl", ".idx", ".ind", ".lof", ".lot", ".out", ".toc", ".pdf")
        expected_names = {f"{stem}{suffix}" for suffix in suffixes if (synctex_root / f"{stem}{suffix}").is_file()}
        if set(before) != expected_names:
            raise ValueError(f"incomplete fixed-point artifact inventory: {stem}")
        for name, expected in before.items():
            relative = Path(name)
            if relative.is_absolute() or relative.name != name or relative.suffix not in suffixes:
                raise ValueError(f"invalid fixed-point artifact name: {name}")
            require_identity(identity(synctex_root / relative), expected, f"fixed-point artifact {name}")
    return receipt


def synctex_pages(root: Path, source: str, line: int) -> list[int]:
    completed = subprocess.run(
        ["synctex", "view", "-i", f"{line}:0:{(root / source).resolve()}",
         "-o", str(root / f"{Path(source).stem}.pdf")],
        cwd=root, check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace", timeout=30,
    )
    pages = sorted({int(value) for value in re.findall(r"^Page:(\d+)\s*$", completed.stdout, re.MULTILINE)})
    if completed.returncode or not pages:
        raise ValueError(f"SyncTeX failed for {source}:{line}: {completed.stdout[-700:]}")
    return pages


def source_interval(data: bytes, start: int, length: int) -> tuple[int, int]:
    if start < 0 or length < 1 or start + length > len(data):
        raise ValueError("invalid final source interval")
    return data.count(b"\n", 0, start) + 1, data.count(b"\n", 0, start + length - 1) + 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--synctex-root", type=Path, required=True)
    parser.add_argument("--build-receipt", type=Path, required=True)
    parser.add_argument("--synctex-receipt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    build_path, instrumentation_path = args.build_receipt.resolve(), args.synctex_receipt.resolve()
    synctex_root = args.synctex_root.resolve()
    build, artifacts = load_build(build_path)
    check_instrumentation(instrumentation_path, build_path, build, artifacts, synctex_root)
    revision = build["source"]["commit"]
    bound_paths = [ROOT / "ai-integrated/registry/overlays.json",
                   ROOT / "validation/overlay-composition-semantic-dispositions-v1.json",
                   ROOT / "tools/compose_overlay_projection.py",
                   ROOT / "tools/verify_overlay_projection.py"]
    for number in range(34, 39):
        directory = ROOT / f"ai-integrated/candidates/commons/stacks/errata/r{number}"
        bound_paths.extend(directory / name for name in ("candidate.manifest.json", "source-map.jsonl"))
    inputs = [frozen_input(path, revision) for path in bound_paths]
    authorities, grouped, round_reports = collect_projection(list(range(34, 39)))
    if set(grouped) != {f"{stem}.tex" for stem in STEMS} or sum(len(rows) for rows in grouped.values()) != 77:
        raise ValueError("R34--R38 admitted operation inventory is not closed")
    dispositions, disposition_hash = load_semantic_dispositions(COMPOSITION_BASE)
    consumed: list[str] = []
    sources: dict[str, dict] = {}
    for stem in STEMS:
        source = f"{stem}.tex"
        authority, base = authorities[source], git_blob(COMPOSITION_BASE, source)
        final = git_blob(COMPOSITION_SOURCE, source)
        if authority != git_blob(OFFICIAL_BASELINE, source):
            raise ValueError(f"authority differs from the pinned official baseline: {source}")
        if git_blob(revision, source) != final or (synctex_root / source).read_bytes() != final:
            raise ValueError(f"live/frozen/composed source identity mismatch: {source}")
        preapplied: list[dict] = []
        semantic: list[dict] = []
        rebased = rebase_operations(authority, base, grouped[source], preapplied,
                                    dispositions, semantic, COMPOSITION_BASE)
        if preapplied or len(rebased) != EXPECTED_APPLIED[stem] or apply_operations(base, rebased) != final:
            raise ValueError(f"applied byte-edit closure failed: {source}")
        consumed.extend(row["operation_id"] for row in semantic)
        pdf, sidecar = synctex_root / f"{stem}.pdf", synctex_root / f"{stem}.synctex.gz"
        before_pdf, before_sidecar = identity(pdf), identity(sidecar)
        final_lines = final.decode("utf-8").splitlines()
        cache: dict[int, list[int]] = {}

        def mapped_lines(first: int, last: int) -> list[dict]:
            records = []
            for line in range(first, last + 1):
                # Blank TeX lines have no glyph. Query the complete interval
                # anyway; SyncTeX's nearest output is recorded, never guessed.
                if line not in cache:
                    cache[line] = synctex_pages(synctex_root, source, line)
                if any(page < 1 or page > artifacts[stem]["pages"] for page in cache[line]):
                    raise ValueError(f"SyncTeX page outside PDF: {source}:{line}")
                records.append({"line": line, "text": final_lines[line - 1], "pages": cache[line]})
            return records

        applied_rows: list[dict] = []
        for row in sorted(rebased, key=lambda item: item["start_byte"]):
            start = row["start_byte"] + sum(
                len(other["replacement_text"].encode("utf-8")) - len(other["old_text"].encode("utf-8"))
                for other in rebased if other["start_byte"] < row["start_byte"]
            )
            replacement = row["replacement_text"].encode("utf-8")
            if final[start:start + len(replacement)] != replacement:
                raise ValueError(f"final replacement mismatch: {row['operation_id']}")
            first, last = source_interval(final, start, len(replacement))
            lines = mapped_lines(first, last)
            applied_rows.append({
                "round": row["round"], "operation_id": row["operation_id"],
                "stable_id": row["stable_id"], "disposition": "applied_byte_edit",
                "authority_start_byte": row["authority_start_byte"],
                "authority_start_line": row["source_start_line"],
                "final_start_byte": start, "final_end_byte_exclusive": start + len(replacement),
                "final_cumulative_line": first, "final_end_line": last,
                "replacement_text": row["replacement_text"],
                "replacement_bytes": len(replacement), "replacement_sha256": sha256(replacement),
                "final_source_lines": lines,
                "pages": sorted({page for record in lines for page in record["pages"]}),
                **({"qualification": "Optional equivalent summation-notation normalization; not a substantive mathematical defect."}
                   if row["stable_id"] == "MC-STK-ERR-1345" else {}),
            })
        historical_rows = []
        for row in semantic:
            if row["operation_id"] != NOOP_ID:
                raise ValueError("unexpected historical no-op")
            evidence = dispositions[NOOP_ID]["evidence"]["text"].encode("utf-8")
            if final.count(evidence) != 1:
                raise ValueError("historical no-op evidence is no longer unique")
            start = final.index(evidence)
            first, last = source_interval(final, start, len(evidence))
            lines = mapped_lines(first, last)
            historical_rows.append({
                "round": row["round"], "operation_id": NOOP_ID, "stable_id": row["stable_id"],
                "disposition": "structurally_superseded_by_ancestor_rewrite",
                "applied_byte_edit": False, "evidence_text": evidence.decode("utf-8"),
                "evidence_bytes": len(evidence), "evidence_sha256": sha256(evidence),
                "final_start_byte": start, "final_end_byte_exclusive": start + len(evidence),
                "final_cumulative_line": first, "final_end_line": last,
                "final_source_lines": lines,
                "pages": sorted({page for record in lines for page in record["pages"]}),
                "disposition_registry_sha256": disposition_hash,
            })
        if identity(pdf) != before_pdf or identity(sidecar) != before_sidecar:
            raise ValueError(f"PDF/SyncTeX bytes changed during mapping: {stem}")
        byte_pages = sorted({page for row in applied_rows for page in row["pages"]})
        historical_pages = sorted({page for row in historical_rows for page in row["pages"]})
        sources[source] = {
            "authority_bytes": len(authority), "authority_sha256": sha256(authority),
            "composed_bytes": len(final), "composed_sha256": sha256(final),
            "composed_git_blob": git("rev-parse", f"{COMPOSITION_SOURCE}:{source}"),
            "operation_count": len(applied_rows), "operations": applied_rows,
            "historical_noop_evidence": historical_rows,
            "byte_edit_pages": byte_pages, "historical_noop_pages": historical_pages,
            "unique_pages": sorted(set(byte_pages + historical_pages)),
            "pdf": {"path": relative_path(pdf), **before_pdf, "pages": artifacts[stem]["pages"]},
            "synctex": {"path": relative_path(sidecar), **before_sidecar}, "synctex_query_count": len(cache),
            "pdf_and_synctex_identity_preserved": True,
        }
    verify_semantic_disposition_consumption({NOOP_ID}, consumed)
    result = {
        "schema": "unofficial-ai-integrated-stacks-operation-page-map/v1",
        "status": "PASS", "created_utc": utc_now(),
        "evidence_kind": "deterministic_source_to_pdf_mapping_not_visual_qa",
        "source": build["source"],
        "synctex_root": relative_path(synctex_root),
        "build_receipt": {"path": relative_path(build_path), **identity(build_path)},
        "synctex_instrumentation_receipt": {"path": relative_path(instrumentation_path), **identity(instrumentation_path)},
        "authority": {"commit": OFFICIAL_BASELINE, "tree": git("rev-parse", f"{OFFICIAL_BASELINE}^{{tree}}")},
        "composition_base": COMPOSITION_BASE, "composition_source": COMPOSITION_SOURCE,
        "accepted_operation_count": 77, "operation_count": 76,
        "historical_noop_operation_count": 1, "mapping_failures": 0,
        "mapping_protocol": {
            "method": "SyncTeX view of every final source line in all replacement/evidence intervals",
            "line_queries_deduplicated_per_source": True,
            "pdf_and_synctex_byte_identity_preserved": True,
            "visual_inspection_performed": False,
        },
        "sources": sources, "overlays": round_reports, "frozen_inputs": inputs,
        "mapper": {"path": relative_path(Path(__file__)), **identity(Path(__file__))},
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"status": "PASS", "mapping_only": True, "output": relative_path(output),
                      "operation_count": 76, "historical_noop_operation_count": 1,
                      "pages": {stem: sources[f"{stem}.tex"]["unique_pages"] for stem in STEMS},
                      **identity(output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
