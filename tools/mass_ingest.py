#!/usr/bin/env python3
"""
High-speed direct ingestion of fetched files into wiki source pages.
NO AI agents - pure Python processing.

Usage:
    python tools/mass_ingest.py --ingest     # Ingest all fetched files
    python tools/mass_ingest.py --status      # Show ingestion status
    python tools/mass_ingest.py --reindex     # Rebuild index from source pages
"""
import os, sys, json, re, hashlib
from pathlib import Path
from datetime import date
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import argparse

WIKI_DIR = Path("/Users/jleechan/llm_wiki")
FETCH_DIR = Path("/tmp/wiki_fetch")
SOURCES_DIR = WIKI_DIR / "sources"
INDEX_FILE = WIKI_DIR / "index.md"
LOG_FILE = WIKI_DIR / "log.md"
MAX_WORKERS = 32
MANIFEST_FILE = FETCH_DIR / "manifest_target.json"  # Quality-filtered + target dirs

# Keywords for auto-tagging and connections
KEYWORD_MAP = {
    "claude": ("ClaudeCode", "entities/ClaudeCode.md"),
    "codex": ("CodexCLI", "entities/CodexCLI.md"),
    "mcp": ("MCP", "concepts/MCP.md"),
    "agent": ("AntigravityLoop", "concepts/AntigravityLoop.md"),
    "worldarchitect": ("WorldArchitect.AI", "sources/worldarchitect-ai.md"),
    "telemetry": ("Telemetry", "concepts/Telemetry.md"),
    "cost": ("CostAnalysis", "concepts/CostAnalysis.md"),
    "token": ("TokenUsageTracking", "concepts/TokenUsageTracking.md"),
    "d&d": ("DungeonsAndDragons", "concepts/DungeonsAndDragons.md"),
    "dnd": ("DungeonsAndDragons", "concepts/DungeonsAndDragons.md"),
    "dice": ("DiceIntegrityProtocol", "concepts/DiceIntegrityProtocol.md"),
    "beads": ("Beads", "sources/bd-beads.md"),
    "living blog": ("LivingBlog", "concepts/LivingBlog.md"),
    "novel engine": ("NovelEngine", "concepts/NovelEngine.md"),
    "github": ("GitHub", "entities/GitHub.md"),
    "openai": ("OpenAI", "entities/OpenAI.md"),
    "anthropic": ("Anthropic", "entities/Anthropic.md"),
    "gcp": ("GoogleCloudPlatform", "concepts/GoogleCloudPlatform.md"),
    "firebase": ("Firebase", "entities/Firebase.md"),
    "flask": ("Flask", "concepts/Flask.md"),
    "python": ("Python", "concepts/Python.md"),
    "typescript": ("TypeScript", "concepts/TypeScript.md"),
    "rust": ("Rust", "concepts/Rust.md"),
    "golang": ("Go", "concepts/Go.md"),
    "health": ("HealthPersonal", "entities/HealthPersonal.md"),
    "consulting": ("LeeChanConsulting", "entities/LeeChanConsulting.md"),
    "1099": ("1099NECFiling", "concepts/1099NECFiling.md"),
    "tax": ("TaxCompliance", "concepts/TaxCompliance.md"),
}

def slugify(text: str) -> str:
    text = re.sub(r'\.md$', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s-]', ' ', text)
    text = re.sub(r'[\s_]+', '-', text.strip())
    text = re.sub(r'-+', '-', text).strip('-').lower()
    return text or "untitled"

def extract_title(content: str) -> str:
    m = re.search(r'^#+\s+(.+)$', content, re.MULTILINE)
    if m: return m.group(1).strip()[:120]
    m = re.search(r'^<title>(.+)</title>', content, re.MULTILINE | re.IGNORECASE)
    if m: return m.group(1).strip()[:120]
    return ""

def extract_summary(content: str) -> str:
    lines = content.split('\n')
    summary = []
    in_code = 0
    for line in lines[:60]:
        if line.strip().startswith('```'): in_code = 1 - in_code
        if in_code: continue
        stripped = line.strip()
        if stripped and not stripped.startswith('#'):
            summary.append(stripped)
            if len(' '.join(summary)) > 250: break
    return ' '.join(summary)[:300].strip()

def extract_claims(content: str) -> list[str]:
    claims = []
    for line in content.split('\n'):
        line = line.strip()
        if re.match(r'^[-*]\s+\S', line) or re.match(r'^\d+\.\s+\S', line):
            claim = re.sub(r'^[-*\d.]+\s+', '', line).strip()
            if claim and 10 < len(claim) < 200:
                claims.append(f"- {claim}")
            if len(claims) >= 10: break
    return claims

