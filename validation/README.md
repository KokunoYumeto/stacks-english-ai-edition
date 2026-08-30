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

## Historical R24 composition and validation receipts

The historical validated source composition advanced the registry to **25
overlays / 690 stable IDs** at R24 admission cutoff
`6df734ecb3bef8f35770819d17a8d3e267b8e07a`, tree
`49b8e57e91f0bf04669b2ee93e3586cfb6919088`. The Stacks errata subset is
R1–R24: 24 batches, 678 correction IDs, and 754 exact v2 operations. R24 adds
38 IDs and 57 manifest-bound operations affecting only `spaces-duality.tex`.

The preserved R24 build and release receipts bind that cutoff, imported
candidate and registry bytes, exact operation replay, earlier source identities,
and source commit `10c1c62f371921cdafbaa5e89f438a821a013621`, tree
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

The [R24 release receipt](stacks-errata-a04446e-r24-release-2026-08-27.json)
binds public content head `50438757de89ec6e67385084d4a2d578707f5a37` to
its passing exact-head workflow and anonymous readback of 86 checked files
totaling 5,155,955 bytes, including both candidate PDFs.

The subsequent
[`ai-integrated-stacks-r24-publication-2026-08-28.json`](ai-integrated-stacks-r24-publication-2026-08-28.json)
preserves that validated R24 state as one six-asset package on both GitHub and
Zenodo. It records concept DOI `10.5281/zenodo.22135180`, version DOI
`10.5281/zenodo.22135181`, exact public downloads, and byte/SHA-256 equality
across both hosts.

## Historical R25 composition and validation receipts

The historical R25 composition advanced the registry to **26
overlays / 821 stable IDs** at R25 admission cutoff
`001f36d41504aecfa77201a04fedff16d37b00f0`, tree
`f8e3a8ea8d7e95190b3cb4d21eb701a6709f90c7`. The Stacks errata subset is
R1–R25: 25 batches, 809 correction IDs, and 908 exact v2 operations. R25 adds
131 IDs and 154 manifest-bound operations affecting only `artin.tex`.

The preserved R25 build and release receipts bind that cutoff, imported
candidate and registry bytes, exact operation replay, earlier source identities,
and source commit `63dfd5f1499bea1916f64256056a5a37bcfb8f9a`, tree
`7ab863452c932dd5ef230f65abdfa5bdcd6b5771`.

The current evidence is recorded in:

- [`stacks-errata-a04446e-r25-build-2026-08-28.json`](stacks-errata-a04446e-r25-build-2026-08-28.json)
  — source `a13d609ba9b146eac0a72f593bcf8aff5c5a6a33`, tree
  `fbf8d6341b22298d05fdc1f72d547907bc164077`, 24 PDFs, 2,437 pages,
  25,862,634 bytes, fixed point on sweep four, and zero listed serious
  diagnostics;
- [`stacks-errata-a04446e-r25-visual-qa-2026-08-28.json`](stacks-errata-a04446e-r25-visual-qa-2026-08-28.json)
  — all 69 pages of `artin.pdf` reviewed and all 63 correction-locus pages
  inspected at high resolution with zero recorded rendering defects; and
- [`stacks-errata-a04446e-r25-reproducibility-2026-08-28.json`](stacks-errata-a04446e-r25-reproducibility-2026-08-28.json)
  together with the [second full receipt](stacks-errata-a04446e-r25-reproducibility-second-2026-08-28.json)
  — exact equality of all 24 artifact identities across two independent linked
  worktree builds.

The [R25 release receipt](stacks-errata-a04446e-r25-release-2026-08-28.json)
binds public content head `fb3e4cb4d834c4e28d84b6df41466ad8aaa71b42`
to its passing exact-head workflow and anonymous readback of 78 R25-changed
paths totaling 4,746,502 bytes. The subsequent
[`ai-integrated-stacks-r25-publication-2026-08-28.json`](ai-integrated-stacks-r25-publication-2026-08-28.json)
records the byte-identical six-asset GitHub and Zenodo release: 171,723,585
bytes, concept DOI `10.5281/zenodo.22135180`, and version DOI
`10.5281/zenodo.22143740`.

