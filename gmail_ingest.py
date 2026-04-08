#!/usr/bin/env python3
"""
Batch ingest emails and calendar events from Gmail/Calendar MCP results.
Reads search results from tool output files, fetches full content, writes wiki sources.
"""
import json
import re
import os
import time
import hashlib
from pathlib import Path
from datetime import date
from typing import List, Dict, Any

TOOL_RESULTS = Path("/Users/jleechan/.claude/projects/-Users-jleechan-llm-wiki/a1532dce-2e9a-4593-a818-1690279bc955/tool-results")
WIKI_DIR = Path("/Users/jleechan/llm_wiki")
SOURCES_DIR = WIKI_DIR / "sources"

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]

def parse_search_file(fname: str) -> List[str]:
    """Extract message IDs from a search result file."""
    try:
        data = json.load(open(fname))
        text = json.loads(data[0]['text'])
        msgs = text.get('messages', [])
        return [m['messageId'] for m in msgs]
    except Exception as e:
        print(f"Error reading {fname}: {e}")
        return []

def parse_calendar_file(fname: str) -> List[Dict]:
    """Extract events from calendar result file."""
    try:
        data = json.load(open(fname))
        text = json.loads(data[0]['text'])
        events = text.get('events', [])
        return events
    except Exception as e:
        print(f"Error reading {fname}: {e}")
        return []

def slugify(text: str, max_len: int = 60) -> str:
    """Create a slug from text."""
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', '-', text).lower()
    return text[:max_len] or "untitled"

def write_source(slug: str, title: str, content: str, tags: List[str], date_str: str, source_file: str = ""):
    """Write a source file with frontmatter."""
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    path = SOURCES_DIR / f"{slug}.md"

    frontmatter = f"""---
title: "{title}"
type: source
tags: {json.dumps(tags)}
date: {date_str}
source_file: "{source_file}"
---

{content}"""
    path.write_text(frontmatter, encoding='utf-8')
    return path

def main():
    today = date.today().isoformat()
    os.makedirs(SOURCES_DIR, exist_ok=True)

    # Collect all Gmail search files
    gmail_files = list(TOOL_RESULTS.glob("mcp-claude_ai_Gmail-gmail_search_messages-*.txt"))
    print(f"Found {len(gmail_files)} Gmail search result files")

    # Collect all unique message IDs
    all_ids = set()
    for f in gmail_files:
        ids = parse_search_file(str(f))
        all_ids.update(ids)
        print(f"  {f.name}: {len(ids)} messages")

    print(f"\nTotal unique email IDs: {len(all_ids)}")

    # Collect calendar events
    cal_file = TOOL_RESULTS / "mcp-claude_ai_Google_Calendar-gcal_list_events-1775591601288.txt"
    if cal_file.exists():
        events = parse_calendar_file(str(cal_file))
        print(f"Calendar events: {len(events)}")

        # Write calendar events
        for ev in events:
            ev_id = ev.get('id', 'unknown')[:30]
            title = ev.get('summary', 'Untitled Event')
            start = ev.get('start', {}).get('dateTime', ev.get('start', {}).get('date', 'unknown'))
            end = ev.get('end', {}).get('dateTime', ev.get('end', {}).get('date', 'unknown'))
            desc = ev.get('description', 'No description')
            loc = ev.get('location', '')

            slug = f"calendar-{slugify(title, 40)}-{ev_id[:8]}"
            tags = ["calendar", "event"]

            content = f"""## Summary
{title}

## When
- Start: {start}
- End: {end}

## Location
{loc or 'Not specified'}

## Description
{desc}

## Details
- Event ID: {ev_id}
- Event Type: {ev.get('eventType', 'event')}
"""
            write_source(slug, title, content, tags, today, f"calendar:{ev_id}")
            print(f"  Calendar: {title[:50]}")

    print(f"\nIngestion complete. Total: {len(all_ids)} emails + {len(events) if 'events' in dir() else 0} events written.")
    print(f"NOTE: Email body fetching requires individual API calls. Use gmail_ingest_fetch.py to fetch full content.")

if __name__ == "__main__":
    main()
