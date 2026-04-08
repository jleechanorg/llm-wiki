#!/usr/bin/env python3
"""Batch write Gmail emails as wiki sources using MCP tool results."""
import json
import re
import os
import hashlib
import subprocess
import concurrent.futures
import html
from pathlib import Path
from datetime import date

TOOL_RESULTS = Path("/Users/jleechan/.claude/projects/-Users-jleechan-llm-wiki/a1532dce-2e9a-4593-a818-1690279bc955/tool-results")
SOURCES_DIR = Path("/Users/jleechan/llm_wiki/sources")
INDEX_FILE = Path("/Users/jleechan/llm_wiki/index.md")
LOG_FILE = Path("/Users/jleechan/llm_wiki/log.md")

def sha256(t):
    return hashlib.sha256(t.encode()).hexdigest()[:8]

def slugify(text, max_len=40):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', '-', text).lower()
    return text[:max_len] or "untitled"

def strip_html(text):
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.I)
    text = re.sub(r'<p[^>]*>', '\n', text, flags=re.I)
    text = re.sub(r'</p>', '\n', text, flags=re.I)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&#\d+;', '', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    text = text.strip()
    return text

def parse_email_date(date_str):
    """Parse email date like 'Tue, 07 Apr 2026 16:02:25 +0000' to YYYY-MM-DD."""
    m = re.search(r'(\d{1,2})\s+(\w+)\s+(\d{4})', date_str)
    if not m:
        return date.today().isoformat()
    months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
              'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    day, mon, year = m.group(1), m.group(2), m.group(3)
    mon = months.get(mon, '01')
    return f"{year}-{mon}-{day.zfill(2)}"

def extract_tags(body, subject, sender):
    tags = ['gmail', 'email']
    combined = (body + ' ' + subject + ' ' + sender).lower()
    if 'worldarchitect' in combined:
        tags.append('worldarchitect')
    if 'deployment' in combined or 'deploy' in combined:
        tags.append('deployment')
    if 'ai universe' in combined:
        tags.append('ai-universe')
    if 'success' in combined:
        tags.append('success')
    if 'failure' in combined or 'failed' in combined:
        tags.append('failure')
    if 'incident' in combined or 'statuspage' in combined:
        tags.append('incident')
    if 'godaddy' in combined:
        tags.append('godaddy')
    if 'ai universe' in combined:
        tags.append('analytics')
    if 'pull/61' in combined or 'pull/61' in combined:
        tags.append('pull-request')
    if 'xai' in combined or 'invoice' in combined:
        tags.append('finance')
    if 'perplexity' in combined:
        tags.append('ai-tool')
    if 'medialyst' in combined:
        tags.append('saas')
    return tags

def write_source(slug, title, content, tags, date_str, source_file):
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    path = SOURCES_DIR / f"{slug}.md"
    if path.exists():
        return path, False
    fm = f"""---
title: "{title}"
type: source
tags: {json.dumps(tags)}
date: {date_str}
source_file: "{source_file}"
---

{content}"""
    path.write_text(fm, encoding='utf-8')
    return path, True

def process_email(msg_id):
    """Process a single email by ID."""
    try:
        result = subprocess.run(
            ['python3', '-c', f'''
import json, sys
sys.path.insert(0, '/Users/jleechan/.claude/projects/-Users-jleechan-llm-wiki/a1532dce-2e9a-4593-a818-1690279bc955/tool-results')
import mcp_ai_gmail as gmail
# read message
import importlib
mod = importlib.import_module('mcp_ai_gmail')
'''],
            capture_output=True, text=True, timeout=5
        )
    except:
        pass

    # Use gmail MCP tool directly
    try:
        result = subprocess.run(
            ['python3', '-c', f'''
import json, subprocess
r = subprocess.run(
    ['claude', 'mcp', 'call', 'mcp__claude_ai_Gmail__gmail_read_message', '--json-args', json.dumps({{"messageId": "{msg_id}"}}))],
    capture_output=True, text=True, timeout=60
)
print(r.stdout[:5000] if r.stdout else r.stderr[:500])
'''],
            capture_output=True, text=True, timeout=65
        )
        if result.stdout:
            try:
                data = json.loads(result.stdout)
            except:
                data = None
        else:
            data = None
    except:
        data = None

    return {"id": msg_id, "data": data}

def write_email_as_source(msg_id):
    """Read email via MCP and write as wiki source."""
    slug = f"email-{msg_id[:8]}"

    # Check if already written
    if (SOURCES_DIR / f"{slug}.md").exists():
        return {"status": "skip", "id": msg_id}

    # Extract data from search results file (we have snippet info)
    # Actually, let's read from the tool result files directly
    tool_files = list(TOOL_RESULTS.glob("mcp-claude_ai_Gmail-gmail_search_messages-*.txt"))
    snippet = msg_id  # fallback

    for tf in tool_files:
        try:
            data = json.load(open(tf))
            text = json.loads(data[0]['text'])
            msgs = text.get('messages', [])
            for m in msgs:
                if m['messageId'] == msg_id:
                    snippet = m.get('snippet', '')
                    break
        except:
            pass

    title = f"Email {msg_id}"
    body = snippet
    email_date = date.today().isoformat()
    sender = "unknown"
    subject = snippet[:50]

    tags = extract_tags(body, subject, sender)

    content = f"""## Email Metadata
- **From:** {sender}
- **Date:** {email_date}
- **Subject:** {subject}
- **Message ID:** {msg_id}

## Email Body
{body}

## Notes
*Full email body not yet fetched from Gmail API.*
"""

    path, created = write_source(slug, title, content, tags, email_date, f"gmail:{msg_id}")

    if created:
        return {"status": "created", "id": msg_id, "title": title, "path": str(path)}
    else:
        return {"status": "exists", "id": msg_id}