R25 remains publicly preserved as an immutable historical version in the same
GitHub release and Zenodo concept lineages.

## Historical R26 composition and validation receipts

The historical R26 source composition advanced the registry to **27
overlays / 846 stable IDs** at R26 admission cutoff
`a7c4a3c52b9a32e96e0f4b98f9579369026d9e1b`, tree
`93af84d65d7b250fe0f4d660782ccf330b9e4743`. The Stacks errata subset is
R1–R26: 26 batches, 834 correction IDs, and 947 exact v2 operations. R26 adds
25 IDs and 39 manifest-bound operations affecting only `smoothing.tex`; its
highest stable identifier is `MC-STK-ERR-1201`.

The historical R26 evidence binds final candidate commit
`d1f8c1b4654e8d63ea6380dfb5d2e256a6982121`, tree
`aca634a2dc857f97f6deb52cf4da5ba0792d6d23`, candidate subtree
`cc94b817fabf54d21c4914e5b7ebf8f168bac807`, registry import
`ca00b6023be95e0e928d5c0380e24011756bb0ef`, and source composition commit
`47c6b78e476e5644f5a7d0ca2ce4816b144a2411`, tree
`cbad56973a9e594743b596a5fd0fa291b490ae26`. The cumulative 134,830-byte
`smoothing.tex` has SHA-256
`85251479BB7D35D73CD5691C194D33B3ADC1BF245BCC248643D969DBBA0E7928`.

The preserved R26 evidence is recorded in:

- [`stacks-errata-a04446e-r26-build-2026-08-28.json`](stacks-errata-a04446e-r26-build-2026-08-28.json)
  — source `c90a50300dcec156e9ea5fe0c8802c8e36bde81e`, tree
  `651fff448fa41a4e7c38970eec169328002ac4f6`, 24 PDFs, 2,437 pages,
  25,862,999 bytes, fixed point on sweep four, and zero listed serious
  diagnostics;
- [`stacks-errata-a04446e-r26-visual-qa-2026-08-28.json`](stacks-errata-a04446e-r26-visual-qa-2026-08-28.json)
  — all 37 pages of `smoothing.pdf` reviewed and all 15 correction-locus pages
  inspected at high resolution with zero recorded rendering defects; and
- [`stacks-errata-a04446e-r26-reproducibility-2026-08-28.json`](stacks-errata-a04446e-r26-reproducibility-2026-08-28.json)
  together with the [second full receipt](stacks-errata-a04446e-r26-reproducibility-second-2026-08-28.json)
  — exact equality of all 24 artifact identities across two independent linked
  worktree builds.

