#!/usr/bin/env python3
"""Reconstruct the exact frozen R184 discovery tree from sealed R261."""

import argparse
import base64
import hashlib
import json
import tempfile
from pathlib import Path


MANIFEST_BYTES = 92_445
MANIFEST_SHA256 = "5C64ECD32FD7C5458D2599D70ED667D2CF06D95517EFFA9C6D6DCEF7626913A0"
TREE_SHA256 = "3BFB1C5103093481246EF4A6365E08544F6D5E19ACC0EA63E717F3F3643F064D"
SUCCESSOR_MANIFEST_BYTES = 32_444
SUCCESSOR_MANIFEST_SHA256 = "A87DC2EDD0BDA5CE6828A2759095B1F4F3278E993DC5661EBA2E345C33BEEF18"
SUCCESSOR_BYTES = 7_284_367
SUCCESSOR_TREE_SHA256 = "3FF379C715F99D2A28F231A54D55996E9CDA27153E5DBBFB14BA6F7F70766CB0"
R261_FIRST_TREE_SHA256 = "1C6755598979359FDB92ACF64CB4F3D3DC56CD99E2056EE264ADC22DE60CBBD2"
R261_SECOND_TREE_SHA256 = "D53A58719F8758E708B6FDF2AA453F274127DFA9F325B59575BFC60354042FB7"
R260_MANIFEST_BYTES = 27_368
R260_MANIFEST_SHA256 = "29DEFA6CC187315E1A791D268CC092DD987F36056F6A206DE72973E05D6D8E32"
R259R_MANIFEST_BYTES = 26_017
R259R_MANIFEST_SHA256 = "BF8107C5DF86F2CABB18A9FA3107FBD86CE1A6E3431B7609A0C210226E9F221F"
R259R_BYTES = 7_284_367
R259R_TREE_SHA256 = "B48C9EE73FE70027FD8E07AFD85EEC144B8BFF0A36374F93049850B7C051665B"
R258_MANIFEST_BYTES = 35_230
R258_MANIFEST_SHA256 = "CD1837FDCD422937A8176BA0BC409AF0D4A32EB291BE88086C66D4EA5098C44D"
R257S_MANIFEST_BYTES = 33_658
R257S_MANIFEST_SHA256 = "D05F864BF3AB5F75871AD4B2DAE4B6C94EA4977C7532190C0E1D8171CAC28AA3"
R258_BYTES = 7_284_367
R258_TREE_SHA256 = "EE22A2E67C7EEA1DF6B8D1D4F0B664ADD6CC22D687FBB4E424FDAD827A19A110"
R257_FIRST_TREE_SHA256 = "8FBE85608A2DA7C8F1ECA5789B88A62CBFFC34AFDF9386DDAD2FF11A91A9857C"
R257_SECOND_TREE_SHA256 = "8954AAF3CFA46704F5CF935FBB368936764AB46DBEED16EE79A4EAEFDD66ACE5"
R256_BYTES = 7_284_367
R256_TREE_SHA256 = "5B3F237438E9F1BD59E24FB9D19FEB647312D0B17EEFBDEA9913449B546627BA"
R255_BYTES = 7_284_367
R255_TREE_SHA256 = "B6B0A39094F1E7799C8F6C032FC1C38840597CD66075202D11F4926C8668DB4C"
R255_CITATION_BYTES = 7_284_191
R255_CITATION_TREE_SHA256 = "4395E86FB39E678A723C6CF43109DB56BFC4FA89A96D980679DCFFC837B0ED91"
R254_BYTES = 7_283_701
R254_TREE_SHA256 = "C32F4904449F6DEDFB6991B569FDD96B8EAD27BE77685E67A52EE0094C896A7E"
R248_BYTES = 7_283_701
R248_TREE_SHA256 = "DDBF5FF8FD0D3A74ED43A06B3F9011855540BBD9D3F029256822CB68E872EE49"
R247_BYTES = 7_283_701
R247_TREE_SHA256 = "F152BFBC3AC3102DCE41975C27EEB373D01770F325639DF9AD01EFB6AD4F36D8"
R243_BYTES = 7_283_701
R243_TREE_SHA256 = "EB6A5465B872682311DD0DA7E6B633071A220C7FB957FCFB601795D5CBA1E39C"
R219_BYTES = 7_283_691
R219_TREE_SHA256 = "AD9F9A8A17882E5DF5EE4D1CFB1EAC03EBF5E22826B97A98207A2C220D106D22"


