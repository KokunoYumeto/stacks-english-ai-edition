from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "authority" / "canon" / "R12_ALG_386_391_ADJUDICATION_SPEC.json"
SPEC = {
    "schema": "mathematics-commons-stacks-r12-adjudication-spec/v1",
    "candidate_id": "stacks-errata-a04446e-r12",
    "authority_commit": "a04446e57ec1fbc252a871afcec7752fb2807b14",
    "authority_tree": "3feeb703b931a6e7259782c10e7d1575adc83e5e",
    "authority_sha256": "FA8BB92E58A4F78A2BD01B3B6A4A87DE0A0D279F5DD90641B574DD5FBFFFA4F3",
    "accepted": [
        {
            "producer_id": "ALGEBRA-386",
            "stable_id": "MC-STK-ERR-0729",
            "class": "subject_verb_agreement",
            "locus": "algebra.tex:46640",
            "disposition": "Use singular agreement for the assumption on one ring map.",
            "result": "confirmed_grammar_error",
            "operations": [{
                "source_start_line": 46640,
                "source_end_line": 46640,
                "old_text": "words, the assumption on the ring map $R \\to S$ are often weaker than",
                "replacement_text": "words, the assumption on the ring map $R \\to S$ is often weaker than",
            }],
        },
        {
            "producer_id": "ALGEBRA-387",
            "stable_id": "MC-STK-ERR-0730",
            "class": "missing_flatness_adjective",
            "locus": "algebra.tex:46698",
            "disposition": "Restore flat in the faithfully flat localization claim.",
            "result": "confirmed_missing_word",
            "operations": [{
                "source_start_line": 46698,
                "source_end_line": 46698,
                "old_text": "is faithfully over $R_{\\mathfrak p}$ too we may assume that",
                "replacement_text": "is faithfully flat over $R_{\\mathfrak p}$ too we may assume that",
            }],
        },
        {
            "producer_id": "ALGEBRA-388",
            "stable_id": "MC-STK-ERR-0731",
            "class": "missing_terminal_punctuation",
            "locus": "algebra.tex:46814",
            "disposition": "Add the missing full stop after the parenthetical sentence.",
            "result": "confirmed_punctuation_error",
            "operations": [{
                "source_start_line": 46814,
                "source_end_line": 46814,
                "old_text": "(by going down, see Lemma \\ref{lemma-flat-going-down})",
                "replacement_text": "(by going down, see Lemma \\ref{lemma-flat-going-down}).",
            }],
        },
        {
            "producer_id": "ALGEBRA-389",
            "stable_id": "MC-STK-ERR-0732",
            "class": "missing_integral_closure_definition",
            "locus": "algebra.tex:46834",
            "disposition": "Define A' as the integral closure of A in Q(A) before using it.",
            "result": "confirmed_missing_definition",
            "operations": [{
                "source_start_line": 46834,
                "source_end_line": 46834,
                "old_text": "Via this map $A'$ maps into $B'$. This induces a map",
                "replacement_text": "Let $A'$ be the integral closure of $A$ in $Q(A)$.\nVia this map $A'$ maps into $B'$. This induces a map",
            }],
        },
        {
            "producer_id": "ALGEBRA-390",
            "stable_id": "MC-STK-ERR-0733",
            "class": "verb_tense_agreement",
            "locus": "algebra.tex:46844",
            "disposition": "Use present tense for the simultaneous module-generation conclusion.",
            "result": "confirmed_grammar_error",
            "operations": [{
                "source_start_line": 46844,
                "source_end_line": 46844,
                "old_text": "the $x_i$ also generated $A'$ as an $A$-module, and we win.",
                "replacement_text": "the $x_i$ also generate $A'$ as an $A$-module, and we win.",
            }],
        },
        {
            "producer_id": "ALGEBRA-391",
            "stable_id": "MC-STK-ERR-0734",
            "class": "residue_field_agreement",
            "locus": "algebra.tex:46856",
            "disposition": "State separately that each local factor has the same residue field as A.",
            "result": "confirmed_grammar_error",
            "operations": [{
                "source_start_line": 46856,
                "source_end_line": 46856,
                "old_text": "respectively, and the same residue fields as that of $A$.",
                "replacement_text": "respectively, and each has the same residue field as $A$.",
            }],
        },
    ],
    "rejected": [],
}


if __name__ == "__main__":
    if OUT.exists():
        raise FileExistsError(f"refusing to overwrite {OUT}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(SPEC, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="",
    )
    print(json.dumps({"accepted": len(SPEC["accepted"]), "path": str(OUT)}))
