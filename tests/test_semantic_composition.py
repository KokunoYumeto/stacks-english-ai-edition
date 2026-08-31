"""Fail-closed tests for explicitly proved historical source rewrites."""

import copy
import json
from pathlib import Path
import sys
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import compose_overlay_projection as composer


class SemanticDispositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = json.loads(composer.SEMANTIC_DISPOSITIONS_PATH.read_bytes())
        cls.disposition = cls.document["dispositions"][0]
        cls.operation_id = cls.disposition["operation"]["operation_id"]
        cls.base = "6c5f549dcdec6051dfeaf0e5300faf3b80576830"
        cls.authority = composer.git_blob(composer.OFFICIAL_BASELINE, "cohomology.tex")
        cls.current = composer.git_blob(cls.base, "cohomology.tex")
        _, operations, _ = composer.collect_projection([34])
        cls.operation = next(op for op in operations["cohomology.tex"]
                             if op["operation_id"] == cls.operation_id)

    def load(self, document):
        raw = json.dumps(document).encode("utf-8")
        with mock.patch.object(composer, "git_path_exists", return_value=True), \
             mock.patch.object(composer, "git_blob", return_value=raw) as reader:
            result = composer.load_semantic_dispositions(self.base)
            reader.assert_called_once_with(
                self.base, "validation/overlay-composition-semantic-dispositions-v1.json")
        return result

    def validate(self, disposition=None, current=None):
        return composer.validate_semantic_disposition(
            self.operation, self.disposition if disposition is None else disposition,
            self.authority, self.current if current is None else current, self.base)

    def test_nested_identity_loads_from_committed_base(self):
        loaded, digest = self.load(self.document)
        self.assertEqual(loaded, {self.operation_id: self.disposition})
        self.assertEqual(len(digest), 64)

    def test_absent_committed_file_does_not_load_worktree_disposition(self):
        with mock.patch.object(composer, "git_path_exists", return_value=False), \
             mock.patch.object(composer, "git_blob") as reader:
            self.assertEqual(composer.load_semantic_dispositions(self.base), ({}, None))
            reader.assert_not_called()

    def test_rejects_flat_or_missing_operation_identity(self):
        for value in (None, [], "wrong"):
            with self.subTest(value=value):
                doc = copy.deepcopy(self.document)
                doc["dispositions"][0]["operation"] = value
                doc["dispositions"][0]["operation_id"] = self.operation_id
                with self.assertRaises(ValueError):
                    self.load(doc)

    def test_rejects_empty_or_duplicate_identity(self):
        doc = copy.deepcopy(self.document)
        doc["dispositions"].append(copy.deepcopy(doc["dispositions"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.load(doc)
        doc = copy.deepcopy(self.document)
        doc["dispositions"][0]["operation"]["operation_id"] = ""
        with self.assertRaises(ValueError):
            self.load(doc)

    def test_real_ancestor_rewrite_is_exact(self):
        self.assertEqual(self.validate(), self.disposition)

    def test_rejects_tampered_hashes_and_locators(self):
        for path in (
            ("operation", "stable_id"),
            ("operation", "old", "sha256"),
            ("authority_source", "sha256"),
            ("rewrite_transition", "parent_source", "sha256"),
            ("rewrite_transition", "result_counts", "evidence"),
            ("composition_base_source", "sha256"),
            ("evidence", "sha256"),
            ("evidence", "base", "byte_offset"),
        ):
            with self.subTest(path=path):
                disposition = copy.deepcopy(self.disposition)
                node = disposition
                for key in path[:-1]:
                    node = node[key]
                node[path[-1]] = "tampered"
                with self.assertRaises(ValueError):
                    self.validate(disposition)

    def test_rejects_wrong_parent_or_nonancestor(self):
        with mock.patch.object(composer, "git_commit_parents", return_value=[]):
            with self.assertRaisesRegex(ValueError, "parent mismatch"):
                self.validate()
        with mock.patch.object(composer, "git_is_ancestor", return_value=False):
            with self.assertRaisesRegex(ValueError, "not an ancestor"):
                self.validate()

    def test_rejects_source_drift_or_reintroduced_defect(self):
        for current in (self.current + b"\n", self.current + self.operation["old_text"].encode()):
            with self.assertRaises(ValueError):
                self.validate(current=current)

    def test_rejects_wrong_positive_assertion(self):
        disposition = copy.deepcopy(self.disposition)
        disposition["semantic_assertions"][0]["occurrence_count"] = 7
        with self.assertRaisesRegex(ValueError, "assertion mismatch"):
            self.validate(disposition)

    def test_rebase_consumes_proved_rewrite_without_editing(self):
        used = []
        result = composer.rebase_operations(
            self.authority, self.current, [self.operation], [],
            {self.operation_id: self.disposition}, used, self.base)
        self.assertEqual(result, [])
        self.assertEqual([op["operation_id"] for op in used], [self.operation_id])

    def test_unproved_rewrite_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "exactly one unchanged region"):
            composer.rebase_operations(self.authority, self.current, [self.operation])

    def test_consumption_rejects_missing_extra_and_duplicate_uses(self):
        composer.verify_semantic_disposition_consumption({"one"}, ["one"])
        composer.verify_semantic_disposition_consumption(set(), [])
        for applicable, consumed in (({"one"}, []), (set(), ["one"]),
                                     ({"one"}, ["one", "one"])):
            with self.assertRaisesRegex(ValueError, "exactly once"):
                composer.verify_semantic_disposition_consumption(applicable, consumed)


if __name__ == "__main__":
    unittest.main()
