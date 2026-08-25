# Candidate export and admission contract

A namespace lease is a single-writer reservation. It does **not** make the
candidate part of Stacks, the Mathematics Commons overlay, any translation, or
any release.

## Writer boundary

The task named by an active lease may write only below that lease's
`candidate_path`. It must not edit:

- the byte-faithful `stacks-project` mirror;
- `registry/leases.json` or any other task's candidate path;
- `registry/overlays.json`, `registry/locales.json`, or `registry/releases.json`;
- generated locale branches or release artifacts.

Registrar, candidate owner, overlay admitter/composer, translator, and
independent replay are separate roles even when one AI system later performs
more than one role in separate, receipt-bound transitions.

## Required candidate closure

The candidate owner replaces the lease-only directory with a
`candidate.manifest.json` satisfying
`schemas/candidate-manifest.schema.json`. Every referenced ledger or artifact
must be inside the leased path and carry an uppercase SHA-256. The manifest must
bind:

1. lease ID, namespace, writer task, and exact Stacks upstream commit/tree;
2. every source authority and source/build artifact with provenance and hash;
3. complete stable-unit inventory and source-to-candidate map;
4. append-only decisions, rejections, and supersession records;
5. formula and diagram classification/invariance evidence;
6. build artifacts and mechanical validation results;
7. rights state, actual review state, unresolved defects, and stop conditions;
8. an independent replay state that begins as `not_performed`.

Historical mutable branches are evidence inputs only. They are never merged
wholesale. A candidate export must be rebuilt from exact authorities into this
contract and must preserve rejected or failed evidence.

## Admission transition

Only a separate admission commit may append a record to
`registry/overlays.json`. Admission requires a complete candidate manifest,
manifest hash, nonempty stable IDs, exact source tree, review receipt, and an
independent replay result. A lease may be released or superseded only by an
append-only registrar event; editing an earlier lease event in place is invalid.
