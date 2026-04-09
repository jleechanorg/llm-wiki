#!/usr/bin/env python3
"""
Parallel batch ingest for wiki sources.
Processes multiple source files in parallel using subprocess workers.
"""
import os
import sys
import json
import hashlib
import re
import subprocess
import time
import concurrent.futures
from pathlib import Path
from datetime import date
from typing import List, Dict, Any

WIKI_DIR = Path("/Users/jleechan/llm_wiki/wiki")
LOG_FILE = WIKI_DIR / "log.md"
INDEX_FILE = WIKI_DIR / "index.md"
OVERVIEW_FILE = WIKI_DIR / "overview.md"
SOURCES_DIR = WIKI_DIR / "sources"

DEFAULT_AGENT = os.environ.get("WIKI_AGENT", "claude")
AO_RUNTIME = os.environ.get("AO_RUNTIME", "antigravity")

# Extended agent commands for batch processing
AGENT_CMD = {
    "claude": "claude",
    "claudem": '"/Applications/cmux DEV.app/Contents/Resources/bin/cmux"',
    "codex": "codex",
    "cursor": "cursor-agent",
    "ao": "ao",
}.get(DEFAULT_AGENT, DEFAULT_AGENT)

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]

def slugify(title: str) -> str:
    """Convert title to kebab-case slug."""
    # Remove file extension
    title = re.sub(r'\.md$', '', title)
    # Replace non-alphanumeric with dashes
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', title)
    slug = re.sub(r'-+', '-', slug).strip('-').lower()
    return slug or "untitled"

def build_wiki_context() -> str:
    """Get current wiki state for context."""
    parts = []
    if INDEX_FILE.exists():
        parts.append(f"## index.md\n{INDEX_FILE.read_text()[:2000]}")
    if OVERVIEW_FILE.exists():
        parts.append(f"## overview.md\n{OVERVIEW_FILE.read_text()[:1000]}")
    sources_dir = WIKI_DIR / "sources"
    if sources_dir.exists():
        recent = sorted(sources_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:3]
        for p in recent:
            parts.append(f"## {p.name}\n{p.read_text()[:1000]}")
    return "\n\n---\n\n".join(parts)

