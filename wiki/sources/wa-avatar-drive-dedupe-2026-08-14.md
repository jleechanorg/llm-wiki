---
title: "WA Avatar Source — Google Drive Folder 1dM4qeRcKTJmRZVq1bB8wTgPhdZNgazc- (2026-08-14)"
type: source
tags: [campaign, worldarchitect, avatar, google-drive, rclone, source]
date: 2026-08-14
drive_folder_id: 1dM4qeRcKTJmRZVq1bB8wTgPhdZNgazc-
drive_total_files: 141
drive_image_files: 135
drive_video_files: 6
unique_avatars: 132
dedupe_collisions: 3
staging_dir: ~/llm_wiki/raw/assets/avatars/
access_method: rclone gdrive: remote (jleechan@gmail.com personal account)
access_gotcha: Use --drive-root-folder-id <ID> not path-based access
related: [[reference-gdrive-upload-via-rclone-own-client]]
---

# Step 2 — Drive Avatar Pull Report

## Source
- Drive folder ID: `1dM4qeRcKTJmRZVq1bB8wTgPhdZNgazc-`
- Auth: `gdrive:` remote (jleechan@gmail.com personal account)
- Listing command: `rclone lsjson gdrive: --drive-root-folder-id 1dM4qeRcKTJmRZVq1bB8wTgPhdZNgazc- --max-depth 2 --files-only`

## Counts
- Total files in Drive folder: **141**
- Image files (after mime filter, kept): **135**
- Video files (skipped, not avatars): **6**
- Files downloaded to `/tmp/avatar_scene_gen/drive_avatars/`: **135**
- Dedupe collisions (same SHA-256): **3**
- Final unique avatars: **132**

## Staging
- Deduped avatar directory: `~/llm_wiki/raw/assets/avatars/`
- File count in staging dir: **132**
- Naming pattern: `<sha256[:8]>_<safe_slug>.<ext>`

## Artefacts
| Path | Purpose |
| --- | --- |
| `/tmp/avatar_scene_gen/drive_listing.json` | Full `rclone lsjson` output (all 141 entries) |
| `/tmp/avatar_scene_gen/drive_avatars/` | Bulk-downloaded originals (135 files) |
| `/tmp/avatar_scene_gen/drive_avatars_hashes.tsv` | `<sha256>\t<filename>\t<size>\t<drive_id>` per file |
| `/tmp/avatar_scene_gen/drive_avatars_deduped.jsonl` | Dedup manifest, one row per unique hash |
| `/Users/jleechan/llm_wiki/raw/assets/avatars/` | Staged final avatars |

## Dedupe detail (3 collisions)
1. `08701306…` — kept `ChatGPT Image Jul 1, 2025, 12_32_59 AM.png` (replaced `12_38_47 AM.png`, both 1858059 bytes)
2. `72059084…` — kept `lucifer_v3.png` (replaced `ChatGPT Image Jun 30, 2025, 10_32_52 AM.png`, both 2666418 bytes — same hash as lucifer_v3 by content)
3. `e387141b…` — kept `twin dragon.png` (replaced `twin_dragon_lava.png`, both 2403705 bytes)

## Errors
None.

## Notes for parent agent
- Manifest at `/tmp/avatar_scene_gen/drive_avatars_deduped.jsonl` has `sha256`, `kept_filename`, `replaced_filenames`, `size_bytes`, `drive_id` per row — ready to cross-reference against the campaign-side avatar scan.
- Wiki assets dir contains 132 unique files prefixed with first 8 hex chars of sha256 (e.g. `08701306_chatgpt_image_jul_1_2025_12_32_59_am.png`). Use the 8-char prefix to join with campaign-side scan output.
- Several files (e.g. `Alexiel Sith.JPG`, `Ains shy lich`) have no standard image extension in the Drive listing (no `.jpg` etc on some). rclone's `{png,jpg,...}` include pattern does not match extensionless files; I downloaded those 16 missing files via per-file `rclone copyto`. All 135 images present on disk.
- 489-byte "ChatGPT Image" PNGs are likely ChatGPT error/empty responses — included in dedupe but flagged for review.


## Auth note (Step 4 — Gemini subagent)

The Google Workspace CLI (`gws`) is **blocked** for personal `@gmail.com` Drive: the `gcloud`/`gws` OAuth clients on this machine have no Drive scopes registered (Google returns `restricted_client: Unregistered scope(s) in the request: drive.file`), so a Gemini worker invoking `gws` against personal Drive will not authenticate. This batch does **not** invoke `gws` at all — Step 2 used `rclone` with a user-owned Desktop-app OAuth client (see [[reference-gdrive-upload-via-rclone-own-client]]), and the Step 4 Gemini subagent fell back to Vertex AI (`worldarchitecture-ai` project) because the configured `GEMINI_API_KEY` was reported leaked by Google (`403 PERMISSION_DENIED`).

Reference: `gws`/`gcloud` cannot grant Drive scope for personal accounts; use the rclone + user-owned-client path documented in [[reference-gdrive-upload-via-rclone-own-client]] instead.
