#!/usr/bin/env python3
"""Reconstruct the exact frozen R184 discovery tree from sealed R247."""

import argparse
import hashlib
import json
import tempfile
from pathlib import Path


MANIFEST_BYTES = 92_445
MANIFEST_SHA256 = "5C64ECD32FD7C5458D2599D70ED667D2CF06D95517EFFA9C6D6DCEF7626913A0"
TREE_SHA256 = "3BFB1C5103093481246EF4A6365E08544F6D5E19ACC0EA63E717F3F3643F064D"
SUCCESSOR_MANIFEST_BYTES = 53_306
SUCCESSOR_MANIFEST_SHA256 = "9A3652BA4E9A762DB0F9EA89A2B84FE26CE0DAD0BC97D3B9B3F7343C17CE4DB5"
SUCCESSOR_BYTES = 7_283_701
SUCCESSOR_TREE_SHA256 = "F152BFBC3AC3102DCE41975C27EEB373D01770F325639DF9AD01EFB6AD4F36D8"
R243_BYTES = 7_283_701
R243_TREE_SHA256 = "EB6A5465B872682311DD0DA7E6B633071A220C7FB957FCFB601795D5CBA1E39C"
R219_BYTES = 7_283_691
R219_TREE_SHA256 = "AD9F9A8A17882E5DF5EE4D1CFB1EAC03EBF5E22826B97A98207A2C220D106D22"


def sha(data):
    return hashlib.sha256(data).hexdigest().upper()


def read_sealed_successor(source, entries):
    """Read and validate one complete immutable R247 source snapshot."""
    source_data = {}
    source_rows = []
    for relative, entry in entries.items():
        data = (source / relative).read_bytes()
        if (len(data), sha(data)) != (entry["bytes"], entry["sha256"]):
            raise RuntimeError(f"live source differs from sealed R247: {relative}")
        source_data[relative] = data
        source_rows.append(f"{relative}\t{len(data)}\t{sha(data)}\n")
    if (sum(len(data) for data in source_data.values()),
            sha("".join(source_rows).encode("utf-8"))) != (
            SUCCESSOR_BYTES, SUCCESSOR_TREE_SHA256):
        raise RuntimeError("live source tree is not the sealed R247 successor")
    return source_data


def replace_at(data, offset, postimage, preimage, expected_bytes, expected_sha):
    if data[offset:offset + len(postimage)] != postimage:
        raise RuntimeError(f"inverse postimage moved at byte {offset}")
    result = data[:offset] + preimage + data[offset + len(postimage):]
    if (len(result), sha(result)) != (expected_bytes, expected_sha):
        raise RuntimeError(f"inverse result mismatch at byte {offset}")
    return result


def invert_r242_ega0_3(data):
    data = replace_at(
        data, 29_092, b"_", b"^", 47_182,
        "22B69BC82FE0378AB5ED16301CB28AE3CA6B440AB2687BA50A1970AF993A4911",
    )
    # R220's descriptive receipt gives stale character-derived offsets. The
    # exact UTF-8 byte offsets, proved by the predecessor hashes, are 26612
    # and 26320.
    data = replace_at(
        data, 26_612,
        b"(\\psi_*(\\sh{F}_2))_{\\psi(x)}\\ar[r]_{\\psi_x}",
        b"(\\psi_*(\\sh{F}_2))_{\\psi(x)}\\ar[r]^{\\psi_x}",
        47_182,
        "9D403486024CBCFBAFE3835BEB1A9EDF09CA642A292ACA2E3A7EBB48EBE41353",
    )
    return replace_at(
        data, 26_320,
        b"neither injective nor surjective",
        b"neither injective or surjective",
        47_181,
        "5CCAEF6A1ADDAC7043D435762145A5A34C6E4E2028E0A7D6688F0D8DCB7295EB",
    )


def invert_r242_ega0_4(data):
    return replace_at(
        data, 4_431, b"_", b"^", 33_207,
        "598BFADD2F888BA48703D8F7182D5D266A54894114CCCF99E57D19E8D572CC23",
    )


def invert_r242_ega0_5(data):
    return replace_at(
        data, 29_790, b"^*", b"", 41_622,
        "CDF520A527EDD63F59558253D0D553856D26AA0D57D430221B6BE93146A8D83B",
    )