def sha(data):
    return hashlib.sha256(data).hexdigest().upper()


def read_sealed_successor(source, entries):
    """Read and validate one complete immutable R261 source snapshot."""
    source_data = {}
    source_rows = []
    for relative, entry in entries.items():
        data = (source / relative).read_bytes()
        if (len(data), sha(data)) != (entry["bytes"], entry["sha256"]):
            raise RuntimeError(f"live source differs from sealed R261: {relative}")
        source_data[relative] = data
        source_rows.append(f"{relative}\t{len(data)}\t{sha(data)}\n")
    if (sum(len(data) for data in source_data.values()),
            sha("".join(source_rows).encode("utf-8"))) != (
            SUCCESSOR_BYTES, SUCCESSOR_TREE_SHA256):
        raise RuntimeError("live source tree is not the sealed R261 successor")
    return source_data


def read_intermediate_manifest(path, expected_bytes, expected_sha,
                               expected_tree, source_data, label):
    """Gate an exact predecessor manifest and its complete file inventory."""
    raw = path.read_bytes()
    if (len(raw), sha(raw)) != (expected_bytes, expected_sha):
        raise RuntimeError(f"{label} manifest identity changed")
    manifest = json.loads(raw.decode("utf-8"))
    if (manifest.get("file_count"), manifest.get("total_bytes"),
            manifest.get("serialization_bytes"),
            manifest.get("canonical_tree_sha256")) != (
            127, R258_BYTES, 12_890, expected_tree):
        raise RuntimeError(f"{label} manifest summary changed")
    entries = {}
    for entry in manifest.get("files", []):
        relative = entry["relative_path"]
        if relative in entries:
            raise RuntimeError(f"duplicate {label} manifest path: {relative}")
        entries[relative] = entry
    if set(entries) != set(source_data):
        raise RuntimeError(f"{label} manifest path set changed")
    for relative, data in source_data.items():
        entry = entries[relative]
        if (len(data), sha(data)) != (entry["bytes"], entry["sha256"]):
            raise RuntimeError(f"{label} file inventory changed: {relative}")
    return manifest


def replace_at(data, offset, postimage, preimage, expected_bytes, expected_sha):
    if data[offset:offset + len(postimage)] != postimage:
        raise RuntimeError(f"inverse postimage moved at byte {offset}")
    result = data[:offset] + preimage + data[offset + len(postimage):]
    if (len(result), sha(result)) != (expected_bytes, expected_sha):
        raise RuntimeError(f"inverse result mismatch at byte {offset}")
    return result


def inverse_layer(entries, source_data, inverses, expected_bytes,
                  expected_tree, label):
    changed = []
    output = {}
    rows = []
    for entry in entries:
        relative = entry["relative_path"]
        data = source_data[relative]
        inverse = inverses.get(relative)
        if inverse is not None:
            data = inverse(data)
            changed.append(relative)
        output[relative] = data
        rows.append(f"{relative}\t{len(data)}\t{sha(data)}\n")
    if (sum(len(data) for data in output.values()),
            sha("".join(rows).encode("utf-8"))) != (
            expected_bytes, expected_tree):
        raise RuntimeError(f"{label} does not reconstruct its exact tree")
    return changed, output


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


def invert_r248_to_r247_ega1_10(data):
    return replace_at(
        data, 133_729, b"^", b"_", 143_891,
        "06D95A924F724193D419A6CEA9FC590381D408A3B03D724177BCD61DD238D54A",
    )