def process_file(source_path: str, agent: str = None) -> Dict[str, Any]:
    """
    Process a single file using the ingest agent.
    Returns dict with results.
    """
    agent = agent or DEFAULT_AGENT
    source = Path(source_path).expanduser().resolve()

    if not source.exists():
        return {"status": "error", "path": source_path, "error": "file not found"}

    try:
        source_content = source.read_text(encoding="utf-8")
    except Exception as e:
        return {"status": "error", "path": source_path, "error": str(e)}

    source_hash = sha256(source_content)
    today = date.today().isoformat()
    wiki_context = build_wiki_context()

    # Determine subdirectory for slug uniqueness
    rel_path = source_path
    for prefix in ["/Users/jleechan/", "~/"]:
        if rel_path.startswith(prefix):
            rel_path = rel_path[len(prefix):]
    slug_base = slugify(source.stem)
    subdir_slug = rel_path.replace("/", "-").replace(" ", "-").lower()
    slug = f"{subdir_slug[:80]}-{source_hash[:8]}"

    prompt = f"""You are maintaining an LLM Wiki. Process this source document and integrate its knowledge.

WIKI_DIR: {WIKI_DIR}

## Wiki Schema (YAML frontmatter required):
```yaml
---
title: "Page Title"
type: source
tags: []
sources: []
last_updated: {today}
---
```

Use [[PageName]] wikilinks.

## Current wiki state:
{wiki_context if wiki_context else "(wiki is empty)"}

## Source to ingest:
=== SOURCE START ===
{source_content[:6000]}
=== SOURCE END ===

## MANDATORY EXTRACTION RULES (Karpathy Pattern):

1. **ALWAYS create entity pages** for:
   - Every person mentioned (create entities/FirstLast.md)
   - Every company/organization mentioned (entities/CompanyName.md)
   - Every project/product mentioned (entities/ProjectName.md)
   - Every PR/issue referenced (entities/PR123.md)

2. **ALWAYS create concept pages** for:
   - Every method, framework, or theory discussed
   - Every technical concept or pattern
   - Every workflow or process described

**CRITICAL**: You MUST create entity_pages and concept_pages arrays with at least one entry each if the source mentions any people, companies, projects, or concepts. Empty arrays are not acceptable.

Return ONLY valid JSON (no markdown fences):
{{
  "title": "Human-readable title",
  "slug": "{slug}",
  "source_page": "full markdown for sources/<slug>.md with YAML frontmatter + summary + key claims",
  "index_entry": "- [Title](sources/slug.md) — one-line summary",
  "overview_update": "updated overview.md content, or null",
  "entity_pages": [],
  "concept_pages": [],
  "contradictions": [],
  "log_entry": "## [{today}] ingest | <title>"
}}"""

    agent_cmd = {
        "claude": "claude",
        "claudem": '"/Applications/cmux DEV.app/Contents/Resources/bin/cmux"',
        "codex": "codex",
        "cursor": "cursor-agent",
    }.get(agent, "claude")

    use_shell = (agent == "claudem")

    try:
        cmd_list = [agent_cmd, "--dangerously-skip-permissions", "-p", prompt]
        # For claudem, use minimax API
        run_env = {**os.environ, "WIKI_AGENT": agent}
        if agent == "claudem":
            run_env["ANTHROPIC_BASE_URL"] = "https://api.minimax.io/anthropic"
            run_env["ANTHROPIC_AUTH_TOKEN"] = os.environ.get("MINIMAX_API_KEY", os.environ.get("ANTHROPIC_AUTH_TOKEN", ""))
            run_env["ANTHROPIC_MODEL"] = "MiniMax-M2.5"
            run_env["ANTHROPIC_SMALL_FAST_MODEL"] = "MiniMax-M2.5"
            cmd_list = [agent_cmd, "--dangerously-skip-permissions", "-p", "-"]
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            timeout=300,  # 5 min timeout
            cwd=str(WIKI_DIR),
            shell=use_shell,
            env=run_env,
            input=prompt if agent == "claudem" else None
        )

        if result.returncode == 0:
            raw = result.stdout
            match = re.search(r"\{[\s\S]*\}", raw)
            if match:
                data = json.loads(match.group())
            else:
                return {"status": "error", "path": source_path, "error": "no JSON in response", "raw": raw[:200]}
        else:
            return {"status": "error", "path": source_path, "error": result.stderr[:200]}

    except subprocess.TimeoutExpired:
        return {"status": "error", "path": source_path, "error": "timeout"}
    except FileNotFoundError:
        return {"status": "error", "path": source_path, "error": f"{agent_cmd} not found"}
    except Exception as e:
        return {"status": "error", "path": source_path, "error": str(e)}

    # Write files
    try:
        slug = data.get("slug", slug)
        src_path = SOURCES_DIR / f"{slug}.md"
        src_path.parent.mkdir(parents=True, exist_ok=True)
        src_path.write_text(data.get("source_page", ""), encoding="utf-8")

        # Update index
        index_content = INDEX_FILE.read_text() if INDEX_FILE.exists() else ""
        if not index_content:
            index_content = "# Wiki Index\n\n## Overview\n- [Overview](overview.md)\n\n## Sources\n\n## Entities\n\n## Concepts\n\n## Syntheses\n"
        idx_entry = data.get("index_entry", "")
        if idx_entry and "## Sources" in index_content:
            if idx_entry.strip() not in index_content:
                index_content = index_content.replace("## Sources\n", "## Sources\n" + idx_entry + "\n")
                INDEX_FILE.write_text(index_content, encoding="utf-8")

        # Append log
        log_entry = data.get("log_entry", f"## [{today}] ingest | {data.get('title', source.name)}")
        existing_log = LOG_FILE.read_text() if LOG_FILE.exists() else ""
        LOG_FILE.write_text(log_entry.strip() + "\n\n" + existing_log, encoding="utf-8")

        return {
            "status": "success",
            "path": source_path,
            "title": data.get("title", source.name),
            "slug": slug,
        }

    except Exception as e:
        return {"status": "write_error", "path": source_path, "error": str(e), "data": data}

def ingest_batch(files: List[str], workers: int = 4, agent: str = None) -> Dict[str, Any]:
    """
    Ingest a batch of files in parallel.
    """
    print(f"\nBatch ingest: {len(files)} files with {workers} workers")
    print(f"Agent: {agent or DEFAULT_AGENT}")

    results = []
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(process_file, f, agent): f for f in files}

        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            result = future.result()
            results.append(result)
            status = result.get("status", "unknown")
            if status == "success":
                print(f"  [{i}/{len(files)}] OK: {Path(result['path']).name}")
            else:
                print(f"  [{i}/{len(files)}] FAIL: {Path(result['path']).name} — {result.get('error', 'unknown')[:80]}")

    elapsed = time.time() - start_time
    successes = sum(1 for r in results if r.get("status") == "success")
    failures = len(results) - successes

    print(f"\nBatch complete: {successes} succeeded, {failures} failed in {elapsed:.1f}s")
    return {"total": len(files), "success": successes, "failed": failures, "elapsed": elapsed, "results": results}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Batch ingest wiki sources")
    parser.add_argument("--files", nargs="+", help="List of files to ingest")
    parser.add_argument("--file-list", help="File containing list of files (one per line)")
    parser.add_argument("--workers", type=int, default=4, help="Parallel workers (default: 4)")
    parser.add_argument("--agent", default=DEFAULT_AGENT, help=f"Agent to use (default: {DEFAULT_AGENT})")
    parser.add_argument("--batch-size", type=int, default=20, help="Batch size for output display")
    args = parser.parse_args()

    files = []
    if args.files:
        files = args.files
    elif args.file_list:
        files = Path(args.file_list).read_text().strip().split("\n")
    else:
        print("Error: provide --files or --file-list")
        sys.exit(1)

    print(f"Ingesting {len(files)} files...")
    result = ingest_batch(files, workers=args.workers, agent=args.agent)
    print(f"\nFinal: {result['success']}/{result['total']} files ingested")
    sys.exit(0 if result['failed'] == 0 else 1)
