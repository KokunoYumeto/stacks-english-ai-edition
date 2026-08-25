# Pre-lease EGA overlay export proposal

This directory is a **prepared, non-admitted pre-lease export proposal** for
the future `KokunoYumeto/mathematics-commons-stacks` sidecar. It is not a
sidecar candidate and is not admission-ready. It exports the reviewed local
EGA-to-Stacks formalizations from `codex/ega-scaffold` without merging that
historical branch or writing to any translation tree.

The sidecar registry has not allocated an EGA namespace lease. Under the
sidecar writer contract, this proposal must remain outside that repository.
After a lease is issued, the payload must be rebuilt under the leased path as
`candidate.manifest.json` against the then-current central schema; this
directory must not simply be copied into the sidecar.

The immutable payload boundary is the exact difference between pinned Stacks
commit `a04446e57ec1fbc252a871afcec7752fb2807b14` and source commit
`dc37296a6ed6cc2947ee0c2c9c5d4c88195cb322` on six named TeX files. That
custody patch is then separated into:

- four mathematical formalization bundles containing seven new local labels;
- a dependent proof-refactor bundle; and
- an unrelated-corrections bundle.

The full custody patch is evidence, not an instruction to merge wholesale.
Future admission may select only reviewed component bundles and must preserve
their dependency order.

## Status and rights

- Lifecycle: `prelease_export_prepared`
- Mathematical review: `integrated_local_mirror`
- Official Stacks tags assigned: **none**
- Upstream acceptance or endorsement claimed: **no**
- Translation-tree writes: **none**
- Rights admission: **blocked pending a separately approved, hash-bound
  rights receipt**

Commons-authored metadata in this package may be treated as CC0. The patches
and any copied or modified Stacks content are not relicensed: the pinned
upstream source remains governed by the GNU Free Documentation License 1.2 or
later. The inserted EGA-derived mathematical prose has not been given a
separate redistribution-clearance receipt, so admission remains fail-closed.

## Rebuild and validation

From the repository root:

```text
python commons-candidates/mc-stacks-overlay-ega-integration-v1/build_candidate.py
python commons-candidates/mc-stacks-overlay-ega-integration-v1/validate.py
python commons-candidates/mc-stacks-overlay-ega-integration-v1/validate.py --admission
```

The first two commands validate this source-repository-local export closure.
They do not invoke the central sidecar validator and are not portable outside
the pinned `stacks-ega` Git object database. The third is a negative admission
preflight and must remain blocked until all of the following occur:

- the registrar allocates a non-overlapping EGA lease;
- the export is rebuilt under the leased canonical path and central schema;
- an independent sidecar replay passes; and
- the central rights manager supplies an approved hash-bound rights receipt.

The public reader statement is: independently maintained, AI-produced
Stacks-derived material; the Stacks Project authors and maintainers have not
requested, reviewed, approved, or endorsed it.
