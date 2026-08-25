# Agent operating contract

After compaction, restart, or uncertainty, summaries are locators only. Reread
`README.md`, `RIGHTS.md`, `upstream/stacks.lock.json`, every registry record,
the current Git state, and the latest accepted release before mutation.

Never push to official upstream. Never edit the literal mirror branch. Never
merge an historical mutable integration branch directly. One writer owns each
`commons/stacks/...` ancestor chain. Candidate admission, registry admission,
composition, translation, and independent replay are distinct transitions.
Preserve failures, rejected evidence, and superseded decisions append-only.

Before creating candidate material, resolve the exact active lease in
`registry/leases.json` and write only below its `candidate_path`. A lease is not
overlay admission. Candidate owners may add manifest-bound metadata and payload
only to their leased path; only the registrar may change lease records, and only
the composer/admitter may change `registry/overlays.json`, locale registries, or
release registries. Candidate manifests must satisfy
`schemas/candidate-manifest.schema.json` and `candidates/CONTRACT.md`.
