# Unified-build receipts

The preserved historical R21 build gate is recorded at the automation-stable path
[`unified-fixed-point-2026-08-25-r19.json`](unified-fixed-point-2026-08-25-r19.json).
The historical-looking filename is retained for automation compatibility; its
JSON schema, composition binding, source commit, and source tree define scope.
The earlier [`R1–R15 receipt`](unified-build-2026-08-25.json) remains preserved
as historical evidence for its exact source tree.

It binds the unified source commit and tree to:

- admitted errata replay through R21;
- all R4–R21 immutable manifest checks;
- all 591 exact v2 operations, including 43 new R20–R21 operations and the
  120-operation bounded R18–R21 replay, plus 69 earlier replacements, nine R1
  tag additions, and 21,819 unique permanent tags;
- exact cumulative identities for both `derived.tex` and `simplicial.tex`;
- EGA scaffold and pinned-map checks; and
- separate linked-worktree fixed-point builds of all 22 receipt-selected chapters.

All 22 PDFs (2,342 pages; 24,385,554 bytes) compiled successfully, were readable
by `pdfinfo`, and reached a global fixed point on sweep four from tooling/build
source `8e9520aa30e0d538e71e787850bac91f5ddb35f9`, tree
`c63e22c9ec1fef6d5af3820f5f83bd316e51ae62`. The aggregate serious diagnostic
classes are zero. PDF bytes are build artifacts; the committed receipt records
their page counts, byte counts, SHA-256 identities, and diagnostics without
placing generated binaries in the source tree.

Visual QA passed all 202 review pages and the affected-page superset. The
independent linked-worktree rebuild also passed with the same commit, tree, builder, and
fixed-point sweep; all 22 `{stem, pages, bytes, sha256}` tuples are exactly
equal. Its [`reproducibility-second-r21.json`](reproducibility-second-r21.json)
full receipt is 19,440 bytes with SHA-256
`7DC3A3EEAA932B8804CC826D52FE0892445CE883FE27AF362A873392B7CA171A`.
The public [`reproducibility-r21.json`](reproducibility-r21.json) summary is
5,977 bytes with SHA-256
`A28E2D9DF4E333B052FBD1EA884F7585A9D07423B3EB98004B511C2EC8C75687`.
The [publication receipt](errata-r18-r19-release-2026-08-25.json) binds these
gates to public content head `780f48fafbb46dc1057bf8fdcd339693fb44d6bf` and
records anonymous readback of the decisive public inventory.

## Current Verdier v4 receipts

The current release advances the integrated registry to 22 overlays
and 559 stable IDs by adding the independently written
`stacks-verdier-a04446e-1-2-13-r1` overlay after the historical R1–R21
composition. Its exact evidence is recorded in:

- [`composition-current.json`](composition-current.json) — admission,
  candidate, context, payload, preimage/postimage, and prefix/suffix bindings;
- [`stacks-verdier-a04446e-1-2-13-r1-build-2026-08-26.json`](stacks-verdier-a04446e-1-2-13-r1-build-2026-08-26.json)
  — 22 PDFs, 2,343 pages, 24,390,066 bytes, fixed point at sweep four, and zero
  listed serious diagnostics;
- [`stacks-verdier-a04446e-1-2-13-r1-visual-qa-2026-08-26.json`](stacks-verdier-a04446e-1-2-13-r1-visual-qa-2026-08-26.json)
  — all 130 affected pages reviewed, plus pages 9–11 at high resolution;
- [`stacks-verdier-a04446e-1-2-13-r1-reproducibility-2026-08-26.json`](stacks-verdier-a04446e-1-2-13-r1-reproducibility-2026-08-26.json)
  — exact equality of all 22 artifact identities across two parallel,
  independent linked-worktree builds.

The historical R21 receipts remain authoritative for their own immutable
snapshot. They are deliberately not treated as proof for the later Verdier
source tree.

The [Verdier publication receipt](stacks-verdier-a04446e-1-2-13-r1-release-2026-08-26.json)
binds public content head `4947e4a6d22971ea793e4b4bc2b09d8ab8cc04d0`,
the passing workflow, and exact anonymous readback identities for the decisive
source, candidate, registry, evidence, documentation, tooling, and candidate
build artifacts.
