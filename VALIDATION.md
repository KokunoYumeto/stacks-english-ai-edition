# Validation

Validation is layered so that repository integrity, mathematical-source
composition, TeX compilation, and visual evidence are not conflated.

## Current local R38 evidence

R34–R38 are composed locally on top of the published R33 source. Independent
source replay, two complete fixed-point builds, and affected-page visual
review pass with the two disclosed observations below. **R38 is not yet a
public release:** no R38 DOI, successful publication workflow, or anonymous
public-byte readback is claimed here.

The [composition receipt](validation/composition-current.json) binds registry
cutoff `69f14d67c3a456c3d1447e1a201bdfc3f3d87f0c`, its linear import
`e4978987d5bf67f09a1b7649bda6fd90fe0fb2d8`, and cumulative source commit
`1242d514b71e60b4fe11b4c867f7de660f9a3b77`. The registry contains 39
overlays and 1,106 stable IDs, including 1,094 errata IDs and 12 Verdier units.
The new tranche has 77 accepted operations: 76 byte edits and one
historically satisfied structural correction, `MC-STK-ERR-1296-OP1`.
The cumulative exact-operation ledger contains 1,243 entries.

The [independent composition review](validation/stacks-errata-a04446e-r38-independent-composition-2026-08-31.json)
replayed the edits without calling the production composer, matched all
three complete chapter postimages, reversed the edits to recover the parent,
and checked the directions of the two non-prose cohomology arrows. The
affected sources are `cohomology.tex`, `sites-cohomology.tex`, and
`more-algebra.tex`; earlier source additions are preserved.

The [first build](validation/stacks-errata-a04446e-r38-build-2026-08-31.json),
[second build](validation/stacks-errata-a04446e-r38-reproducibility-second-2026-08-31.json),
and [reproducibility comparison](validation/stacks-errata-a04446e-r38-reproducibility-2026-08-31.json)
bind build source `bb6e7ccca41fe00a06815d81e174c5261e7a1ce3`, tree
`bfcfa4103af8bb253cac76ffacf791147ea7c683`. Both builds reach a global fixed
point on sweep four and produce exactly the same 30 PDF identities:
**3,005 pages and 32,046,922 PDF bytes**. Their recorded fatal,
missing-glyph, internal undefined-reference, undefined-citation, multiply-defined,
rerun-required, and destination-warning marker counts are zero. This does
not mean that all TeX box warnings are zero.

The [completed visual review](validation/stacks-errata-a04446e-r38-visual-qa-2026-08-31.json)
covers all 681 pages of the three affected chapters in 44 contact sheets,
plus all 42 enlarged correction-bearing or preserved-evidence pages:
86 inspected images. The [source-to-page map](validation/stacks-errata-a04446e-r38-source-page-map-2026-08-31.json)
locates all 76 byte edits and the one historical no-op with no mapping
failures. A known nonblocking layout residual remains on
`cohomology.pdf` page 123: the double-derived-Hom display extends
16.28908 pt beyond the text width, but stays within the page and remains
legible without overlap or clipping. It must not be reported as zero new
box warnings.

The second nonblocking observation is the visible “Sheaves on Stacks,
Section ??” reference on `sites-cohomology.pdf` page 102. The target
`stacks-sheaves-section-QC` is outside this selected 30-chapter profile and
is reported separately as an external reference, not an undefined internal
reference. The visual PASS therefore does not claim complete references or
full reference closure across all 116 chapters.

The [append-only R38 clarification](ai-integrated/registry/admission-receipts/r38-clarification-0001.json)
distinguishes the equivalent summation-notation change `MC-STK-ERR-1345`
from a substantive mathematical defect. It also resolves the older
regeneration receipt's stale nested review pointer to the final
manifest-bound review, without rewriting any candidate, operation,
manifest, or admission. Historical private raster references are not a
substitute for fresh cumulative visual review.

## Fast unified-repository gate

Run from the repository root:

```sh
python tools/validate_unified_repository.py --pre-publication
```

The `--pre-publication` profile skips only the release/public-readback block.
All composition, registry, build, historical-preservation, and documentation
checks remain active. After publication evidence exists, omit the flag to run
the complete gate.

The gate is intended to verify the complete local validation package,
including the completed visual receipt and its explicit qualifications.
Passing local source, build, and visual checks is not proof of publication.
Its scope includes:

- the R38 registry chain at cutoff
  `69f14d67c3a456c3d1447e1a201bdfc3f3d87f0c`, comprising 39 overlays,
  1,106 globally unique stable IDs, and 1,243 cumulative exact v2 operations;
- manifest-only R34–R38 composition on cumulative source, with 76 byte edits
  and one separately bound historical structural disposition;
- two byte-identical 30-PDF fixed-point builds (3,005 pages; 32,046,922 bytes)
  and the separate affected-page visual evidence;
- ancestry of the pinned upstream, source-union, EGA, and protected linear
  registry/source history;
- the final immutable Verdier candidate, its 12 stable units, 27 manifest
  references, independent replay, rights boundary, and exact registered
  insertion into `derived.tex`;