def invert_r261_first_ega1_5(data):
    if (len(data), sha(data)) != (
            48_204,
            "B5323F253347AFAF0489059C0B6E02C850176473EBD4551DA5AA533F217AF574"):
        raise RuntimeError("R261 ega1-5 postimage file identity changed")
    return replace_at(
        data, 18_692, b"_", b"^", 48_204,
        "C7D7C26C37D7E8FC3B38B9F60A68A37117B6955EF76FE1B667C900A4FEEFB46F",
    )


def invert_r261_second_ega1_5(data):
    if (len(data), sha(data)) != (
            48_204,
            "C7D7C26C37D7E8FC3B38B9F60A68A37117B6955EF76FE1B667C900A4FEEFB46F"):
        raise RuntimeError("R261 first inverse intermediate changed")
    return replace_at(
        data, 10_214, b"^", b"_", 48_204,
        "9189040BDD957957FE92012B6147950BBF37580556ADA1D5C5BC8A794637C44C",
    )


def invert_r261_third_ega1_5(data):
    if (len(data), sha(data)) != (
            48_204,
            "9189040BDD957957FE92012B6147950BBF37580556ADA1D5C5BC8A794637C44C"):
        raise RuntimeError("R261 second inverse intermediate changed")
    return replace_at(
        data, 5_590, b"_", b"^", 48_204,
        "813B4929AA5506E41327A3D9185C35A71CD8A86469D2064661E030F0D8D4D3A5",
    )


R259R_DIAGRAM_POST = b"\\ar[d]_{\\pi''}"
R259R_DIAGRAM_PRE = b"\\ar[d]^{\\pi''}"


def invert_r259r_to_r258_ega1_3(data):
    if (len(data), sha(data)) != (
            56_998,
            "1E69D58C1E0E8D076CD885925F87A7F064F8C92B7FE965FB60B0018573022890"):
        raise RuntimeError("R259R ega1-3 postimage file identity changed")
    if sha(data[21_590:22_225]) != (
            "DC01C2B195D933BC34425B7C9E25D364CC99BF6461FDD28EB538FB461E81C019"):
        raise RuntimeError("R259R diagram witness changed at byte 21590")
    if data.count(R259R_DIAGRAM_POST) != 1:
        raise RuntimeError("R259R diagram postimage is not unique")
    if data.count(R259R_DIAGRAM_PRE) != 0:
        raise RuntimeError("R258 diagram preimage already occurs in R259R")
    return replace_at(
        data, 22_149, R259R_DIAGRAM_POST, R259R_DIAGRAM_PRE, 56_998,
        "5A080F25CB54435CAE26E078431CF06A145A2CAE862E96613222EB2D860547ED",
    )


def invert_r257_first_ega1_5(data):
    return replace_at(
        data, 27_479, b"_", b"^", 48_204,
        "9C63FBCF2D735CBF2E147FDED4B03C3D76CA3A03CB201D1CA41363E92E6383FE",
    )


def invert_r257_second_ega1_5(data):
    return replace_at(
        data, 27_306, b"_", b"^", 48_204,
        "ED7DB37AA11B95A06C9F993D35FB97B5315A6709856F473C6EFC0864375A3BBA",
    )


def invert_r257_third_ega1_5(data):
    return replace_at(
        data, 25_598, b"_", b"^", 48_204,
        "0D1567EB2CFED2FA0ADDFB055F31CC3E840EC8B46CB6B1DBCA33E3CE8CBF0738",
    )


