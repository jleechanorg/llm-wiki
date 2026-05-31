#!/usr/bin/env python3
"""
Batch Campaign Download + Wiki Ingest Pipeline (Inline version)

Downloads all campaigns for jleechan@gmail.com from Firestore and ingests
them as wiki source pages. Does NOT use subprocess for downloads — calls
firestore_service and document_generator directly to avoid gRPC FD inheritance
issues.

Usage:
    python tools/batch_campaign_ingest_inline.py --dry-run
    python tools/batch_campaign_ingest_inline.py --min-entries 50 --campaigns-dir /tmp/campaign_downloads

Environment:
    GOOGLE_APPLICATION_CREDENTIALS=~/serviceAccountKey.json
    WORLDAI_DEV_MODE=true
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ── Config ───────────────────────────────────────────────────────────────────
WORLDARCHITECT_REPO = Path("/Users/jleechan/projects/worldarchitect.ai")
WIKI_DIR = Path("/Users/jleechan/llm_wiki/wiki")
WIKI_SOURCES = WIKI_DIR / "sources"
WIKI_INDEX = WIKI_DIR / "index.md"
CREDENTIALS = Path(os.path.expanduser("~/serviceAccountKey.json"))
EMAIL = "jleechan@gmail.com"
MANIFEST_FILE = Path("/tmp/campaign_ingest_manifest.jsonl")

# Add worldarchitect.ai to path for imports
sys.path.insert(0, str(WORLDARCHITECT_REPO))
sys.path.insert(0, str(WORLDARCHITECT_REPO / "mvp_site"))

from clock_skew_credentials import apply_clock_skew_patch
apply_clock_skew_patch()

import firebase_admin
from firebase_admin import auth, credentials, firestore

import firestore_service
import document_generator


def slugify(text: str) -> str:
    """Convert title to kebab-case slug."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text[:80]


def init_firebase():
    """Init Firebase."""
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(CREDENTIALS)
    os.environ["WORLDAI_DEV_MODE"] = "true"
    if not firebase_admin._apps:
        cred = credentials.Certificate(str(CREDENTIALS))
        firebase_admin.initialize_app(cred)
    return firestore.client()


def query_campaigns(uid: str, min_entries: int = 0) -> list[dict]:
    """Query all campaigns for a user, optionally filtered by entry count."""
    db = init_firebase()
    campaigns_ref = db.collection("users").document(uid).collection("campaigns")

    results = []
    print(f"Querying campaigns for {uid}...", flush=True)
    for camp in campaigns_ref.stream():
        entry_count = sum(1 for _ in camp.reference.collection("story").stream())
        if entry_count < min_entries:
            continue
        data = camp.to_dict()
        name = data.get("name", data.get("title", "Untitled"))
        results.append({
            "campaign_id": camp.id,
            "title": name,
            "entry_count": entry_count,
        })

    results.sort(key=lambda x: x["entry_count"], reverse=True)
    return results


