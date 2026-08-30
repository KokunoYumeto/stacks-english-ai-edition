# Validation

Validation is layered so that repository integrity, mathematical-source
composition, TeX compilation, and visual evidence are not conflated.

## Fast unified-repository gate

Run from the repository root:

```sh
python tools/validate_unified_repository.py --pre-publication
```

The `--pre-publication` profile skips only the release/public-readback block.
All composition, registry, build, historical-preservation, and documentation
checks remain active. After publication evidence exists, omit the flag to run
the complete gate.

The gate verifies:

- the repaired R31/R32 registry chain at cutoff
  `cdea2e13a447e7cdcf5f6f805d3a767d907fd679`, comprising 33 overlays,
  1,035 globally unique stable IDs, and 1,159 cumulative exact v2 operations;
- manifest-only composition of one R31 operation in `sites-modules.tex` followed
  by 125 R32 operations in `fields.tex`, `categories.tex`, and `algebra.tex`;
- two byte-identical 27-PDF fixed-point builds (2,614 pages; 28,121,719 bytes)
  and visual inspection of all 700 affected-chapter pages and 72 mapped loci;

- ancestry of the pinned upstream, source-union, EGA, and protected linear
  registry/source history;
- 31 admitted overlays containing exactly 931 stable IDs at R30 registry cutoff
  `256846d6a4193f21cd6e1af675dc09e6950aa3d6`, tree
  `9a4f0ba1bd342cde5bf3f8f36a2d68cd7792aef3`;
- the final immutable Verdier candidate, its 12 stable units, 27 manifest
  references, independent replay, rights boundary, and exact registered
  insertion into `derived.tex`;
- the R1–R30 Stacks errata sequence: 30 batches, 919 correction IDs, and all
  1,033 v2 operations, including the ordered R22/R23 replay, the 57-operation R24
  replay in `spaces-duality.tex`, the 154-operation R25 replay in `artin.tex`,
  the 39-operation R26 replay in `smoothing.tex`, the 14-operation R27 replay
  in `modules.tex`, the one-operation supersession-aware R28 replay in
  `smoothing.tex`, the 31-operation R29 replay in `sites-modules.tex`, and the
  40-operation R30 replay in `injectives.tex`;
- preservation of the historical R1–R21 snapshot at prior cutoff
  `13ca6aaaca454f5930c4885c93f427e30cf21959` and of the separately composed
  Verdier source;
- exact authority, context, payload, preimage, postimage, prefix/suffix, label,
  registry Git blob, admission-chain, and changed-path bindings;
- the independent `injectives.tex` correction;
- required integration dossiers and public documentation;
- parseability of the live registry JSON files;
- relative links in the public Markdown landing documents; and
- absence of unresolved merge markers in the live root TeX source and public
  documentation.

The same gate runs in
[`validate.yml`](.github/workflows/validate.yml) with full Git history.

The current R30 build result is recorded at
[`validation/stacks-errata-a04446e-r30-build-2026-08-29.json`](validation/stacks-errata-a04446e-r30-build-2026-08-29.json).
All 26 required chapters (2,572 pages; 27,531,529 PDF bytes) compiled
successfully, were readable by `pdfinfo`, and reached a global PDF fixed point
on sweep four. The build is bound to source commit
`c521604343534f94c7a59086c94b99712eb1d754`, tree
`4fe26c45da3edc493b8406824f90db06ef3df28c`. Aggregate diagnostics contain
zero fatal, missing-glyph, undefined-reference, undefined-citation,
multiply-defined, rerun-required, or destination-warning markers.

Visual QA rendered and reviewed all 111 pages of the affected
`sites-modules.pdf` and `injectives.pdf` at 96 DPI and inspected all 42 unique
correction-locus pages individually at 180 DPI.
The current
[visual receipt](validation/stacks-errata-a04446e-r30-visual-qa-2026-08-29.json)
records zero clipped, overlapping, blank, corrupt, missing-glyph, or
broken-diagram defects. A second build ran independently in a parallel linked
worktree. Both runs use the same source, builder, environment, and fixed-point
sweep, and all 26 `{stem, pages, bytes, sha256}` tuples are exactly equal. See
the [reproducibility summary](validation/stacks-errata-a04446e-r30-reproducibility-2026-08-29.json)
and [second full receipt](validation/stacks-errata-a04446e-r30-reproducibility-second-2026-08-29.json).

The [source composition receipt](validation/composition-current.json) records
R30 cutoff `256846d6a4193f21cd6e1af675dc09e6950aa3d6`, tree
`9a4f0ba1bd342cde5bf3f8f36a2d68cd7792aef3`, linear registry import
`6df0e967030bcf818f3c49584fa5e9a992278d75`, and exact composition source
`3e57820736a5a57ddb1c9fbaaf2206e455b5ee31`, tree
`c4ce1faf96257fe11c0123ca649c9c020982aa33`. It binds 1,033 cumulative v2
operations. R29 yields 312,179-byte `sites-modules.tex` with SHA-256
`B097799584BD00B3D8046F62A0A56FCFE045516FD04D130C2A4C547CE3BB6C19`;
R30 yields 105,225-byte `injectives.tex` with SHA-256
`BDC721593BE0B491334C707B371A2EECD1787787903A71E059721BDB66C5AC04`.
Historical R24, R22/R23, Verdier, and R21 receipts remain preserved and
authoritative for their immutable source snapshots; they are not rebound to the
R30 tree.

R29's repaired final manifest SHA-256 is
`52920239C887757CE937267C5505AD98980464329BC6BBBD62086ED4E1D98CE5`;
R30's manifest SHA-256 is
`C903DFCA06DA4063782BB88B2F2AC5FCF56352CF948CF03382D77F1A54A48C9E`.