R256_DIAGRAM_POST = base64.b64decode(
    "ICBceHltYXRyaXh7CiAgICBYXHRpbWVzIFlcYXJbcl1ee2ZcdGltZXMgMX1cYXJbZF0gJg"
    "ogICAgWCdcdGltZXMgWVxhcltyXV57ZidcdGltZXMgMX1cYXJbZF0gJgogICAgWCcnXHRp"
    "bWVzIFlcYXJbZF1cXAogICAgWFxhcltyXV9mICYKICAgIFgnXGFyW3JdX3tmJ30gJgogICAg"
    "WCcnCiAgfQ=="
)
R256_DIAGRAM_PRE = base64.b64decode(
    "ICBceHltYXRyaXh7CiAgICBYXHRpbWVzIFlcYXJbcl1ee2ZcdGltZXMgMX1cYXJbZF0gJg"
    "ogICAgWCdcdGltZXMgWVxhcltyXV57ZidcdGltZXMgMX1cYXJbZF0gJgogICAgWCcnXHRp"
    "bWVzIFlcYXJbZF1cXAogICAgWFxhcltyXV5mICYKICAgIFgnXGFyW3JdXntmJ30gJgogICAg"
    "WCcnCiAgfQ=="
)


def invert_r256_to_r255_ega1_3(data):
    return replace_at(
        data, 17_172, R256_DIAGRAM_POST, R256_DIAGRAM_PRE, 56_998,
        "3A733719B8D6C768CC2A73FA15C26EF6B1CE580246F738C43F90069A4C749DCC",
    )


