#!/usr/bin/env python3
"""
Batch Campaign Download + Wiki Ingest Pipeline

Downloads all campaigns for jleechan@gmail.com from Firestore and ingests
them as wiki source pages. Designed to run in a dedicated worktree.

Usage:
    python tools/batch_campaign_ingest.py --dry-run
    python tools/batch_campaign_ingest.py --min-entries 100 --workers 4

Workflow:
    1. Query Firestore for all jleechan campaigns
    2. Filter by minimum entry count
    3. Download each campaign via worldarchitect.ai scripts
    4. Convert entries to wiki markdown format
    5. Write source pages to wiki/sources/
    6. Update wiki/index.md

Environment:
    GOOGLE_APPLICATION_CREDENTIALS=~/serviceAccountKey.json
    WORLDAI_DEV_MODE=true
"""

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
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

# ── Firebase Query ────────────────────────────────────────────────────────────


@dataclass
class CampaignInfo:
    campaign_id: str
    title: str
    entry_count: int
    last_played: str | None


def init_firebase():
    """Init Firebase using worldarchitect.ai repo's credentials pattern."""
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(CREDENTIALS)
    os.environ["WORLDAI_DEV_MODE"] = "true"

    sys.path.insert(0, str(WORLDARCHITECT_REPO))
    from mvp_site.clock_skew_credentials import apply_clock_skew_patch

    apply_clock_skew_patch()

    import firebase_admin
    from firebase_admin import auth, credentials, firestore

    if not firebase_admin._apps:
        cred = credentials.Certificate(str(CREDENTIALS))
        firebase_admin.initialize_app(cred)
    return firestore.client()


def get_uid(email: str) -> str:
    """Get Firebase UID by email."""
    from firebase_admin import auth

    init_firebase()
    user = auth.get_user_by_email(email)
    return user.uid


def query_campaigns(uid: str, min_entries: int = 0) -> list[CampaignInfo]:
    """Query all campaigns for a user, optionally filtered by entry count."""
    db = init_firebase()
    campaigns_ref = db.collection("users").document(uid).collection("campaigns")

    results = []
    print(f"Querying campaigns for {uid}...")
    for camp in campaigns_ref.stream():
        entry_count = sum(
            1 for _ in camp.reference.collection("story").stream()
        )
        if entry_count < min_entries:
            continue
        data = camp.to_dict()
        last_played = None
        if "lastSessionEnd" in data:
            try:
                ts = data["lastSessionEnd"]
                if isinstance(ts, datetime):
                    last_played = ts.isoformat()
                else:
                    last_played = str(ts)
            except Exception:
                pass

        results.append(
            CampaignInfo(
                campaign_id=camp.id,
                title=data.get("title", "Untitled"),
                entry_count=entry_count,
                last_played=last_played,
            )
        )

    results.sort(key=lambda x: x.entry_count, reverse=True)
    return results


# ── Download ─────────────────────────────────────────────────────────────────


def download_campaign(campaign_id: str, output_dir: Path) -> Path | None:
    """Download a single campaign using worldarchitect.ai's script."""
    output_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["WORLDAI_DEV_MODE"] = "true"
    env["GOOGLE_APPLICATION_CREDENTIALS"] = str(CREDENTIALS)

    cmd = [
        sys.executable,
        str(WORLDARCHITECT_REPO / "scripts" / "download_campaign.py"),
        "--email",
        EMAIL,
        "--campaign-id",
        campaign_id,
        "--output-dir",
        str(output_dir),
    ]

    result = subprocess.run(
        cmd, env=env, capture_output=True, text=True, timeout=300
    )

    if result.returncode != 0:
        print(f"  [ERROR] download failed: {result.stderr[:200]}")
        return None

    # Find the downloaded story file (not game state JSON)
    # Download script saves as {title}_{campaign_id[:8]}.txt
    files = list(output_dir.glob(f"*{campaign_id[:8]}*.txt"))
    if files:
        return files[0]
    # Fallback: try full campaign_id
    files = list(output_dir.glob(f"*{campaign_id}*.txt"))
    for f in files:
        if f.suffix == ".txt":
            return f
    return None


# ── Wiki Conversion ───────────────────────────────────────────────────────────


