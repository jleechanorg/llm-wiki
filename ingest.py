#!/usr/bin/env python3
"""
Ingest a source document into the LLM Wiki using coding agent.

Usage:
    python ingest.py <path-to-source>
    python ingest.py ~/some-document.md

Options:
    --agent=NAME   Use specific agent (default: from WIKI_AGENT env or 'claude')
                   Options: claude, claudem, codex, cursor

Environment:
    WIKI_AGENT     Default agent to use (e.g., 'claudem')
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

# Get agent from env or CLI args
DEFAULT_AGENT = os.environ.get("WIKI_AGENT", "claude")
AGENT_NAME = DEFAULT_AGENT
AGENT_CMD = {
    "claude": "claude",
    "claudem": "claudem",
    "codex": "codex",
    "cursor": "cursor-agent",
    "ao": "ao",  # Agent Orchestrator integration
}.get(AGENT_NAME, "claude")

# AO runtime configuration (when AGENT_NAME is "ao")
AO_RUNTIME = os.environ.get("AO_RUNTIME", "antigravity")  # antigravity, tmux, etc.
AO_PROJECT = os.environ.get("AO_PROJECT", None)  # Explicit AO project ID


def ao_ingest(source: Path, source_content: str, prompt: str):
    """Ingest using Agent Orchestrator workers."""
    import tempfile

    # Write prompt to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(prompt)
        prompt_file = f.name

    try:
        # Build ao spawn command
        cmd = ["ao", "spawn"]
        if AO_RUNTIME:
            cmd.extend(["--runtime", AO_RUNTIME])
        if AO_PROJECT:
            cmd.extend(["-p", AO_PROJECT])
        cmd.append("wiki-ingest")  # Issue identifier

        print(f"  Running: {' '.join(cmd)}")
        print(f"  Prompt file: {prompt_file}")

        # Run ao spawn with the prompt
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,
            cwd=str(WIKI_DIR)
        )

        if result.returncode == 0:
            print(f"  AO response: {result.stdout[:500]}")
            return {"status": "ao_spawned", "output": result.stdout}
        else:
            print(f"  AO error: {result.stderr}")
            # Fall back to inline processing
            print("  Falling back to inline processing...")
            return inline_ao_ingest(source, source_content, prompt)

    finally:
        os.unlink(prompt_file)


def inline_ao_ingest(source: Path, source_content: str, prompt: str):
    """Process ingestion using AO workers inline."""
    # Process via AO CLI with workers
    cmd = [
        "ao", "spawn",
        "--runtime", AO_RUNTIME or "antigravity",
        "--max-depth", "2",
        "wiki-source-ingest"
    ]

    try:
        result = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=600,
            cwd=str(WIKI_DIR)
        )

        if result.returncode == 0:
            # Try to parse JSON from output
            try:
                data = json.loads(result.stdout)
                return data
            except json.JSONDecodeError:
                print(f"  Could not parse AO JSON, using fallback")
                return fallback_ingest(source, source_content)
        else:
            print(f"  AO inline error: {result.stderr}")
            return fallback_ingest(source, source_content)

    except Exception as e:
        print(f"  AO error: {e}")
        return fallback_ingest(source, source_content)


def fallback_ingest(source: Path, source_content: str):
    """Simple fallback when AO is not available."""
    print("  Using fallback ingestion...")
    # Basic extraction - will be enhanced by wiki
    title = source.stem.replace('-', ' ').title()
    slug = source.stem.lower()

    data = {
        "title": title,
        "slug": slug,
        "source_page": f"""---
title: "{title}"
type: source
tags: []
last_updated: {date.today().isoformat()}
---

## Summary
Ingested from {source.name}

## Key Claims
- Source file: {source.name}

## Connections
- [[Wiki Index]] — main index
""",
        "index_entry": f"- [{title}](sources/{slug}.md) — {source.name}",
        "overview_update": None,
        "entity_pages": [],
        "concept_pages": [],
        "contradictions": [],
        "log_entry": f"## [{date.today().isoformat()}] ingest | {title}\n\nIngested via fallback mode"
    }
    return data

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
        # Limit index to last 100 lines to avoid arg-list-too-long
        idx_content = read_file(INDEX_FILE)
        idx_lines = idx_content.split("\n")
        if len(idx_lines) > 100:
            idx_content = "\n".join(idx_lines[:50]) + f"\n\n... ({len(idx_lines)} total entries)"
        parts.append(f"## index.md\n{idx_content}")
    if OVERVIEW_FILE.exists():
        parts.append(f"## overview.md\n{read_file(OVERVIEW_FILE)}")
    sources_dir = WIKI_DIR / "sources"
    if sources_dir.exists():
        recent = sorted(sources_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:3]
        for p in recent:
            parts.append(f"## {p.name}\n{p.read_text()[:1000]}")
    return "\n\n---\n\n".join(parts)

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
    print(f"  Using agent: {AGENT_NAME}")

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

    print(f"  Spawning coding agent: {AGENT_NAME}...")

    # AO integration: use Agent Orchestrator workers
    if AGENT_NAME == "ao":
        return ao_ingest(source, source_content, prompt)

    # Use shell=True for claudem to work via bash
    cmd = [AGENT_CMD, "--dangerously-skip-permissions", "-p", prompt]

    # Build env with WIKI_AGENT
    run_env = {**os.environ, "WIKI_AGENT": AGENT_NAME}

    # For claudem (MiniMax): use direct claude binary path, pass prompt via stdin to avoid arg limit
    if AGENT_NAME == "claudem":
        cmd = ["/Applications/cmux DEV.app/Contents/Resources/bin/claude",
               "--dangerously-skip-permissions", "-p", "-"]
        run_env["ANTHROPIC_BASE_URL"] = "https://api.minimax.io/anthropic"
        run_env["ANTHROPIC_AUTH_TOKEN"] = os.environ.get("MINIMAX_API_KEY", os.environ.get("ANTHROPIC_AUTH_TOKEN", ""))
        run_env["ANTHROPIC_MODEL"] = "MiniMax-M2.5"
        run_env["ANTHROPIC_SMALL_FAST_MODEL"] = "MiniMax-M2.5"

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,  # 10 min timeout for minimax
            cwd=str(WIKI_DIR),
            shell=False,
            env=run_env,
            input=prompt if AGENT_NAME == "claudem" else None
        )

        if result.returncode == 0:
            raw = result.stdout
            try:
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
        print(f"Error: {AGENT_CMD} not found")
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
    # Parse args for --agent
    agent_override = None
    source_file = None

    for arg in sys.argv[1:]:
        if arg.startswith("--agent="):
            agent_override = arg.split("=")[1]
        elif not arg.startswith("--"):
            source_file = arg

    if agent_override:
        AGENT_NAME = agent_override
        AGENT_CMD = {
            "claude": "claude",
            "claudem": "claudem",
            "codex": "codex",
            "cursor": "cursor-agent",
        }.get(AGENT_NAME, "claude")

    if not source_file:
        print("Usage: python ingest.py <path-to-source> [--agent=NAME]")
        print(f"  Default agent: {DEFAULT_AGENT} (set WIKI_AGENT env var to change)")
        print("  Options: claude, claudem, codex, cursor")
        sys.exit(1)

    ingest(source_file)