R255_CITATION_POST = base64.b64decode(
    "d2UgYXJlIGRvbmUsIGJ5IFxzcmVme0kuNC4yLjV9XGZvb3Rub3Rle1xlbXBoe1tUcmFucy5d"
    "IFRoZSBGcmVuY2ggc291cmNlIHByaW50cyBcc3JlZntJLjQuMi40fSBoZXJlOyBwdWJsaXNo"
    "ZWQgRUdBfklJSS4yLCBFcnJhdGEgYW5kIEFkZGVuZGEgKGxpc3R+MiksIGV4cGxpY2l0bHkg"
    "ZGlyZWN0cyBpdHMgcmVwbGFjZW1lbnQgYnkgXHNyZWZ7SS40LjIuNX0ufX0gKHJlc3AuIFxz"
    "cmVme0kuNC41LjV9KS4="
)
R255_CITATION_PRE = base64.b64decode(
    "d2UgYXJlIGRvbmUsIGJ5IFxzcmVme0kuNC4yLjR9IChyZXNwLiBcc3JlZntJLjQuNS41fSku"
)
R255_PROOF_POST = base64.b64decode(
    "XGJlZ2lue3Byb29mfQpUaGUgcHJvb2YgcHJpbnRlZCBpbiB0aGUgRnJlbmNoIHNvdXJjZSBp"
    "cyBpbnN1ZmZpY2llbnQsIGJlY2F1c2UgaXQgZG9lcyBub3QKc2hvdyB0aGF0ICRcRGVsdGFf"
    "WChYKSQgaXMgbG9jYWxseSBjbG9zZWQgaW4gJFhcdGltZXNfUyBYJC5cZm9vdG5vdGV7XGVt"
    "cGh7W1RyYW5zLl0gUHVibGlzaGVkIEVHQX5JSUkuMiwgRXJyYXRhIGFuZCBBZGRlbmRhIChs"
    "aXN0fjIpLCBpdGVtICRcbWF0aHJte0Vycn1fe1xtYXRocm17SUlJfX0sMTAkLCBleHBsaWNp"
    "dGx5IGlkZW50aWZpZXMgdGhpcyBnYXAgYW5kIGdpdmVzIHRoZSBhZmZpbmUtbG9jYWwgcHJv"
    "b2YgdHJhbnNsYXRlZCBoZXJlLn19CkZvciBhIGNvcnJlY3QgcHJvb2YsIGl0IHN1ZmZpY2Vz"
    "IHRvIHVzZSBcc3JlZntJLjQuMi40fVthXToKZm9yIGV2ZXJ5ICR4XGluIFgkIGFuZCBldmVy"
    "eSBhZmZpbmUgbmVpZ2hib3VyaG9vZCAkVSQgb2YgJHgkIGluICRYJCwKJFVcdGltZXNfUyBV"
    "JCBpcyBhbiBhZmZpbmUgbmVpZ2hib3VyaG9vZCBvZiAkXERlbHRhX1goeCkkLgpUYWtpbmcg"
    "YWNjb3VudCBvZiBcc3JlZntJLjUuMy4xNn0gKHdob3NlIHByb29mIHVzZXMgb25seSBEZWZp"
    "bml0aW9uClxzcmVme0kuNS4zLjEuMX0pLCB3ZSBhcmUgcmVkdWNlZCB0byBwcm92aW5nIFxz"
    "cmVme0kuNS4zLjl9IHdoZW4KJFM9XFNwZWMoQikkIGFuZCAkWD1cU3BlYyhBKSQgYXJlIGFm"
    "ZmluZSBzY2hlbWVzLgpJdCBpcyB0aGVuIGNsZWFyIGZyb20gXHNyZWZ7SS41LjMuMS4xfSB0"
    "aGF0ICRcRGVsdGFfWCQgY29ycmVzcG9uZHMgdG8gdGhlCmNhbm9uaWNhbCBob21vbW9ycGhp"
    "c20gJEFcb3RpbWVzX0IgQVx0byBBJCB0YWtpbmcgJHhcb3RpbWVzIHkkIHRvICR4eSQuClNp"
    "bmNlIHRoaXMgaG9tb21vcnBoaXNtIGlzIHN1cmplY3RpdmUsICRcRGVsdGFfWCQgaXMgaW4g"
    "dGhpcyBjYXNlIGEgY2xvc2VkCmltbWVyc2lvbiBcc3JlZntJLjQuMi4zfSwgd2hpY2ggY29t"
    "cGxldGVzIHRoZSBwcm9vZi4KXGVuZHtwcm9vZn0="
)
R255_PROOF_PRE = base64.b64decode(
    "XGJlZ2lue3Byb29mfQpJbmRlZWQsIHNpbmNlIHRoZSBjb250aW51b3VzIG1hcHMgJHBfMSQg"
    "YW5kICRcRGVsdGFfWCQgZnJvbSB0aGUgdW5kZXJseWluZyBzcGFjZXMgYXJlIHN1Y2ggdGhh"
    "dCAkcF8xXGNpcmNcRGVsdGFfWCQgaXMgdGhlIGlkZW50aXR5LCAkXERlbHRhX1gkIGlzIGEg"
    "aG9tZW9tb3JwaGlzbSBmcm9tICRYJCB0byAkXERlbHRhX1goWCkkLgpTaW1pbGFybHksIHRo"
    "ZSBjb21wb3NpdGUgaG9tb21vcnBoaXNtICRcc2h7T31feFx0b1xzaHtPfV97XERlbHRhX1go"
    "eCl9XHRvXHNoe099X3gkIChjb21wb3NlZCBvZiB0aGUgaG9tb21vcnBoaXNtcyBjb3JyZXNw"
    "b25kaW5nIHRvICRwXzEkIGFuZCAkXERlbHRhX1gkKSBpcyB0aGUgaWRlbnRpdHksIHdoaWNo"
    "IG1lYW5zIHRoYXQgdGhlIGhvbW9tb3JwaGlzbSBjb3JyZXNwb25kaW5nIHRvICRcRGVsdGFf"
    "WCQgaXMgc3VyamVjdGl2ZTsKdGhlIHByb3Bvc2l0aW9uIHRodXMgZm9sbG93cyBmcm9tIFxz"
    "cmVme0kuNC4yLjJ9LgpcZW5ke3Byb29mfQ=="
)


R257_FIRST_INVERSES = {
    "ega1/ega1-5.tex": invert_r257_first_ega1_5,
}


R261_FIRST_INVERSES = {
    "ega1/ega1-5.tex": invert_r261_first_ega1_5,
}


R261_SECOND_INVERSES = {
    "ega1/ega1-5.tex": invert_r261_second_ega1_5,
}


R261_THIRD_INVERSES = {
    "ega1/ega1-5.tex": invert_r261_third_ega1_5,
}


R259R_TO_R258_INVERSES = {
    "ega1/ega1-3.tex": invert_r259r_to_r258_ega1_3,
}


R257_SECOND_INVERSES = {
    "ega1/ega1-5.tex": invert_r257_second_ega1_5,
}


