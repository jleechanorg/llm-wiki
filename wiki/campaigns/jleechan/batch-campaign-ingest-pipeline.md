---
title: "Batch Campaign Ingest Pipeline"
type: concept
tags: [campaign, ingest, firebase, firestore, worldarchitect.ai]
sources: [batch_campaign_ingest.py]
last_updated: 2026-04-13
---

# Batch Campaign Ingest Pipeline

## Overview

Script: `tools/batch_campaign_ingest.py`

Downloads all campaigns from Firestore for jleechan@gmail.com and ingests them as wiki source pages.

## Methodology

### Step 1: Firebase Auth → UID
```
Email → Firebase Auth → UID
```
Uses `WORLDAI_DEV_MODE=true` to connect to worldarchitecture-ai Firestore project.

### Step 2: Campaign Discovery
```
users/{uid}/campaigns/ → stream → filter by entry_count >= min_entries
```
For each campaign, counts entries by streaming `story` subcollection. Expensive but accurate.

### Step 3: Download
```
scripts/download_campaign.py --email jleechan@gmail.com --campaign-id {id} --output-dir {tmp}
```
Uses worldarchitect.ai download script with proper env vars.

### Step 4: Wiki Conversion
```
Downloaded text → split by "Entry N" patterns → wiki/sources/{slug}/{slug}-entry-NNN.md
```
Each entry becomes a source page with YAML frontmatter (type: source, campaign_id, tags).

### Step 5: Entity Extraction (separate script)
```
tools/extract_campaign_entities.py --batch 8 --batch-index N
```
Runs in 8 parallel batches. Extracts: player character, NPCs in 3+ scenes, locations, factions.

## Usage

```bash
# Dry run — list campaigns only
python tools/batch_campaign_ingest.py --dry-run --min-entries 100

# Actual ingest
python tools/batch_campaign_ingest.py --min-entries 100 --workers 4
```

## Required Environment Variables

```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/serviceAccountKey.json
export WORLDAI_DEV_MODE=true
```

## Dry Run Results (2026-04-13)

Found **68 campaigns** with ≥100 entries:

| Entries | Campaign |
|---|---|
| 2414 | Nocturne bg3 v4 |
| 2130 | visenya v1 (dunk and egg) |
| 2054 | Nocturne bg3 after |
| 2007 | Nocturne post bg3 zhent |
| 1850 | Nocturne bg3 v5 (fixed v2) |
| 1644 | alexiel swtor |
| 1370 | Sariel killer |
| 1212 | faction - Nocturne bg3 V3 |
| 1194 | Aizen bg3 |
| 1069 | Itachi Evil Campaign 2 |
| 1042 | gaia julia v2 |
| 1000 | Dragon knight evil |

Total: 68 campaigns, top 12 listed above.

## Key Files

- `tools/batch_campaign_ingest.py` — Main pipeline script
- `tools/extract_campaign_entities.py` — Entity extraction (runs separately after batch ingest)
- `scripts/download_campaign.py` — worldarchitect.ai download script

## Notes

- The Firestore query counts entries by streaming the story subcollection — slow for large campaigns (2000+ entries)
- Entity extraction runs as separate batches post-ingest
- MCP query for campaigns is blocked by missing Firestore composite index — script uses Python Firebase SDK directly instead
