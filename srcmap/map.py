#!/usr/bin/env python3
"""Apply append-only decisions and graph corrections to a source inventory."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "fga"))
import mkidx as fidx  # noqa: E402
import mkmap as fmap  # noqa: E402


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def output_transaction_paths(out: Path) -> dict[str, dict[str, Path]]:
    return {
        "map.csv": {
            "target": out / "map.csv",
            "temp": out / ".map.csv.tmp",
            "backup": out / ".map.bak",
            "restore": out / ".map.restore.tmp",
        },
        "ucand.csv": {
            "target": out / "ucand.csv",
            "temp": out / ".ucand.csv.tmp",
            "backup": out / ".ucand.bak",
            "restore": out / ".ucand.restore.tmp",
        },
        "mcheck.json": {
            "target": out / "mcheck.json",
            "temp": out / ".mcheck.json.tmp",
            "backup": out / ".mcheck.bak",
            "restore": out / ".mcheck.restore.tmp",
        },
    }


def _unlink(paths: list[Path]) -> None:
    for path in paths:
        path.unlink(missing_ok=True)


def recover_output_transaction(out: Path) -> tuple[str, list[str], list[str]]:
    specs = output_transaction_paths(out)
    journal = out / ".map.txn.json"
    journal_temp = out / ".map.txn.tmp"
    failure_temp = out / ".mcheck.fail.tmp"
    artifacts = [
        item[key]
        for item in specs.values()
        for key in ("temp", "backup", "restore")
    ]
    if not journal.exists():
        orphans = [
            path for path in [*artifacts, journal_temp, failure_temp] if path.exists()
        ]
        if not orphans:
            return "none", [], []
        receipt_path = specs["mcheck.json"]["target"]
        receipt_consistent = False
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt_hashes = receipt.get("sha256", {})
            receipt_consistent = all(
                specs[name]["target"].exists()
                and receipt_hashes.get(f"{out.name}/{name}")
                == fidx.sha256(specs[name]["target"])
                for name in ("map.csv", "ucand.csv")
            )
        except (AttributeError, OSError, json.JSONDecodeError):
            receipt_consistent = False
        if not receipt_consistent:
            names = ", ".join(sorted(path.name for path in orphans))
            return (
                "blocked",
                [f"output transaction artifacts lack a consistent journal or receipt: {names}"],
                [],
            )
        try:
            _unlink(orphans)
        except OSError as exc:
            return "blocked", [f"cannot clean output transaction artifacts: {exc}"], []
        return (
            "none",
            [],
            ["removed journal-free artifacts after verifying the current output receipt"],
        )
    try:
        data = json.loads(journal.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return "blocked", [f"cannot read output transaction journal: {exc}"], []
    if not isinstance(data, dict):
        return "blocked", ["invalid output transaction journal"], []
    names = set(specs)
    expected = data.get("expected_sha256", {})
    existed = data.get("existed_before", {})
    old_sha256 = data.get("old_sha256", {})
    if (
        data.get("schema") != "source-map-output-transaction-v1"
        or not isinstance(expected, dict)
        or not isinstance(existed, dict)
        or not isinstance(old_sha256, dict)
        or set(expected) != names
        or set(existed) != names
        or set(old_sha256) != names
        or any(
            not re.fullmatch(r"[0-9A-F]{64}", expected.get(name) or "")
            for name in names
        )
        or any(not isinstance(existed.get(name), bool) for name in names)
    ):
        return "blocked", ["invalid output transaction journal"], []
    committed = all(
        specs[name]["target"].exists()
        and fidx.sha256(specs[name]["target"]) == expected[name]
        for name in names
    )
    if committed:
        try:
            journal.unlink(missing_ok=True)
            _unlink(
                [
                    *[item["backup"] for item in specs.values()],
                    *artifacts,
                    journal_temp,
                    failure_temp,
                ]
            )
        except OSError as exc:
            return "blocked", [f"cannot clean committed output transaction: {exc}"], []
        return "committed", [], ["completed interrupted output transaction"]
    errors: list[str] = []
    for name, item in specs.items():
        if existed[name]:
            old_hash = old_sha256.get(name)
            if not re.fullmatch(r"[0-9A-F]{64}", old_hash or ""):
                errors.append(f"missing prior hash for {name} in output transaction")
            elif not item["backup"].exists():
                errors.append(f"missing output transaction backup for {name}")
            elif fidx.sha256(item["backup"]) != old_hash:
                errors.append(f"output transaction backup hash mismatch for {name}")
        elif old_sha256.get(name) is not None:
            errors.append(f"unexpected prior hash for absent output {name}")
    if errors:
        return "blocked", errors, []
    try:
        for name, item in specs.items():
            if existed[name]:
                shutil.copy2(item["backup"], item["restore"])
                item["restore"].replace(item["target"])
            else:
                item["target"].unlink(missing_ok=True)
        for name, item in specs.items():
            if existed[name] and fidx.sha256(item["target"]) != old_sha256[name]:
                raise OSError(f"restored output hash mismatch for {name}")
            if not existed[name] and item["target"].exists():
                raise OSError(f"output should be absent after rollback: {name}")
    except OSError as exc:
        _unlink([item["restore"] for item in specs.values()])
        return "blocked", [f"output transaction rollback failed: {exc}"], []
    try:
        journal.unlink(missing_ok=True)
        _unlink([*artifacts, journal_temp, failure_temp])
    except OSError as exc:
        return "blocked", [f"cannot clean rolled-back output transaction: {exc}"], []
    return "rolled_back", [], ["recovered interrupted output transaction"]


def promote_output_transaction(
    out: Path,
    expected_sha256: dict[str, str],
) -> tuple[bool, list[str], list[str]]:
    specs = output_transaction_paths(out)
    journal = out / ".map.txn.json"
    journal_temp = out / ".map.txn.tmp"
    names = set(specs)
    if set(expected_sha256) != names:
        _unlink([item["temp"] for item in specs.values()])
        return False, ["output transaction expected-hash set is incomplete"], []
    existed = {name: item["target"].exists() for name, item in specs.items()}
    old_sha256 = {
        name: fidx.sha256(item["target"]) if existed[name] else None
        for name, item in specs.items()
    }
    try:
        for name, item in specs.items():
            if existed[name]:
                shutil.copy2(item["target"], item["backup"])
        journal_data = {
            "schema": "source-map-output-transaction-v1",
            "expected_sha256": expected_sha256,
            "existed_before": existed,
            "old_sha256": old_sha256,
        }
        journal_temp.write_text(
            json.dumps(journal_data, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        journal_temp.replace(journal)
    except OSError as exc:
        if journal.exists():
            state, recovery_errors, recovery_warnings = recover_output_transaction(out)
            if recovery_errors:
                return (
                    False,
                    [f"cannot prepare output transaction: {exc}", *recovery_errors],
                    recovery_warnings,
                )
            if state == "committed":
                return True, [], recovery_warnings
            return (
                False,
                [f"output transaction preparation failed and was rolled back: {exc}"],
                recovery_warnings,
            )
        _unlink(
            [
                *[item["temp"] for item in specs.values()],
                *[item["backup"] for item in specs.values()],
                *[item["restore"] for item in specs.values()],
                journal_temp,
            ]
        )
        return False, [f"cannot prepare output transaction: {exc}"], []
    try:
        for name, item in specs.items():
            item["temp"].replace(item["target"])
        for name, item in specs.items():
            if fidx.sha256(item["target"]) != expected_sha256[name]:
                raise OSError(f"promoted output hash mismatch for {name}")
    except OSError as exc:
        state, recovery_errors, recovery_warnings = recover_output_transaction(out)
        if recovery_errors:
            return False, [f"output promotion failed: {exc}", *recovery_errors], recovery_warnings
        if state == "committed":
            return True, [], recovery_warnings
        return False, [f"output promotion failed and was rolled back: {exc}"], recovery_warnings
    try:
        journal.unlink(missing_ok=True)
        _unlink([item["backup"] for item in specs.values()])
    except OSError as exc:
        state, recovery_errors, recovery_warnings = recover_output_transaction(out)
        still_committed = all(
            item["target"].exists()
            and fidx.sha256(item["target"]) == expected_sha256[name]
            for name, item in specs.items()
        )
        if still_committed:
            return (
                True,
                [],
                [
                    *recovery_warnings,
                    f"output transaction committed; cleanup deferred: {exc}",
                    *recovery_errors,
                ],
            )
        if recovery_errors:
            return False, recovery_errors, recovery_warnings
        return state in {"committed", "none"}, [], recovery_warnings
    return True, [], []


def write_json_atomic(path: Path, data: dict, temp_name: str) -> None:
    temp = path.parent / temp_name
    temp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp.replace(path)


def apply_graph_corrections(
    path: Path,
    mapped: list[dict[str, str]],
    root_id: str,
) -> tuple[list[dict[str, str]], list[str], int]:
    if not path.exists():
        return [], [], 0
    required = {
        "correction_id",
        "unit_id",
        "field",
        "old_value",
        "new_value",
        "action",
        "supersedes",
        "rationale",
        "review_state",
    }
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            return rows, ["corr.csv is missing required columns"], 0
    errors: list[str] = []
    working = [dict(row) for row in mapped]
    by_unit = {row["unit_id"]: row for row in working}
    seen_ids: set[str] = set()
    correction_by_id: dict[str, dict[str, str]] = {}
    terminal_by_field: dict[tuple[str, str], str] = {}
    accepted_ids: set[str] = set()
    superseded_ids: set[str] = set()
    for position, row in enumerate(rows, start=1):
        row_errors: list[str] = []
        correction_id = row.get("correction_id", "")
        unit_id = row.get("unit_id", "")
        field = row.get("field", "")
        key = (unit_id, field)
        if not re.fullmatch(r"G[0-9]{6}", correction_id):
            row_errors.append(f"invalid graph correction ID: {correction_id}")
        expected_id = f"G{position:06d}"
        if correction_id != expected_id:
            row_errors.append(
                f"non-contiguous graph correction ID at row {position}: "
                f"expected {expected_id}, found {correction_id}"
            )
        if correction_id in seen_ids:
            row_errors.append(f"duplicate graph correction ID: {correction_id}")
        seen_ids.add(correction_id)
        action = row.get("action", "")
        supersedes = row.get("supersedes", "")
        prior_id = terminal_by_field.get(key, "")
        if action == "set":
            if prior_id:
                row_errors.append(
                    f"set action repeats corrected field in {correction_id}: "
                    f"{unit_id}:{field}"
                )
            if supersedes:
                row_errors.append(f"set action has supersedes value in {correction_id}")
        elif action == "replace":
            if not prior_id:
                row_errors.append(
                    f"replace action has no prior correction in {correction_id}"
                )
            elif supersedes != prior_id:
                row_errors.append(
                    f"replace action in {correction_id} must supersede active "
                    f"terminal {prior_id}"
                )
            prior = correction_by_id.get(supersedes)
            if supersedes and prior is None:
                row_errors.append(
                    f"unknown superseded correction in {correction_id}: {supersedes}"
                )
            if prior and (prior.get("unit_id"), prior.get("field")) != key:
                row_errors.append(
                    f"superseded correction has a different field in {correction_id}"
                )
            if supersedes in superseded_ids:
                row_errors.append(
                    f"correction superseded twice in {correction_id}: {supersedes}"
                )
        else:
            row_errors.append(
                f"invalid graph correction action in {correction_id}: {action}"
            )
        if unit_id not in by_unit:
            row_errors.append(f"unknown graph correction unit: {unit_id}")
        if field != "parent_id":
            row_errors.append(f"unsupported graph correction field in {correction_id}")
        old_value = row.get("old_value", "")
        new_value = row.get("new_value", "")
        if old_value == new_value:
            row_errors.append(f"no-op graph correction in {correction_id}")
        if (
            unit_id in by_unit
            and field == "parent_id"
            and by_unit[unit_id][field] != old_value
        ):
            row_errors.append(f"graph correction old value mismatch in {correction_id}")
        if new_value != root_id and new_value not in by_unit:
            row_errors.append(f"unknown corrected parent in {correction_id}: {new_value}")
        if (
            not row.get("rationale", "").strip()
            or not row.get("review_state", "").strip()
        ):
            row_errors.append(f"incomplete graph correction rationale in {correction_id}")
        if row_errors:
            errors.extend(row_errors)
            continue
        by_unit[unit_id][field] = new_value
        correction_by_id[correction_id] = row
        accepted_ids.add(correction_id)
        terminal_by_field[key] = correction_id
        if action == "replace":
            superseded_ids.add(supersedes)
    for unit_id in by_unit:
        seen: set[str] = set()
        cursor = unit_id
        while cursor in by_unit:
            if cursor in seen:
                errors.append(f"parent cycle after graph corrections at {unit_id}")
                break
            seen.add(cursor)
            cursor = by_unit[cursor]["parent_id"]
    expected_terminals = accepted_ids - superseded_ids
    actual_terminals = set(terminal_by_field.values())
    if actual_terminals != expected_terminals:
        errors.append("graph correction ledger does not have one active terminal per field")
    if errors:
        return rows, errors, 0
    mapped[:] = working
    return rows, [], len(actual_terminals)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("corpus_dir", type=Path)
    args = parser.parse_args()
    out = args.corpus_dir.resolve()
    _, recovery_errors, recovery_warnings = recover_output_transaction(out)
    if recovery_errors:
        for error in recovery_errors:
            print(error, file=sys.stderr)
        return 1
    cfg = json.loads((out / "cfg.json").read_text(encoding="utf-8"))
    intake = json.loads((out / "intake.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    units_path = out / "units.csv"
    if fidx.sha256(units_path) != intake["outputs"]["units.csv"]["sha256"]:
        errors.append("units.csv differs from the frozen intake")
    units = load_csv(units_path)
    if len(units) != int(cfg["expected_units"]):
        errors.append("unit count changed")
    index, index_errors, warnings, _ = fidx.build_index()
    warnings = [*recovery_warnings, *warnings]
    errors.extend(index_errors)
    topics = load_csv(out / "topics.csv")
    topic_rows, topic_errors, topic_warnings = fidx.topic_map_rows(index, topics)
    errors.extend(topic_errors)
    warnings.extend(topic_warnings)
    topic_map = {row["topic_id"]: row for row in topic_rows}
    structural = set(cfg.get("structural_types", []))
    embedded = set(cfg.get("embedded_types", []))
    historical = set(cfg.get("historical_types", []))
    mapped: list[dict[str, str]] = []
    for unit in units:
        topic_ids = [value for value in unit["topics"].split(";") if value]
        unknown = sorted(set(topic_ids) - set(topic_map))
        if unknown:
            errors.append(f"unknown topics for {unit['id']}: {';'.join(unknown)}")
        labels = sorted(
            {
                label
                for topic in topic_ids
                if topic in topic_map
                for label in topic_map[topic]["evidence_labels"].split(";")
                if label
            }
        )
        tags = sorted(
            {
                tag
                for topic in topic_ids
                if topic in topic_map
                for tag in topic_map[topic]["evidence_tags"].split(";")
                if tag
            }
        )
        kind = unit["unit_type"]
        if kind in structural:
            disposition = "structural_only"
            state = "classified"
            rationale = "Source structure; no independent Stacks object."
        elif kind in embedded:
            disposition = "structural_only"
            state = "inherits_parent"
            rationale = "Embedded source component; inherit the parent disposition."
        elif kind in historical:
            disposition = "historical_reference"
            state = "needs_link_review"
            rationale = "Historical or bibliographic unit requiring source linkage."
        else:
            disposition = "needs_review"
            state = "generated_intake"
            rationale = "Requires statement-level mathematical comparison."
        mapped.append(
            {
                "unit_id": unit["id"],
                "item": unit["item"],
                "unit_type": kind,
                "parent_id": unit["parent_id"],
                "source_start": unit["source_start"],
                "source_end": unit["source_end"],
                "source_loc": f"{unit['source_file']}:{unit['source_line']}",
                "authority_sha256": unit["authority_sha256"],
                "source_topics": ";".join(topic_ids),
                "topic_evidence_labels": ";".join(labels),
                "topic_evidence_tags": ";".join(tags),
                "decision_id": "",
                "disposition": disposition,
                "review_state": state,
                "stacks_labels": "",
                "stacks_tags": "",
                "rationale": rationale,
            }
        )
    correction_path = out / "corr.csv"
    corrections, correction_errors, active_corrections = apply_graph_corrections(
        correction_path, mapped, cfg["root_id"]
    )
    errors.extend(correction_errors)
    decisions, decision_errors = fmap.load_decisions(out / "dec.csv", mapped, index)
    errors.extend(decision_errors)
    fmap.apply_decisions(mapped, decisions)
    issues, issue_errors = fmap.load_issues(out / "issues.csv", mapped, index, decisions)
    errors.extend(issue_errors)
    review_ids = {
        row["unit_id"] for row in mapped if row["disposition"] == "needs_review"
    }
    candidates = fmap.bm25_candidates(units, index, review_ids)
    candidate_ids = {row["unit_id"] for row in candidates}
    if candidate_ids != review_ids:
        errors.append("candidate unit set differs from review unit set")
    transaction_paths = output_transaction_paths(out)
    map_path = transaction_paths["map.csv"]["target"]
    candidate_path = transaction_paths["ucand.csv"]["target"]
    map_temp_path = transaction_paths["map.csv"]["temp"]
    candidate_temp_path = transaction_paths["ucand.csv"]["temp"]
    fidx.write_csv(
        map_temp_path,
        mapped,
        [
            "unit_id", "item", "unit_type", "parent_id", "source_start",
            "source_end", "source_loc", "authority_sha256", "source_topics",
            "topic_evidence_labels", "topic_evidence_tags", "decision_id",
            "disposition", "review_state", "stacks_labels", "stacks_tags",
            "rationale",
        ],
    )
    fidx.write_csv(
        candidate_temp_path,
        candidates,
        [
            "unit_id", "unit_type", "unit_title", "rank", "score", "overlap",
            "tag", "full_label", "file", "line", "kind", "section_title",
            "snippet", "query_sha256", "status",
        ],
    )
    errors.extend(
        fmap.privacy_errors(
            [
                map_temp_path,
                candidate_temp_path,
                out / "dec.csv",
                out / "issues.csv",
                *([correction_path] if correction_path.exists() else []),
            ]
        )
    )
    attempted_output_sha256 = {
        f"{out.name}/map.csv": fidx.sha256(map_temp_path),
        f"{out.name}/ucand.csv": fidx.sha256(candidate_temp_path),
    }

    def current_output_sha256() -> dict[str, str]:
        return {
            **(
                {f"{out.name}/map.csv": fidx.sha256(map_path)}
                if map_path.exists()
                else {}
            ),
            **(
                {f"{out.name}/ucand.csv": fidx.sha256(candidate_path)}
                if candidate_path.exists()
                else {}
            ),
        }

    def make_result(
        result_errors: list[str],
        outputs_promoted: bool,
        output_sha256: dict[str, str],
    ) -> dict:
        return {
            "schema": "historical-source-stacks-map-v1",
            "corpus": cfg["corpus"],
            "official_upstream": cfg["official_upstream"],
            "integration_base": cfg["integration_base"],
            "status": "PASS" if not result_errors else "FAIL",
            "outputs_promoted": outputs_promoted,
            "errors": result_errors,
            "warnings": warnings,
            "counts": {
                "units": len(units),
                "decisions": len(decisions),
                "decided_units": sum(1 for row in mapped if row["decision_id"]),
                "graph_corrections": len(corrections),
                "active_graph_corrections": active_corrections,
                "source_issues": len(issues),
                "active_source_issues": sum(
                    1 for row in issues if row["status"] != "resolved"
                ),
                "review_units": len(review_ids),
                "candidate_units": len(candidate_ids),
                "unit_candidates": len(candidates),
                "dispositions": dict(
                    sorted(Counter(row["disposition"] for row in mapped).items())
                ),
            },
            "sha256": {
                f"{out.name}/cfg.json": fidx.sha256(out / "cfg.json"),
                f"{out.name}/intake.json": fidx.sha256(out / "intake.json"),
                f"{out.name}/units.csv": fidx.sha256(units_path),
                f"{out.name}/dec.csv": fidx.sha256(out / "dec.csv"),
                f"{out.name}/issues.csv": fidx.sha256(out / "issues.csv"),
                **output_sha256,
                **(
                    {f"{out.name}/corr.csv": fidx.sha256(correction_path)}
                    if correction_path.exists()
                    else {}
                ),
            },
            **(
                {"attempted_output_sha256": attempted_output_sha256}
                if result_errors
                else {}
            ),
        }

    mcheck_path = transaction_paths["mcheck.json"]["target"]
    if errors:
        _unlink([map_temp_path, candidate_temp_path])
        result = make_result(errors, False, current_output_sha256())
        write_json_atomic(mcheck_path, result, ".mcheck.fail.tmp")
        return 1
    result = make_result([], True, attempted_output_sha256)
    mcheck_temp_path = transaction_paths["mcheck.json"]["temp"]
    mcheck_temp_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    expected_transaction_sha256 = {
        "map.csv": attempted_output_sha256[f"{out.name}/map.csv"],
        "ucand.csv": attempted_output_sha256[f"{out.name}/ucand.csv"],
        "mcheck.json": fidx.sha256(mcheck_temp_path),
    }
    promoted, promotion_errors, promotion_warnings = promote_output_transaction(
        out, expected_transaction_sha256
    )
    warnings.extend(promotion_warnings)
    if promoted:
        return 0
    errors.extend(promotion_errors)
    result = make_result(errors, False, current_output_sha256())
    write_json_atomic(mcheck_path, result, ".mcheck.fail.tmp")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