R257_THIRD_INVERSES = {
    "ega1/ega1-5.tex": invert_r257_third_ega1_5,
}


R256_TO_R255_INVERSES = {
    "ega1/ega1-3.tex": invert_r256_to_r255_ega1_3,
}


def invert_r255_citation_ega1_5(data):
    return replace_at(
        data, 24_780, R255_CITATION_POST, R255_CITATION_PRE, 48_028,
        "38C3CB436162FCB60A8D4BEED799EC4416EB767B8E56B5DDA130C954F299E1D2",
    )


def invert_r255_proof_ega1_5(data):
    return replace_at(
        data, 21_078, R255_PROOF_POST, R255_PROOF_PRE, 47_538,
        "18034F9FCF24CDA1D6AD9D05E543DD404A55FF19F33DF5113B963529FCB6B208",
    )


def invert_r251_to_r248_ega1_5(data):
    if sha(data[19_655:19_775]) != (
            "367A45461D46ADCBE6012D2C7D18040301343A1B9B3D0C73E5616790EC639359"):
        raise RuntimeError("R251 inverse source slice changed at byte 19655")
    return replace_at(
        data, 19_712, b"_", b"^", 47_538,
        "B344B67200DF1DA5E962BCB8AE5AD7E20224168D55C3E53BD52B5F0311F8EE56",
    )


R255_CITATION_INVERSES = {
    "ega1/ega1-5.tex": invert_r255_citation_ega1_5,
}


R255_PROOF_INVERSES = {
    "ega1/ega1-5.tex": invert_r255_proof_ega1_5,
}


R251_TO_R248_INVERSES = {
    "ega1/ega1-5.tex": invert_r251_to_r248_ega1_5,
}


