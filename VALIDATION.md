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
- 24 admitted overlays containing exactly 652 stable IDs at R23 registry cutoff
  `49fc23ab2f3d94cc98f27bc0f315fb0da6f2c98a`, tree
  `a67a8529b853da8834502456e8ca75afe71aa78c`;
- the final immutable Verdier candidate, its 12 stable units, 27 manifest
  references, independent replay, rights boundary, and exact registered
  insertion into `derived.tex`;
- the R1–R23 Stacks errata sequence: 23 batches, 640 correction IDs, all 697 v2
  operations, and the manifest-bound R22-before-R23 replay of 106 operations
  affecting only `more-algebra.tex`;
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

The current R22/R23 build result is recorded at
[`validation/stacks-errata-a04446e-r22-r23-build-2026-08-27.json`](validation/stacks-errata-a04446e-r22-r23-build-2026-08-27.json).
All 22 required chapters (2,343 pages; 24,389,773 PDF bytes) compiled
successfully, were readable by `pdfinfo`, and reached a global PDF fixed point
on sweep four. The build is bound to source commit
`1e9771352840bd70224027d13e9b32546838ccd2`, tree
`4a3b7398f7607b73ee5596d359e5cf7a401c2256`. Aggregate diagnostics contain
zero fatal, missing-glyph, undefined-reference, undefined-citation,
multiply-defined, rerun-required, or destination-warning markers.

Visual QA rendered and reviewed all 406 pages of the affected
`more-algebra.pdf`; 63 correction-locus pages were also inspected at high
resolution. The current
[visual receipt](validation/stacks-errata-a04446e-r22-r23-visual-qa-2026-08-27.json)
records zero clipped, overlapping, blank, corrupt, missing-glyph, or
broken-diagram defects. A second build ran independently in a parallel linked
worktree. Both runs use the same source, builder, environment, and fixed-point
sweep, and all 22 `{stem, pages, bytes, sha256}` tuples are exactly equal. See
the [reproducibility summary](validation/stacks-errata-a04446e-r22-r23-reproducibility-2026-08-27.json)
and [second full receipt](validation/stacks-errata-a04446e-r22-r23-reproducibility-second-2026-08-27.json).

The [source composition receipt](validation/composition-current.json) records
R23 cutoff `49fc23ab2f3d94cc98f27bc0f315fb0da6f2c98a`, linear registry
import `806ed1d11943f5a66b17b75f9fddccd61f58b62b`, and exact composition
source `3a1100a79abc76315592711c9f2c86ad21b5f6a9`, tree
`28980ba358cadddecc67d5013c7a9b624fee6305`. It binds 697 cumulative v2
operations, including the 106 new R22/R23 operations, to the 1,517,988-byte
`more-algebra.tex` postimage with SHA-256
`69CD9E00183C17938EC4DFC1FF1EB33C292DDACF8B64AD054FD666054D2CBE2C`.
The historical R21 and Verdier composition, build, publication, and readback
receipts remain preserved and authoritative for their own immutable source
snapshots; they are not rebound to the R22/R23 tree.

The [current publication receipt](validation/stacks-errata-a04446e-r22-r23-release-2026-08-27.json)
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
- [Tôhoku r71 closure](tohoku_r71/STATUS.md)
- [GAGA r3 closure](gaga_r3/STATUS.md)
- [FGA post-merge audit](fga/audit.json)
- [EGA checker and active dossier](ega/README.md)
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
