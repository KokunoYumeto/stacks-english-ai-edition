# Stacks — English AI Edition

This repository maintains the independent English AI edition of Stacks: proved
source errata, exact correction overlays, deterministic composition records,
build evidence, and release provenance. Its public home is
<https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project>;
`main` is the canonical generated-source edition branch.

<https://github.com/KokunoYumeto/stacks-project> is retained only as a
provenance/canonical-upstream mirror and is not the AI-integrated edition. This
repository owns independently proved AI-edition overlays, deterministic
composition records, and the generated English edition. The dedicated
composer writes admitted overlays to `main`; translation tasks do not.

Simplified Chinese, Japanese, and Korean are separate editions. Each receives
its own GitHub repository and Zenodo concept/version lineage; their release
artifacts are not presented as branches or variants of this English edition.

## Bound state

- Upstream repository: <https://github.com/stacks/stacks-project>
- Commit: `a04446e57ec1fbc252a871afcec7752fb2807b14`
- Tree: `3feeb703b931a6e7259782c10e7d1575adc83e5e`
- Upstream licence text: GNU Free Documentation License 1.2, identified by
  [`upstream/stacks.lock.json`](upstream/stacks.lock.json)
- Registered overlays: **twenty-six** (`stacks-errata-a04446e-r1`,
  `stacks-errata-a04446e-r2`, `stacks-errata-a04446e-r3`,
  `stacks-errata-a04446e-r4`, `stacks-errata-a04446e-r5`,
  `stacks-errata-a04446e-r6`, `stacks-errata-a04446e-r7`,
  `stacks-errata-a04446e-r8`, `stacks-errata-a04446e-r9`,
  `stacks-errata-a04446e-r10`, `stacks-errata-a04446e-r11`,
  `stacks-errata-a04446e-r12`, `stacks-errata-a04446e-r13`,
  `stacks-errata-a04446e-r14`, `stacks-errata-a04446e-r15`,
  `stacks-errata-a04446e-r16`, `stacks-errata-a04446e-r17`,
  `stacks-errata-a04446e-r18`, `stacks-errata-a04446e-r19`,
  `stacks-errata-a04446e-r20`, `stacks-errata-a04446e-r21`,
  `stacks-errata-a04446e-r22`, `stacks-errata-a04446e-r23`,
  `stacks-errata-a04446e-r24`, `stacks-errata-a04446e-r25`, and
  `stacks-verdier-a04446e-1-2-13-r1`), each admitted
  from a manifest-complete candidate
  after independent replay.
- Active candidate-namespace leases: **four** (`fac`, `tohoku`, `gaga`,
  `errata/r26`). The first three are held by task
  `019fca5a-c29e-7330-acdc-c93f4a3dc9fb`; `errata/r26` is held by canon task
  `01a0256d-5693-77c1-96b2-cf37101e0c6c`.
- Imported historical integration branches on this registry branch: **zero**
- Generated English edition: public `main`, maintained by the dedicated
  composer from admitted overlays; registry admission does not itself imply
  source composition.

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
