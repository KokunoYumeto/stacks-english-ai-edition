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

- Current integrated overlays: **22**, containing **559 stable IDs**.
- Current cutoff: Verdier admission commit
  `60f1d97ecbd376ff7a91298d17e1f162b9996c3a`.
- The Stacks errata subset remains **R1–R21**: 21 batches and 547 correction
  IDs. Its highest identifier is `MC-STK-ERR-0914`; gaps are intentional.
- The 22nd overlay is `stacks-verdier-a04446e-1-2-13-r1`, an independently
  written historical-source insertion with 12 non-official stable units. It
  claims no official Stacks tag, upstream review, approval, or endorsement.

The authoritative overlay list is
[`registry/overlays.json`](registry/overlays.json). The integrated root source
contains the admitted R1–R21 composition followed by the separately composed
Verdier insertion; registry admission and source composition remain separately
testable states. R21 is replayed as exact manifest-bound operations over the
cumulative `simplicial.tex`, preserving the independent AI-integrated additions
already present there. Verdier is inserted into cumulative `derived.tex` through
one unique unchanged context with exact prefix/suffix invariance.

R22 (`cec63f082819c0580c43f59790ab441260fe1ccc`, 83 stable units / 94
operations) and R23 (`49fc23ab2f3d94cc98f27bc0f315fb0da6f2c98a`, 10
stable units / 12 operations) are later admitted `more-algebra.tex` overlays.
They remain queued after this cutoff and must be composed in that order by
manifest operations only; neither payload may replace cumulative source
wholesale.

## Directory map

| Path | Role |
| --- | --- |
| [`registry/`](registry/) | Admitted overlays, namespace leases, locales, and releases |
| [`candidates/`](candidates/) | Immutable candidates, adjudication, exact source maps, replay, and rejected proposals |
| [`schemas/`](schemas/) | Machine-readable registry and candidate contracts |
| [`upstream/`](upstream/) | Pinned upstream identity and license hashes |
| [`RIGHTS.md`](RIGHTS.md) | Rights and attribution boundary |

Detailed integration dossiers for FAC, Tôhoku, GAGA, FGA, and EGA remain at
the repository root so that mathematical source, mapping evidence, and build
records can be browsed together. See the project [status dashboard](../STATUS.md).
