# Stacks errata candidate R24

R24 is the source-materialized candidate for independently adjudicated corrections to `spaces-duality.tex` at Stacks Project commit `a04446e57ec1fbc252a871afcec7752fb2807b14`. The frozen authority is 80,778 bytes with SHA-256 `B13FFE40A679F3E86EA82972ED7955DD4FBCFD0D98F954936B0E5FBF56F92C7D`.

The frozen adjudication accepts 45 producer identities as 38 semantic units, assigns contiguous IDs `MC-STK-ERR-1008` through `MC-STK-ERR-1045`, and seals 57 nonoverlapping exact operations. `prepare-inputs.py` derives the intake ledgers from that spec and the frozen authority. `materialize.py` creates the authority closure and corrected payload. `verify-source.py` independently reconstructs the payload and writes `source-validation.json`.

The source-only payload is 80,995 bytes with SHA-256 `3CFCEF73EB9172CF69082FF07B9D84442DD5E545D8AD22917D5A694BAA57298E`. The source verification gate passes. The frozen semantic locus for `MC-STK-ERR-1040` is lines 1998–1999; its exact replacement interval is line 1998, as explicitly recorded in `INTAKE_VALIDATION.json` while preserving the frozen adjudication-spec bytes.

The isolated candidate and frozen-authority controls each build deterministically to 25 pages. The candidate PDF is 545,818 bytes with SHA-256 `133E4350908AC12FDE9E06C82E28031E79EDEE2C2A69B5D763A829434F444CEC`; the authority control is 545,653 bytes with SHA-256 `E9D76F06B7698CDE5A32F59A5DF5BF3AA88221C90795E75DFF7AF7E611C7CCA6`. Two fresh builds are byte-identical, the candidate and authority undefined cross-chapter target multisets agree, all 25 candidate pages and all 20 correction-bearing pages pass visual inspection, and the independent adverse replay is unconditional PASS. Candidate admission, registry mutation, generated-source composition, Git publication, and downstream release remain separate transitions.

The lease remains bound to registrar-issued `stacks-lease-000028-errata-r24`. The Stacks Project authors and maintainers have not requested, reviewed, approved, or endorsed this independently maintained AI-produced candidate. Upstream content remains under GNU Free Documentation License 1.2.
