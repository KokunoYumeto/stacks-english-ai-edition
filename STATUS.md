# Integration status

Status date: **2026-08-27**

Pinned official upstream: `a04446e57ec1fbc252a871afcec7752fb2807b14`

This dashboard summarizes the live integrated tree. Detailed evidence remains
in each corpus dossier and in the machine-readable registry.

## Source integrations

| Workstream | Current state | Bounded claim |
| --- | --- | --- |
| FAC | Integrated | The full 661-target review is dispositioned. The dossier records 37 new theorem or lemma statements, seven source corrections, 27 corrected Stacks defects, successful validators, builds, and targeted visual inspection. |
| Tôhoku | Integrated through r71 | The sealed successor records 1,066 decisions, 679 decided units, 33 resolved source issues, and zero remaining gap-class dispositions. This does not convert the dossier's explicit nonclaims into a claim of upstream acceptance or an official release. |
| GAGA | Integrated through r3 | All 126 source units are classified; all 79 substantive units have reviewed decisions. The 23-page English chapter and deterministic mapping replay pass. The three previously dangling cross-reference targets are closed. |
| FGA | Integrated and normalized | The combined source contains the normalized FGA chapter and its post-merge dossier. The closure covers 1,253 units, 1,612 term links, and 579 append-only decisions; the recorded fixed-point Moduli build is 83 pages. |
| EGA | Active | Direct-French semantic review reaches EGA I 6.1.13. The active graph contains 1,059 edges across 355 generated units; the next semantic cursor is EGA I 6.2.1. |

## Errata state

- Current integrated registry: **24 overlays / 652 stable IDs**, frozen at R23
  admission commit `49fc23ab2f3d94cc98f27bc0f315fb0da6f2c98a`, tree
  `a67a8529b853da8834502456e8ca75afe71aa78c`.
- The Stacks errata component is **R1–R23**: 23 batches, 640 stable correction
  IDs, and 697 exact v2 operations. `MC-STK-ERR-1007` is the highest Stacks
  correction identifier through R23; intentional gaps mean it is not a count
  of corrections. R22–R23 add 93 IDs and 106 operations affecting only
  `more-algebra.tex`.
- The 22nd overlay is the separately admitted historical-source contribution
  `stacks-verdier-a04446e-1-2-13-r1`, containing 12 non-official stable units.
  It inserts the manifest-bound Lemma 4.15 into cumulative `derived.tex` through
  a unique unchanged context. No official Stacks tag or upstream endorsement is
  claimed.
- The prior Stacks-only external registry cutoff is
  `13ca6aaaca454f5930c4885c93f427e30cf21959`; the integrated history preserves
  its byte-for-byte registry import and R1–R21 composition as historical state.
- R20 is composed into `derived.tex`. R21 is operation-replayed onto the
  verified cumulative `simplicial.tex`, preserving earlier AI-integrated
  additions outside its manifest-bound operations.
- The independent `injectives.tex` parenthesis correction is included in the
  live source and retained in Git history.
- R22 and R23 are composed in registry order by replaying their manifest-bound
  operations onto cumulative `more-algebra.tex`; neither isolated payload
  replaces the integrated source. The rejected producer `MORE-ALGEBRA-J-006`
  remains excluded.
- R24 is the active errata intake lease. The 29-row French
  `MORE-ALGEBRA-L-001..029` packet remains unadmitted intake evidence and is not
  part of this composition or fixed point.

The authoritative registry is
[`ai-integrated/registry/overlays.json`](ai-integrated/registry/overlays.json).
Candidate manifests, source maps, adjudication, replay evidence, and rejected
proposals remain under
[`ai-integrated/candidates/commons/stacks/errata/`](ai-integrated/candidates/commons/stacks/errata/).

## Validation state

The repository integrity gate checks the pinned authority, protected linear
ancestry, all 24 registry entries and 652 stable IDs, the immutable Verdier,
R22, and R23 candidates, the retained Verdier insertion, all 697 exact v2
operations, exact manifest/source-map/payload/review joins, the independent
source correction, public-document links, JSON registries, and unresolved merge
markers. See [VALIDATION.md](VALIDATION.md).

Per-corpus build and visual receipts remain linked from the detailed dossiers;
they are not silently generalized beyond their recorded source identity.

The current R22/R23 gate built all 22 required chapters (2,343 pages and
24,389,773 PDF bytes) to a global PDF fixed point on sweep four. It is bound to
source `1e9771352840bd70224027d13e9b32546838ccd2`, tree
`4a3b7398f7607b73ee5596d359e5cf7a401c2256`, and records zero fatal,
missing-glyph, undefined-reference, undefined-citation, multiply-defined,
rerun-required, or destination-warning diagnostics. Visual QA passed for all
406 affected `more-algebra.pdf` pages and 63 high-resolution correction-locus
pages. The exact artifact inventory is in the
[current fixed-point build receipt](validation/stacks-errata-a04446e-r22-r23-build-2026-08-27.json).

The [parallel linked-worktree reproducibility gate](validation/stacks-errata-a04446e-r22-r23-reproducibility-2026-08-27.json)
is **PASS**. Both builds use the same commit, tree, builder, environment, and
fixed-point sweep; all 22 `{stem, pages, bytes, sha256}` artifact tuples are
exactly equal. The earlier Verdier and R21 fixed points remain preserved as
historical evidence for their exact source identities and scopes.

The preceding Verdier content release remains public at
`4947e4a6d22971ea793e4b4bc2b09d8ab8cc04d0`. Exact anonymous readback of 62
source, registry, candidate, receipt, documentation, tool, and candidate-build
artifact files is recorded in the
[historical Verdier publication receipt](validation/stacks-verdier-a04446e-1-2-13-r1-release-2026-08-26.json).