def invert_r242_ega0_7(data):
    return replace_at(
        data, 27_599,
        (
            b"    \\widehat{A}^{\\,p}\\ar[r] &\n"
            b"    \\widehat{A}^{\\,q}\\ar[r] &\n"
            b"    \\widehat{M}\\ar[r] &\n"
            b"    0"
        ),
        (
            b"    \\widehat{A^p}\\ar[r] &\n"
            b"    \\widehat{A^q}\\ar[r] &\n"
            b"    \\widehat{M}\\ar[r] &\n"
            b"    0,"
        ),
        75_637,
        "96983D270206173230D51B70885CB846FD03BB1692D5DFAC03667EE7F4156252",
    )


def invert_r242_ega1_1(data):
    return replace_at(
        data, 64_219,
        b"B_{\\psi(x)}\\ar[r]_{\\theta_x^\\sharp} &",
        b"B_{\\psi(x)}\\ar[r]^{\\theta_x^\\sharp} &",
        78_943,
        "F32A8DB7385B1730556DB39FE0609B71BA1CC7E340D76BF87B5B9019FBC83764",
    )


def invert_r242_ega1_10(data):
    data = replace_at(
        data, 48_549, b"_", b"^", 143_891,
        "998124FF2641FE7022280BEECD17A4CD6491BE55C9E124FA4B2E4FA563A3BFAF",
    )
    data = replace_at(
        data, 47_794, b"_", b"^", 143_891,
        "E06496832D6D0000F9CD86BE44146B8684B0BB37CE8CAE9B374B5914420BA737",
    )
    data = replace_at(
        data, 33_751, b"_", b"^", 143_891,
        "A6D326DBFA8D002FBE92B6A451566FAB172B4D70E05DA6DEAE9259F7BDB113EA",
    )
    data = replace_at(
        data, 31_498, b"_", b"^", 143_891,
        "F6553DA9AD9D42F17DC81A3B56E688FA486CB46AAA3B06D09BDE3F51B98BF101",
    )
    data = replace_at(
        data, 11_257, b"_", b"^", 143_891,
        "B946F98EC54F976CA6AA16DD525E8CDE2CA36B1C5E2BC71D77C35FBE6CB9D1D4",
    )
    return replace_at(
        data, 9_712,
        b"\\ar[r]_{\\Gamma(\\theta_{\\mathfrak{D}(g)})}",
        b"\\ar[r]^{\\Gamma(\\theta_{\\mathfrak{D}(g)})}",
        143_891,
        "FCF8334A2C158768B792E2EA4F596762F8AA48B61593227482170DD9EC4654A1",
    )


def invert_r247_to_r243_ega1_10(data):
    return replace_at(
        data, 78_592, b"_", b"^", 143_891,
        "1EE78A1031C27C4A6E8358213914ED6B8022A31D5DEFC59517E3A01501993DCF",
    )


R247_TO_R243_INVERSES = {
    "ega1/ega1-10.tex": invert_r247_to_r243_ega1_10,
}


R243_TO_R219_INVERSES = {
    "ega0/ega0-3.tex": invert_r242_ega0_3,
    "ega0/ega0-4.tex": invert_r242_ega0_4,
    "ega0/ega0-5.tex": invert_r242_ega0_5,
    "ega0/ega0-7.tex": invert_r242_ega0_7,
    "ega1/ega1-1.tex": invert_r242_ega1_1,
    "ega1/ega1-10.tex": invert_r242_ega1_10,
}


def invert_ega0_1(data):
    data = replace_at(
        data, 25_825, b"^-\\tau_-\\sim", b"^-\\sim_-\\tau", 33_832,
        "EB5DFE559EE1192EC9E6B764DCAA2C51C791A0E1BAAA51D509023AAE26465325",
    )
    data = replace_at(
        data, 25_624, b"_", b"^", 33_832,
        "B965D330C8D1C545D2FA6B5029F8D16FCE6EF3A432DDFAE4D84C09C9A9181700",
    )
    data = replace_at(
        data, 25_362, b"_", b"^", 33_832,
        "9BAFD35A7B625CBD8B2655D8405DAE262A64F564286AB12B161B12AF0E761547",
    )
    return replace_at(
        data, 19_753, b"_", b"^", 33_832,
        "1FEC1B0BF5C558633512545C460F97BEEA7789FC77BBA709AEBB693C5C2113F7",
    )


