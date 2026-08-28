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
- 26 admitted overlays containing exactly 821 stable IDs at R25 registry cutoff
  `001f36d41504aecfa77201a04fedff16d37b00f0`, tree
  `f8e3a8ea8d7e95190b3cb4d21eb701a6709f90c7`;
- the final immutable Verdier candidate, its 12 stable units, 27 manifest
  references, independent replay, rights boundary, and exact registered
  insertion into `derived.tex`;
- the R1–R25 Stacks errata sequence: 25 batches, 809 correction IDs, and all
  908 v2 operations, including the ordered R22/R23 replay, the 57-operation R24
  replay in `spaces-duality.tex`, and the 154-operation R25 replay in
  `artin.tex`;
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

The current R25 build result is recorded at
[`validation/stacks-errata-a04446e-r25-build-2026-08-28.json`](validation/stacks-errata-a04446e-r25-build-2026-08-28.json).
All 24 required chapters (2,437 pages; 25,862,634 PDF bytes) compiled
successfully, were readable by `pdfinfo`, and reached a global PDF fixed point
on sweep four. The build is bound to source commit
`a13d609ba9b146eac0a72f593bcf8aff5c5a6a33`, tree
`fbf8d6341b22298d05fdc1f72d547907bc164077`. Aggregate diagnostics contain
zero fatal, missing-glyph, undefined-reference, undefined-citation,
multiply-defined, rerun-required, or destination-warning markers.

Visual QA rendered and reviewed all 69 pages of the affected `artin.pdf` at
96 DPI and inspected all 63 correction-locus pages individually at 180 DPI.
The current
[visual receipt](validation/stacks-errata-a04446e-r25-visual-qa-2026-08-28.json)
records zero clipped, overlapping, blank, corrupt, missing-glyph, or
broken-diagram defects. A second build ran independently in a parallel linked
worktree. Both runs use the same source, builder, environment, and fixed-point
sweep, and all 24 `{stem, pages, bytes, sha256}` tuples are exactly equal. See
the [reproducibility summary](validation/stacks-errata-a04446e-r25-reproducibility-2026-08-28.json)
and [second full receipt](validation/stacks-errata-a04446e-r25-reproducibility-second-2026-08-28.json).

The [source composition receipt](validation/composition-current.json) records
R25 cutoff `001f36d41504aecfa77201a04fedff16d37b00f0`, linear registry
import `fb12027d697fce54f2f0d5fd1454f1e5069dd937`, and exact composition
source `63dfd5f1499bea1916f64256056a5a37bcfb8f9a`, tree
`7ab863452c932dd5ef230f65abdfa5bdcd6b5771`. It binds 908 cumulative
v2 operations, including the 154 new R25 operations, to the 254,488-byte
`artin.tex` postimage with SHA-256
`F196752E6D872B3B888E57C7183B326287F1A241286991C075E4896996FD185B`.
Historical R24, R22/R23, Verdier, and R21 receipts remain preserved and
authoritative for their immutable source snapshots; they are not rebound to the
R25 tree.

The [current public R25 release receipt](validation/stacks-errata-a04446e-r25-release-2026-08-28.json)
binds public content head `fb3e4cb4d834c4e28d84b6df41466ad8aaa71b42`,
tree `406a1c289c2d45f901de4356bd6e8d0ced48a661`, to its successful exact-head
workflow. Anonymous HTTPS readback matched 78 R25-changed paths totaling
4,746,502 bytes by filename, byte count, SHA-256, and Git blob.

The [cross-host preservation receipt](validation/ai-integrated-stacks-r25-publication-2026-08-28.json)
binds the exact six-file R25 package to the
[GitHub release](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r25-2026-08-28)
and [Zenodo record 22143740](https://doi.org/10.5281/zenodo.22143740), concept
DOI [`10.5281/zenodo.22135180`](https://doi.org/10.5281/zenodo.22135180).
Anonymous downloads from both hosts matched all six filenames and 171,723,585
bytes by byte count and SHA-256. This preserves R25; it is not evidence that the
active EGA I--IV integration program is complete. The R24 receipts remain
historical evidence for their exact source and package identities.

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
