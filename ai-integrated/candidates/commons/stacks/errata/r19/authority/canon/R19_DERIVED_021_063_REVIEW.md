# Independent review: DERIVED-021–063

Frozen authority: `EFDA4CB361DD40909D1991161EAE716E58B6CF9E79380971502E1DA12396D402`
at commit `a04446e57ec1fbc252a871afcec7752fb2807b14`, tree
`3feeb703b931a6e7259782c10e7d1575adc83e5e`.

The 43 disjoint producer allegations were replayed directly against the frozen
`derived.tex`, typed against their surrounding definitions and proofs, and
deduplicated against admitted R1–R18 material. All 43 are accepted as
`MC-STK-ERR-0832` through `MC-STK-ERR-0874`. The adjudication specification binds
57 exact, nonoverlapping UTF-8 operations. Every preimage occurs exactly once in
its declared line or line range.

Two accepted units require canon-side amendments to the producer operations.
For DERIVED-034 the degree-`n` homotopy identity also forces
`\alpha^{n - 1}` to become `\alpha^n` at line 6328; the correctly typed
occurrences elsewhere are retained. For DERIVED-037, deleting only the editorial
placeholder would strand the preceding `, and`, so one two-line operation replaces
`, and\n\item add more here.` with a period.

The mathematical subset repairs reversed or undefined functors, ill-typed
homotopy indices and compositions, wrong bounded-complex and filtered-homotopy
categories, a reversed resolution-functor tuple, an undefined resolution object,
and the spectral-sequence abutment and filtration statement. It also restores the
intended Homology cross-reference. The remaining units are bounded grammatical,
punctuation, or editorial-placeholder corrections.

Application is by fixed half-open byte span in descending `start_byte` order,
never by stable-ID order or global replacement. Stable-ID order is not source
order, several accepted preimages occur legitimately elsewhere, DERIVED-037 spans
one LF byte, and DERIVED-062's second replacement introduces the degree-`n` string
corrected by its first operation. The descending-span contract avoids every such
hazard; no spans overlap.

The intake-frozen producer snapshot ended at DERIVED-063 with 76 cumulative
producer operations. The live append-only producer evidence later grew beyond
that boundary; those later rows are R20 evidence and are excluded here. Frozen
authority and canonical locale bytes remain unchanged. The eventual corrected
English payload must be derived directly from the frozen authority, never from a
prior round's payload.