- the R1–R38 Stacks errata sequence: 38 batches, 1,094 correction IDs, and all
  1,243 v2 operations, including the ordered R22/R23 replay, the 57-operation R24
  replay in `spaces-duality.tex`, the 154-operation R25 replay in `artin.tex`,
  the 39-operation R26 replay in `smoothing.tex`, the 14-operation R27 replay
  in `modules.tex`, the one-operation supersession-aware R28 replay in
  `smoothing.tex`, the 31-operation R29 replay in `sites-modules.tex`, and the
  40-operation R30 replay in `injectives.tex`, the single R31 replay in
  `sites-modules.tex`, the 125-operation R32 replay across `fields.tex`,
  `categories.tex`, and `algebra.tex`, and the seven-operation R33 replay in
  `spaces-morphisms.tex`, followed by the R34–R38 tranche described above;
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

## Historical R33 validation and latest public errata release

R33 remains the latest publicly preserved errata checkpoint while the R38
publication workflow is unfinished. Its evidence below
applies to the historical R33 source, not the current local R38 tree.

The R33 build result is recorded at
[`validation/stacks-errata-a04446e-r33-build-2026-08-30.json`](validation/stacks-errata-a04446e-r33-build-2026-08-30.json).
All 28 required chapters (2,730 pages; 29,277,302 PDF bytes) compiled
successfully, were readable by `pdfinfo`, and reached a global PDF fixed point
on sweep four. The build is bound to source commit
`1c90a67eb42de28884be05abd8fb58f781aed7db`, tree
`3c292f9a4b94162ede69d2633b1272b057a498c3`. Aggregate diagnostics contain
zero fatal, missing-glyph, undefined-reference, undefined-citation,
multiply-defined, rerun-required, or destination-warning markers.

Visual QA rendered and reviewed all 116 pages of the affected
`spaces-morphisms.pdf` at 96 DPI and inspected all five unique correction-locus
pages individually at 180 DPI.
The historical R33
[visual receipt](validation/stacks-errata-a04446e-r33-visual-qa-2026-08-30.json)
records zero clipped, overlapping, blank, corrupt, missing-glyph, or
broken-diagram defects. A second build ran independently in a parallel linked
worktree. Both runs use the same source, builder, environment, and fixed-point
sweep, and all 28 `{stem, pages, bytes, sha256}` tuples are exactly equal. See
the [reproducibility summary](validation/stacks-errata-a04446e-r33-reproducibility-2026-08-30.json)
and [second full receipt](validation/stacks-errata-a04446e-r33-reproducibility-second-2026-08-30.json).

The R33 composition recorded cutoff `acb48c7edaf9595b542b003ed360399870188b7f`, tree
`8356ae1652ae4ce6a22a457855072c5a3e7b3ad4`, linear registry import
`b2ffa008fc27bfdb8b93c431f4df0c3e197d3440`, and exact composition source
`9100eefe0819f9632c6129e6d6f19a4101d223d1`, tree
`d786a8604e7c0be79fab77c380247bd971555520`. It binds 1,166 cumulative v2
operations and the seven-operation `spaces-morphisms.tex` replay. The
validated build source is `1c90a67eb42de28884be05abd8fb58f781aed7db`, tree
`3c292f9a4b94162ede69d2633b1272b057a498c3`.
The live [composition receipt](validation/composition-current.json) now binds
R38. Historical R33, R24, R22/R23, Verdier, and R21 receipts remain preserved
and authoritative for their immutable source snapshots; they are not rebound
to the R38 tree.

R33's manifest SHA-256 is
`1D2EA4F6463FB775CFF3F0E3616BE125F6D20709BB32DB84D1D1889582BFAC75`.

The [R33 release receipt](validation/stacks-errata-a04446e-r33-release-2026-08-30.json)
binds the current public errata preservation checkpoint at content head
`a52883a83081348d0ea4927a03d5fd8aa036890b`, tree
`2d686e92dacdc8e01d6c6950bf81f250e657cd8f`, and tag
[`ai-integrated-stacks-r33-2026-08-30`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r33-2026-08-30).
Its six current assets total 184,010,318 bytes on each host. Anonymous readback
covered all six GitHub assets and all nine Zenodo files. The Zenodo version DOI is
[`10.5281/zenodo.22182175`](https://doi.org/10.5281/zenodo.22182175) under
concept DOI [`10.5281/zenodo.22135180`](https://doi.org/10.5281/zenodo.22135180).
Archive replay passed, and the current preservation package binds 28 PDFs,
2,730 pages, and 29,277,302 PDF bytes.

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

The current public EGA semantic checkpoint covers EGA I through §6.6.3 and
advances the next cursor to §6.6.4. The exact checkpoint is
[`ega-i-6.6.3-semantic-checkpoint-2026-08-30.json`](validation/ega-i-6.6.3-semantic-checkpoint-2026-08-30.json)
(SHA-256 `58CC0464C1EDAC665CA72B80F8156E77773F9B983F83D76BA948551A3D15456E`),
bound to content commit `85024a5e3456cadc79c6cde67bf1fcbbc09c48cb`, GitHub tag
[`ega-i-6.6.3-semantic-2026-08-30`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ega-i-6.6.3-semantic-2026-08-30),
and Zenodo version DOI [`10.5281/zenodo.22177421`](https://doi.org/10.5281/zenodo.22177421)
under the existing concept DOI. It is semantic-only and changes no root TeX or
PDF; R33 is the latest errata release.

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
