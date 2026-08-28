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
- 28 admitted overlays containing exactly 860 stable IDs at R27 registry cutoff
  `8c0539a6a7aa001cc6152daee92d5c7a49bf6a93`, tree
  `110a3006fcbb27b94c4170639aab56db507f9a89`;
- the final immutable Verdier candidate, its 12 stable units, 27 manifest
  references, independent replay, rights boundary, and exact registered
  insertion into `derived.tex`;
- the R1–R27 Stacks errata sequence: 27 batches, 848 correction IDs, and all
  961 v2 operations, including the ordered R22/R23 replay, the 57-operation R24
  replay in `spaces-duality.tex`, the 154-operation R25 replay in `artin.tex`,
  the 39-operation R26 replay in `smoothing.tex`, and the 14-operation R27
  replay in `modules.tex`;
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

The current R27 build result is recorded at
[`validation/stacks-errata-a04446e-r27-build-2026-08-28.json`](validation/stacks-errata-a04446e-r27-build-2026-08-28.json).
All 25 required chapters (2,492 pages; 26,609,586 PDF bytes) compiled
successfully, were readable by `pdfinfo`, and reached a global PDF fixed point
on sweep four. The build is bound to source commit
`dc849731c9768048b993eb5a9df218118b817f40`, tree
`b3462d130dedb3b3c0625cab0d7a2d406114e17f`. Aggregate diagnostics contain
zero fatal, missing-glyph, undefined-reference, undefined-citation,
multiply-defined, rerun-required, or destination-warning markers.

Visual QA rendered and reviewed all 55 pages of the affected `modules.pdf` at
96 DPI and inspected all 10 correction-locus pages individually at 180 DPI.
The current
[visual receipt](validation/stacks-errata-a04446e-r27-visual-qa-2026-08-28.json)
records zero clipped, overlapping, blank, corrupt, missing-glyph, or
broken-diagram defects. A second build ran independently in a parallel linked
worktree. Both runs use the same source, builder, environment, and fixed-point
sweep, and all 25 `{stem, pages, bytes, sha256}` tuples are exactly equal. See
the [reproducibility summary](validation/stacks-errata-a04446e-r27-reproducibility-2026-08-28.json)
and [second full receipt](validation/stacks-errata-a04446e-r27-reproducibility-second-2026-08-28.json).

The [source composition receipt](validation/composition-current.json) records
R27 cutoff `8c0539a6a7aa001cc6152daee92d5c7a49bf6a93`, tree
`110a3006fcbb27b94c4170639aab56db507f9a89`, leased intake commit
`1f05772d6f46ab851cdecdf53b70c11ea698cb14`, candidate commit
`77fcc9fc2341e72b077224399743f1062e73b228`, linear registry import
`f3bfc1b987ac9defc1b7811650bac0ec84a01373`, and exact composition source
`5a42b7d2a04c4d08be7861ec91306d8be05d631e`, tree
`ecbad57ee36b4fb290c80cb4d1f83eab50a47460`. It binds 961 cumulative v2
operations, including the 14 new R27 operations, to the 211,777-byte
`modules.tex` postimage with SHA-256
`BA34DCC89DCEE1BD5F0B9D3C986B18EE9618F723C10E7C7FD3DBD80E9E0B2300`.
Historical R24, R22/R23, Verdier, and R21 receipts remain preserved and
authoritative for their immutable source snapshots; they are not rebound to the
R27 tree.

R27 admitted 14 stable units with 14 exact operations. Its manifest SHA-256 is
`A4D03B8B47A1005B6DAC8B0EE4B9D0F4361E065E51D324B9634F38B51053DE3C`,
payload SHA-256 is
`59C250D528258DCB8B2EB88234CA88AB48C1F5AB073EEA4618703F96BED4CE6B`,
and review-receipt SHA-256 is
`8D62F79E9E6CB44A0FD4E69B9D7D64CF41DDDD77DB0D2660436906078AB68C56`.
The candidate tree is `6183d66d4f907b7b83f1b69dc799dcfe92a0f4d0` with candidate
subtree `fe8a24fb2c4e0279a22d9839364fb3ffd12367d8`.

R27 is validated pre-publication and has no claimed R27 GitHub release or Zenodo
version at this stage. The [latest published R26 release receipt](validation/stacks-errata-a04446e-r26-release-2026-08-28.json)
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
