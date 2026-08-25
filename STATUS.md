# Integration status

Status date: **2026-08-25**

Pinned official upstream: `a04446e57ec1fbc252a871afcec7752fb2807b14`

This dashboard summarizes the live integrated tree. Detailed evidence remains
in each corpus dossier and in the machine-readable registry.

## Source integrations

| Workstream | Current state | Bounded claim |
| --- | --- | --- |
| FAC | Integrated | The full 661-target review is dispositioned. The dossier records 37 new theorem or lemma statements, seven source corrections, 27 corrected Stacks defects, successful validators, builds, and targeted visual inspection. |
| Tôhoku | Integrated through r71 | The sealed successor records 1,066 decisions, 679 decided units, 33 resolved source issues, and zero remaining gap-class dispositions. This does not convert the dossier's explicit nonclaims into a claim of upstream acceptance or an official release. |
| GAGA | Integrated through r3 | All 126 source units are classified; all 79 substantive units have reviewed decisions. The 22-page English chapter and deterministic mapping replay pass. |
| FGA | Integrated and normalized | The combined source contains the normalized FGA chapter and its post-merge dossier. The closure covers 1,253 units, 1,612 term links, and 579 append-only decisions; the recorded fixed-point Moduli build is 83 pages. |
| EGA | Active | Direct-French semantic review reaches EGA I 6.1.13. The active graph contains 1,059 edges across 355 generated units; the next semantic cursor is EGA I 6.2.1. |

## Errata state

- Registered and composed: **R1–R17**.
- Registered batches: **17**.
- Stable correction IDs represented: **444**. The highest identifier is
  `MC-STK-ERR-0811`; the sequence contains intentional gaps, so this is not a
  claim of 811 corrections.
- R18 is the next leased candidate namespace; it is not an admitted overlay.
- The independent `injectives.tex` parenthesis correction is included in the
  live source and retained in Git history.

The authoritative registry is
[`ai-integrated/registry/overlays.json`](ai-integrated/registry/overlays.json).
Candidate manifests, source maps, adjudication, replay evidence, and rejected
proposals remain under
[`ai-integrated/candidates/commons/stacks/errata/`](ai-integrated/candidates/commons/stacks/errata/).

## Validation state

The repository integrity gate checks the required merge ancestry, all 17
registry entries and 444 stable IDs, exact replacement text for v2 overlay
operations, the independent source correction, public-document links, JSON
registries, and unresolved merge markers. See [VALIDATION.md](VALIDATION.md).

Per-corpus build and visual receipts remain linked from the detailed dossiers;
they are not silently generalized beyond their recorded source identity.

The current unified-tree gate additionally built 19 directly affected or
headline chapters to a global PDF fixed point on sweep four. The exact page,
byte, and SHA-256 inventory is in the
[`2026-08-25 build receipt`](validation/unified-build-2026-08-25.json).