R248_TO_R247_INVERSES = {
    "ega1/ega1-10.tex": invert_r248_to_r247_ega1_10,
}


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
        raise RuntimeError("R261 manifest identity changed")
    successor_manifest = json.loads(raw_successor_manifest.decode("utf-8"))
    if (successor_manifest.get("file_count"),
            successor_manifest.get("total_bytes"),
            successor_manifest.get("serialization_bytes"),
            successor_manifest.get("canonical_tree_sha256")) != (
            127, SUCCESSOR_BYTES, 12_890, SUCCESSOR_TREE_SHA256):
        raise RuntimeError("R261 manifest summary changed")

    if args.out.exists():
        raise RuntimeError("output already exists")
    args.out.parent.mkdir(parents=True, exist_ok=True)

    successor_entries = {}
    for entry in successor_manifest["files"]:
        relative = entry["relative_path"]
        if relative in successor_entries:
            raise RuntimeError(f"duplicate R261 manifest path: {relative}")
        successor_entries[relative] = entry
    r184_paths = {entry["relative_path"] for entry in manifest["files"]}
    if set(successor_entries) != r184_paths:
        raise RuntimeError("R261 and R184 path sets differ")
    source_data = read_sealed_successor(args.source, successor_entries)

    r261_first_changed, r261_first_data = inverse_layer(
        manifest["files"], source_data, R261_FIRST_INVERSES,
        SUCCESSOR_BYTES, R261_FIRST_TREE_SHA256, "R261 first label inverse")
    r261_second_changed, r261_second_data = inverse_layer(
        manifest["files"], r261_first_data, R261_SECOND_INVERSES,
        SUCCESSOR_BYTES, R261_SECOND_TREE_SHA256, "R261 second label inverse")
    r261_third_changed, r260_data = inverse_layer(
        manifest["files"], r261_second_data, R261_THIRD_INVERSES,
        R259R_BYTES, R259R_TREE_SHA256, "R261 third label inverse")
    read_intermediate_manifest(
        args.successor_manifest.with_name("R260.json"),
        R260_MANIFEST_BYTES, R260_MANIFEST_SHA256,
        R259R_TREE_SHA256, r260_data, "R260")
    read_intermediate_manifest(
        args.successor_manifest.with_name("R259R.json"),
        R259R_MANIFEST_BYTES, R259R_MANIFEST_SHA256,
        R259R_TREE_SHA256, r260_data, "R259R")

    r259r_changed, r258_data = inverse_layer(
        manifest["files"], r260_data, R259R_TO_R258_INVERSES,
        R258_BYTES, R258_TREE_SHA256, "R259R inverse")
    read_intermediate_manifest(
        args.successor_manifest.with_name("R258.json"),
        R258_MANIFEST_BYTES, R258_MANIFEST_SHA256,
        R258_TREE_SHA256, r258_data, "R258")
    read_intermediate_manifest(
        args.successor_manifest.with_name("R257S.json"),
        R257S_MANIFEST_BYTES, R257S_MANIFEST_SHA256,
        R258_TREE_SHA256, r258_data, "R257S")

    first_changed, first_data = inverse_layer(
        manifest["files"], r258_data, R257_FIRST_INVERSES,
        R258_BYTES, R257_FIRST_TREE_SHA256, "R257S first label inverse")
    second_changed, second_data = inverse_layer(
        manifest["files"], first_data, R257_SECOND_INVERSES,
        SUCCESSOR_BYTES, R257_SECOND_TREE_SHA256, "R257S second label inverse")
    third_changed, r256_data = inverse_layer(
        manifest["files"], second_data, R257_THIRD_INVERSES,
        R256_BYTES, R256_TREE_SHA256, "R257S third label inverse")
    r256_changed, r255_data = inverse_layer(
        manifest["files"], r256_data, R256_TO_R255_INVERSES,
        R255_BYTES, R255_TREE_SHA256, "R256 inverse")

    citation_changed = []
    citation_data = {}
    citation_rows = []
    for entry in manifest["files"]:
        relative = entry["relative_path"]
        data = r255_data[relative]
        inverse = R255_CITATION_INVERSES.get(relative)
        if inverse is not None:
            data = inverse(data)
            citation_changed.append(relative)
        citation_data[relative] = data
        citation_rows.append(f"{relative}\t{len(data)}\t{sha(data)}\n")
    if (sum(len(data) for data in citation_data.values()),
            sha("".join(citation_rows).encode("utf-8"))) != (
            R255_CITATION_BYTES, R255_CITATION_TREE_SHA256):
        raise RuntimeError("R255 citation inverse does not reconstruct its exact intermediate")

    proof_changed = []
    r254_data = {}
    r254_rows = []
    for entry in manifest["files"]:
        relative = entry["relative_path"]
        data = citation_data[relative]
        inverse = R255_PROOF_INVERSES.get(relative)
        if inverse is not None:
            data = inverse(data)
            proof_changed.append(relative)
        r254_data[relative] = data
        r254_rows.append(f"{relative}\t{len(data)}\t{sha(data)}\n")
    if (sum(len(data) for data in r254_data.values()),
            sha("".join(r254_rows).encode("utf-8"))) != (
            R254_BYTES, R254_TREE_SHA256):
        raise RuntimeError("R255 proof inverse does not reconstruct sealed R254/R251")

    r254_changed = []
    r248_data = {}
    r248_rows = []
    for entry in manifest["files"]:
        relative = entry["relative_path"]
        data = r254_data[relative]
        inverse = R251_TO_R248_INVERSES.get(relative)
        if inverse is not None:
            data = inverse(data)
            r254_changed.append(relative)
        r248_data[relative] = data
        r248_rows.append(f"{relative}\t{len(data)}\t{sha(data)}\n")
    if (sum(len(data) for data in r248_data.values()),
            sha("".join(r248_rows).encode("utf-8"))) != (
            R248_BYTES, R248_TREE_SHA256):
        raise RuntimeError("R254/R251 inverse does not reconstruct sealed R248")

    r248_changed = []
    r247_data = {}
    r247_rows = []
    for entry in manifest["files"]:
        relative = entry["relative_path"]
        data = r248_data[relative]
        inverse = R248_TO_R247_INVERSES.get(relative)
        if inverse is not None:
            data = inverse(data)
            r248_changed.append(relative)
        r247_data[relative] = data
        r247_rows.append(f"{relative}\t{len(data)}\t{sha(data)}\n")
    if (sum(len(data) for data in r247_data.values()),
            sha("".join(r247_rows).encode("utf-8"))) != (
            R247_BYTES, R247_TREE_SHA256):
        raise RuntimeError("R248 inverse does not reconstruct sealed R247")

    r247_changed = []
    r243_data = {}
    r243_rows = []
    for entry in manifest["files"]:
        relative = entry["relative_path"]
        data = r247_data[relative]
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
        final_successor_manifest = args.successor_manifest.read_bytes()
        if (len(final_successor_manifest), sha(final_successor_manifest)) != (
                SUCCESSOR_MANIFEST_BYTES, SUCCESSOR_MANIFEST_SHA256):
            raise RuntimeError("R261 manifest changed before promotion")
        read_sealed_successor(args.source, successor_entries)
        read_intermediate_manifest(
            args.successor_manifest.with_name("R260.json"),
            R260_MANIFEST_BYTES, R260_MANIFEST_SHA256,
            R259R_TREE_SHA256, r260_data, "R260")
        read_intermediate_manifest(
            args.successor_manifest.with_name("R259R.json"),
            R259R_MANIFEST_BYTES, R259R_MANIFEST_SHA256,
            R259R_TREE_SHA256, r260_data, "R259R")
        read_intermediate_manifest(
            args.successor_manifest.with_name("R258.json"),
            R258_MANIFEST_BYTES, R258_MANIFEST_SHA256,
            R258_TREE_SHA256, r258_data, "R258")
        read_intermediate_manifest(
            args.successor_manifest.with_name("R257S.json"),
            R257S_MANIFEST_BYTES, R257S_MANIFEST_SHA256,
            R258_TREE_SHA256, r258_data, "R257S")
        stage.replace(args.out)

    result = {
        "schema": "ega-r184-exact-replay-v1",
        "status": "PASS",
        "files": len(manifest["files"]),
        "bytes": sum(entry["bytes"] for entry in manifest["files"]),
        "tree_sha256": TREE_SHA256,
        "successor_tree_sha256": SUCCESSOR_TREE_SHA256,
        "r261_first_tree_sha256": R261_FIRST_TREE_SHA256,
        "r261_second_tree_sha256": R261_SECOND_TREE_SHA256,
        "r260_r259r_tree_sha256": R259R_TREE_SHA256,
        "r258_tree_sha256": R258_TREE_SHA256,
        "r257_first_tree_sha256": R257_FIRST_TREE_SHA256,
        "r257_second_tree_sha256": R257_SECOND_TREE_SHA256,
        "r256_tree_sha256": R256_TREE_SHA256,
        "r255_tree_sha256": R255_TREE_SHA256,
        "r255_citation_tree_sha256": R255_CITATION_TREE_SHA256,
        "r254_tree_sha256": R254_TREE_SHA256,
        "r248_tree_sha256": R248_TREE_SHA256,
        "r247_tree_sha256": R247_TREE_SHA256,
        "r243_tree_sha256": R243_TREE_SHA256,
        "intermediate_tree_sha256": R219_TREE_SHA256,
        "successor_inverted_files": sorted(set(
            r261_first_changed + r261_second_changed + r261_third_changed +
            r259r_changed + first_changed + second_changed + third_changed + r256_changed +
            citation_changed + proof_changed + r254_changed +
            r248_changed + r247_changed + r243_changed)),
        "r184_inverted_files": changed,
        "inverted_files": sorted(set(
            r261_first_changed + r261_second_changed + r261_third_changed +
            r259r_changed + first_changed + second_changed + third_changed + r256_changed +
            citation_changed + proof_changed + r254_changed +
            r248_changed + r247_changed + r243_changed + changed)),
        "inverse_operations": 41,
        "inverse_paths": 12,
        "source_mutated": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
