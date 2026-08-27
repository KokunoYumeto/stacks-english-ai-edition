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

- ancestry of the pinned upstream, source-union, EGA, and protected linear
  registry/source history;
- 25 admitted overlays containing exactly 690 stable IDs at R24 registry cutoff
  `6df734ecb3bef8f35770819d17a8d3e267b8e07a`, tree
  `49b8e57e91f0bf04669b2ee93e3586cfb6919088`;
- the final immutable Verdier candidate, its 12 stable units, 27 manifest
  references, independent replay, rights boundary, and exact registered
  insertion into `derived.tex`;
- the R1–R24 Stacks errata sequence: 24 batches, 678 correction IDs, and all
  754 v2 operations, including the ordered 106-operation R22/R23 replay in
  `more-algebra.tex` and the 57-operation R24 replay in
  `spaces-duality.tex`;
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

The current R24 build result is recorded at
[`validation/stacks-errata-a04446e-r24-build-2026-08-27.json`](validation/stacks-errata-a04446e-r24-build-2026-08-27.json).
All 23 required chapters (2,368 pages; 24,949,361 PDF bytes) compiled
successfully, were readable by `pdfinfo`, and reached a global PDF fixed point
on sweep four. The build is bound to source commit
`c3bc402b03dea3c5ac92c9e226645b5895a78887`, tree
`626b67a2c32f4b2bc1b8ad7b4586cdb036b25a21`. Aggregate diagnostics contain
zero fatal, missing-glyph, undefined-reference, undefined-citation,
multiply-defined, rerun-required, or destination-warning markers.

Visual QA rendered and reviewed all 25 pages of the affected
`spaces-duality.pdf` at 96 DPI and inspected every page individually at 180 DPI.
The current
[visual receipt](validation/stacks-errata-a04446e-r24-visual-qa-2026-08-27.json)
records zero clipped, overlapping, blank, corrupt, missing-glyph, or
broken-diagram defects. A second build ran independently in a parallel linked
worktree. Both runs use the same source, builder, environment, and fixed-point
sweep, and all 23 `{stem, pages, bytes, sha256}` tuples are exactly equal. See
the [reproducibility summary](validation/stacks-errata-a04446e-r24-reproducibility-2026-08-27.json)
and [second full receipt](validation/stacks-errata-a04446e-r24-reproducibility-second-2026-08-27.json).

The [source composition receipt](validation/composition-current.json) records
R24 cutoff `6df734ecb3bef8f35770819d17a8d3e267b8e07a`, linear registry
import `0e5c4596d85072fecae6e061bb54bed6979d66c3`, and exact composition
source `10c1c62f371921cdafbaa5e89f438a821a013621`, tree
`6ec98b8ee6919070a24130877d4eeb9e1a0e874b`. It binds 754 cumulative
v2 operations, including the 57 new R24 operations, to the 80,995-byte
`spaces-duality.tex` postimage with SHA-256
`3CFCEF73EB9172CF69082FF07B9D84442DD5E545D8AD22917D5A694BAA57298E`.
The historical R22/R23, Verdier, and R21 composition, build, publication, and
readback receipts remain preserved and authoritative for their own immutable
source snapshots; they are not rebound to the R24 tree.

The [historical R22/R23 publication receipt](validation/stacks-errata-a04446e-r22-r23-release-2026-08-27.json)
binds the public R22/R23 content head
`3c2b49fe0d20519de4ab06951ac2cb5151b68782`, tree
`eeb92e6723554f9b8465bee9eac3de58d4a69705`, to its successful exact-head
workflow. Anonymous HTTPS readback matched 138 checked files totaling
25,024,008 bytes by filename, byte count, SHA-256, and Git blob.

The preceding Verdier content release remains public at
`4947e4a6d22971ea793e4b4bc2b09d8ab8cc04d0`. The
[historical publication receipt](validation/stacks-verdier-a04446e-1-2-13-r1-release-2026-08-26.json)
binds its exact CI run and anonymous raw-byte inventory. Full validation omits
`--pre-publication` and independently rechecks the public ref, every decisive
row, and the recorded GitHub Actions run after current publication evidence has
been added.

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
