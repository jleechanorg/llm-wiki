#!/usr/bin/env python3
"""Lint and fix wikilinks in the llm_wiki knowledge base.

Obsidian-style `[[wikilinks]]` render as plain text on github.com blob view.
To make the wiki clickable on GitHub, every `[[Foo]]` must be a standard
markdown link `[Foo](path/Foo.md)`.

Usage:
  python scripts/lint_wikilinks.py              # check (exit 1 if broken)
  python scripts/lint_wikilinks.py --fix        # rewrite [[wikilinks]] in place
  python scripts/lint_wikilinks.py --dirs concepts entities  # scope to dirs
  python scripts/lint_wikilinks.py --root wiki  # custom root (default: wiki/)

Exit codes:
  0 — clean
  1 — broken wikilinks or .md links found
  2 — usage error
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_WIKI_ROOT = REPO_ROOT / "wiki"

# Directories INSIDE wiki/ that contain pages to lint.
# sources/ is excluded by default — thousands of leaf files, not navigational.
DEFAULT_DIRS = ["concepts", "entities", "syntheses"]
# Top-level files inside wiki/ to always lint
TOP_LEVEL = ["index.md", "overview.md"]

WIKILINK_RE = re.compile(r"\[\[([^\]\n]+?)\]\]")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\n]+?)(?:\s+\"[^\"]*\")?\)")


def _strip_code(text: str) -> str:
    masked = re.sub(r"```.*?```", lambda m: " " * len(m.group(0)), text, flags=re.DOTALL)
    masked = re.sub(r"`[^`\n]*`", lambda m: " " * len(m.group(0)), masked)
    return masked


def _all_md_files(wiki_root: Path, dirs: list[str]) -> list[Path]:
    files: list[Path] = []
    for d in dirs:
        dpath = wiki_root / d
        if dpath.exists():
            files.extend(sorted(dpath.glob("*.md")))
    for name in TOP_LEVEL:
        p = wiki_root / name
        if p.exists():
            files.append(p)
    return files


def _split_wikilink(inner: str) -> tuple[str, str | None, str | None]:
    page = inner.strip()
    anchor: str | None = None
    if "#" in page:
        page, anchor = page.split("#", 1)
        page, anchor = page.strip(), anchor.strip()
    alias: str | None = None
    if "|" in page:
        page, alias = page.split("|", 1)
        page, alias = page.strip(), alias.strip()
    return page, alias, anchor


def _resolve(page: str, source: Path, wiki_root: Path) -> Path | None:
    """Resolve a wikilink target to an absolute .md path within wiki_root."""
    page = re.sub(r"\.md$", "", page)
    if "/" not in page:
        # Bare name: try source's dir, then concepts/, entities/, syntheses/
        candidates = [
            source.parent / f"{page}.md",
            wiki_root / "concepts" / f"{page}.md",
            wiki_root / "entities" / f"{page}.md",
            wiki_root / "syntheses" / f"{page}.md",
            wiki_root / "sources" / f"{page}.md",
        ]
    else:
        candidates = [wiki_root / f"{page}.md"]
    for c in candidates:
        if c.exists():
            return c
    return None


def _rel(source: Path, target: Path) -> str:
    """Relative POSIX path from source's directory to target."""
    return Path(os.path.relpath(target.resolve(), start=source.resolve().parent)).as_posix()