def invert_ega0_3(data):
    data = replace_at(
        data, 22_662, b"_", b"^", 47_181,
        "BACB39CBD6BBCA7311AB73E970559351E5F317E3C135C0DB49F1BBC9964818E5",
    )
    return replace_at(
        data, 22_224, b"_", b"^", 47_181,
        "4A999C21EA00458A1C3B5537F17858B6E89FF598357BFF083DC31B05FA0C3A3A",
    )


def invert_ega1_1(data):
    return replace_at(
        data, 61_529,
        b"which, after choosing such an isomorphism, is canonically identified with the ring $A$",
        b"which is canonically identified with the ring $A$",
        78_906,
        "EB62DDA7A40E93BFF26BEF9513693192A7C46540E08D244C18218F9BAAEF4FFA",
    )


def invert_ega1_2(data):
    return replace_at(
        data, 19_052,
        b"The morphisms $\\Spec(K)\\to\\Spec(A)$ whose unique point maps to the closed point $\\mathfrak{m}$ thus correspond bijectively to monomorphisms of fields $A/\\mathfrak{m}\\to K$.",
        b"The morphisms $\\Spec(K)\\to\\Spec(A)$ thus correspond bijectively to monomorphisms of fields $A/\\mathfrak{m}\\to K$.",
        25_429,
        "5785621211C98B1A4452864F3D408325ECED8F84C6CB16DE0875E052A6E7984F",
    )


def invert_ega1_3(data):
    return replace_at(
        data, 16_495,
        (
            b"The reader will notice that all the properties stated in this section, except\n"
            b"\\sref{I.3.3.13}, \\sref{I.3.3.15}, and the assertion on sums in the final sentence\n"
            b"of \\sref{I.3.3.10}, are true without modification in \\emph{any category}, whenever\n"
            b"the products involved in the statements \\emph{exist} (since it is\n"
        ),
        (
            b"The reader will notice that all the properties stated in this section, except\n"
            b"\\sref{I.3.3.13} and \\sref{I.3.3.15}, are true without modification in \\emph{any\n"
            b"category}, whenever the products involved in the statements \\emph{exist} (since it is\n"
        ),
        56_933,
        "55C1E1129E40F1E2F8DB7B46867B3E49AE2556F04C1CFE1FBF5EE3C149B63BD9",
    )


def invert_ega1_4(data):
    data = replace_at(
        data, 24_273,
        (
            b"In addition, if $\\mathfrak{b}$ (resp. $\\mathfrak{c}$) is the kernel of "
            b"$\\rho$ (resp. $\\sigma$), then the kernel of $\\tau$ is\n"
            b"$\\operatorname{Im}(\\mathfrak{b}\\otimes_A C\\to B\\otimes_A C)+"
            b"\\operatorname{Im}(B\\otimes_A\\mathfrak{c}\\to B\\otimes_A C)$,\n"
            b"equivalently the sum of the ideals generated by $u(\\mathfrak{b})$ and "
            b"$v(\\mathfrak{c})$, where $u$ (resp. $v$) is the homomorphism "
            b"$b\\mapsto b\\otimes 1$ (resp. $c\\mapsto 1\\otimes c$).\n"
        ),
        (
            b"In addition, if $\\mathfrak{b}$ (resp. $\\mathfrak{c}$) is the kernel of "
            b"$\\rho$ (resp. $\\sigma$), then the kernel of $\\tau$ is "
            b"$u(\\mathfrak{b})+v(\\mathfrak{c})$, where $u$ (resp. $v$) is the "
            b"homomorphism $b\\mapsto b\\otimes 1$ (resp. $c\\mapsto 1\\otimes c$).\n"
        ),
        33_646,
        "7BF08F3B232A9C9DE0D04C1E465C6863482BA472ABDC2DD36BB32AE1CF0BA82F",
    )
    return replace_at(
        data, 17_681, b"\\Gamma(\\theta)", b"\\Gamma(\\psi)", 33_644,
        "C933CDFEB1C7F64B0BFFB8D510A732349B196E3E53B8044A70098D999CAB1BF8",
    )


