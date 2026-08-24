# Tôhoku-to-Stacks r71 terminal formalization release

This successor preserves the complete eight-file inventory of the latest
Tôhoku French/English edition and adds the terminal r71 statement-level mapping,
append-only source repairs, audited Stacks source surfaces, deterministic build
evidence, and reproduction tools.

## Terminal mapping result

The r71 dossier records:

- 991 audited source units;
- 1,066 append-only decisions;
- 679 decided units;
- 33 resolved source issues and 0 active source issues;
- 0 review units;
- 0 candidate units; and
- 0 remaining gap-class dispositions.

The r71 successor appends exactly four final mapping closures (`D001063` through
`D001066`) and one resolved source issue (`I000033`) over the sealed r70 dossier.
It changes four unit rows and preserves the other 987 unit rows. The source
scanner covers 119 top-level TeX files, 22,116 labels, and reports no errors.

## Append-only source repairs and builds

The final repair surface is bound to `cohomology.tex`, `divisors.tex`, and
`homology.tex`. Their corresponding PDFs were rebuilt and checked:

- `cohomology.pdf` — SHA-256
  `146ADB22B666F2069B794535AA360D2F969F5BC0A2521CA7119AEE6AD728FF8D`;
- `divisors.pdf` — SHA-256
  `6B480E31B285358CDFB03BCEADB556F602112F2B43DAD7ACC5504C4DFF666487`;
- `homology.pdf` — SHA-256
  `75AAB417A5EB5E39C3D29A3FEF2DA824A19FC58E0132FA0092C3A47F72D2CE67`.

The terminal receipt binds the exact source, PDF, log, mapping, audit, contract,
and builder identities. The public source-repair audit is a semantics-preserving
privacy projection: ten local home-directory prefixes are replaced by the
literal marker `[LOCAL_HOME]`; no semantic field is removed. Its wrapper records
the original private audit's byte count and SHA-256.

## Files and verification

Files `70_` through `105_` contain this README, the non-self-referential manifest,
the r71 dossier, formalization audits, exact-source reviews, three Stacks source
chapters and their PDFs, the privacy-projection builder, and the restart-safe
Zenodo publisher. The manifest records local path, remote filename, byte count,
MD5, and SHA-256 for every new file except itself.

The publisher validates all receipt-bound identities, admits only an exact
inherited inventory plus an exact subset of the frozen payload, persists a
sanitized transaction state before remote mutation, resumes partial uploads,
recovers the publish-response crash window, verifies stable metadata, and
anonymously downloads every new public file for SHA-256 comparison.

## Rights and provenance

The successor inherits the edition record's citation, rights, and provenance
metadata without alteration. The mapping and build artifacts document the
formalization work and do not grant additional rights in the underlying source
edition or third-party materials.
