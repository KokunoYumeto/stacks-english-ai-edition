# Deterministic replay

Use an exact copy of the source tree bound by `authority/upstream.lock.json`.
The frozen source files must reproduce the hashes in `verify.py` before any
payload is applied.

The receipt-producing replay entry point is:

`python replay-build.py --upstream-root FROZEN_SOURCE_ROOT --work-root NEW_EMPTY_TEMP_ROOT --private-evidence-root PRIVATE_EVIDENCE_ROOT`

It refuses an existing work directory, verifies the authority and payload
hashes before compilation, fixes `SOURCE_DATE_EPOCH` to the frozen commit time,
records every command and exit code, binds candidate and authority source hashes
to their PDF/log hashes, writes only sanitized build text under `builds/`, and
removes the temporary work tree after success. Raw build text is retained only
in the separately controlled private evidence root.

1. Copy the complete frozen source tree into a new, empty build directory.
2. Replace only `smoothing.tex`, `crystalline.tex`,
   `spaces-cohomology.tex`, and `tags/tags` with their counterparts under
   `payload/`.
3. From the copied source root, run the frozen allocator read-only:

   `python -c 'import sys; sys.path.insert(0, "scripts"); from functions import get_tags,get_new_tags; print(get_new_tags("./", get_tags("./")))'`

   The exact result must be `[]`; any remaining label is a failure.
4. For each of `smoothing`, `crystalline`, and `spaces-cohomology`, run
   sequentially:

   `pdflatex -interaction=nonstopmode -halt-on-error -file-line-error STEM.tex`

   `bibtex STEM`

   `pdflatex -interaction=nonstopmode -halt-on-error -file-line-error STEM.tex`

   `pdflatex -interaction=nonstopmode -halt-on-error -file-line-error STEM.tex`

5. Repeat the same three builds after restoring the exact authority source for
   each stem. Compare the undefined reference and citation target multisets.
   Candidate and authority must match. Standalone builds intentionally lack the
   complete corpus AUX set, so unchanged cross-chapter references remain
   unresolved.
6. Run `python verify.py` from this candidate root. It must reconstruct each
   payload byte-for-byte from the mapped replacements, validate all authority
   hashes and JSONL files, prove ordered structural invariants, and prove that
   `tags/tags` is the exact authority prefix plus the nine allocator records.
7. Run `python build-receipt.py` after `replay-build.py`. It cross-checks the
   execution receipt, candidate and authority source hashes, PDFs, logs, and
   warning multisets and must return `passed: true`.

Do not build in or modify the frozen source tree. Do not use the workspace root
as a build directory. Do not admit the candidate merely because these
mechanical checks pass; admission requires the separate independent replay and
review receipt.