def download_and_ingest(campaign: dict, campaigns_dir: Path) -> dict | None:
    """Download a campaign directly (no subprocess) and write to wiki."""
    campaign_id = campaign["campaign_id"]
    title = campaign["title"]
    entry_count = campaign["entry_count"]

    # Get Firebase UID
    user = auth.get_user_by_email(EMAIL)
    uid = user.uid

    # Step 1: Download campaign data directly
    print(f"  Downloading [{entry_count}] {title}...", flush=True)

    try:
        campaign_data, story_context = firestore_service.get_campaign_by_id(uid, campaign_id)
    except Exception as e:
        print(f"  [ERROR] get_campaign_by_id failed: {e}", flush=True)
        return None

    if not campaign_data or story_context is None:
        print(f"  [ERROR] No data for {title}", flush=True)
        return None

    if not isinstance(story_context, list):
        print(f"  [ERROR] Invalid story format for {title}", flush=True)
        return None

    # Step 2: Convert to text
    try:
        story_text = document_generator.get_story_text_from_context_enhanced(
            story_context, include_scenes=True
        )
    except (AttributeError, TypeError):
        story_text = document_generator.get_story_text_from_context(story_context)

    # Step 3: Save raw download
    safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in title)[:50]
    file_prefix = f"{safe_title}_{campaign_id[:8]}"

    camp_dir = campaigns_dir / campaign_id
    camp_dir.mkdir(parents=True, exist_ok=True)

    raw_path = camp_dir / f"{file_prefix}.txt"
    raw_path.write_text(story_text, errors="replace")

    # Also save game state
    try:
        game_state = firestore_service.get_campaign_game_state(uid, campaign_id)
        gs_data = game_state.to_dict() if game_state is not None else {}
        gs_path = camp_dir / f"{file_prefix}_game_state.json"
        gs_path.write_text(json.dumps(gs_data, indent=2, default=str), errors="replace")
    except Exception as e:
        print(f"  [WARN] Could not save game state: {e}", flush=True)

    # Step 4: Write wiki source page
    base_slug = slugify(title)
    wiki_path = WIKI_SOURCES / f"{base_slug}.md"
    WIKI_SOURCES.mkdir(parents=True, exist_ok=True)

    frontmatter = f"""---
title: "{title}"
type: source
tags: [campaign, {base_slug}]
date: {datetime.now(timezone.utc).strftime("%Y-%m-%d")}
source_file: {str(raw_path)}
campaign_id: {campaign_id}
entry_count: {entry_count}
last_updated: {datetime.now(timezone.utc).strftime("%Y-%m-%d")}
---

"""

    # Truncate to 100KB per page
    body = story_text[:100000] if len(story_text) > 100000 else story_text
    wiki_path.write_text(frontmatter + body, errors="replace")

    print(f"  ✅ Wrote wiki page: {wiki_path.name} ({len(story_text)} chars)", flush=True)

    return {
        "title": title,
        "campaign_id": campaign_id,
        "entry_count": entry_count,
        "wiki_path": str(wiki_path),
        "raw_path": str(raw_path),
    }


def main():
    parser = argparse.ArgumentParser(description="Batch campaign download + wiki ingest (inline)")
    parser.add_argument("--min-entries", type=int, default=50)
    parser.add_argument("--campaigns-dir", type=str, default="/tmp/campaign_downloads")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-existing", action="store_true", help="Skip campaigns that already have wiki pages")
    args = parser.parse_args()

    campaigns_dir = Path(args.campaigns_dir)

    print(f"=== Batch Campaign Ingest (Inline) ===")
    print(f"Min entries: {args.min_entries}")
    print(f"Dry run: {args.dry_run}")
    print(f"Skip existing: {args.skip_existing}")
    print()

    # Step 1: Init Firebase and get UID
    init_firebase()
    user = auth.get_user_by_email(EMAIL)
    uid = user.uid
    print(f"UID: {uid}")

    # Step 2: Query campaigns
    campaigns = query_campaigns(uid, min_entries=args.min_entries)
    print(f"\nFound {len(campaigns)} campaigns with >={args.min_entries} entries")

    if args.dry_run:
        for c in campaigns:
            print(f"  {c['entry_count']:5d} | {c['title']}")
        return

    # Step 3: Download + ingest each campaign
    results = []
    skipped = 0
    errors = 0

    for i, camp in enumerate(campaigns):
        print(f"\n[{i+1}/{len(campaigns)}]", flush=True)

        # Skip existing?
        if args.skip_existing:
            slug = slugify(camp["title"])
            wiki_path = WIKI_SOURCES / f"{slug}.md"
            if wiki_path.exists():
                # Check if it has real content (not just frontmatter)
                content = wiki_path.read_text(errors="replace")
                if len(content) > 500:
                    print(f"  ⏭️  Already exists: {wiki_path.name}")
                    skipped += 1
                    continue

        result = download_and_ingest(camp, campaigns_dir)
        if result:
            results.append(result)
        else:
            errors += 1

    # Step 4: Write manifest
    with open(MANIFEST_FILE, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    print(f"\n=== Done ===")
    print(f"Processed: {len(results)}")
    print(f"Skipped (existing): {skipped}")
    print(f"Errors: {errors}")
    print(f"Manifest: {MANIFEST_FILE}")


if __name__ == "__main__":
    main()