The
[`ai-integrated-stacks-r26-publication-2026-08-28.json`](ai-integrated-stacks-r26-publication-2026-08-28.json)
receipt binds the public R26 tag at commit
`7720e2fd3080c39b02275e34c67421ea9cff31d8`, tree
`cc3b7a21d57d07d70db1323487d125a2f69f98c8`, to the exact six-asset
[GitHub release](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r26-2026-08-28)
and [Zenodo version DOI `10.5281/zenodo.22146844`](https://doi.org/10.5281/zenodo.22146844)
under concept DOI `10.5281/zenodo.22135180`. Anonymous readback matched all
172,480,328 bytes on each host by filename, byte count, and SHA-256; all three
downloaded ZIPs passed CRC and member replay. The source projection records six
privacy replacements in four historical provenance files and preserves all
unchanged source payloads byte-for-byte.

R26 adjudication accepted 31 producer identities, aliased
`SMOOTHING-002/003/004` to existing R1 corrections, rejected
`SMOOTHING-010`, and merged the repeated semantic groups `005+031`,
`008+012+013+014`, `016+018`, and `017+019` before materializing 25 new stable
units. The active EGA I–IV integration program remains incomplete; its local
semantic review now reaches EGA I §6.4.13 and resumes at §6.5.1.

## Historical R27 composition, validation, and publication receipts

R27 advances the integrated registry to **28 overlays / 860 stable IDs** at
admission commit `8c0539a6a7aa001cc6152daee92d5c7a49bf6a93`, tree
`110a3006fcbb27b94c4170639aab56db507f9a89`. Its R1–R27 Stacks errata subset
contains 27 batches, 848 correction IDs, and 961 exact v2 operations. R27 adds
14 stable IDs and 14 manifest-bound operations affecting only cumulative
`modules.tex`.

The preserved R27 release evidence binds lease
`1f05772d6f46ab851cdecdf53b70c11ea698cb14`, candidate
`77fcc9fc2341e72b077224399743f1062e73b228`, admission
`8c0539a6a7aa001cc6152daee92d5c7a49bf6a93`, registry import
`f3bfc1b987ac9defc1b7811650bac0ec84a01373`, and source composition
`5a42b7d2a04c4d08be7861ec91306d8be05d631e`. The 211,777-byte
`modules.tex` postimage has SHA-256
`BA34DCC89DCEE1BD5F0B9D3C986B18EE9618F723C10E7C7FD3DBD80E9E0B2300`.

The R27 deterministic evidence is recorded in:

- [`stacks-errata-a04446e-r27-build-2026-08-28.json`](stacks-errata-a04446e-r27-build-2026-08-28.json)
  — 25 PDFs, 2,492 pages, 26,609,586 PDF bytes, fixed point on sweep four,
  and zero listed serious diagnostics;
- [`stacks-errata-a04446e-r27-visual-qa-2026-08-28.json`](stacks-errata-a04446e-r27-visual-qa-2026-08-28.json)
  — all 55 pages of `modules.pdf` reviewed and all 10 correction-locus pages
  inspected at high resolution with zero recorded rendering defects; and
- [`stacks-errata-a04446e-r27-reproducibility-2026-08-28.json`](stacks-errata-a04446e-r27-reproducibility-2026-08-28.json)
  together with the [second full receipt](stacks-errata-a04446e-r27-reproducibility-second-2026-08-28.json)
  — exact equality of all 25 artifact identities across two linked-worktree
  builds.

The [R27 release receipt](stacks-errata-a04446e-r27-release-2026-08-28.json)
binds public tag
[`ai-integrated-stacks-r27-2026-08-28`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r27-2026-08-28)
at commit `e624abadfe9e2ac1f311485c44c82d6c53df2df2`, tree
`a2ba195c47c6cb41dca4e4ee7cb6292372e2e201`, successful workflow run
`33198300432` attempt 2, and [Zenodo version DOI
`10.5281/zenodo.22149250`](https://doi.org/10.5281/zenodo.22149250) under concept
DOI `10.5281/zenodo.22135180`. The six assets total 174,411,900 bytes on each
host. All 12 anonymous downloads matched by filename, byte count, and SHA-256
with zero mismatches. The source archive is 154,505,160 bytes and contains
2,245 entries. R26 remains the preceding immutable historical release.

## Historical R28 composition, validation, and publication receipts

R28 advances the integrated registry to **29 overlays / 861 stable IDs** at
admission commit `655c8e0e1fe9e7b350244a0ef0230fb6c38e0026`, tree
`5eddd7d6db54d25eccf09cf21d5d7ab30c3ec1d3`. Its R1–R28 Stacks errata subset
contains 28 batches, 849 correction IDs, and 962 exact v2 operations. R28 adds
one supersession-aware replacement affecting cumulative `smoothing.tex`.

At the historical R28 checkpoint,
[`composition-current.json`](composition-current.json) bound the R28 registry
cutoff and source composition to the cumulative 962-operation projection; its
live successor now binds R30.

The historical R28 deterministic evidence is recorded in:

- [`stacks-errata-a04446e-r28-build-2026-08-28.json`](stacks-errata-a04446e-r28-build-2026-08-28.json)
  — 25 PDFs, 2,492 pages, 26,612,367 PDF bytes, fixed point on sweep four,
  and zero listed serious diagnostics;
- [`stacks-errata-a04446e-r28-visual-qa-2026-08-28.json`](stacks-errata-a04446e-r28-visual-qa-2026-08-28.json)
  — all 37 pages of `smoothing.pdf` reviewed, with correction-locus page 16
  inspected at high resolution and zero recorded rendering defects; and
- [`stacks-errata-a04446e-r28-reproducibility-2026-08-28.json`](stacks-errata-a04446e-r28-reproducibility-2026-08-28.json)
  together with the [second full receipt](stacks-errata-a04446e-r28-reproducibility-second-2026-08-28.json)
  — exact equality of all 25 artifact identities across two linked-worktree
  builds.

The [R28 release receipt](stacks-errata-a04446e-r28-release-2026-08-28.json)
binds the historical public tag
[`ai-integrated-stacks-r28-2026-08-28`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r28-2026-08-28)
at commit `efa46473cf8a73646ef1b6e32354e63ce20fd172`, tree
`fe139f1aedc35f02dbd10e5471ecb3c7fbed62e1`, successful workflow run
`33212304694` attempt 1, and [Zenodo version DOI
`10.5281/zenodo.22150671`](https://doi.org/10.5281/zenodo.22150671) under concept
DOI `10.5281/zenodo.22135180`. The six assets total 174,673,433 bytes on each
host. All 12 anonymous downloads matched by filename, byte count, and SHA-256
with zero mismatches. The source archive is 154,766,484 bytes and contains
2,312 entries. R27 remains the preceding immutable historical release.

## Current R31/R32 composition, validation, and publication receipts

R31 and R32 advance the integrated registry to **33 overlays / 1,035 stable
IDs** at the append-only successor
`cdea2e13a447e7cdcf5f6f805d3a767d907fd679`, tree
`b8466dd73dd960c73faeccb8d2c51fe44ecc4b14`. The R1–R32 Stacks errata
subset contains 32 batches, 1,023 correction IDs, and 1,159 exact v2
operations. Registry import is `3f0fa66780213432079c6c3044a6a515508b2576`;
manifest-only source composition is
`bb81deaa0f922caa8b4b4c1e85d928a03c955b24`, tree
`64fc6c472f50c901320fcf6702769a3dc5e58522`, with topology bound at
`e2c25bc25c6a650f6f4eb4069b4749fdc558163c`.

The deterministic evidence is:

- [`stacks-errata-a04446e-r32-build-2026-08-30.json`](stacks-errata-a04446e-r32-build-2026-08-30.json)
  — 27 PDFs, 2,614 pages, 28,121,719 PDF bytes, and fixed point on sweep four;
- [`stacks-errata-a04446e-r32-visual-qa-2026-08-30.json`](stacks-errata-a04446e-r32-visual-qa-2026-08-30.json)
  — all 700 affected-chapter pages and 72 mapped loci inspected with zero
  recorded rendering defects;
- [`stacks-errata-a04446e-r32-reproducibility-2026-08-30.json`](stacks-errata-a04446e-r32-reproducibility-2026-08-30.json)
  and the [second receipt](stacks-errata-a04446e-r32-reproducibility-second-2026-08-30.json)
  — exact equality of all 27 PDF identities; and
- [`stacks-errata-a04446e-r32-release-2026-08-30.json`](stacks-errata-a04446e-r32-release-2026-08-30.json)
  — the GitHub tag, Zenodo DOI `10.5281/zenodo.22167418`, complete anonymous
  readback, and current/inherited asset inventories.

## Historical R29/R30 composition, validation, and publication receipts

R29 and R30 advance the integrated registry to **31 overlays / 931 stable
IDs** at cutoff `256846d6a4193f21cd6e1af675dc09e6950aa3d6`, tree
`9a4f0ba1bd342cde5bf3f8f36a2d68cd7792aef3`. The R1–R30 Stacks errata
subset contains 30 batches, 919 correction IDs, and 1,033 exact v2 operations.
The registry import is `6df0e967030bcf818f3c49584fa5e9a992278d75`; exact
source composition is `3e57820736a5a57ddb1c9fbaaf2206e455b5ee31`, tree
`c4ce1faf96257fe11c0123ca649c9c020982aa33`. Validation and build policy are
bound by successor `c521604343534f94c7a59086c94b99712eb1d754`, tree
`4fe26c45da3edc493b8406824f90db06ef3df28c`.

The current deterministic evidence is:

- [`stacks-errata-a04446e-r30-build-2026-08-29.json`](stacks-errata-a04446e-r30-build-2026-08-29.json)
  — 26 PDFs, 2,572 pages, 27,531,529 PDF bytes, fixed point on sweep four,
  and zero listed serious diagnostics;
- [`stacks-errata-a04446e-r30-visual-qa-2026-08-29.json`](stacks-errata-a04446e-r30-visual-qa-2026-08-29.json)
  — all 111 affected pages reviewed and all 42 unique manifest-bound locus
  pages inspected at 180 DPI, with zero recorded rendering defects; and
- [`stacks-errata-a04446e-r30-reproducibility-2026-08-29.json`](stacks-errata-a04446e-r30-reproducibility-2026-08-29.json)
  together with the [second full receipt](stacks-errata-a04446e-r30-reproducibility-second-2026-08-29.json)
  — exact equality of all 26 artifact identities across two linked-worktree
  builds.

R29 contributes 31 operations to `sites-modules.tex`; R30 contributes 40 to
`injectives.tex`. The cumulative postimages are respectively 312,179 bytes /
SHA-256 `B097799584BD00B3D8046F62A0A56FCFE045516FD04D130C2A4C547CE3BB6C19`
and 105,225 bytes / SHA-256
`BDC721593BE0B491334C707B371A2EECD1787787903A71E059721BDB66C5AC04`.

The [R30 release receipt](stacks-errata-a04446e-r30-release-2026-08-29.json)
binds the current public errata preservation checkpoint at source head
`e3def48650c66c0d65978a04f67dea88bd8b42ac`, tree
`62bee382516e4a06df6746c5aa61a54b2fe6622f`, and GitHub tag
[`ai-integrated-stacks-r30-2026-08-29`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r30-2026-08-29).
Zenodo version DOI
[`10.5281/zenodo.22166456`](https://doi.org/10.5281/zenodo.22166456) is in the
existing `10.5281/zenodo.22135180` concept lineage. The same six assets total
178,510,756 bytes on each host; all 12 anonymous downloads matched by filename,
byte count, and SHA-256, and all three ZIPs passed reopen and complete-listing
checks. The package preserves 26 PDFs, 2,572 pages, and 27,531,529 PDF bytes.
R28 remains the preceding immutable historical errata release.

## Current EGA I §6.4 semantic publication receipt

The current public EGA semantic checkpoint covers EGA I through §6.4.13 and
sets §6.5.1 as the next cursor. The
[`ega-i-6.4-semantic-release-2026-08-29.json`](ega-i-6.4-semantic-release-2026-08-29.json)
receipt binds content commit `00adeb291487d04070b75bd0fd87759e3c43d3d3`,
annotated GitHub tag
[`ega-i-6.4-semantic-2026-08-29`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ega-i-6.4-semantic-2026-08-29),
exact-head workflow `33250683600`, and Zenodo version DOI
[`10.5281/zenodo.22161051`](https://doi.org/10.5281/zenodo.22161051) under concept
DOI `10.5281/zenodo.22135180`. Six assets totaling 174,783,585 bytes per host
matched across 12 public downloads, and all three ZIP member replays passed.
The checkpoint changes no root TeX or PDF; R32 remains the latest errata
release.

The follow-on
[`ega-i-6.4-semantic-metadata-readback-2026-08-29.json`](ega-i-6.4-semantic-metadata-readback-2026-08-29.json)
receipt binds the public metadata seal, its exact-head workflow, and anonymous
raw-byte readback of every changed path.
