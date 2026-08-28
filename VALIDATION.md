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
- 27 admitted overlays containing exactly 846 stable IDs at R26 registry cutoff
  `a7c4a3c52b9a32e96e0f4b98f9579369026d9e1b`, tree
  `93af84d65d7b250fe0f4d660782ccf330b9e4743`;
- the final immutable Verdier candidate, its 12 stable units, 27 manifest
  references, independent replay, rights boundary, and exact registered
  insertion into `derived.tex`;
- the R1–R26 Stacks errata sequence: 26 batches, 834 correction IDs, and all
  947 v2 operations, including the ordered R22/R23 replay, the 57-operation R24
  replay in `spaces-duality.tex`, the 154-operation R25 replay in `artin.tex`,
  and the 39-operation R26 replay in `smoothing.tex`;
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

The current R26 build result is recorded at
[`validation/stacks-errata-a04446e-r26-build-2026-08-28.json`](validation/stacks-errata-a04446e-r26-build-2026-08-28.json).
All 24 required chapters (2,437 pages; 25,862,999 PDF bytes) compiled
successfully, were readable by `pdfinfo`, and reached a global PDF fixed point
on sweep four. The build is bound to source commit
`c90a50300dcec156e9ea5fe0c8802c8e36bde81e`, tree
`651fff448fa41a4e7c38970eec169328002ac4f6`. Aggregate diagnostics contain
zero fatal, missing-glyph, undefined-reference, undefined-citation,
multiply-defined, rerun-required, or destination-warning markers.

Visual QA rendered and reviewed all 37 pages of the affected `smoothing.pdf` at
96 DPI and inspected all 15 correction-locus pages individually at 180 DPI.
The current
[visual receipt](validation/stacks-errata-a04446e-r26-visual-qa-2026-08-28.json)
records zero clipped, overlapping, blank, corrupt, missing-glyph, or
broken-diagram defects. A second build ran independently in a parallel linked
worktree. Both runs use the same source, builder, environment, and fixed-point
sweep, and all 24 `{stem, pages, bytes, sha256}` tuples are exactly equal. See
the [reproducibility summary](validation/stacks-errata-a04446e-r26-reproducibility-2026-08-28.json)
and [second full receipt](validation/stacks-errata-a04446e-r26-reproducibility-second-2026-08-28.json).

The [source composition receipt](validation/composition-current.json) records
R26 cutoff `a7c4a3c52b9a32e96e0f4b98f9579369026d9e1b`, tree
`93af84d65d7b250fe0f4d660782ccf330b9e4743`, candidate commit
`d1f8c1b4654e8d63ea6380dfb5d2e256a6982121`, linear registry import
`ca00b6023be95e0e928d5c0380e24011756bb0ef`, and exact composition source
`47c6b78e476e5644f5a7d0ca2ce4816b144a2411`, tree
`cbad56973a9e594743b596a5fd0fa291b490ae26`. It binds 947 cumulative v2
operations, including the 39 new R26 operations, to the 134,830-byte
`smoothing.tex` postimage with SHA-256
`85251479BB7D35D73CD5691C194D33B3ADC1BF245BCC248643D969DBBA0E7928`.
Historical R24, R22/R23, Verdier, and R21 receipts remain preserved and
authoritative for their immutable source snapshots; they are not rebound to the
R26 tree.

R26 adjudication accepted 31 producer identities, resolved
`SMOOTHING-002/003/004` as aliases of existing R1 corrections, rejected
`SMOOTHING-010`, and merged four repeated semantic groups before materializing
25 new stable units. The candidate tree is
`aca634a2dc857f97f6deb52cf4da5ba0792d6d23` with candidate subtree
`cc94b817fabf54d21c4914e5b7ebf8f168bac807`.

The [current R26 release receipt](validation/stacks-errata-a04446e-r26-release-2026-08-28.json)
binds the validated content composition and build evidence. The public release
tag resolves to commit `7720e2fd3080c39b02275e34c67421ea9cff31d8`, tree
`cc3b7a21d57d07d70db1323487d125a2f69f98c8`, whose exact-head workflow passed.

The [cross-host preservation receipt](validation/ai-integrated-stacks-r26-publication-2026-08-28.json)
binds the exact six-file R26 package to the
[GitHub release](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r26-2026-08-28)
and [Zenodo record 22146844](https://doi.org/10.5281/zenodo.22146844), concept
DOI [`10.5281/zenodo.22135180`](https://doi.org/10.5281/zenodo.22135180).
Anonymous downloads from both hosts matched all six filenames and 172,480,328
bytes per host by byte count and SHA-256. All three downloaded ZIPs passed CRC
and member replay. The source projection contains 2,169 entries and records six
privacy replacements in four historical provenance files, with every unchanged
payload byte-identical to the bound Git archive. This preserves R26; it is not
evidence that the active EGA I--IV integration program is complete. Earlier
R25 and R24 receipts remain historical evidence for their exact versions.

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