The [R30 release receipt](validation/stacks-errata-a04446e-r30-release-2026-08-29.json)
binds the current public errata preservation checkpoint at source head
`e3def48650c66c0d65978a04f67dea88bd8b42ac`, tree
`62bee382516e4a06df6746c5aa61a54b2fe6622f`, and tag
[`ai-integrated-stacks-r30-2026-08-29`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r30-2026-08-29).
Its six assets total 178,510,756 bytes on each of GitHub and Zenodo, and all 12
anonymous downloads matched by filename, byte count, and SHA-256. The Zenodo
version DOI is
[`10.5281/zenodo.22166456`](https://doi.org/10.5281/zenodo.22166456) under
concept DOI [`10.5281/zenodo.22135180`](https://doi.org/10.5281/zenodo.22135180).
Archive replay passed, and the preservation package binds 26 PDFs, 2,572 pages,
and 27,531,529 PDF bytes.

The historical [R28 release receipt](validation/stacks-errata-a04446e-r28-release-2026-08-28.json)
binds the preceding published tag
[`ai-integrated-stacks-r28-2026-08-28`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r28-2026-08-28)
to commit `efa46473cf8a73646ef1b6e32354e63ce20fd172`, tree
`fe139f1aedc35f02dbd10e5471ecb3c7fbed62e1`, successful GitHub Actions run
`33212304694` attempt 1, and [Zenodo version DOI
`10.5281/zenodo.22150671`](https://doi.org/10.5281/zenodo.22150671) under concept
DOI [`10.5281/zenodo.22135180`](https://doi.org/10.5281/zenodo.22135180).
Anonymous downloads from both hosts matched all six filenames and 174,673,433
bytes per host by byte count and SHA-256: 12 exact downloads and zero
mismatches. The 154,766,484-byte source archive contains 2,312 entries.

The historical [R27 release receipt](validation/stacks-errata-a04446e-r27-release-2026-08-28.json)
binds the preceding published tag
[`ai-integrated-stacks-r27-2026-08-28`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r27-2026-08-28)
to commit `e624abadfe9e2ac1f311485c44c82d6c53df2df2`, tree
`a2ba195c47c6cb41dca4e4ee7cb6292372e2e201`, successful GitHub Actions run
`33198300432` attempt 2, and [Zenodo version DOI
`10.5281/zenodo.22149250`](https://doi.org/10.5281/zenodo.22149250) under concept
DOI [`10.5281/zenodo.22135180`](https://doi.org/10.5281/zenodo.22135180).
Anonymous downloads from both hosts matched all six filenames and 174,411,900
bytes per host by byte count and SHA-256: 12 exact downloads and zero
mismatches. The 154,505,160-byte source archive contains 2,245 entries. The
receipt also binds archive-member replay and the 25-PDF, 2,492-page,
26,609,586-byte build inventory. R26, R25, and R24 remain historical evidence
for their exact immutable versions; this historical R27 release is not evidence
that the active EGA I--IV integration program is complete.

The current public EGA semantic checkpoint covers EGA I through §6.4.13 and
advances the next cursor to §6.5.1. The
[semantic release receipt](validation/ega-i-6.4-semantic-release-2026-08-29.json)
binds content commit `00adeb291487d04070b75bd0fd87759e3c43d3d3`, annotated GitHub tag
[`ega-i-6.4-semantic-2026-08-29`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ega-i-6.4-semantic-2026-08-29),
successful exact-head workflow `33250683600`, and Zenodo version DOI
[`10.5281/zenodo.22161051`](https://doi.org/10.5281/zenodo.22161051) under the
existing concept DOI. All six assets and 174,783,585 bytes per host matched in
12 public downloads; archive-member replay passed. The source mapping and
residual evidence introduce no root TeX or PDF change, so R30 remains the latest
errata release.

The [historical R22/R23 publication receipt](validation/stacks-errata-a04446e-r22-r23-release-2026-08-27.json)
binds the preceding public R22/R23 content head
`3c2b49fe0d20519de4ab06951ac2cb5151b68782`, tree
`eeb92e6723554f9b8465bee9eac3de58d4a69705`, to its successful exact-head
workflow. Anonymous HTTPS readback matched 138 checked files totaling
25,024,008 bytes by filename, byte count, SHA-256, and Git blob.

The preceding Verdier content release remains public at
`4947e4a6d22971ea793e4b4bc2b09d8ab8cc04d0`. The
[historical publication receipt](validation/stacks-verdier-a04446e-1-2-13-r1-release-2026-08-26.json)
binds its exact CI run and anonymous raw-byte inventory. Full validation omits
`--pre-publication` and independently rechecks the public ref, every decisive
row, and the recorded GitHub Actions run.

## Source-specific deterministic evidence

Detailed validators and receipts are intentionally kept with the scope they
actually prove:

- [FAC status and build evidence](fac/STATUS.md)
- [Tôhoku r71 dossier-only closure](tohoku_r71/STATUS.md)
- [GAGA r3 closure](gaga_r3/STATUS.md)
- [FGA post-merge audit](fga/audit.json)
- [EGA partial root composition and separate-edition inputs](ega/README.md)
- [Historical Verdier composition and release receipt](validation/stacks-verdier-a04446e-1-2-13-r1-release-2026-08-26.json)
- [Errata overlay registry](ai-integrated/registry/overlays.json)
- [Project roadmap and next integration order](ROADMAP.md)

## TeX builds

The upstream build entry points remain available:

```sh
make pdfs
make book
make all
```

For a targeted chapter, use the standard fixed-point sequence:

```sh
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error STEM.tex
bibtex STEM
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error STEM.tex
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error STEM.tex
```

A successful historical receipt is never silently treated as a receipt for a
later tree. Each dossier identifies the exact source and artifact hashes to
which its claim applies.
