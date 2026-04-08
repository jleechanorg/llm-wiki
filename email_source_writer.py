#!/usr/bin/env python3
"""
Write Gmail emails and calendar events as wiki sources from MCP tool results.
"""
import json
import re
import os
import hashlib
from pathlib import Path
from datetime import date
from typing import Dict, Any, List

TOOL_RESULTS = Path("/Users/jleechan/.claude/projects/-Users-jleechan-llm-wiki/a1532dce-2e9a-4593-a818-1690279bc955/tool-results")
WIKI_DIR = Path("/Users/jleechan/llm_wiki")
SOURCES_DIR = WIKI_DIR / "sources"

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:8]

def slugify(text: str, max_len: int = 50) -> str:
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', '-', text).lower()
    return text[:max_len] or "untitled"

def write_source(slug: str, title: str, content: str, tags: List[str], date_str: str, source_file: str = ""):
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    path = SOURCES_DIR / f"{slug}.md"
    if path.exists():
        return path
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

def email_to_source(msg: Dict) -> Dict:
    """Convert email message dict to source content."""
    headers = msg.get('headers', {})
    subject = headers.get('Subject', 'No Subject')
    sender = headers.get('From', 'Unknown')
    recipient = headers.get('To', '')
    email_date = headers.get('Date', '')
    body = msg.get('body', msg.get('snippet', ''))
    msg_id = msg.get('messageId', '')
    thread_id = msg.get('threadId', '')

    # Extract tags from content
    tags = ['gmail', 'email']
    body_lower = body.lower()
    if 'deployment' in body_lower or 'deploy' in body_lower:
        tags.append('deployment')
    if 'success' in body_lower:
        tags.append('success')
    elif 'failure' in body_lower or 'failed' in body_lower:
        tags.append('failure')
    if 'worldarchitect' in body_lower:
        tags.append('worldarchitect')
    if 'pr ' in body_lower or 'pull request' in body_lower:
        tags.append('pull-request')

    # Extract PR number
    pr_match = re.search(r'pull/(\d+)', body)
    pr_num = pr_match.group(1) if pr_match else ''

    # Extract commit
    commit_match = re.search(r'commit[:\s]+([a-f0-9]{8,40})', body, re.I)
    commit = commit_match.group(1) if commit_match else ''

    # Extract deployment URL
    url_match = re.search(r'(https://[^\s]+run\.app[^\s]*)', body)
    deploy_url = url_match.group(1) if url_match else ''

    content = f"""## Email Metadata
- **From:** {sender}
- **To:** {recipient}
- **Date:** {email_date}
- **Subject:** {subject}
- **Message ID:** {msg_id}
- **Thread ID:** {thread_id}

## Email Body
{body}

## Extracted Data
- PR: #{pr_num}
- Commit: {commit}
- Deployment URL: {deploy_url}
"""
    slug = f"email-{slugify(subject, 40)}-{sha256(msg_id)}"
    return {'slug': slug, 'title': subject, 'content': content, 'tags': tags, 'date': email_date[:10] or date.today().isoformat(), 'source_file': f"gmail:{msg_id}"}

def calendar_to_source(ev: Dict) -> Dict:
    """Convert calendar event dict to source content."""
    ev_id = ev.get('id', 'unknown')[:30]
    title = ev.get('summary', 'Untitled Event')
    start = ev.get('start', {}).get('dateTime', ev.get('start', {}).get('date', 'unknown'))
    end = ev.get('end', {}).get('dateTime', ev.get('end', {}).get('date', 'unknown'))
    desc = ev.get('description', 'No description')
    loc = ev.get('location', '')
    ev_type = ev.get('eventType', 'event')

    tags = ['calendar', 'event']
    if 'workout' in title.lower() or 'gym' in title.lower():
        tags.append('health')
    if 'doctor' in title.lower() or 'medical' in title.lower() or 'blood' in title.lower():
        tags.append('health')
    if 'therapy' in title.lower():
        tags.append('health')
    if 'dinner' in title.lower() or 'lunch' in title.lower() or 'reservation' in title.lower():
        tags.append('social')
    if 'lecture' in title.lower() or 'class' in title.lower():
        tags.append('education')

    content = f"""## Summary
{title}

## When
- **Start:** {start}
- **End:** {end}
- **Type:** {ev_type}

## Location
{loc or 'Not specified'}

## Description
{desc}

## Details
- Event ID: {ev_id}
"""
    slug = f"calendar-{slugify(title, 40)}-{sha256(ev_id)}"
    return {'slug': slug, 'title': title, 'content': content, 'tags': tags, 'date': start[:10] if start and start != 'unknown' else date.today().isoformat(), 'source_file': f"calendar:{ev_id}"}

def process_all():
    today = date.today().isoformat()
    os.makedirs(SOURCES_DIR, exist_ok=True)

    # Process calendar events
    cal_file = TOOL_RESULTS / "mcp-claude_ai_Google_Calendar-gcal_list_events-1775591601288.txt"
    if cal_file.exists():
        try:
            data = json.load(open(cal_file))
            text = json.loads(data[0]['text'])
            events = text.get('events', [])
            for ev in events:
                try:
                    src = calendar_to_source(ev)
                    write_source(src['slug'], src['title'], src['content'], src['tags'], src['date'], src['source_file'])
                except Exception as e:
                    print(f"Calendar error: {e}")
            print(f"Processed {len(events)} calendar events")
        except Exception as e:
            print(f"Calendar file error: {e}")

    print(f"\nTotal sources: {len(list(SOURCES_DIR.glob('*.md')))}")
    print("Email content should be written from MCP read_message results.")
    print("Use write_email_sources.py to process individual email reads.")

if __name__ == "__main__":
    process_all()