def extract_quotes(content: str) -> list[str]:
    quotes = []
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('>'):
            q = line.lstrip('>').strip()
            if q and 10 < len(q) < 400:
                quotes.append(f'> "{q[:300]}"')
            if len(quotes) >= 5: break
    return quotes

def auto_tag(content: str) -> list[str]:
    tags = []
    content_lower = content.lower()
    if 'claude' in content_lower: tags.append("claude")
    if 'codex' in content_lower: tags.append("codex")
    if 'mcp' in content_lower: tags.append("mcp")
    if 'agent' in content_lower: tags.append("agent")
    if 'worldarchitect' in content_lower: tags.append("dnd")
    if 'd&d' in content_lower or 'dnd' in content_lower: tags.append("dnd")
    if 'telemetry' in content_lower: tags.append("telemetry")
    if 'cost' in content_lower or 'token' in content_lower: tags.append("cost")
    if 'health' in content_lower or 'sleep' in content_lower: tags.append("health")
    if 'consulting' in content_lower or 'tax' in content_lower or '1099' in content_lower: tags.append("business")
    if 'github' in content_lower: tags.append("github")
    return list(set(tags))

def auto_connect(content: str) -> list[str]:
    connections = []
    content_lower = content.lower()
    for kw, (name, _) in KEYWORD_MAP.items():
        if kw in content_lower:
            connections.append(f"- [[{name}]]")
    return list(set(connections))[:10]

def generate_source_page(entry: dict) -> tuple[str, str, str]:
    """Generate source page content. Returns (slug, index_entry, title)."""
    repo = entry["repo"]
    path = entry["path"]
    content = entry["content"]
    url = entry.get("url", "")
    source = entry.get("source", "unknown")

    # Generate slug
    raw_slug = f"{repo}-{path}"
    slug = hashlib.sha256(raw_slug.encode()).hexdigest()[:10] + "-" + slugify(f"{repo}-{path}")[:85]

    # Extract title
    title = extract_title(content)
    if not title:
        title = path.split('/')[-1].replace('.md','').replace('-',' ').replace('_',' ').title()
    if not title:
        title = repo.split('/')[-1].replace('-',' ').title()

    # Build page
    summary = extract_summary(content)
    claims = extract_claims(content)
    quotes = extract_quotes(content)
    tags = auto_tag(content)
    connections = auto_connect(content)

    today = date.today().isoformat()
    tags_str = ", ".join(f'"{t}"' for t in tags) if tags else "[]"

    claims_str = "\n".join(claims) if claims else "- See source document for details"
    quotes_str = "\n".join(f'  {q}' for q in quotes) if quotes else ""
    connections_str = "\n".join(connections) if connections else "- [[Wiki Index]] — main index"

    page = f"""---
title: "{title}"
type: source
tags: [{tags_str}]
date: {today}
source_file: {url}
repository: {repo}
---

## Summary
{summary}

## Key Claims
{claims_str}

## Key Quotes
{quotes_str}

## Connections
{connections_str}
"""

    index_entry = f"- [{title}](sources/{slug}.md) — {summary[:100]}"
    return slug, index_entry, title, page

def ingest_file(entry: dict) -> tuple[str, str, str, str] | None:
    """Ingest a single file. Returns (slug, index_entry, title, page) or None."""
    try:
        return generate_source_page(entry)
    except Exception as e:
        return None

def ingest_batch(entries: list[dict], max_workers: int = 32) -> tuple[int, int, list[str], list[str]]:
    """Ingest batch of entries. Returns (success, failed, slugs, index_entries)."""
    success = 0
    failed = 0
    slugs = []
    index_entries = []
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)

    def process(e):
        try:
            slug, idx, title, page = generate_source_page(e)
            # Write source page
            sf = SOURCES_DIR / f"{slug}.md"
            # Don't overwrite existing - append
            if sf.exists():
                sf.write_text(page + "\n\n---\n\n## Existing\n\n" + sf.read_text()[:3000])
            else:
                sf.write_text(page)
            return ("ok", slug, idx, title, page)
        except Exception as ex:
            return ("err", str(ex))

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(process, e): e for e in entries}
        for i, f in enumerate(as_completed(futures)):
            result = f.result()
            if result[0] == "ok":
                _, slug, idx, title, _ = result
                success += 1
                slugs.append(slug)
                index_entries.append(idx)
            else:
                failed += 1
            if (i+1) % 500 == 0:
                print(f"  Progress: {i+1}/{len(entries)}")

    return success, failed, slugs, index_entries