def main():
    # Load all email IDs from tool result files
    tool_files = list(TOOL_RESULTS.glob("mcp-claude_ai_Gmail-gmail_search_messages-*.txt"))
    all_ids = set()
    all_data = {}  # msg_id -> {subject, snippet, from, date}

    for tf in sorted(tool_files, key=lambda p: -p.stat().st_mtime):
        try:
            data = json.load(open(tf))
            text = json.loads(data[0]['text'])
            msgs = text.get('messages', [])
            for m in msgs:
                mid = m['messageId']
                all_ids.add(mid)
                if mid not in all_data:
                    all_data[mid] = {
                        'subject': m.get('subject', ''),
                        'snippet': m.get('snippet', ''),
                        'from': m.get('from', ''),
                        'date': m.get('date', ''),
                    }
        except Exception as e:
            print(f"  Error reading {tf.name}: {e}")

    print(f"Total unique emails: {len(all_ids)}")

    # Filter to recent ones (from most recent file - latest search)
    recent_ids = list(all_ids)
    print(f"Processing {len(recent_ids)} emails...")

    results = []
    created = 0
    skipped = 0

    for i, msg_id in enumerate(recent_ids, 1):
        data = all_data.get(msg_id, {})
        subject = data.get('subject', data.get('snippet', f'Email {msg_id[:8]}'))[:80]
        snippet = data.get('snippet', '')
        sender = data.get('from', '')
        email_date_str = data.get('date', '')

        email_date = parse_email_date(email_date_str) if email_date_str else date.today().isoformat()

        slug = f"email-{slugify(subject, 40)}-{sha256(msg_id)}"
        path = SOURCES_DIR / f"{slug}.md"

        if path.exists():
            skipped += 1
            continue

        tags = extract_tags(snippet + ' ' + subject, subject, sender)

        content = f"""## Email Metadata
- **From:** {sender}
- **Date:** {email_date}
- **Subject:** {subject}
- **Message ID:** {msg_id}

## Email Body
{snippet}

## Notes
*Full email body not yet fetched from Gmail API. Snippet extracted from search results.*
"""

        try:
            write_source(slug, subject, content, tags, email_date, f"gmail:{msg_id}")
            created += 1
            if i % 10 == 0:
                print(f"  [{i}/{len(recent_ids)}] Created: {created}, Skipped: {skipped}")
        except Exception as e:
            print(f"  Error writing {msg_id}: {e}")

    print(f"\nDone: {created} created, {skipped} already existed")

    # Update index
    sources = sorted(SOURCES_DIR.glob("email-*.md"), key=lambda p: -p.stat().st_mtime)[:50]
    index_lines = []
    for src in sources:
        content = src.read_text(encoding='utf-8', errors='ignore')
        fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        title = src.stem
        if fm_match:
            for line in fm_match.group(1).split('\n'):
                if line.startswith('title:'):
                    title = line.split(':', 1)[1].strip().strip('"').strip("'")
                    break
        slug = src.stem
        index_lines.append(f"- [{title[:60]}](sources/{slug}.md)")

    # Append to index
    if INDEX_FILE.exists():
        idx_content = INDEX_FILE.read_text()
    else:
        idx_content = "# Wiki Index\n\n## Overview\n- [Overview](overview.md)\n\n## Sources\n\n## Entities\n\n## Concepts\n\n## Syntheses\n"

    if "## Sources\n" in idx_content:
        # Count current entries
        parts = idx_content.split("## Sources\n")
        if len(parts) > 1:
            rest = parts[1].split("\n## ")[0]
            current_count = len([l for l in rest.strip().split('\n') if l.strip() and l.startswith('-')])
        else:
            current_count = 0

        # Add email entries to index
        new_entries = "\n".join(index_lines[:50])
        if new_entries:
            idx_content = idx_content.replace(
                "## Sources\n",
                "## Sources\n" + new_entries + "\n"
            )
        INDEX_FILE.write_text(idx_content, encoding='utf-8')

    # Append to log
    today = date.today().isoformat()
    log_entry = f"## [{today}] gmail_ingest | {created} emails ingested from recent Gmail search\n"
    if LOG_FILE.exists():
        existing = LOG_FILE.read_text()
        LOG_FILE.write_text(log_entry + existing)
    else:
        LOG_FILE.write_text(log_entry, encoding='utf-8')

    print(f"Index updated. {len(index_lines)} email sources in index.")

if __name__ == "__main__":
    main()
