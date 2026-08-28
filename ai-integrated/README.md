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

- Current integrated overlays: **26**, containing **821 stable IDs**.
- Current cutoff: R25 admission commit
  `001f36d41504aecfa77201a04fedff16d37b00f0`, tree
  `f8e3a8ea8d7e95190b3cb4d21eb701a6709f90c7`.
- The Stacks errata subset is **R1–R25**: 25 batches, 809 correction IDs, and
  908 exact v2 operations. Its highest identifier is `MC-STK-ERR-1176`; gaps
  are intentional.
- The 22nd overlay is `stacks-verdier-a04446e-1-2-13-r1`, an independently
  written historical-source insertion with 12 non-official stable units. It
  claims no official Stacks tag, upstream review, approval, or endorsement.

The authoritative overlay list is
[`registry/overlays.json`](registry/overlays.json). The integrated root source
contains the admitted R1–R21 composition, the separately composed Verdier
insertion, the R22-before-R23 `more-algebra.tex` composition, the R24
`spaces-duality.tex` composition, and the R25 `artin.tex` composition;
registry admission and source composition remain separately testable states.
R21 is replayed as exact manifest-bound operations over cumulative
`simplicial.tex`, and Verdier is inserted into cumulative `derived.tex` through
one unique unchanged context with exact prefix/suffix invariance.

R22 and R23 add 93 IDs and 106 operations affecting only `more-algebra.tex`.
R24 adds 38 IDs and 57 operations affecting only `spaces-duality.tex`. R25 adds
131 IDs and 154 manifest-bound operations affecting only `artin.tex`. Every
round is composed in registry order from manifest operations; no isolated
payload replaces cumulative source wholesale. The R25 source composition is
commit `63dfd5f1499bea1916f64256056a5a37bcfb8f9a`, tree
`7ab863452c932dd5ef230f65abdfa5bdcd6b5771`. Its 254,488-byte `artin.tex`
postimage has SHA-256
`F196752E6D872B3B888E57C7183B326287F1A241286991C075E4896996FD185B`.
`MORE-ALGEBRA-L-001..029` and `SMOOTHING-001..035` remain separate intake
evidence.

The current R25 fixed-point receipts cover 24 PDFs, 2,437 pages, and 25,862,634
PDF bytes at source `a13d609ba9b146eac0a72f593bcf8aff5c5a6a33`, tree
`fbf8d6341b22298d05fdc1f72d547907bc164077`. Both linked-worktree builds are
byte-for-byte reproducible. All 69 pages of the affected `artin.pdf` passed
review, including 63 correction-locus pages inspected individually at high
resolution. The preceding public R24 content head remains
`50438757de89ec6e67385084d4a2d578707f5a37` until the R25 publication
transaction and anonymous readback complete.

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
