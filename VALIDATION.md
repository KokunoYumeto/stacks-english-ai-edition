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
- 22 admitted overlays containing exactly 559 stable IDs at Verdier registry
  cutoff `60f1d97ecbd376ff7a91298d17e1f162b9996c3a`;
- the final immutable Verdier candidate, its 12 stable units, 27 manifest
  references, independent replay, rights boundary, and exact registered
  insertion into `derived.tex`;
- the preserved historical R1–R21 snapshot: 21 Stacks errata batches, 547
  correction IDs, all 591 v2 operations, the 120-operation R18–R21 replay, and
  the prior cutoff `13ca6aaaca454f5930c4885c93f427e30cf21959`;
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

The current Verdier v4 build result is recorded at
[`validation/stacks-verdier-a04446e-1-2-13-r1-build-2026-08-26.json`](validation/stacks-verdier-a04446e-1-2-13-r1-build-2026-08-26.json).
All 22 required chapters (2,343 pages; 24,390,066 PDF bytes) compiled
successfully, were readable by `pdfinfo`, and reached a global PDF fixed point
on sweep four. The build is bound to source commit
`7ee4b3a46e995e9e36b259bbc9300828c3c6988b`, tree
`5b3349e5944ecf9d0718c6a31728a457adcd1c69`. Aggregate diagnostics contain
zero fatal, missing-glyph, undefined-reference, undefined-citation,
multiply-defined, rerun-required, or destination-warning markers.

Visual QA rendered and reviewed all 130 pages of the affected `derived.pdf`;
pages 9–11 were also inspected individually at 220 DPI around the complete
page-10 insertion. The current
[visual receipt](validation/stacks-verdier-a04446e-1-2-13-r1-visual-qa-2026-08-26.json)
records zero clipped, overlapping, blank, corrupt, missing-glyph, or
broken-diagram defects. A second build ran independently in a parallel linked
worktree. Both runs use the same source, builder, environment, and fixed-point
sweep, and all 22 `{stem, pages, bytes, sha256}` tuples are exactly equal. See
the [reproducibility summary](validation/stacks-verdier-a04446e-1-2-13-r1-reproducibility-2026-08-26.json)
and [second full receipt](validation/stacks-verdier-a04446e-1-2-13-r1-reproducibility-second-2026-08-26.json).

The [source composition receipt](validation/composition-current.json) records
the Verdier cutoff `60f1d97ecbd376ff7a91298d17e1f162b9996c3a`, linear
registry import `2b4328c7caf2fc698ab2b0534385c576a74fa7c3`, and exact
composition source `39d99b0080b1f55e1d924cb73134dca885274e3f`. It binds the
449,715-byte `derived.tex` preimage
`66D17FBE6743002D29A78543E46122CD3ED34AA5A5574B14718C1189ACEB456F`,
the 2,339-byte payload, and the 452,054-byte postimage
`8B389993D3B364A926C7DCD7AD598E5B8245D8E92BCC5A23646069F9AD617860`.
The historical R21 composition, build, publication, and readback receipts
remain preserved and validated against their own immutable source snapshot;
they are not rebound to the Verdier tree.

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
