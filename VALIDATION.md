# Validation

Validation is layered so that repository integrity, mathematical-source
composition, TeX compilation, and visual evidence are not conflated.

## Fast unified-repository gate

Run from the repository root:

```sh
python tools/validate_unified_repository.py
```

The gate verifies:

- ancestry of the pinned upstream, source-union, EGA, and protected linear
  registry/source history;
- 19 admitted registry entries containing exactly 507 stable correction IDs;
- exact candidate/source-map joins and presence of every v2 replacement span
  in the live source, including the 77 byte-bound R18–R19 operations;
- the frozen external registry cutoff, imported registry Git blob, source tree,
  authority tree, and exact changed-path set;
- the independent `injectives.tex` correction;
- required integration dossiers and public documentation;
- parseability of the live registry JSON files;
- relative links in the public Markdown landing documents; and
- absence of unresolved merge markers in the live root TeX source and public
  documentation.

The same gate runs in
[`validate.yml`](.github/workflows/validate.yml) with full Git history.

The current unified-tree build result is recorded in
[`validation/unified-fixed-point-2026-08-25-r19.json`](validation/unified-fixed-point-2026-08-25-r19.json):
all 21 required chapters (2,269 pages; 23,549,238 PDF bytes) compiled
successfully, were readable by `pdfinfo`, and reached a global PDF fixed point
on sweep four. The build is bound to source commit
`400159979d40624724fde62c36a9cbfe582ac6fd`, tree
`1b4375bc4b2c40503812baa54dcfca577d43a320`. The aggregate diagnostics contain
zero fatal, missing-glyph, undefined-reference, undefined-citation,
multiply-defined, rerun, or destination-warning markers; 2,164 standalone
cross-root references are classified as mechanically resolved external links.

The source composition receipt records the frozen external cutoff
`24861b306a34991c0da3d803f92d67e206c805da`, the linear registry import
`c06400fc323abb62990f37563cc31e9ae93fbf8e`, the composition source
`1f204fb27ff418fd0e75cb35ac8dab5256037f15`, and the exact `derived.tex`
projection SHA-256 `317B3A8E626BCCB3BC579DAB6AA57F4FDFEF513CA82805B02BCDC8C22FB8C1A1`.
The corresponding anonymous public readback inventory is preserved in the
[`R18–R19 release receipt`](validation/errata-r18-r19-release-2026-08-25.json).

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