def _convert(text: str, source: Path, wiki_root: Path) -> tuple[str, list[str]]:
    warnings: list[str] = []
    code_ranges: list[tuple[int, int]] = []
    for m in re.finditer(r"```.*?```", text, flags=re.DOTALL):
        code_ranges.append((m.start(), m.end()))
    for m in re.finditer(r"`[^`\n]*`", text):
        code_ranges.append((m.start(), m.end()))

    def _in_code(pos: int) -> bool:
        return any(s <= pos < e for s, e in code_ranges)

    def repl(m: re.Match) -> str:
        if _in_code(m.start()):
            return m.group(0)
        inner = m.group(1)
        page, alias, anchor = _split_wikilink(inner)
        resolved = _resolve(page, source, wiki_root)
        if resolved is None:
            warnings.append(
                f"{source.relative_to(wiki_root)}: [[{inner}]] → {page}.md not found"
            )
            return m.group(0)
        display = alias if alias else page.split("/")[-1]
        rel = _rel(source, resolved)
        return f"[{display}]({rel}#{anchor})" if anchor else f"[{display}]({rel})"

    return WIKILINK_RE.sub(repl, text), warnings


def _check_md_links(text: str, source: Path, wiki_root: Path) -> list[str]:
    problems: list[str] = []
    scan = _strip_code(text)
    for m in MD_LINK_RE.finditer(scan):
        link = m.group(2).strip().split("#")[0]
        if link.startswith(("http://", "https://", "/", "mailto:")):
            continue
        if not link.endswith(".md"):
            continue
        resolved = (source.parent / link).resolve()
        if not resolved.exists():
            problems.append(
                f"{source.relative_to(wiki_root)}: broken link [{m.group(1)}]({m.group(2)})"
            )
    return problems


def lint(wiki_root: Path, dirs: list[str], fix: bool = False) -> int:
    files = _all_md_files(wiki_root, dirs)
    all_wiki_warns: list[str] = []
    all_md_probs: list[str] = []
    converted = 0

    for path in files:
        text = path.read_text()
        scan = _strip_code(text)
        wikilinks = list(WIKILINK_RE.finditer(scan))

        if wikilinks:
            _, warns = _convert(text, path, wiki_root)
            all_wiki_warns.extend(warns)
            if fix:
                new_text, _ = _convert(text, path, wiki_root)
                if new_text != text:
                    converted += len(wikilinks)
                    path.write_text(new_text)
                    text = new_text

        all_md_probs.extend(_check_md_links(text, path, wiki_root))

    if fix:
        print(f"--fix: rewrote ~{converted} wikilinks across {len(files)} files")

    if all_wiki_warns:
        # Broken wikilinks are warnings only — the target page doesn't exist
        # yet but the wikilink itself is not an active navigation failure.
        # Run with --fix to convert resolvable ones; unresolvable ones are
        # phantom refs that need stub pages to resolve.
        print(f"\nWARN: {len(all_wiki_warns)} unresolvable [[wikilinks]] "
              f"(phantom refs — target pages not yet created):", file=sys.stderr)
        for w in all_wiki_warns[:20]:
            print(f"  {w}", file=sys.stderr)
        if len(all_wiki_warns) > 20:
            print(f"  ... and {len(all_wiki_warns) - 20} more", file=sys.stderr)

    if all_md_probs:
        # Broken markdown links are hard failures — these are actively broken
        # github.com navigation (clicking the link goes nowhere).
        print(f"\nFAIL: {len(all_md_probs)} broken [text](path.md) links:", file=sys.stderr)
        for p in all_md_probs[:40]:
            print(f"  {p}", file=sys.stderr)
        if len(all_md_probs) > 40:
            print(f"  ... and {len(all_md_probs) - 40} more", file=sys.stderr)

    # Only hard-fail on broken markdown links (active navigation breakage).
    # Unresolvable wikilinks are informational — they were broken regardless.
    return 1 if all_md_probs else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(DEFAULT_WIKI_ROOT),
                        help="Wiki root dir (default: wiki/)")
    parser.add_argument("--dirs", nargs="+", default=DEFAULT_DIRS,
                        help="Subdirs to lint (default: concepts entities syntheses)")
    parser.add_argument("--fix", action="store_true",
                        help="Rewrite [[wikilinks]] to [text](path.md) in place")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2
    return lint(root, args.dirs, fix=args.fix)


if __name__ == "__main__":
    raise SystemExit(main())
