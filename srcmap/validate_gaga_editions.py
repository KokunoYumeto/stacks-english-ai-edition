#!/usr/bin/env python3
"""Narrow structural validator for the Japanese and Simplified-Chinese GAGA sources."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
ENGLISH = ROOT / "gaga.tex"
ENGLISH_CHAPTERS = ROOT / "chapters.tex"
ENGLISH_SHA256 = "BBCCEE29FE3AF084E8435F3E32F8537EE3DDED2558E1A9FCD2940F8664BB5201"

COMMAND_TARGETS = ("label", "ref", "eqref", "pageref", "hyperref", "cite")
ENVIRONMENT_RE = re.compile(r"\\(begin|end)\{([^{}]+)\}")
TARGET_RE = re.compile(
    r"\\(" + "|".join(command for command in COMMAND_TARGETS if command != "hyperref")
    + r")(?:\[[^\]]*\])?\{([^{}]+)\}"
)
HYPERREF_TARGET_RE = re.compile(r"\\hyperref\[([^\]]+)\]\{")
INLINE_OR_DISPLAY_MATH_RE = re.compile(r"(?<!\\)(\$\$.*?(?<!\\)\$\$|\$.*?(?<!\\)\$)", re.S)
CJK_RE = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        match = re.search(r"(?<!\\)%", line)
        lines.append(line[: match.start()] if match else line)
    return "\n".join(lines)


def ordered_targets(text: str, command: str) -> list[str]:
    if command == "hyperref":
        return HYPERREF_TARGET_RE.findall(text)
    return [target for found, target in TARGET_RE.findall(text) if found == command]


def normalized_math(text: str) -> list[str]:
    return [re.sub(r"\s+", " ", item).strip() for item in INLINE_OR_DISPLAY_MATH_RE.findall(text)]


def structural_math(item: str) -> str:
    """Ignore layout whitespace and translated prose inside math text boxes."""
    item = re.sub(r"\\(?:text|hbox)\{[^{}]*\}", "", item)
    return re.sub(r"\s+", "", item)


def environment_events(text: str) -> list[tuple[str, str]]:
    return ENVIRONMENT_RE.findall(text)


def validate_one(language: str, source: Path, chapters: Path) -> dict[str, Any]:
    errors: list[str] = []
    english = strip_comments(ENGLISH.read_text(encoding="utf-8"))
    localized = strip_comments(source.read_text(encoding="utf-8"))
    english_chapters = strip_comments(ENGLISH_CHAPTERS.read_text(encoding="utf-8"))
    localized_chapters = strip_comments(chapters.read_text(encoding="utf-8"))

    expected_font = "Yu Gothic" if language == "ja" else "SimSun"
    expected_input = f"output/source/chapters-{language if language == 'ja' else 'zh-cn'}"
    expected_captions = (
        {"proof": "証明", "theorem": "定理", "proposition": "命題", "lemma": "補題",
         "definition": "定義", "remark": "注意"}
        if language == "ja"
        else {"proof": "证明", "theorem": "定理", "proposition": "命题", "lemma": "引理",
              "definition": "定义", "remark": "注"}
    )
    require(f"\\def\\GAGACJKMainFont{{{expected_font}}}" in localized,
            f"{language}: CJK font declaration missing", errors)
    require("\\renewcommand{\\contentsname}" in localized,
            f"{language}: contents localization missing", errors)
    require("\\renewcommand{\\refname}" in localized,
            f"{language}: reference-heading localization missing", errors)
    require(
        f"\\renewcommand{{\\proofname}}{{{expected_captions['proof']}}}" in localized,
        f"{language}: proof-caption localization missing",
        errors,
    )
    for environment in ("theorem", "proposition", "lemma", "definition", "remark"):
        require(
            f"\\newtheorem{{{environment}}}[subsection]{{{expected_captions[environment]}}}"
            in localized,
            f"{language}: {environment}-caption localization missing",
            errors,
        )
    require(localized.count(f"\\input{{{expected_input}}}") == 1,
            f"{language}: localized chapters input missing or duplicated", errors)
    require(localized.count("\\input{chapters}") == 0,
            f"{language}: English chapters input remains", errors)

    target_counts: dict[str, int] = {}
    for command in COMMAND_TARGETS:
        left = ordered_targets(english, command)
        right = ordered_targets(localized, command)
        target_counts[command] = len(left)
        require(left == right, f"{language}: ordered \\{command} targets differ", errors)

    left_env = environment_events(english)
    right_env = environment_events(localized)
    require(left_env == right_env, f"{language}: ordered environment events differ", errors)
    require(Counter(name for action, name in right_env if action == "begin")
            == Counter(name for action, name in right_env if action == "end"),
            f"{language}: begin/end environment counts are unbalanced", errors)

    left_math = normalized_math(english)
    right_math = normalized_math(localized)
    require(
        Counter(structural_math(item) for item in left_math)
        == Counter(structural_math(item) for item in right_math),
        f"{language}: inline/display mathematical structure differs",
        errors,
    )

    left_chapter_targets = ordered_targets(english_chapters, "hyperref")
    right_chapter_targets = ordered_targets(localized_chapters, "hyperref")
    require(left_chapter_targets == right_chapter_targets,
            f"{language}: chapter hyperref targets differ", errors)
    require(len(left_chapter_targets) == 118,
            f"{language}: expected 118 chapter hyperref targets", errors)
    require(re.findall(r"\\setcounter\{enumi\}\{\d+\}", english_chapters)
            == re.findall(r"\\setcounter\{enumi\}\{\d+\}", localized_chapters),
            f"{language}: chapter counters differ", errors)
    require(environment_events(english_chapters) == environment_events(localized_chapters),
            f"{language}: chapter environment events differ", errors)

    cjk_characters = len(CJK_RE.findall(localized + localized_chapters))
    require(cjk_characters >= 2500, f"{language}: too little localized CJK text ({cjk_characters})", errors)
    english_markers = {
        marker: len(re.findall(marker, localized, re.I))
        for marker in (
            r"\bThis chapter develops\b", r"\bThroughout this section\b",
            r"\bIt remains\b", r"\bWe first\b", r"\bThe assertion follows\b",
            r"\bOther chapters\b", r"\bApplications of the comparison theorems\b",
        )
    }
    require(not any(english_markers.values()),
            f"{language}: known English prose markers remain: {english_markers}", errors)

    return {
        "language": language,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "source": {"path": str(source.relative_to(ROOT)).replace("\\", "/"),
                   "bytes": source.stat().st_size, "sha256": sha256(source)},
        "chapters": {"path": str(chapters.relative_to(ROOT)).replace("\\", "/"),
                     "bytes": chapters.stat().st_size, "sha256": sha256(chapters)},
        "counts": {
            "ordered_targets": target_counts,
            "environment_events": len(left_env),
            "math_segments": len(left_math),
            "chapter_hyperrefs": len(left_chapter_targets),
            "cjk_characters": cjk_characters,
            "known_english_prose_markers": english_markers,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", choices=("ja", "zh-cn", "all"), default="all")
    args = parser.parse_args()
    if sha256(ENGLISH) != ENGLISH_SHA256:
        raise RuntimeError("Authoritative English GAGA source identity drift")
    selected = ("ja", "zh-cn") if args.language == "all" else (args.language,)
    results = []
    for language in selected:
        source = ROOT / "output" / "source" / f"gaga-{language}.tex"
        chapters = ROOT / "output" / "source" / f"chapters-{language}.tex"
        if not source.is_file() or not chapters.is_file():
            results.append({"language": language, "status": "FAIL",
                            "errors": ["localized source or chapter list missing"]})
            continue
        results.append(validate_one(language, source, chapters))
    payload = {"schema": "gaga-localized-source-validation-v1",
               "english_sha256": ENGLISH_SHA256, "results": results,
               "status": "PASS" if all(row["status"] == "PASS" for row in results) else "FAIL"}
    print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
