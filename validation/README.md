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

## Historical Verdier v4 receipts

The Verdier release advanced the integrated registry to 22 overlays and 559
stable IDs by adding the independently written
`stacks-verdier-a04446e-1-2-13-r1` overlay after the historical R1–R21
composition. Its preserved evidence includes:

- [`stacks-verdier-a04446e-1-2-13-r1-build-2026-08-26.json`](stacks-verdier-a04446e-1-2-13-r1-build-2026-08-26.json)
  — 22 PDFs, 2,343 pages, 24,390,066 bytes, fixed point at sweep four, and zero
  listed serious diagnostics;
- [`stacks-verdier-a04446e-1-2-13-r1-visual-qa-2026-08-26.json`](stacks-verdier-a04446e-1-2-13-r1-visual-qa-2026-08-26.json)
  — all 130 affected pages reviewed, plus pages 9–11 at high resolution;
- [`stacks-verdier-a04446e-1-2-13-r1-reproducibility-2026-08-26.json`](stacks-verdier-a04446e-1-2-13-r1-reproducibility-2026-08-26.json)
  — exact equality of all 22 artifact identities across two parallel,
  independent linked-worktree builds; and
- the [Verdier publication receipt](stacks-verdier-a04446e-1-2-13-r1-release-2026-08-26.json),
  which binds public content head
  `4947e4a6d22971ea793e4b4bc2b09d8ab8cc04d0` to its passing workflow and
  anonymous readback inventory.

The historical R21 and Verdier receipts remain authoritative for their own
immutable snapshots. They are deliberately not treated as proof for the later
R22/R23 source tree.

## Historical R22/R23 receipts

The R22/R23 validated composition advanced the registry to 24 overlays and 652
stable IDs at cutoff `49fc23ab2f3d94cc98f27bc0f315fb0da6f2c98a`. The Stacks
errata subset is R1–R23: 23 batches, 640 correction IDs, and 697 exact v2
operations. R22 and R23 contribute 93 IDs and 106 operations affecting only
`more-algebra.tex`. Its historical evidence is recorded in:

- [`stacks-errata-a04446e-r22-r23-build-2026-08-27.json`](stacks-errata-a04446e-r22-r23-build-2026-08-27.json)
  — source `1e9771352840bd70224027d13e9b32546838ccd2`, tree
  `4a3b7398f7607b73ee5596d359e5cf7a401c2256`, 22 PDFs, 2,343 pages,
  24,389,773 bytes, fixed point at sweep four, and zero listed serious
  diagnostics;
- [`stacks-errata-a04446e-r22-r23-visual-qa-2026-08-27.json`](stacks-errata-a04446e-r22-r23-visual-qa-2026-08-27.json)
  — all 406 `more-algebra.pdf` pages reviewed and 63 correction-locus pages
  inspected at high resolution; and
- [`stacks-errata-a04446e-r22-r23-reproducibility-2026-08-27.json`](stacks-errata-a04446e-r22-r23-reproducibility-2026-08-27.json)
  together with the [second full receipt](stacks-errata-a04446e-r22-r23-reproducibility-second-2026-08-27.json)
  — exact equality of all 22 artifact identities across two independent linked
  worktree builds; and
- [`stacks-errata-a04446e-r22-r23-release-2026-08-27.json`](stacks-errata-a04446e-r22-r23-release-2026-08-27.json)
  — public content head `3c2b49fe0d20519de4ab06951ac2cb5151b68782`, successful
  exact-head CI, and anonymous byte/hash/blob readback of 138 files totaling
  25,024,008 bytes.

These receipts remain authoritative for their immutable R22/R23 source tree;
they are not build or publication evidence for the later R24 composition.

## Current R24 composition and validation receipts

The current validated source composition advances the registry to **25
overlays / 690 stable IDs** at R24 admission cutoff
`6df734ecb3bef8f35770819d17a8d3e267b8e07a`, tree
`49b8e57e91f0bf04669b2ee93e3586cfb6919088`. The Stacks errata subset is
R1–R24: 24 batches, 678 correction IDs, and 754 exact v2 operations. R24 adds
38 IDs and 57 manifest-bound operations affecting only `spaces-duality.tex`.

[`composition-current.json`](composition-current.json) binds that cutoff,
the imported candidate and registry bytes, exact operation replay, preserved
R21/Verdier/R22/R23 source identities, and source commit
`10c1c62f371921cdafbaa5e89f438a821a013621`, tree
`6ec98b8ee6919070a24130877d4eeb9e1a0e874b`.

The current evidence is recorded in:

- [`stacks-errata-a04446e-r24-build-2026-08-27.json`](stacks-errata-a04446e-r24-build-2026-08-27.json)
  — source `c3bc402b03dea3c5ac92c9e226645b5895a78887`, tree
  `626b67a2c32f4b2bc1b8ad7b4586cdb036b25a21`, 23 PDFs, 2,368 pages,
  24,949,361 bytes, fixed point on sweep four, and zero listed serious
  diagnostics;
- [`stacks-errata-a04446e-r24-visual-qa-2026-08-27.json`](stacks-errata-a04446e-r24-visual-qa-2026-08-27.json)
  — all 25 pages of `spaces-duality.pdf` inspected at high resolution with
  zero recorded rendering defects; and
- [`stacks-errata-a04446e-r24-reproducibility-2026-08-27.json`](stacks-errata-a04446e-r24-reproducibility-2026-08-27.json)
  together with the [second full receipt](stacks-errata-a04446e-r24-reproducibility-second-2026-08-27.json)
  — exact equality of all 23 artifact identities across two independent linked
  worktree builds.

Publication and public-readback metrics are recorded only after their separate
release receipt exists.

Successor registry head `53c517215ef542cfc987e2445a07bb23c7b120fb`
only materializes the active R25 lease. R25 is neither admitted nor composed.
The French `MORE-ALGEBRA-L-001..029` and `SMOOTHING-001..035` packets remain
unadmitted. No later intake is treated as part of the current composition.
