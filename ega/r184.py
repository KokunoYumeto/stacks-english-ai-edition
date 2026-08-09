#!/usr/bin/env python3
"""Reconstruct the exact frozen R184 discovery tree from its known successor."""

import argparse
import hashlib
import json
import tempfile
from pathlib import Path


MANIFEST_BYTES = 92_445
MANIFEST_SHA256 = "5C64ECD32FD7C5458D2599D70ED667D2CF06D95517EFFA9C6D6DCEF7626913A0"
TREE_SHA256 = "3BFB1C5103093481246EF4A6365E08544F6D5E19ACC0EA63E717F3F3643F064D"


def sha(data):
    return hashlib.sha256(data).hexdigest().upper()


def replace_at(data, offset, postimage, preimage, expected_bytes, expected_sha):
    if data[offset:offset + len(postimage)] != postimage:
        raise RuntimeError(f"inverse postimage moved at byte {offset}")
    result = data[:offset] + preimage + data[offset + len(postimage):]
    if (len(result), sha(result)) != (expected_bytes, expected_sha):
        raise RuntimeError(f"inverse result mismatch at byte {offset}")
    return result


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
    "ega2/ega2-2.tex": (
        103_713,
        "6BF6FD80D3CAF6E1DFC75AC574D63E6CC15AE200132051FD492E0B130E412BED",
        invert_ega2_2,
    ),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
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
    if args.out.exists():
        raise RuntimeError("output already exists")
    args.out.parent.mkdir(parents=True, exist_ok=True)

    changed = []
    canonical = []
    with tempfile.TemporaryDirectory(
            prefix=f".{args.out.name}.", dir=args.out.parent) as directory:
        stage = Path(directory) / "tree"
        stage.mkdir()
        for entry in manifest["files"]:
            relative = entry["relative_path"]
            data = (args.source / relative).read_bytes()
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
        stage.replace(args.out)

    result = {
        "schema": "ega-r184-exact-replay-v1",
        "status": "PASS",
        "files": len(manifest["files"]),
        "bytes": sum(entry["bytes"] for entry in manifest["files"]),
        "tree_sha256": TREE_SHA256,
        "inverted_files": changed,
        "source_mutated": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
