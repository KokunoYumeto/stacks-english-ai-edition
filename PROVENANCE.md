# Provenance and preserved histories

## Canonical upstream

The canonical external source is the official
[Stacks Project repository](https://github.com/stacks/stacks-project). This
unofficial derivative is pinned to upstream commit
`a04446e57ec1fbc252a871afcec7752fb2807b14`, tree
`3feeb703b931a6e7259782c10e7d1575adc83e5e`.

The upstream source and this modified source retain the GNU Free Documentation
License 1.2 recorded in [COPYING](COPYING). Nothing in this repository implies
upstream review or endorsement.

## Pre-unification repositories

Two public repositories previously split the work by workflow rather than by
mathematical product:

| Repository | Pre-unification role | Captured refs |
| --- | --- | --- |
| [`KokunoYumeto/stacks-project`](https://github.com/KokunoYumeto/stacks-project) | Full Stacks source plus FAC, GAGA, and FGA source branches, the Tôhoku mapping dossier, and the EGA partial-integration scaffold | `master` plus five `codex/*` integration branches |
| [`KokunoYumeto/unofficial-ai-integrated-stacks-project`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project) | Errata candidates, overlay registry, schemas, and replay evidence | `main` and `codex/stacks-cjk-canon` |

The split is now resolved in favor of one integrated public edition.
The former `stacks-project` fork is retained publicly as a read-only archive;
its six branch heads were verified unchanged after archival. Active integrated
development and publication now use this repository's protected `main` branch.

## Frozen full-history copies

Before unification, complete remote mirrors were fetched, checked with
`git fsck --full`, exported as Git bundles, and verified with
`git bundle verify`. GitHub reported no tags, release assets, Git LFS payloads,
or submodules in either input repository.

| Original repository | Bundle bytes | SHA-256 |
| --- | ---: | --- |
| `KokunoYumeto/stacks-project` | 241,336,664 | `0DFA9F785757BE07D755DB315947A90ECB18DA4152666CAFEAE4ADDDB47FF74D` |
| `KokunoYumeto/unofficial-ai-integrated-stacks-project` | 14,610,301 | `B048584F27D4A9482FC9040D4946024F3584FCF71C66DA245D1B879AF912E9A3` |

The preservation release is
[`pre-unification-snapshots-2026-08-25`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/pre-unification-snapshots-2026-08-25).
The exact validation, preservation, publication, and public-readback identities
are recorded in the machine-readable
[`release receipt`](validation/unification-release-2026-08-25.json).

## Unification method

The histories were combined without flattening either input:

1. The source union at `ad58625f60e6816905ff217d21d91b07b2722fcf`
   supplied the FAC, GAGA, and FGA source additions, notation-normalized Stacks
   tree, and the Tôhoku dossier-only mapping history. The sealed Tôhoku r71
   successor changes no live TeX.
2. EGA scaffold and export history through
   `91df7f1c96bd4973264c29b0e121253a05d1d361` was merged into that source.
   Only bounded local EGA additions are composed into root TeX; the complete
   English discovery and French diplomatic editions remain separate read-only
   inputs.
3. The complete registry content through the frozen external cutoff
   `13ca6aaaca454f5930c4885c93f427e30cf21959` was transferred byte-for-byte
   under `ai-integrated/`. The integrated linear history records that transfer
   as import `e3b28d7d7068eb45d3348a57e201c49044826e86`; the external cutoff
   remains provenance and is not asserted as a `main` ancestor.
4. Each admitted errata batch R1–R21 is manifest-bound and composed in registry
   order. R20 extends the cumulative `derived.tex` projection. R21 is replayed
   onto the verified cumulative `simplicial.tex`, preserving earlier
   AI-integrated additions outside its operations. The resulting source is
   committed at `ef467614041d569e56a6c1758b8fe74b51d99f4a`, tree
   `b181820f096c3b78b6608429e477aaa8acd614c4`, as a direct linear successor
   of the registry import.
5. The independent `injectives.tex` correction was carried into the unified
   source.
6. The separately admitted Verdier II.1.2.13 contribution was composed through
   its unique unchanged context in cumulative `derived.tex`, preserving the
   R1–R21 source and claiming no official Stacks tag or upstream endorsement.
7. Registry content through R23 cutoff
   `49fc23ab2f3d94cc98f27bc0f315fb0da6f2c98a`, tree
   `a67a8529b853da8834502456e8ca75afe71aa78c`, was imported into the linear
   integrated history at `806ed1d11943f5a66b17b75f9fddccd61f58b62b`.
   R22 and R23 were then composed in registry order by replaying 106
   manifest-bound operations onto cumulative `more-algebra.tex`. The resulting
   source commit is `3a1100a79abc76315592711c9f2c86ad21b5f6a9`, tree
   `28980ba358cadddecc67d5013c7a9b624fee6305`.
8. Registry content through the R25 admission cutoff
   `001f36d41504aecfa77201a04fedff16d37b00f0`, tree
   `f8e3a8ea8d7e95190b3cb4d21eb701a6709f90c7`, together with the successor
   R26 lease pointer, was imported at
   `fb12027d697fce54f2f0d5fd1454f1e5069dd937`. R25 was then composed by
   replaying its 154 manifest-bound operations onto cumulative `artin.tex`.
   The resulting source commit is
   `63dfd5f1499bea1916f64256056a5a37bcfb8f9a`, tree
   `7ab863452c932dd5ef230f65abdfa5bdcd6b5771`.
9. The final R26 candidate was frozen at
   `d1f8c1b4654e8d63ea6380dfb5d2e256a6982121`, tree
   `aca634a2dc857f97f6deb52cf4da5ba0792d6d23`, with candidate subtree
   `cc94b817fabf54d21c4914e5b7ebf8f168bac807`. Admission cutoff
   `a7c4a3c52b9a32e96e0f4b98f9579369026d9e1b`, tree
   `93af84d65d7b250fe0f4d660782ccf330b9e4743`, was imported over public R25
   preservation head `795313c42799161a69eb2c3d2ae3fa4b40279dfd`, tree
   `c2bf5e701c4e3b94d4124049aea1a36b41353ce1`, at
   `ca00b6023be95e0e928d5c0380e24011756bb0ef`. R26 was then composed by
   replaying only its 39 manifest-bound operations onto cumulative
   `smoothing.tex`. The resulting source commit is
   `47c6b78e476e5644f5a7d0ca2ce4816b144a2411`, tree
   `cbad56973a9e594743b596a5fd0fa291b490ae26`.
10. R27 used an append-only leased-candidate topology after the R26 cutoff:
    lease `1f05772d6f46ab851cdecdf53b70c11ea698cb14`, candidate
    `77fcc9fc2341e72b077224399743f1062e73b228`, and admission
    `8c0539a6a7aa001cc6152daee92d5c7a49bf6a93`, tree
    `110a3006fcbb27b94c4170639aab56db507f9a89`. The admitted registry was
    imported linearly at `f3bfc1b987ac9defc1b7811650bac0ec84a01373`, then
    its 14 manifest-bound operations were replayed onto cumulative FAC-expanded
    `modules.tex`. The resulting source commit is
    `5a42b7d2a04c4d08be7861ec91306d8be05d631e`, tree
    `ecbad57ee36b4fb290c80cb4d1f83eab50a47460`.

The mathematical source therefore stays at the repository root while the
complete evidence and registry system remains browsable under
[`ai-integrated/`](ai-integrated/README.md).

The verified R21 build is separately bound to tooling/build source
`8e9520aa30e0d538e71e787850bac91f5ddb35f9`, tree
`c63e22c9ec1fef6d5af3820f5f83bd316e51ae62`. It produced 22 readable PDFs
(2,342 pages; 24,385,554 bytes) at fixed-point sweep four, with zero recorded
fatal or listed serious diagnostics. Visual QA passed all 202 review pages and
the affected-page superset. A separate linked-worktree reproduction also passed:
both builds use the same commit, tree, builder, and sweep, and all 22 artifact
identity tuples are exactly equal. The resulting R21 content fixed point is
public at `780f48fafbb46dc1057bf8fdcd339693fb44d6bf`; anonymous readback matched
the recorded public bytes and hashes.

The next separately admitted contribution is the independently written Verdier
II.1.2.13 overlay `stacks-verdier-a04446e-1-2-13-r1`, frozen at registry commit
`60f1d97ecbd376ff7a91298d17e1f162b9996c3a`. It adds one 2,339-byte
manifest-bound insertion to cumulative `derived.tex` through a unique unchanged
803-byte context. Prefix and suffix bytes remain unchanged, and the proposed
local label occurs exactly once. The candidate and source addition claim no
official Stacks tag, affiliation, review, approval, or upstream endorsement.
The historical Verdier fixed-point build is bound to source
`7ee4b3a46e995e9e36b259bbc9300828c3c6988b`, tree
`5b3349e5944ecf9d0718c6a31728a457adcd1c69`.

The historical R22/R23 fixed-point build is bound to source
`1e9771352840bd70224027d13e9b32546838ccd2`, tree
`4a3b7398f7607b73ee5596d359e5cf7a401c2256`. It preserves the Verdier
`derived.tex`, cumulative R21 `simplicial.tex`, and independent `injectives.tex`
identities while advancing `more-algebra.tex` through 93 new correction IDs and
106 operations. Two independent builds produced exactly matching identities
for all 22 PDFs: 2,343 pages, 24,389,773 bytes, and a global fixed point on
sweep four. Visual QA covers all 406 pages of `more-algebra.pdf` and 63
high-resolution correction-locus pages. These receipts remain authoritative
for that immutable R22/R23 tree and are not build or publication evidence for
the later R24 source composition.

The current validated R27 fixed-point build is bound to source
`dc849731c9768048b993eb5a9df218118b817f40`, tree
`b3462d130dedb3b3c0625cab0d7a2d406114e17f`. It preserves every earlier
composed source identity while advancing `modules.tex` through 14 new
correction IDs and 14 operations. Two independent linked-worktree builds
produced exactly matching identities for all 25 PDFs: 2,492 pages, 26,609,586
bytes, and a global fixed point on sweep four. Visual QA covers all 55 pages of
`modules.pdf`, including 10 correction-locus pages at high resolution. R27 is
validated pre-publication; this paragraph does not claim a public R27 release.

R26 remains the latest published preservation tag at commit
`7720e2fd3080c39b02275e34c67421ea9cff31d8`, tree
`cc3b7a21d57d07d70db1323487d125a2f69f98c8`, after a successful exact-head
workflow. The source, 24 PDFs, and validation evidence are preserved as six
byte-identical assets on GitHub and Zenodo version DOI
`10.5281/zenodo.22146844`, under concept DOI
`10.5281/zenodo.22135180`, as recorded by the
[cross-host receipt](validation/ai-integrated-stacks-r26-publication-2026-08-28.json).
Anonymous readback matched 172,480,328 bytes on each host across all 12
downloads. The deterministic source projection binds its exact Git preimage,
retains every unchanged payload byte-for-byte, and records six privacy
replacements in four historical build-provenance files in an embedded manifest.
R25 remains publicly preserved as the preceding immutable version.

## Branch preservation

The unified repository retains the pre-unification integration heads as
clearly named historical branches in addition to the integrated default
branch. Their presence is provenance, not a claim that they remain competing
editions. The published Verdier content release at
`4947e4a6d22971ea793e4b4bc2b09d8ab8cc04d0` remains historical evidence for
the 22-overlay / 559-ID cutoff at `60f1d97e`. The current validated source
composition advances the validated repository state to 28 overlays and 860
stable IDs at R27 cutoff `8c0539a6`; R22 and R23 affect only
`more-algebra.tex`, R24 affects only `spaces-duality.tex`, R25 affects only
`artin.tex`, R26 affects only `smoothing.tex`, and R27 affects only
`modules.tex`.
