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

- Current integrated overlays: **24**, containing **652 stable IDs**.
- Current cutoff: R23 admission commit
  `49fc23ab2f3d94cc98f27bc0f315fb0da6f2c98a`, tree
  `a67a8529b853da8834502456e8ca75afe71aa78c`.
- The Stacks errata subset is **R1–R23**: 23 batches, 640 correction IDs, and
  697 exact v2 operations. Its highest identifier is `MC-STK-ERR-1007`; gaps
  are intentional.
- The 22nd overlay is `stacks-verdier-a04446e-1-2-13-r1`, an independently
  written historical-source insertion with 12 non-official stable units. It
  claims no official Stacks tag, upstream review, approval, or endorsement.

The authoritative overlay list is
[`registry/overlays.json`](registry/overlays.json). The integrated root source
contains the admitted R1–R21 composition, the separately composed Verdier
insertion, and the R22-before-R23 `more-algebra.tex` composition; registry
admission and source composition remain separately testable states. R21 is
replayed as exact manifest-bound operations over cumulative `simplicial.tex`,
and Verdier is inserted into cumulative `derived.tex` through one unique
unchanged context with exact prefix/suffix invariance.

R22 (`cec63f082819c0580c43f59790ab441260fe1ccc`, 83 stable units / 94
operations) and R23 (`49fc23ab2f3d94cc98f27bc0f315fb0da6f2c98a`, 10
stable units / 12 operations) add 93 IDs and 106 operations affecting only
`more-algebra.tex`. They are composed in that order from manifest operations;
neither isolated payload replaces cumulative source wholesale. The external
registry lane subsequently admitted R24 at
`6df734ecb3bef8f35770819d17a8d3e267b8e07a`; its source composition is pending,
and successor head `53c517215ef542cfc987e2445a07bb23c7b120fb` materializes
the active R25 lease. `MORE-ALGEBRA-L-001..029` remains unadmitted intake
evidence.

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
