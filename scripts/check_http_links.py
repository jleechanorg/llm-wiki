#!/usr/bin/env python3
"""Check all HTTP(S) links in the wiki actually respond with 2xx/3xx.

Two classes of links are checked:

1. **External URLs** — any `https?://` link found in wiki markdown.
   Verified via HTTP HEAD (falls back to GET on 405).

2. **Internal relative links** — `[text](path.md)` links to sibling .md files
   are verified as GitHub blob URLs:
   https://github.com/jleechanorg/worldai_wiki/blob/main/{path}
   This catches the case where a file exists locally but was never pushed.

Exit codes:
  0 — all links OK
  1 — one or more broken links
  2 — usage error
"""
from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GITHUB_BLOB_BASE = "https://github.com/jleechanorg/llm_wiki/blob/main/wiki"
DEFAULT_WIKI_DIRS = ["concepts", "entities", "syntheses"]
TOP_LEVEL_PAGES = ["index.md", "overview.md"]

# Links matching these patterns are skipped (examples, placeholders, etc.)
SKIP_PATTERNS = [
    re.compile(r"https?://example\.com"),
    re.compile(r"https?://localhost"),
    re.compile(r"https?://127\.0\.0\."),
]

HTTP_URL_RE = re.compile(r"\bhttps?://[^\s\)\]\"'<>]+")
MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)\s]+\.md)(?:#[^)]*)?\)")


def _strip_code_blocks(text: str) -> str:
    masked = re.sub(r"```.*?```", lambda m: " " * len(m.group(0)), text, flags=re.DOTALL)
    masked = re.sub(r"`[^`\n]*`", lambda m: " " * len(m.group(0)), masked)
    return masked


def _all_md_files(root: Path, dirs: list[str]) -> list[Path]:
    files: list[Path] = []
    for d in dirs:
        dpath = root / d
        if dpath.exists():
            files.extend(sorted(dpath.glob("*.md")))
    for name in TOP_LEVEL_PAGES:
        p = root / name
        if p.exists():
            files.append(p)
    return files


def _collect_links(root: Path, dirs: list[str]) -> dict[str, list[str]]:
    """Return {url: [source_file, ...]} for all links to check."""
    links: dict[str, list[str]] = {}

    def add(url: str, source: str) -> None:
        # Clean up trailing punctuation that got swept into the URL match
        url = url.rstrip(".,;:!?)")
        for pat in SKIP_PATTERNS:
            if pat.search(url):
                return
        links.setdefault(url, []).append(source)

    for path in _all_md_files(root, dirs):
        text = path.read_text()
        scan = _strip_code_blocks(text)
        src = str(path.relative_to(root))

        # External http(s) URLs
        for m in HTTP_URL_RE.finditer(scan):
            add(m.group(0), src)

        # Internal .md links → check as GitHub blob URLs
        for m in MD_LINK_RE.finditer(scan):
            rel = m.group(1)
            if rel.startswith(("http://", "https://", "/")):
                continue
            # Resolve relative to source file's directory
            resolved = (path.parent / rel).resolve()
            try:
                repo_path = resolved.relative_to(root.resolve())
            except ValueError:
                continue  # escapes repo root — ignore
            github_url = f"{GITHUB_BLOB_BASE}/{repo_path.as_posix()}"
            add(github_url, src)

    return links


def _check_url(url: str, timeout: int = 12, retries: int = 1) -> tuple[str, int | None, str]:
    """Return (url, status_code_or_None, error_msg)."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; worldai-wiki-link-checker/1.0; "
            "+https://github.com/jleechanorg/worldai_wiki)"
        )
    }
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=headers, method="HEAD")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return url, resp.status, ""
        except urllib.error.HTTPError as e:
            if e.code == 405:
                # Server doesn't support HEAD — retry with GET
                try:
                    req = urllib.request.Request(url, headers=headers, method="GET")
                    with urllib.request.urlopen(req, timeout=timeout) as resp:
                        return url, resp.status, ""
                except urllib.error.HTTPError as e2:
                    return url, e2.code, str(e2)
                except Exception as e2:
                    if attempt < retries:
                        time.sleep(1)
                        continue
                    return url, None, str(e2)
            return url, e.code, str(e)
        except Exception as e:
            if attempt < retries:
                time.sleep(1)
                continue
            return url, None, str(e)
    return url, None, "max retries exceeded"


def _is_ok(status: int | None) -> bool:
    if status is None:
        return False
    return 200 <= status < 400


def check(root: Path, dirs: list[str], workers: int = 8, github_only: bool = False,
          external_only: bool = False) -> int:
    links = _collect_links(root, dirs)
    if not links:
        print("No links found.")
        return 0

    to_check: dict[str, list[str]] = {}
    for url, sources in links.items():
        is_github = url.startswith(GITHUB_BLOB_BASE)
        if github_only and not is_github:
            continue
        if external_only and is_github:
            continue
        to_check[url] = sources

    print(f"Checking {len(to_check)} links with {workers} workers...")
    broken: list[tuple[str, int | None, str, list[str]]] = []

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_check_url, url): (url, srcs)
                   for url, srcs in to_check.items()}
        done = 0
        for future in as_completed(futures):
            url, srcs = futures[future]
            _, status, err = future.result()
            done += 1
            if not _is_ok(status):
                broken.append((url, status, err, srcs))
                print(f"  BROKEN [{status or 'ERR'}] {url}")
                for s in srcs[:2]:
                    print(f"    ↳ {s}")
            elif done % 20 == 0:
                print(f"  {done}/{len(to_check)} checked...")

    print(f"\n{'=' * 60}")
    if broken:
        print(f"FAIL: {len(broken)} broken link(s) out of {len(to_check)} checked")
        return 1
    print(f"OK: all {len(to_check)} links responded 2xx/3xx")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent.parent / "wiki"),
                        help="Wiki root dir (default: wiki/)")
    parser.add_argument("--dirs", nargs="+", default=DEFAULT_WIKI_DIRS,
                        help="Subdirs to scan (default: concepts entities syntheses)")
    parser.add_argument("--workers", type=int, default=8, help="Parallel workers (default: 8)")
    parser.add_argument("--github-only", action="store_true",
                        help="Only check internal GitHub blob URLs")
    parser.add_argument("--external-only", action="store_true",
                        help="Only check external (non-GitHub blob) URLs")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2
    return check(root, dirs=args.dirs, workers=args.workers,
                 github_only=args.github_only,
                 external_only=args.external_only)


if __name__ == "__main__":
    raise SystemExit(main())
