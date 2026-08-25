# Stacks — English AI Edition

This repository maintains the independent English AI edition of Stacks: proved
source errata, exact correction overlays, deterministic composition records,
build evidence, and release provenance. It is paired with the literal GitHub
fork at <https://github.com/KokunoYumeto/stacks-project>.

The fork's `master` branch remains an exact upstream mirror. This repository
owns only independently proved AI-edition overlays and deterministic
composition records. Generated English-edition branches may later be written
to the fork by a dedicated composer, but translation and source-integration
tasks do not write those branches directly.

Simplified Chinese, Japanese, and Korean are separate editions. Each receives
its own GitHub repository and Zenodo concept/version lineage; their release
artifacts are not presented as branches or variants of this English edition.

## Bound state

- Upstream repository: <https://github.com/stacks/stacks-project>
- Commit: `a04446e57ec1fbc252a871afcec7752fb2807b14`
- Tree: `3feeb703b931a6e7259782c10e7d1575adc83e5e`
- Upstream licence text: GNU Free Documentation License 1.2, identified by
  [`upstream/stacks.lock.json`](upstream/stacks.lock.json)
- Registered overlays: **sixteen** (`stacks-errata-a04446e-r1`,
  `stacks-errata-a04446e-r2`, `stacks-errata-a04446e-r3`,
  `stacks-errata-a04446e-r4`, `stacks-errata-a04446e-r5`,
  `stacks-errata-a04446e-r6`, `stacks-errata-a04446e-r7`,
  `stacks-errata-a04446e-r8`, `stacks-errata-a04446e-r9`,
  `stacks-errata-a04446e-r10`, `stacks-errata-a04446e-r11`,
  `stacks-errata-a04446e-r12`, `stacks-errata-a04446e-r13`,
  `stacks-errata-a04446e-r14`, `stacks-errata-a04446e-r15`, and
  `stacks-errata-a04446e-r16`), each admitted
  from a manifest-complete candidate
  after independent replay.
- Active candidate-namespace leases: **four** (`fac`, `tohoku`, `gaga`,
  `errata/r17`). The first three are held by task
  `019fca5a-c29e-7330-acdc-c93f4a3dc9fb`; `errata/r17` is held by canon task
  `01a0256d-5693-77c1-96b2-cf37101e0c6c`.
- Imported historical integration branches: **zero**
- Generated editions or builds: **zero**

Existing mutable FGA, EGA, FAC, Tôhoku, and GAGA branches are deliberately not
imported. Each must first become a manifest-complete candidate with its own
stable IDs, provenance, decisions, tests, and review evidence.

Namespace leases are reservations, not mathematical or release admission. See
[`registry/leases.json`](registry/leases.json) and the candidate contract in
[`candidates/CONTRACT.md`](candidates/CONTRACT.md). A source-integration owner
may write only its leased candidate path. It may not modify the literal mirror,
locale trees, the overlay registry, or generated releases.

## Edition label

Every public output must state prominently:

> Independently maintained, AI-produced Stacks-derived edition. The Stacks
> Project authors and maintainers have not requested, reviewed, approved, or
> endorsed this edition.

“Stacks Project” identifies the upstream source. “English AI Edition” identifies
this independent edition and does not imply upstream affiliation or endorsement.
