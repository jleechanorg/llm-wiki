#!/usr/bin/env python3
"""
Lint the LLM Wiki using coding agent.

Usage:
    python lint.py
    python lint.py --save
    python lint.py --agent=claudem
"""
import os
import sys
import re
import subprocess
from pathlib import Path
from collections import defaultdict
from datetime import date

WIKI_DIR = Path("/Users/jleechan/llm_wiki")
LOG_FILE = WIKI_DIR / "log.md"

DEFAULT_AGENT = os.environ.get("WIKI_AGENT", "claude")

def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""

def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def all_wiki_pages() -> list[Path]:
    return [p for p in WIKI_DIR.rglob("*.md")
            if p.name not in ("index.md", "log.md", "lint-report.md")]

def extract_wikilinks(content: str) -> list[str]:
    return re.findall(r'\[\[([^\]]+)\]\]', content)

def page_name_to_path(name: str) -> list[Path]:
    candidates = []
    for p in all_wiki_pages():
        if p.stem.lower() == name.lower() or p.stem == name:
            candidates.append(p)
    return candidates

def find_orphans(pages: list[Path]) -> list[Path]:
    inbound = defaultdict(int)
    for p in pages:
        content = read_file(p)
        for link in extract_wikilinks(content):
            resolved = page_name_to_path(link)
            for r in resolved:
                inbound[r] += 1
    return [p for p in pages if inbound[p] == 0 and p != WIKI_DIR / "overview.md"]

def find_broken_links(pages: list[Path]) -> list[tuple[Path, str]]:
    broken = []
    for p in pages:
        content = read_file(p)
        for link in extract_wikilinks(content):
            if not page_name_to_path(link):
                broken.append((p, link))
    return broken

def find_missing_entities(pages: list[Path]) -> list[str]:
    mention_counts = defaultdict(int)
    existing_pages = {p.stem.lower() for p in pages}
    for p in pages:
        content = read_file(p)
        links = extract_wikilinks(content)
        for link in links:
            if link.lower() not in existing_pages:
                mention_counts[link] += 1
    return [name for name, count in mention_counts.items() if count >= 3]

def run_lint():
    pages = all_wiki_pages()
    today = date.today().isoformat()

    if not pages:
        print("Wiki is empty. Nothing to lint.")
        return ""

    print(f"Linting {len(pages)} wiki pages...")

    # Structural checks
    orphans = find_orphans(pages)
    broken = find_broken_links(pages)
    missing_entities = find_missing_entities(pages)

    print(f"  orphans: {len(orphans)}")
    print(f"  broken links: {len(broken)}")
    print(f"  missing entity pages: {len(missing_entities)}")

    # Get sample pages for agent review
    sample = pages[:15]
    pages_context = ""
    for p in sample:
        rel = p.relative_to(WIKI_DIR)
        pages_context += f"\n\n### {rel}\n{read_file(p)[:1500]}"

    prompt = f"""You are linting an LLM Wiki. Review the pages below and identify:
1. Contradictions between pages (claims that conflict)
2. Stale content (summaries that newer sources have superseded)
3. Data gaps (important questions the wiki can't answer)
4. Concepts mentioned but lacking depth

Wiki at: {WIKI_DIR}

Pages (sample of {len(sample)}):
{pages_context}

Return a markdown lint report with sections:
## Contradictions
## Stale Content
## Data Gaps
## Concepts Needing Depth

Be specific — name exact pages and claims."""

    print("  Spawning coding agent for semantic lint...")

    try:
        result = subprocess.run(
            ["claude", "--dangerously-skip-permissions", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(WIKI_DIR)
        )

        if result.returncode == 0:
            semantic_report = result.stdout
        else:
            print(f"Agent error: {result.stderr}")
            semantic_report = "Error running semantic lint."
    except FileNotFoundError:
        print("Error: claude CLI not found")
        semantic_report = "Error: claude CLI not found."
    except subprocess.TimeoutExpired:
        print("Error: Agent timed out")
        semantic_report = "Error: Agent timed out."

    # Compose report
    report_lines = [
        f"# Wiki Lint Report — {today}",
        "",
        f"Scanned {len(pages)} pages.",
        "",
        "## Structural Issues",
        "",
    ]

    if orphans:
        report_lines.append("### Orphan Pages (no inbound links)")
        for p in orphans:
            report_lines.append(f"- `{p.relative_to(WIKI_DIR)}`")
        report_lines.append("")

    if broken:
        report_lines.append("### Broken Wikilinks")
        for page, link in broken:
            report_lines.append(f"- `{page.relative_to(WIKI_DIR)}` links to `[[{link}]]` — not found")
        report_lines.append("")

    if missing_entities:
        report_lines.append("### Missing Entity Pages")
        for name in missing_entities:
            report_lines.append(f"- `[[{name}]]`")
        report_lines.append("")

    if not orphans and not broken and not missing_entities:
        report_lines.append("No structural issues found.")
        report_lines.append("")

    report_lines.append("---")
    report_lines.append("")
    report_lines.append(semantic_report)

    report = "\n".join(report_lines)
    print("\n" + report)
    return report

def append_log(entry: str):
    existing = read_file(LOG_FILE)
    write_file(LOG_FILE, entry.strip() + "\n\n" + existing)

if __name__ == "__main__":
    save = "--save" in sys.argv

    report = run_lint()

    if save and report:
        report_path = WIKI_DIR / "lint-report.md"
        write_file(report_path, report)
        print(f"\nSaved: {report_path}")

    today = date.today().isoformat()
    append_log(f"## [{today}] lint | Wiki health check")
