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

- Current integrated overlays: **27**, containing **846 stable IDs**.
- Current cutoff: R26 admission commit
  `a7c4a3c52b9a32e96e0f4b98f9579369026d9e1b`, tree
  `93af84d65d7b250fe0f4d660782ccf330b9e4743`.
- The Stacks errata subset is **R1–R26**: 26 batches, 834 correction IDs, and
  947 exact v2 operations. Its highest identifier is `MC-STK-ERR-1201`; gaps
  are intentional.
- The 22nd overlay is `stacks-verdier-a04446e-1-2-13-r1`, an independently
  written historical-source insertion with 12 non-official stable units. It
  claims no official Stacks tag, upstream review, approval, or endorsement.

The authoritative overlay list is
[`registry/overlays.json`](registry/overlays.json). The integrated root source
contains the admitted R1–R21 composition, the separately composed Verdier
insertion, the R22-before-R23 `more-algebra.tex` composition, the R24
`spaces-duality.tex` composition, the R25 `artin.tex` composition, and the R26
`smoothing.tex` composition;
registry admission and source composition remain separately testable states.
R21 is replayed as exact manifest-bound operations over cumulative
`simplicial.tex`, and Verdier is inserted into cumulative `derived.tex` through
one unique unchanged context with exact prefix/suffix invariance.

R22 and R23 add 93 IDs and 106 operations affecting only `more-algebra.tex`.
R24 adds 38 IDs and 57 operations affecting only `spaces-duality.tex`. R25 adds
131 IDs and 154 manifest-bound operations affecting only `artin.tex`. R26 adds
25 IDs and 39 operations affecting only `smoothing.tex`. Every round is
composed in registry order from manifest operations; no isolated payload
replaces cumulative source wholesale. The R26 source composition is commit
`47c6b78e476e5644f5a7d0ca2ce4816b144a2411`, tree
`cbad56973a9e594743b596a5fd0fa291b490ae26`. Its 134,830-byte `smoothing.tex`
postimage has SHA-256
`85251479BB7D35D73CD5691C194D33B3ADC1BF245BCC248643D969DBBA0E7928`.

R26 candidate commit `d1f8c1b4654e8d63ea6380dfb5d2e256a6982121` has tree
`aca634a2dc857f97f6deb52cf4da5ba0792d6d23` and candidate subtree
`cc94b817fabf54d21c4914e5b7ebf8f168bac807`; the admitted registry was
imported at `ca00b6023be95e0e928d5c0380e24011756bb0ef`. Adjudication accepted 31
producer identities, aliased `SMOOTHING-002/003/004` to their R1 antecedents,
rejected `SMOOTHING-010`, and merged four repeated semantic groups before
materializing 25 new stable units.

The current R26 fixed-point receipts cover 24 PDFs, 2,437 pages, and 25,862,999
PDF bytes at source `c90a50300dcec156e9ea5fe0c8802c8e36bde81e`, tree
`651fff448fa41a4e7c38970eec169328002ac4f6`. Both linked-worktree builds are
byte-for-byte reproducible. All 37 pages of the affected `smoothing.pdf` passed
review, including 15 correction-locus pages inspected individually at high
resolution. Before R26 publication, the public R25 content head remains
`fb3e4cb4d834c4e28d84b6df41466ad8aaa71b42`; exact-head CI and anonymous
readback pass. The six-asset R25 preservation package is public and
byte-identical on GitHub and Zenodo version DOI `10.5281/zenodo.22143740` under
concept DOI `10.5281/zenodo.22135180`. Public `main` is the later R25
preservation head `795313c42799161a69eb2c3d2ae3fa4b40279dfd`, tree
`c2bf5e701c4e3b94d4124049aea1a36b41353ce1`.

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