def invert_ega1_5(data):
    return replace_at(
        data, 3_384,
        b"prescheme \\sref{I.2.1.8}, it is necessary",
        b"prescheme \\sref{I.2.1.7}, it is necessary",
        47_538,
        "E4E6D19A7C19B69E61CBBE8792DB0EED1AD6DAA0DD559E61811057F11641651C",
    )


def invert_ega2_2(data):
    data = replace_at(
        data, 52_292,
        (
            b"The homomorphisms $\\lambda_f$ therefore induce a canonical functorial "
            b"homomorphism of $\\sh{O}_X$-modules\n"
        ),
        (
            b"Thus $\\lambda$ induces a canonical functorial homomorphism of "
            b"$\\sh{O}_X$-modules\n"
        ),
        103_689,
        "FE223682E244AEC245E283DBC14077B08B4D0A36F67994A790129C192AF46624",
    )
    data = replace_at(
        data, 42_180, b"^{(d)}", b"", 103_683,
        "72BB91295A24787AF6E6F030E16005E5A2E220863377DD89FD2FFAC1F4FE2A85",
    )
    return replace_at(
        data, 17_184, b"$k\\geq a$", b"$k>-a$", 103_680,
        "33C44C60F4DBC6BDDD1EA5C3739E765C43368D160E2B6C01755331270D2AF63D",
    )


