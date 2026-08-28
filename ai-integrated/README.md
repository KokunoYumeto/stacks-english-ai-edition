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

- Current integrated overlays: **29**, containing **861 stable IDs**.
- Current cutoff: R28 admission commit
  `655c8e0e1fe9e7b350244a0ef0230fb6c38e0026`, tree
  `5eddd7d6db54d25eccf09cf21d5d7ab30c3ec1d3`.
- The Stacks errata subset is **R1–R28**: 28 batches, 849 correction IDs, and
  962 exact v2 operations. Its highest identifier is `MC-STK-ERR-1216`; gaps
  are intentional.
- The 22nd overlay is `stacks-verdier-a04446e-1-2-13-r1`, an independently
  written historical-source insertion with 12 non-official stable units. It
  claims no official Stacks tag, upstream review, approval, or endorsement.

The authoritative overlay list is
[`registry/overlays.json`](registry/overlays.json). The integrated root source
contains the admitted R1–R21 composition, the separately composed Verdier
insertion, the R22-before-R23 `more-algebra.tex` composition, the R24
`spaces-duality.tex` composition, the R25 `artin.tex` composition, the R26
`smoothing.tex` composition, the R27 `modules.tex` composition, and the R28
supersession-aware `smoothing.tex` composition;
registry admission and source composition remain separately testable states.
R21 is replayed as exact manifest-bound operations over cumulative
`simplicial.tex`, and Verdier is inserted into cumulative `derived.tex` through
one unique unchanged context with exact prefix/suffix invariance.

R22 and R23 add 93 IDs and 106 operations affecting only `more-algebra.tex`.
R24 adds 38 IDs and 57 operations affecting only `spaces-duality.tex`. R25 adds
131 IDs and 154 manifest-bound operations affecting only `artin.tex`. R26 adds
25 IDs and 39 operations affecting only `smoothing.tex`. R27 adds 14 IDs and
14 operations affecting only `modules.tex`. R28 adds one ID and one operation
affecting only `smoothing.tex`, superseding `MC-STK-ERR-1183-OP1`. Every round is composed in
registry order from manifest operations; no isolated payload replaces
cumulative source wholesale. The R28 source composition is commit
`1ed5b9fce0f75dec5ad551d32badd8e99abf058a`, tree
`28c377be399e04fb75f7568000c62e5cfafa291f`. Its 134,835-byte `smoothing.tex`
postimage has SHA-256
`85A37C95D5591632D11E7BE6775039638B6F5200B44729ABCEA1A644D9F5B056`.

R27 is bound by lease `1f05772d6f46ab851cdecdf53b70c11ea698cb14`,
candidate `77fcc9fc2341e72b077224399743f1062e73b228`, and admission
`8c0539a6a7aa001cc6152daee92d5c7a49bf6a93`. The candidate tree is
`6183d66d4f907b7b83f1b69dc799dcfe92a0f4d0`, its candidate subtree is
`fe8a24fb2c4e0279a22d9839364fb3ffd12367d8`, and the admitted registry was
imported at `f3bfc1b987ac9defc1b7811650bac0ec84a01373`. The exact R27 manifest
SHA-256 is `A4D03B8B47A1005B6DAC8B0EE4B9D0F4361E065E51D324B9634F38B51053DE3C`.

The current R28 fixed-point receipts cover 25 PDFs, 2,492 pages, and 26,612,367
PDF bytes at source `9a68186b09bfd9ac66c51359d94b22074d43ebbf`, tree
`fa91f3313576065f7ffa8a3c131435e5b764b162`. Both linked-worktree builds are
byte-for-byte reproducible. All 37 pages of the affected `smoothing.pdf` passed
review, including correction-locus page 16 inspected individually at high
resolution. R27 remains public as tag
[`ai-integrated-stacks-r27-2026-08-28`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r27-2026-08-28)
at commit `e624abadfe9e2ac1f311485c44c82d6c53df2df2`, tree
`a2ba195c47c6cb41dca4e4ee7cb6292372e2e201`, and Zenodo version DOI
[`10.5281/zenodo.22149250`](https://doi.org/10.5281/zenodo.22149250) under
concept DOI `10.5281/zenodo.22135180`. Workflow run `33198300432`, attempt 2,
passed. The six-asset package totals 174,411,900 bytes on each host; all 12
anonymous downloads matched by filename, byte count, and SHA-256 with zero
mismatches. The 154,505,160-byte source archive contains 2,245 entries. See the
[R27 release receipt](../validation/stacks-errata-a04446e-r27-release-2026-08-28.json).
R26 is the preceding immutable historical release.

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
