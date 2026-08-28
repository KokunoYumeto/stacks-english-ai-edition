# Errata and integration registry

This directory contains machine-readable provenance, correction overlays,
candidate contracts, replay evidence, schemas, and release records for the
[Unofficial AI-Integrated Stacks Project](../README.md). It is part of the
unified repository, not a separate edition.

> [!IMPORTANT]
> This is independently maintained, AI-produced work. The Stacks Project
> authors and maintainers have not requested, reviewed, approved, or endorsed
> this edition or its overlays.

## Bound upstream

- Official upstream repository:
  <https://github.com/stacks/stacks-project>
- Commit: `a04446e57ec1fbc252a871afcec7752fb2807b14`
- Tree: `3feeb703b931a6e7259782c10e7d1575adc83e5e`
- Upstream lock: [`upstream/stacks.lock.json`](upstream/stacks.lock.json)
- Upstream license boundary: [`RIGHTS.md`](RIGHTS.md)

## Integrated registry cutoff

- Current integrated overlays: **28**, containing **860 stable IDs**.
- Current cutoff: R27 admission commit
  `8c0539a6a7aa001cc6152daee92d5c7a49bf6a93`, tree
  `110a3006fcbb27b94c4170639aab56db507f9a89`.
- The Stacks errata subset is **R1–R27**: 27 batches, 848 correction IDs, and
  961 exact v2 operations. Its highest identifier is `MC-STK-ERR-1215`; gaps
  are intentional.
- The 22nd overlay is `stacks-verdier-a04446e-1-2-13-r1`, an independently
  written historical-source insertion with 12 non-official stable units. It
  claims no official Stacks tag, upstream review, approval, or endorsement.

The authoritative overlay list is
[`registry/overlays.json`](registry/overlays.json). The integrated root source
contains the admitted R1–R21 composition, the separately composed Verdier
insertion, the R22-before-R23 `more-algebra.tex` composition, the R24
`spaces-duality.tex` composition, the R25 `artin.tex` composition, the R26
`smoothing.tex` composition, and the R27 `modules.tex` composition;
registry admission and source composition remain separately testable states.
R21 is replayed as exact manifest-bound operations over cumulative
`simplicial.tex`, and Verdier is inserted into cumulative `derived.tex` through
one unique unchanged context with exact prefix/suffix invariance.

R22 and R23 add 93 IDs and 106 operations affecting only `more-algebra.tex`.
R24 adds 38 IDs and 57 operations affecting only `spaces-duality.tex`. R25 adds
131 IDs and 154 manifest-bound operations affecting only `artin.tex`. R26 adds
25 IDs and 39 operations affecting only `smoothing.tex`. R27 adds 14 IDs and
14 operations affecting only `modules.tex`. Every round is composed in
registry order from manifest operations; no isolated payload replaces
cumulative source wholesale. The R27 source composition is commit
`5a42b7d2a04c4d08be7861ec91306d8be05d631e`, tree
`ecbad57ee36b4fb290c80cb4d1f83eab50a47460`. Its 211,777-byte `modules.tex`
postimage has SHA-256
`BA34DCC89DCEE1BD5F0B9D3C986B18EE9618F723C10E7C7FD3DBD80E9E0B2300`.

R27 is bound by lease `1f05772d6f46ab851cdecdf53b70c11ea698cb14`,
candidate `77fcc9fc2341e72b077224399743f1062e73b228`, and admission
`8c0539a6a7aa001cc6152daee92d5c7a49bf6a93`. The candidate tree is
`6183d66d4f907b7b83f1b69dc799dcfe92a0f4d0`, its candidate subtree is
`fe8a24fb2c4e0279a22d9839364fb3ffd12367d8`, and the admitted registry was
imported at `f3bfc1b987ac9defc1b7811650bac0ec84a01373`. The exact R27 manifest
SHA-256 is `A4D03B8B47A1005B6DAC8B0EE4B9D0F4361E065E51D324B9634F38B51053DE3C`.

The current R27 fixed-point receipts cover 25 PDFs, 2,492 pages, and 26,609,586
PDF bytes at source `dc849731c9768048b993eb5a9df218118b817f40`, tree
`b3462d130dedb3b3c0625cab0d7a2d406114e17f`. Both linked-worktree builds are
byte-for-byte reproducible. All 55 pages of the affected `modules.pdf` passed
review, including 10 correction-locus pages inspected individually at high
resolution. R27 is validated pre-publication and no R27 GitHub release or
Zenodo version is claimed yet. The six-asset R26 preservation package remains
the latest published package and is public and byte-identical
on GitHub and Zenodo version DOI `10.5281/zenodo.22146844` under concept DOI
`10.5281/zenodo.22135180`. Its tag resolves to commit
`7720e2fd3080c39b02275e34c67421ea9cff31d8`, tree
`cc3b7a21d57d07d70db1323487d125a2f69f98c8`; exact-head CI and anonymous
readback of all six assets from both hosts pass with zero mismatches. The source
projection’s embedded manifest binds six privacy replacements in four
historical provenance files while preserving every unchanged source payload.

## Directory map

| Path | Role |
| --- | --- |
| [`registry/`](registry/) | Admitted overlays, namespace leases, locales, and releases |
| [`candidates/`](candidates/) | Immutable candidates, adjudication, exact source maps, replay, and rejected proposals |
| [`schemas/`](schemas/) | Machine-readable registry and candidate contracts |
| [`upstream/`](upstream/) | Pinned upstream identity and license hashes |
| [`RIGHTS.md`](RIGHTS.md) | Rights and attribution boundary |

Detailed dossiers for FAC, Tôhoku, GAGA, FGA, and EGA remain at the repository
root so that mathematical source, mapping evidence, and build records can be
browsed together. FAC, GAGA, and FGA have root-source additions; the sealed
Tôhoku r71 result is dossier-only and changes no live TeX; EGA has only bounded
partial root-source additions, while its complete English discovery and French
diplomatic editions remain separate read-only inputs. See the project
[status dashboard](../STATUS.md).
