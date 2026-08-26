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

- Admitted overlay batches: **21** (`R1` through `R21`).
- Stable correction IDs in those batches: **547**.
- Highest stable identifier: `MC-STK-ERR-0914`; identifier gaps are
  intentional and retained.
- This subtree is bound to registry commit
  `13ca6aaaca454f5930c4885c93f427e30cf21959`. R22 was the next leased
  namespace at that cutoff; later admissions enter a subsequent cycle.

The authoritative overlay list is
[`registry/overlays.json`](registry/overlays.json). The integrated root source
contains the admitted R1–R21 composition; registry admission and source
composition remain separately testable states. R21 is replayed as exact
manifest-bound operations over the cumulative `simplicial.tex`, preserving
the independent AI-integrated additions already present there.

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
