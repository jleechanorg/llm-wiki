---
title: "CampaignDownloadMethodology"
type: concept
tags: [worldarchitect, campaigns, firestore, download, methodology]
sources: [campaign-download-methodology]
last_updated: 2026-04-12
---

## Summary

`CampaignDownloadMethodology` is the pattern for discovering and downloading all campaigns for a user from Firestore. The key insight: use Firebase Auth to find the UID, then traverse `users/{uid}/campaigns/` subcollections.

## Why It Was Hard

1. **MCP tools connect to wrong project**: `ops_firestore_query_collection_group` and `admin_download_campaign_entries` connect to `ai-universe-b3551` but the service account only has access to `worldarchitecture-ai`
2. **Firestore project mismatch**: Campaign data lives in `ai-universe-b3551` but credentials scope is `worldarchitecture-ai` — the `scripts/download_campaign.py` works because it uses `WORLDAI_DEV_MODE=true`
3. **Collection_group queries need indexes**: `COLLECTION_GROUP` scope indexes must be deployed, can't be created via gcloud directly for single-field indexes
4. **No single endpoint lists all campaigns**: Must iterate Firebase Auth users → each user's campaigns subcollection

## The Working Pattern

### Step 1: Find Firebase UID by email

```python
import firebase_admin
from firebase_admin import auth, credentials, firestore

firebase_admin.initialize_app(credentials.Certificate("/path/to/serviceAccountKey.json"))
# OR with WORLDAI_DEV_MODE:
# firebase_admin.initialize_app()  # uses default credentials

user = auth.get_user_by_email("jleechan@gmail.com")
uid = user.uid  # e.g., "vnLp2G3m21PJL6kxcuAqmWSOtm73"
```

### Step 2: Traverse campaigns subcollection

```python
db = firestore.client()
campaigns_ref = db.collection("users").document(uid).collection("campaigns")

for camp in campaigns_ref.stream():
    # Count story entries (expensive — one query per campaign)
    entry_count = sum(1 for _ in camp.reference.collection("story").stream())

    data = camp.to_dict()
    print(f"{entry_count} entries | {camp.id} | {data.get('title', 'Untitled')}")
```

### Step 3: Download with download_campaign.py

```bash
cd /Users/jleechan/projects/worldarchitect.ai
WORLDAI_DEV_MODE=true python scripts/download_campaign.py \
    --email jleechan@gmail.com \
    --campaign-id <campaign_id> \
    --output-dir /tmp/campaign_downloads
```

## Key Files

- `scripts/download_campaign.py` — Downloads campaign story + game_state
- `scripts/daily_campaign_report.py` — Has the user/campaign iteration pattern
- `scripts/campaign_selector_real.py` — Alternative iteration with campaign analysis
- `deployment/firebase/firestore.indexes.json` — Index definitions (COLLECTION scope)

## Root Cause: Project Mismatch

The MCP server for worldai connects to `ai-universe-b3551` Firestore project. The service account key grants access to `worldarchitecture-ai`. The `scripts/download_campaign.py` works because `WORLDAI_DEV_MODE=true` bypasses some credential checks and uses application default credentials.

## Related

- [[FirestoreProjectMismatch]] — MCP connects to wrong project
- [[FirebaseAdminSDK]] — Python SDK for Firebase operations
- [[CampaignIngestion]] — Ingesting campaigns into wiki