def rebuild_index():
    """Rebuild index from all source pages."""
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    entries = []
    for sf in SOURCES_DIR.glob("*.md"):
        try:
            content = sf.read_text()
            tm = re.search(r'^title:\s*["\'](.+)["\']', content, re.MULTILINE)
            title = tm.group(1) if tm else sf.stem
            sm = re.search(r'^## Summary\n+(.+?)(?=\n## |\n---|\Z)', content, re.DOTALL)
            summary = sm.group(1).strip()[:100] if sm else "See source"
            entries.append(f"- [{title}](sources/{sf.name}) — {summary}")
        except: pass

    # Read existing index
    if INDEX_FILE.exists():
        idx_content = INDEX_FILE.read_text()
    else:
        idx_content = "# Wiki Index\n\n## Overview\n- [Overview](overview.md)\n\n## Sources\n\n## Entities\n\n## Concepts\n\n## Syntheses\n"

    # Replace ## Sources section with fresh entries, preserve other sections
    if "## Sources" in idx_content:
        lines = idx_content.split('\n')
        new_lines = []
        skip_sources = False
        for line in lines:
            if line.strip() == "## Sources":
                skip_sources = False
                new_lines.append(line)
            elif skip_sources and line.startswith('## '):
                skip_sources = False
                new_lines.append(line)
            elif not skip_sources:
                new_lines.append(line)
        new_lines.append("")  # trailing newline
        idx_content = "\n".join(new_lines)
    else:
        idx_content = "# Wiki Index\n\n## Overview\n- [Overview](overview.md)\n\n## Sources\n\n## Entities\n\n## Concepts\n\n## Syntheses\n"

    idx_content += "\n".join(sorted(entries, key=lambda x: x.lower())) + "\n"

    INDEX_FILE.write_text(idx_content)
    return len(entries)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ingest", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--reindex", action="store_true")
    parser.add_argument("--workers", type=int, default=32)
    args = parser.parse_args()

    manifest_path = FETCH_DIR / "manifest.json"

    if args.status:
        for mf in [MANIFEST_FILE, manifest_path]:
            if mf.exists():
                with open(mf) as f:
                    m = json.load(f)
                print(f"{mf.name}: {len(m)} entries")
        src_count = len(list(SOURCES_DIR.glob("*.md")))
        print(f"Source pages: {src_count}")
        return

    if args.reindex:
        print("Rebuilding index from source pages...")
        count = rebuild_index()
        print(f"Index rebuilt with {count} source entries")
        return

    if args.ingest:
        # Try manifest_target first, fall back to manifest
        if MANIFEST_FILE.exists():
            manifest_path = MANIFEST_FILE
            print(f"Using filtered manifest: {MANIFEST_FILE.name}")
        elif not manifest_path.exists():
            print("No fetched files. Run: python tools/mass_fetch.py --all first")
            return
        else:
            print(f"Using full manifest: {manifest_path.name}")

        with open(manifest_path) as f:
            manifest = json.load(f)

        # Load entries by looking up individual JSON files
        entries = []
        missing = 0
        for item in manifest:
            slug = item["slug"]
            fp = FETCH_DIR / f"{slug}.json"
            if fp.exists():
                try:
                    with open(fp) as f:
                        entries.append(json.load(f))
                except:
                    missing += 1
            else:
                missing += 1

        print(f"Loaded {len(entries)} entries ({missing} files not found)")

        if not entries:
            print("No entries to ingest.")
            return

        print(f"Ingesting {len(entries)} files...")
        success, failed, slugs, index_entries = ingest_batch(entries, max_workers=args.workers)
        print(f"\nIngestion complete: {success} success, {failed} failed")

        # Update index
        print("Updating index...")
        count = rebuild_index()
        print(f"Index: {count} source entries")

        # Update log
        today = date.today().isoformat()
        log_entry = f"## [{today}] mass_ingest | +{success} files via mass_fetch\n\nBatch ingestion from GitHub repos and local directories\n"
        if LOG_FILE.exists():
            log_entry = LOG_FILE.read_text() + "\n" + log_entry
        LOG_FILE.write_text(log_entry)

        print(f"\n=== DONE: {success} source pages created ===")
        return

    print("Usage:")
    print("  python tools/mass_fetch.py --all    # Fetch files")
    print("  python tools/mass_ingest.py --ingest # Ingest fetched files")
    print("  python tools/mass_ingest.py --status  # Show status")

if __name__ == "__main__":
    main()
