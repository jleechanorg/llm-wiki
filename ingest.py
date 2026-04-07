#!/usr/bin/env python3
"""
Ingest a source document into the LLM Wiki using coding agent.

Usage:
    python ingest.py <path-to-source>
    python ingest.py ~/some-document.md

This spawns a coding agent to process the source and update the wiki:
  - Creates sources/<slug>.md
  - Updates index.md
  - Updates overview.md (if warranted)
  - Creates entity and concept pages
  - Appends to log.md
"""
import os
import sys
import json
import hashlib
import re
import subprocess
from pathlib import Path
from datetime import date

WIKI_DIR = Path("/Users/jleechan/llm_wiki")
LOG_FILE = WIKI_DIR / "log.md"
INDEX_FILE = WIKI_DIR / "index.md"
OVERVIEW_FILE = WIKI_DIR / "overview.md"

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]

def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""

def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  wrote: {path.relative_to(WIKI_DIR)}")

def build_wiki_context() -> str:
    parts = []
    if INDEX_FILE.exists():
        parts.append(f"## index.md\n{read_file(INDEX_FILE)}")
    if OVERVIEW_FILE.exists():
        parts.append(f"## overview.md\n{read_file(OVERVIEW_FILE)}")
    sources_dir = WIKI_DIR / "sources"
    if sources_dir.exists():
        recent = sorted(sources_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:3]
        for p in recent:
            parts.append(f"## {p.name}\n{p.read_text()[:1000]}")
    return "\n\n---\n\n".join(parts)

def spawn_coding_agent(prompt: str) -> dict:
    """Spawn Claude Code or other coding agent to do the work."""

    # Create a temp file with the task
    task_file = Path("/tmp/wiki_ingest_task.md")
    task_file.write_text(prompt)

    # Try claude CLI first, then codex, then others
    for cmd in ["claude", "codex", "cursor-agent"]:
        result = subprocess.run(
            ["which", cmd],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"  Using {cmd} for ingestion...")
            # Spawn the agent with the task
            proc = subprocess.Popen(
                [cmd, "--print", f"$(cat {task_file})"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = proc.communicate(timeout=300)

            if proc.returncode == 0 and stdout:
                try:
                    return json.loads(stdout)
                except:
                    pass

    print("Error: No coding agent found (tried claude, codex, cursor-agent)")
    sys.exit(1)

def update_index(new_entry: str, section: str = "Sources"):
    content = read_file(INDEX_FILE)
    if not content:
        content = "# Wiki Index\n\n## Overview\n- [Overview](overview.md)\n\n## Sources\n\n## Entities\n\n## Concepts\n\n## Syntheses\n"
    section_header = f"## {section}"
    if section_header in content:
        content = content.replace(section_header + "\n", section_header + "\n" + new_entry + "\n")
    else:
        content += f"\n{section_header}\n{new_entry}\n"
    write_file(INDEX_FILE, content)

def append_log(entry: str):
    existing = read_file(LOG_FILE)
    write_file(LOG_FILE, entry.strip() + "\n\n" + existing)

def ingest(source_path: str):
    source = Path(source_path).expanduser().resolve()
    if not source.exists():
        print(f"Error: file not found: {source_path}")
        sys.exit(1)

    source_content = source.read_text(encoding="utf-8")
    source_hash = sha256(source_content)
    today = date.today().isoformat()

    print(f"\nIngesting: {source.name}  (hash: {source_hash})")
    print("  (Using coding agent instead of direct API)")

    wiki_context = build_wiki_context()

    prompt = f"""You are maintaining an LLM Wiki (Karpathy pattern). Process this source document and integrate its knowledge into the wiki.

The wiki is at: {WIKI_DIR}

## Wiki Schema (follow exactly):

Every page must have YAML frontmatter:
```yaml
---
title: "Page Title"
type: source | entity | concept | synthesis
tags: []
sources: []
last_updated: {today}
---
```

Use [[PageName]] wikilinks to link to other wiki pages.

## Current wiki state:
{wiki_context if wiki_context else "(wiki is empty)"}

## Source to ingest:
=== SOURCE START ===
{source_content[:5000]}
=== SOURCE END ===

Process this source and return ONLY a JSON object:
{{
  "title": "Human-readable title",
  "slug": "kebab-case-slug",
  "source_page": "full markdown for sources/<slug>.md",
  "index_entry": "- [Title](sources/slug.md) — one-line summary",
  "overview_update": "updated overview.md content, or null",
  "entity_pages": [{{"path": "entities/EntityName.md", "content": "full content"}}],
  "concept_pages": [{{"path": "concepts/ConceptName.md", "content": "full content"}}],
  "contradictions": ["list any contradictions", or []],
  "log_entry": "## [{today}] ingest | <title>\\n\\nKey claims: ..."
}}

Respond ONLY with JSON, no markdown fences or other text."""

    # Write task to temp file for agent
    task_file = Path("/tmp/wiki_ingest_task.md")
    task_file.write_text(prompt)

    print("  Spawning coding agent...")

    # Use claude CLI with --dangerously-skip-permissions to avoid prompts
    try:
        result = subprocess.run(
            ["claude", "--dangerously-skip-permissions", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(WIKI_DIR)
        )

        if result.returncode == 0:
            raw = result.stdout
            # Try to extract JSON from response
            try:
                # Find JSON in response
                match = re.search(r"\{[\s\S]*\}", raw)
                if match:
                    data = json.loads(match.group())
                else:
                    print("No JSON found in agent response")
                    print(f"Response: {raw[:500]}")
                    sys.exit(1)
            except (ValueError, json.JSONDecodeError) as e:
                print(f"Error parsing agent response: {e}")
                Path("/tmp/ingest_debug.txt").write_text(raw)
                sys.exit(1)
        else:
            print(f"Agent error: {result.stderr}")
            sys.exit(1)
    except FileNotFoundError:
        print("Error: claude CLI not found")
        print("Install Claude Code: https://claude.ai/code")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("Error: Agent timed out")
        sys.exit(1)

    # Write source page
    slug = data.get("slug", source.stem)
    write_file(WIKI_DIR / "sources" / f"{slug}.md", data.get("source_page", ""))

    # Write entity pages
    for page in data.get("entity_pages", []):
        write_file(WIKI_DIR / page["path"], page["content"])

    # Write concept pages
    for page in data.get("concept_pages", []):
        write_file(WIKI_DIR / page["path"], page["content"])

    # Update overview
    if data.get("overview_update"):
        write_file(OVERVIEW_FILE, data["overview_update"])

    # Update index
    update_index(data.get("index_entry", ""), section="Sources")

    # Append log
    append_log(data.get("log_entry", ""))

    # Report contradictions
    contradictions = data.get("contradictions", [])
    if contradictions:
        print("\n  ⚠️  Contradictions detected:")
        for c in contradictions:
            print(f"     - {c}")

    print(f"\nDone. Ingested: {data.get('title', source.name)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ingest.py <path-to-source>")
        sys.exit(1)
    ingest(sys.argv[1])