def slugify(text: str) -> str:
    """Convert title to kebab-case slug."""
    import re

    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text[:80]


def entries_to_wiki_pages(
    campaign_title: str, campaign_id: str, entry_count: int, download_path: Path
) -> list[tuple[Path, str]]:
    """Convert downloaded campaign entries to wiki source pages.

    Returns list of (file_path, slug) tuples.
    """
    # Determine the campaign slug from title
    base_slug = slugify(campaign_title)
    if base_slug not in campaign_id.lower():
        base_slug = f"{base_slug}-{campaign_id[:8]}"

    # Sources go in wiki/sources/
    WIKI_SOURCES.mkdir(parents=True, exist_ok=True)
    filename = WIKI_SOURCES / f"{base_slug}.md"

    pages = []

    # Read full campaign content
    content = download_path.read_text(errors="replace")

    # Build frontmatter
    frontmatter = f"""---
title: "{campaign_title}"
type: source
tags: [campaign, {base_slug}]
date: {datetime.now(timezone.utc).strftime("%Y-%m-%d")}
source_file: {str(download_path)}
campaign_id: {campaign_id}
entry_count: {entry_count}
last_updated: {datetime.now(timezone.utc).strftime("%Y-%m-%d")}
---

"""

    # Read full content and truncate if needed
    body = content[:100000] if len(content) > 100000 else content

    filename.write_text(frontmatter + body, errors="replace")
    pages.append((filename, base_slug))

    return pages


def update_index(campaigns: list[dict]):
    """Update wiki/index.md with new campaign entries."""
    # Build new index entries using the same slug logic as entries_to_wiki_pages
    lines = []
    for camp in campaigns:
        slug = slugify(camp["title"])
        if slug not in camp["campaign_id"].lower():
            slug = f"{slug}-{camp['campaign_id'][:8]}"
        lines.append(
            f"- [{camp['title']}](sources/{slug}.md) — {camp['entry_count']} entries"
        )

    # Append to index
    with open(WIKI_INDEX, "a") as f:
        f.write("\n## Campaigns (batch ingest)\n")
        f.write("\n".join(lines))
        f.write("\n")


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Batch campaign download + wiki ingest")
    parser.add_argument("--min-entries", type=int, default=100)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--campaign-id", type=str, default=None)
    args = parser.parse_args()

    print(f"=== Batch Campaign Ingest ===")
    print(f"Min entries: {args.min_entries}")
    print(f"Workers: {args.workers}")
    print(f"Dry run: {args.dry_run}")

    if args.dry_run:
        print("[DRY RUN] Would query and list campaigns only")

    # Step 1: Query campaigns
    uid = get_uid(EMAIL)
    campaigns = query_campaigns(uid, min_entries=args.min_entries)

    print(f"\nFound {len(campaigns)} campaigns with >={args.min_entries} entries:")
    for c in campaigns:
        print(f"  {c.entry_count:4d} | {c.title}")

    if args.dry_run:
        return

    # Step 2: Download + ingest
    manifest = []
    tmp_dir = Path("/tmp/campaign_downloads")
    tmp_dir.mkdir(exist_ok=True)

    def process_campaign(camp: CampaignInfo) -> list[dict]:
        print(f"\n[{camp.entry_count}] {camp.title} ({camp.campaign_id})")
        download_path = download_campaign(camp.campaign_id, tmp_dir / camp.campaign_id)
        if not download_path:
            return []

        pages = entries_to_wiki_pages(camp.title, camp.campaign_id, camp.entry_count, download_path)
        print(f"  Created {len(pages)} wiki pages")
        return [{"camp": vars(camp), "pages": [(str(p[0]), p[1]) for p in pages], "file": str(download_path)}]

    all_results = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(process_campaign, c): c for c in campaigns}
        for fut in as_completed(futures):
            result = fut.result()
            all_results.extend(result)

    # Step 3: Write manifest
    with open(MANIFEST_FILE, "w") as f:
        for r in all_results:
            f.write(json.dumps(r) + "\n")

    # Step 4: Update index
    update_index([r["camp"] for r in all_results])

    print(f"\n=== Done ===")
    print(f"Manifest: {MANIFEST_FILE}")
    print(f"Total campaigns processed: {len(all_results)}")


if __name__ == "__main__":
    main()
