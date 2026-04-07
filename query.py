#!/usr/bin/env python3
"""
Query the LLM Wiki using coding agent.

Usage:
    python query.py "What are the main themes?"
    python query.py "Summarize EntityName" --save synthesis/my-analysis.md
    python query.py "question" --agent=claudem
"""
import os
import sys
import re
import json
import subprocess
from pathlib import Path
from datetime import date

WIKI_DIR = Path("/Users/jleechan/llm_wiki")
INDEX_FILE = WIKI_DIR / "index.md"
LOG_FILE = WIKI_DIR / "log.md"

DEFAULT_AGENT = os.environ.get("WIKI_AGENT", "claude")

def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""

def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  saved: {path.relative_to(WIKI_DIR)}")

def find_relevant_pages(question: str, index_content: str) -> list[Path]:
    """Find wiki pages relevant to the question."""
    md_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', index_content)
    question_lower = question.lower()
    relevant = []
    for title, href in md_links:
        if any(word in question_lower for word in title.lower().split() if len(word) > 3):
            p = WIKI_DIR / href
            if p.exists():
                relevant.append(p)
    overview = WIKI_DIR / "overview.md"
    if overview.exists() and overview not in relevant:
        relevant.insert(0, overview)
    return relevant[:10]

def append_log(entry: str):
    existing = read_file(LOG_FILE)
    write_file(LOG_FILE, entry.strip() + "\n\n" + existing)

def query(question: str, save_path: str | None = None):
    today = date.today().isoformat()

    # Read index
    index_content = read_file(INDEX_FILE)
    if not index_content:
        print("Wiki is empty. Ingest some sources first.")
        sys.exit(1)

    # Find relevant pages
    relevant_pages = find_relevant_pages(question, index_content)
    print(f"  Found {len(relevant_pages)} relevant pages")

    # Build context from relevant pages
    pages_context = ""
    for p in relevant_pages:
        rel = p.relative_to(WIKI_DIR)
        pages_context += f"\n\n### {rel}\n{p.read_text(encoding='utf-8')[:2000]}"

    if not pages_context:
        pages_context = f"\n\n### index.md\n{index_content[:2000]}"

    prompt = f"""You are querying an LLM Wiki (Karpathy pattern). Use the wiki pages below to answer the question.

Wiki at: {WIKI_DIR}

## Wiki pages (use these to answer):
{pages_context}

## Question: {question}

Write a well-structured markdown answer with headers, bullets, and [[wikilink]] citations. At the end, add a ## Sources section listing the pages you drew from.

Respond ONLY with the answer (no JSON)."""

    print("  Spawning coding agent...")

    try:
        result = subprocess.run(
            ["claude", "--dangerously-skip-permissions", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(WIKI_DIR)
        )

        if result.returncode == 0:
            answer = result.stdout
        else:
            print(f"Agent error: {result.stderr}")
            sys.exit(1)
    except FileNotFoundError:
        print("Error: claude CLI not found")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("Error: Agent timed out")
        sys.exit(1)

    print("\n" + "=" * 60)
    print(answer)
    print("=" * 60)

    # Optionally save
    if save_path is not None:
        if save_path == "":
            slug = input("\nSave as (slug): ").strip()
            if not slug:
                print("Skipping save.")
                return
            save_path = f"syntheses/{slug}.md"

        full_save_path = WIKI_DIR / save_path
        frontmatter = f"""---
title: "{question[:80]}"
type: synthesis
tags: []
sources: []
last_updated: {today}
---

"""
        write_file(full_save_path, frontmatter + answer)
        print(f"  saved: {save_path}")

    append_log(f"## [{today}] query | {question[:80]}")

if __name__ == "__main__":
    save_path = None
    question = " ".join(sys.argv[1:])
    if "--save" in sys.argv:
        idx = sys.argv.index("--save")
        question = " ".join(sys.argv[1:idx])
        save_path = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else ""

    if not question:
        print("Usage: python query.py <question> [--save]")
        sys.exit(1)

    query(question, save_path)
