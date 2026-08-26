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
- 21 admitted registry entries containing exactly 547 stable correction IDs;
- exact candidate/source-map joins and all 591 v2 operations in the live
  source, including 43 new R20–R21 operations and the 120-operation bounded
  R18–R21 replay;
- the frozen external registry cutoff `13ca6aaa`, imported registry Git blob,
  source and authority trees, candidate/admission chain, and exact changed-path
  set (`derived.tex` and `simplicial.tex`);
- the independent `injectives.tex` correction;
- required integration dossiers and public documentation;
- parseability of the live registry JSON files;
- relative links in the public Markdown landing documents; and
- absence of unresolved merge markers in the live root TeX source and public
  documentation.

The same gate runs in
[`validate.yml`](.github/workflows/validate.yml) with full Git history.

The current unified-tree build result is recorded at the automation-stable path
[`validation/unified-fixed-point-2026-08-25-r19.json`](validation/unified-fixed-point-2026-08-25-r19.json).
Its JSON scope and source identities, not the compatibility filename, are
authoritative. All 22 required chapters (2,342 pages; 24,385,554 PDF bytes)
compiled successfully, were readable by `pdfinfo`, and reached a global PDF
fixed point on sweep four. The build is bound to tooling/build source commit
`8e9520aa30e0d538e71e787850bac91f5ddb35f9`, tree
`c63e22c9ec1fef6d5af3820f5f83bd316e51ae62`. Aggregate diagnostics contain
zero fatal, missing-glyph, undefined-reference, undefined-citation,
multiply-defined, rerun-required, or destination-warning markers.

Visual QA passed for all 202 review pages and an affected-page superset. The
independent linked-worktree rebuild gate also passed: both builds use the same commit,
tree, builder, and fixed-point sweep four, and all 22
`{stem, pages, bytes, sha256}` tuples are exactly equal. The
[second full receipt](validation/reproducibility-second-r21.json) is 19,440
bytes with SHA-256
`7DC3A3EEAA932B8804CC826D52FE0892445CE883FE27AF362A873392B7CA171A`.
The public [reproducibility summary](validation/reproducibility-r21.json) is
5,977 bytes with SHA-256
`A28E2D9DF4E333B052FBD1EA884F7585A9D07423B3EB98004B511C2EC8C75687`.
The validated R21 content fixed point was then fast-forwarded to public `main`
at `780f48fafbb46dc1057bf8fdcd339693fb44d6bf`, and anonymous byte readback of
the decisive public inventory matched the committed identities exactly.

The [source composition receipt](validation/composition-current.json) records
the frozen external cutoff
`13ca6aaaca454f5930c4885c93f427e30cf21959`, linear registry import
`e3b28d7d7068eb45d3348a57e201c49044826e86`, and composition source
`ef467614041d569e56a6c1758b8fe74b51d99f4a`. Its exact composed SHA-256
identities are `66D17FBE6743002D29A78543E46122CD3ED34AA5A5574B14718C1189ACEB456F`
for `derived.tex` and
`650ABA33A184CE9945DD70C04D83A3A4CBD6E540426B171E828336855DC97A0B`
for `simplicial.tex`. The automation-stable
[publication receipt path](validation/errata-r18-r19-release-2026-08-25.json)
records the R21 content head, exact public readback inventory, and the
successful metadata-head workflow used by the fail-closed validator.

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