INVERSES = {
    "ega0/ega0-1.tex": (
        33_832,
        "1C856A83AEA956E9E201D12C16D3C43917AD8420BBD64720F53792CAEE741957",
        invert_ega0_1,
    ),
    "ega0/ega0-3.tex": (
        47_181,
        "5CCAEF6A1ADDAC7043D435762145A5A34C6E4E2028E0A7D6688F0D8DCB7295EB",
        invert_ega0_3,
    ),
    "ega1/ega1-1.tex": (
        78_943,
        "F32A8DB7385B1730556DB39FE0609B71BA1CC7E340D76BF87B5B9019FBC83764",
        invert_ega1_1,
    ),
    "ega1/ega1-2.tex": (
        25_488,
        "0B89DB848D4A9820B293B3D8120CB953775DA107718001B43EBCDC1553BA1A85",
        invert_ega1_2,
    ),
    "ega1/ega1-3.tex": (
        56_998,
        "3A733719B8D6C768CC2A73FA15C26EF6B1CE580246F738C43F90069A4C749DCC",
        invert_ega1_3,
    ),
    "ega1/ega1-4.tex": (
        33_820,
        "1BCD0A186CC35721947F0653953BAE387BE1D9EC695733E193970C503AF2DDFA",
        invert_ega1_4,
    ),
    "ega1/ega1-5.tex": (
        47_538,
        "B344B67200DF1DA5E962BCB8AE5AD7E20224168D55C3E53BD52B5F0311F8EE56",
        invert_ega1_5,
    ),
    "ega2/ega2-2.tex": (
        103_713,
        "6BF6FD80D3CAF6E1DFC75AC574D63E6CC15AE200132051FD492E0B130E412BED",
        invert_ega2_2,
    ),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--successor-manifest", required=True, type=Path)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    raw_manifest = args.manifest.read_bytes()
    if (len(raw_manifest), sha(raw_manifest)) != (
            MANIFEST_BYTES, MANIFEST_SHA256):
        raise RuntimeError("R184 manifest identity changed")
    manifest = json.loads(raw_manifest.decode("utf-8"))
    if manifest.get("file_count") != 127:
        raise RuntimeError("R184 file count changed")

    raw_successor_manifest = args.successor_manifest.read_bytes()
    if (len(raw_successor_manifest), sha(raw_successor_manifest)) != (
            SUCCESSOR_MANIFEST_BYTES, SUCCESSOR_MANIFEST_SHA256):
        raise RuntimeError("R247 manifest identity changed")
    successor_manifest = json.loads(raw_successor_manifest.decode("utf-8"))
    if (successor_manifest.get("file_count"),
            successor_manifest.get("total_bytes"),
            successor_manifest.get("canonical_tree_sha256")) != (
            127, SUCCESSOR_BYTES, SUCCESSOR_TREE_SHA256):
        raise RuntimeError("R247 manifest summary changed")

    if args.out.exists():
        raise RuntimeError("output already exists")
    args.out.parent.mkdir(parents=True, exist_ok=True)

    successor_entries = {}
    for entry in successor_manifest["files"]:
        relative = entry["relative_path"]
        if relative in successor_entries:
            raise RuntimeError(f"duplicate R247 manifest path: {relative}")
        successor_entries[relative] = entry
    r184_paths = {entry["relative_path"] for entry in manifest["files"]}
    if set(successor_entries) != r184_paths:
        raise RuntimeError("R247 and R184 path sets differ")
    source_data = read_sealed_successor(args.source, successor_entries)

    r247_changed = []
    r243_data = {}
    r243_rows = []
    for entry in manifest["files"]:
        relative = entry["relative_path"]
        data = source_data[relative]
        inverse = R247_TO_R243_INVERSES.get(relative)
        if inverse is not None:
            data = inverse(data)
            r247_changed.append(relative)
        r243_data[relative] = data
        r243_rows.append(f"{relative}\t{len(data)}\t{sha(data)}\n")
    if (sum(len(data) for data in r243_data.values()),
            sha("".join(r243_rows).encode("utf-8"))) != (
            R243_BYTES, R243_TREE_SHA256):
        raise RuntimeError("R247 inverse does not reconstruct sealed R243")

    r243_changed = []
    r219_data = {}
    r219_rows = []
    for entry in manifest["files"]:
        relative = entry["relative_path"]
        data = r243_data[relative]
        inverse = R243_TO_R219_INVERSES.get(relative)
        if inverse is not None:
            data = inverse(data)
            r243_changed.append(relative)
        r219_data[relative] = data
        r219_rows.append(f"{relative}\t{len(data)}\t{sha(data)}\n")
    if (sum(len(data) for data in r219_data.values()),
            sha("".join(r219_rows).encode("utf-8"))) != (
            R219_BYTES, R219_TREE_SHA256):
        raise RuntimeError("R243 inverse does not reconstruct sealed R219")

    changed = []
    canonical = []
    with tempfile.TemporaryDirectory(
            prefix=f".{args.out.name}.", dir=args.out.parent) as directory:
        stage = Path(directory) / "tree"
        stage.mkdir()
        for entry in manifest["files"]:
            relative = entry["relative_path"]
            data = r219_data[relative]
            identity = (len(data), sha(data))
            expected = (entry["bytes"], entry["sha256"])
            if identity != expected:
                inverse = INVERSES.get(relative)
                if inverse is None or identity != inverse[:2]:
                    raise RuntimeError(f"unrecognized successor identity: {relative}")
                data = inverse[2](data)
                changed.append(relative)
            if (len(data), sha(data)) != expected:
                raise RuntimeError(f"R184 reconstruction mismatch: {relative}")
            target = stage / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            canonical.append(
                f"{relative}\t{len(data)}\t{sha(data)}\n")
        tree = sha("".join(canonical).encode("utf-8"))
        if tree != TREE_SHA256:
            raise RuntimeError("R184 reconstructed tree mismatch")
        # A producer may advance the shared live tree while reconstruction is
        # running. Re-read every sealed input immediately before promotion so
        # a mixed-time snapshot can never be reported as a successful replay.
        read_sealed_successor(args.source, successor_entries)
        stage.replace(args.out)

    result = {
        "schema": "ega-r184-exact-replay-v1",
        "status": "PASS",
        "files": len(manifest["files"]),
        "bytes": sum(entry["bytes"] for entry in manifest["files"]),
        "tree_sha256": TREE_SHA256,
        "successor_tree_sha256": SUCCESSOR_TREE_SHA256,
        "r243_tree_sha256": R243_TREE_SHA256,
        "intermediate_tree_sha256": R219_TREE_SHA256,
        "successor_inverted_files": sorted(set(r247_changed + r243_changed)),
        "r184_inverted_files": changed,
        "inverted_files": sorted(set(r247_changed + r243_changed + changed)),
        "source_mutated": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
