---
title: "FirestoreProjectMismatch"
type: concept
tags: [worldarchitect, firestore, MCP, credentials, project]
sources: [firestore-project-mismatch]
last_updated: 2026-04-12
---

## Summary

`FirestoreProjectMismatch` is the issue where the worldai MCP tools connect to `ai-universe-b3551` Firestore project, but the service account credentials only have access to `worldarchitecture-ai`. This causes `ops_firestore_query_collection_group` and `admin_download_campaign_entries` to return 0 results even when campaigns exist.

## The Problem

| Tool | Expected Project | Actual Project | Result |
|------|----------------|----------------|--------|
| `ops_firestore_query_collection_group` | worldarchitecture-ai | ai-universe-b3551 | 0 docs |
| `admin_download_campaign_entries` | worldarchitecture-ai | ai-universe-b3551 | 0 entries |
| `scripts/download_campaign.py` | ai-universe-b3551 | works with WORLDAI_DEV_MODE | 50+ campaigns |

## Why download_campaign.py Works

The `download_campaign.py` script uses `WORLDAI_DEV_MODE=true` which:
1. Applies clock skew patch for GCP metadata server time sync
2. Uses application default credentials (ADC) from gcloud
3. Successfully accesses the Firestore data in `ai-universe-b3551`

## The Fix Options

1. **Use `download_campaign.py`** — Works today, use Firebase Auth + Firestore SDK directly
2. **Fix MCP credentials** — Configure MCP to use service account with access to ai-universe-b3551
3. **Add COLLECTION_GROUP indexes** — Update `deployment/firebase/firestore.indexes.json` and redeploy (but single-field COLLECTION_GROUP indexes aren't supported)

## Related

- [[CampaignDownloadMethodology]] — Working pattern for downloading campaigns
- [[FirebaseAdminSDK]] — Python SDK pattern
