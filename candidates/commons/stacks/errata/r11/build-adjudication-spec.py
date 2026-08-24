from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "authority" / "canon" / "R11_ALG_382_385_ADJUDICATION_SPEC.json"
SPEC = {'schema': 'mathematics-commons-stacks-r11-adjudication-spec/v1',
 'candidate_id': 'stacks-errata-a04446e-r11',
 'authority_commit': 'a04446e57ec1fbc252a871afcec7752fb2807b14',
 'authority_tree': '3feeb703b931a6e7259782c10e7d1575adc83e5e',
 'authority_sha256': 'FA8BB92E58A4F78A2BD01B3B6A4A87DE0A0D279F5DD90641B574DD5FBFFFA4F3',
 'accepted': [{'producer_id': 'ALGEBRA-382',
               'stable_id': 'MC-STK-ERR-0725',
               'class': 'zero_module_dimension_case',
               'locus': 'algebra.tex:46321',
               'disposition': 'Add the omitted zero-module case before introducing the finite '
                              'right-hand-side dimension.',
               'result': 'confirmed_missing_case',
               'operations': [{'source_start_line': 46321,
                               'source_end_line': 46321,
                               'old_text': 'Denote $n$ the right hand side. First assume that $n$ '
                                           'is zero.',
                               'replacement_text': 'If $M = 0$ or $N = 0$, then both sides of the '
                                                   'formula are infinite,\n'
                                                   'and there is nothing to prove. Thus we may '
                                                   'assume that $M$ and $N$ are nonzero.\n'
                                                   'Denote $n$ the right hand side. First assume '
                                                   'that $n$ is zero.'}]},
              {'producer_id': 'ALGEBRA-383',
               'stable_id': 'MC-STK-ERR-0726',
               'class': 'missing_item_punctuation',
               'locus': 'algebra.tex:46464,46493',
               'disposition': 'Add the missing terminal comma to both repeated list items.',
               'result': 'confirmed_grammar_error',
               'operations': [{'source_start_line': 46464,
                               'source_end_line': 46464,
                               'old_text': '\\item $S$ is Noetherian',
                               'replacement_text': '\\item $S$ is Noetherian,'},
                              {'source_start_line': 46493,
                               'source_end_line': 46493,
                               'old_text': '\\item $S$ is Noetherian',
                               'replacement_text': '\\item $S$ is Noetherian,'}]},
              {'producer_id': 'ALGEBRA-384',
               'stable_id': 'MC-STK-ERR-0727',
               'class': 'missing_subring_subject_and_comma',
               'locus': 'algebra.tex:46536',
               'disposition': 'Identify R_0 as a subring and punctuate the introductory clause.',
               'result': 'confirmed_grammar_error',
               'operations': [{'source_start_line': 46536,
                               'source_end_line': 46536,
                               'old_text': 'However, since $R_0 \\subset R$ is reduced we see that',
                               'replacement_text': 'However, since the subring $R_0 \\subset R$ is '
                                                   'reduced, we see that'}]},
              {'producer_id': 'ALGEBRA-385',
               'stable_id': 'MC-STK-ERR-0728',
               'class': 'incorrect_lemma_application_quantifier',
               'locus': 'algebra.tex:46623',
               'disposition': 'State the lemma application with the correct per-index quantifier.',
               'result': 'confirmed_proof_exposition_error',
               'operations': [{'source_start_line': 46623,
                               'source_end_line': 46623,
                               'old_text': 'This follows from Lemma \\ref{lemma-Rk-goes-up} '
                                           'applied for all $(R_k)$',
                               'replacement_text': 'This follows by applying Lemma '
                                                   '\\ref{lemma-Rk-goes-up} for every $k \\geq '
                                                   '0$'}]}],
 'rejected': []}


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
