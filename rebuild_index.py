#!/usr/bin/env python3
"""
Rebuild index and log from all source files.
"""
import os
import re
from pathlib import Path
from datetime import date

WIKI_DIR = Path("/Users/jleechan/llm_wiki")
SOURCES_DIR = WIKI_DIR / "sources"
INDEX_FILE = WIKI_DIR / "index.md"
LOG_FILE = WIKI_DIR / "log.md"
OVERVIEW_FILE = WIKI_DIR / "overview.md"

def extract_frontmatter(content: str):
    """Extract YAML frontmatter from markdown."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm

def extract_title(content: str, filename: str) -> str:
    """Get title from frontmatter or filename."""
    fm = extract_frontmatter(content)
    if fm.get('title'):
        return fm['title']
    # Fallback: convert filename to title
    name = filename.replace('.md', '').replace('-', ' ').replace('_', ' ')
    # Remove hash prefix if present
    name = re.sub(r'^[0-9a-f]{10}-', '', name)
    return name.title()

def extract_summary(content: str, max_len: int = 100) -> str:
    """Extract first paragraph as summary."""
    fm = extract_frontmatter(content)
    rest = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    # Get first non-empty paragraph
    for para in rest.split('\n\n'):
        para = para.strip()
        if para and not para.startswith('#'):
            # Remove markdown formatting
            para = re.sub(r'#+ ', '', para)
            para = para[:max_len] + ('...' if len(para) > max_len else '')
            return para
    return ""

def rebuild_index():
    """Rebuild index from all sources."""
    sources = sorted(SOURCES_DIR.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)

    print(f"Rebuilding index from {len(sources)} sources...")

    entries = []
    for src in sources:
        try:
            content = src.read_text(encoding='utf-8', errors='ignore')
            title = extract_title(content, src.name)
            summary = extract_summary(content)
            slug = src.stem
            entry = f"- [{title}](sources/{slug}.md) — {summary}"
            entries.append(entry)
        except Exception as e:
            print(f"  Error reading {src.name}: {e}")

    # Build new index
    index = """# Wiki Index

## Overview
- [Overview](overview.md)

## Sources

"""
    for entry in entries:
        index += entry + "\n"

    index += """

## Entities

## Concepts

## Syntheses
"""

    INDEX_FILE.write_text(index, encoding='utf-8')
    print(f"Wrote index with {len(entries)} entries")

def rebuild_log():
    """Rebuild log from all sources."""
    sources = sorted(SOURCES_DIR.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    today = date.today().isoformat()

    log_parts = [f"## [{today}] batch_rebuild | Restored index from {len(sources)} sources\n"]

    for src in sources[:500]:  # Most recent 500
        try:
            content = src.read_text(encoding='utf-8', errors='ignore')
            fm = extract_frontmatter(content)
            title = fm.get('title', src.stem)
            last_updated = fm.get('last_updated', today)
            log_parts.append(f"## [{last_updated}] ingest | {title}\n")
        except:
            pass

    LOG_FILE.write_text("\n".join(log_parts), encoding='utf-8')
    print(f"Wrote log with {len(log_parts)} entries")

def rebuild_overview():
    """Create overview from sources."""
    sources = sorted(SOURCES_DIR.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)

    # Sample titles from recent sources
    recent_titles = []
    for src in sources[:20]:
        try:
            content = src.read_text(encoding='utf-8', errors='ignore')
            title = extract_title(content, src.name)
            recent_titles.append(title)
        except:
            pass

    overview = f"""# Wiki Overview

This wiki contains {len(sources)} source documents covering AI, Claude Code, D&D game development, and more.

## Recent Sources
"""
    for t in recent_titles[:15]:
        overview += f"- {t}\n"

    overview += """
## Categories
- [[Sources]] — Raw documents and notes
- [[Entities]] — People, companies, projects
- [[Concepts]] — Ideas, frameworks, methods
- [[Syntheses]] — Query answers and analyses
"""

    OVERVIEW_FILE.write_text(overview, encoding='utf-8')
    print(f"Wrote overview referencing {len(recent_titles)} recent sources")

if __name__ == "__main__":
    rebuild_index()
    rebuild_log()
    rebuild_overview()
    print("\nDone! Wiki rebuilt from all sources.")
