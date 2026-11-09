#!/usr/bin/env python3
"""스킬 폴더 구조 검사.

사용: python3 scripts/check_skills.py [skills_root] [--expect a,b,c]
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REF_RE = re.compile(r"references/[\w\-]+\.md")


def _frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    meta = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta


def check_skill(path: Path, common: "str | None") -> list:
    name = path.name
    skill_md = path / "SKILL.md"
    if not skill_md.is_file():
        return ["missing SKILL.md"]
    text = skill_md.read_text(encoding="utf-8")
    meta = _frontmatter(text)
    problems = []
    if "name" not in meta:
        problems.append("no name in frontmatter")
    elif meta["name"] != name:
        problems.append(f"name '{meta['name']}' != folder '{name}'")
    desc = meta.get("description", "")
    if not desc:
        problems.append("no description in frontmatter")
    elif len(desc) > 1024:
        problems.append("description longer than 1024 chars")
    for ref in sorted(set(REF_RE.findall(text))):
        if not (path / ref).is_file():
            problems.append(f"missing {ref}")
    if common is not None and common.strip() not in text:
        problems.append("common rules not included")
    return problems


def check_root(root: Path, expect: list = [], common: "str | None" = None) -> list:
    problems = []
    names = {p.name for p in root.iterdir() if p.is_dir()} if root.is_dir() else set()
    for name in expect:
        if name not in names:
            problems.append(f"{name}: missing SKILL.md")
    for name in sorted(names):
        problems.extend(f"{name}: {p}" for p in check_skill(root / name, common))
    return problems


def main(argv: list) -> int:
    expect = []
    args = list(argv)
    if "--expect" in args:
        i = args.index("--expect")
        expect = [s for s in args[i + 1].split(",") if s]
        del args[i:i + 2]
    root = Path(args[0]) if args else REPO / ".agents" / "skills"
    common_file = REPO / "docs" / "common-rules.md"
    common = common_file.read_text(encoding="utf-8") if common_file.is_file() else None
    problems = check_root(root, expect, common)
    if problems:
        print("\n".join(problems))
        return 1
    count = len([p for p in root.iterdir() if p.is_dir()]) if root.is_dir() else 0
    print(f"OK {count} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
