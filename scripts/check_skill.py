#!/usr/bin/env python3
"""Structure validator for the paper-deep-reading skill repo.

Prints PASS/FAIL per check (C1-C7) and exits 0 only when all pass.
Run from anywhere: the repo root is resolved from this script's location.

Usage: python3 scripts/check_skill.py
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SKILL_PATH = REPO_ROOT / "skills" / "paper-deep-reading" / "SKILL.md"
REFERENCES_DIR = REPO_ROOT / "skills" / "paper-deep-reading" / "references"
MEMORY_DIR = REPO_ROOT / "skills" / "paper-deep-reading" / "memory" / "paper-deep-reading"
EXAMPLES_DIR = REPO_ROOT / "examples"
DEMO_DIR = REPO_ROOT / "demo"
EVALS_DIR = REPO_ROOT / "evals"

TRIGGER_WORDS = ["读论文", "文献", "看不懂", "值不值得读", "继续读", "出笔记"]

REFERENCE_FILES = [
    "three-pass-method.md",
    "critical-checklist.md",
    "reader-diagnosis.md",
    "note-template.md",
]

NOTE_FIELDS = [
    "## 问题",
    "## 核心贡献",
    "## 方法拆解",
    "## 关键公式与直觉",
    "## 实验与证据强度",
    "## 局限与质疑",
    "## 与我读它的目的的关系",
    "## 延伸阅读",
]

OVERVIEW_MARKERS = ["【一句话】", "【问题】", "【方法】", "【证据】", "【判断】"]

SKILL_LINE_LIMIT = 200


def extract_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    if end == -1:
        return ""
    return text[3:end]


def extract_description(frontmatter: str) -> str:
    """Collect a possibly folded YAML scalar: the description line plus
    following lines indented deeper than the key."""
    lines = frontmatter.splitlines()
    collected = []
    for i, line in enumerate(lines):
        if re.match(r"^description:", line):
            collected.append(line.split(":", 1)[1])
            for follow in lines[i + 1:]:
                if follow[:1] in (" ", "\t"):
                    collected.append(follow)
                else:
                    break
            break
    return "".join(collected)


def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" ({detail})" if detail and not ok else ""))
    return ok


def c1_frontmatter():
    if not SKILL_PATH.is_file():
        return check("C1 frontmatter", False, f"{SKILL_PATH} missing")
    fm = extract_frontmatter(SKILL_PATH.read_text(encoding="utf-8"))
    if f"name: paper-deep-reading" not in fm:
        return check("C1 frontmatter", False, "name line missing")
    desc = extract_description(fm)
    missing = [w for w in TRIGGER_WORDS if w not in desc]
    return check("C1 frontmatter", not missing, f"trigger words missing: {missing}")


def c2_line_count():
    if not SKILL_PATH.is_file():
        return check("C2 line count", False, f"{SKILL_PATH} missing")
    n = len(SKILL_PATH.read_text(encoding="utf-8").splitlines())
    return check("C2 line count", n < SKILL_LINE_LIMIT, f"{n} lines >= {SKILL_LINE_LIMIT}")


def c3_references():
    missing = [f for f in REFERENCE_FILES if not (REFERENCES_DIR / f).is_file()]
    return check("C3 references", not missing, f"missing: {missing}")


def c4_note_fields():
    template = REFERENCES_DIR / "note-template.md"
    if not template.is_file():
        return check("C4 note fields", False, "note-template.md missing")
    text = template.read_text(encoding="utf-8")
    missing = [f for f in NOTE_FIELDS if f not in text]
    if missing:
        return check("C4 note fields", False, f"template missing: {missing}")
    examples = sorted(EXAMPLES_DIR.glob("*.md")) if EXAMPLES_DIR.is_dir() else []
    if not examples:
        return check("C4 note fields", False, "no examples/*.md")
    for example in examples:
        etext = example.read_text(encoding="utf-8")
        missing = [f for f in NOTE_FIELDS if f not in etext]
        if missing:
            return check("C4 note fields", False, f"{example.name} missing: {missing}")
    return check("C4 note fields", True)


def c5_overview_markers():
    demos = sorted(DEMO_DIR.glob("*.md")) if DEMO_DIR.is_dir() else []
    if not demos:
        return check("C5 overview card", False, "no demo/*.md")
    for demo in demos:
        text = demo.read_text(encoding="utf-8")
        missing = [m for m in OVERVIEW_MARKERS if m not in text]
        if missing:
            return check("C5 overview card", False, f"{demo.name} missing: {missing}")
    return check("C5 overview card", True)


def c6_memory_sample():
    samples = sorted(MEMORY_DIR.glob("*.md")) if MEMORY_DIR.is_dir() else []
    return check("C6 memory sample", bool(samples), "memory/paper-deep-reading/*.md empty")


def c7_evals():
    cases_dir = EVALS_DIR / "cases"
    cases = sorted(cases_dir.glob("E*.md")) if cases_dir.is_dir() else []
    if len(cases) < 8:
        return check("C7 evals", False, f"{len(cases)} case files, need >= 8")
    for name in ("scoring_rubric.md", "failure_cases.md"):
        if not (EVALS_DIR / name).is_file():
            return check("C7 evals", False, f"{name} missing")
    return check("C7 evals", True)


def main() -> int:
    results = [
        c1_frontmatter(),
        c2_line_count(),
        c3_references(),
        c4_note_fields(),
        c5_overview_markers(),
        c6_memory_sample(),
        c7_evals(),
    ]
    print(f"\n{sum(results)}/{len(results)} checks passed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
