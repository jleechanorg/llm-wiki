---
title: "Disk-audit apparent-vs-actual size + backup-home.sh dual Dropbox target bug"
type: source
tags: [disk-audit, dropbox, backup-home, verification, filesystem]
date: 2026-08-31
source_file: raw/feedback_2026-08-31_disk-audit-apparent-vs-actual-size.md
---

## Summary
A Dropbox duplication report claimed ~220GB used and ~55GB wasted on duplicate top-level vs nested `codex_conversations`/`claude_conversations` folders. Empirical verification with `stat -f "blocks=%b"` and `du` (actual disk blocks, not apparent/`-A` size) showed the claim was false for local disk: total actual local disk usage across all of Dropbox was only 10GB, and the "duplicate" top-level folders were `compressed,dataless` macOS FileProvider/Dropbox Smart Sync placeholders consuming 0 local bytes. However, re-verifying the underlying mechanism surfaced a real, distinct bug in `scripts/backup-home.sh`: two backup legs write the same source data to two different Dropbox root locations, causing genuine cloud-quota (not local-disk) duplication.

## Key Claims
- Dropbox/macOS CloudStorage FileProvider mounts report full logical size via `ls`/`find`/`du` even for files with zero local bytes ("dataless" placeholders) — never trust a duplication/waste report on such a mount without checking `stat -f blocks` or `du` (real blocks) vs apparent size.
- `scripts/backup-home.sh` line 49 (`DROPBOX_TARGET`) correctly prefixes uploads with `conversation-backups/`; the rclone leg at ~line 1220 (`dst_remote="dropbox:${rel_norm%/}"`) does not, causing the same `BACKUP_ITEMS` data to land at both Dropbox-root and `conversation-backups/` every 2 hours (`StartInterval=7200`).
- This produces real ~55GB Dropbox cloud-quota duplication (root: ~118,570 files) vs ~94GB nested (>450,000 files) — verified consistent with the original report's file counts and apparent sizes, even though the report's "local disk" framing was wrong.
- Fix identified (`dst_remote="dropbox:${DROPBOX_BACKUP_SUBDIR:-conversation-backups}/${rel_norm%/}"`) but not applied — pending explicit approval since it changes a live launchd-scheduled automation's write destination.

## Key Quotes
> "stat -f blocks=%b showed most flagged directories are dataless Smart Sync placeholders (0 local bytes); real total Dropbox local disk usage was 10GB."

## Connections
- [[backup-home-sh]] — the script with the dual-target bug
- [[Dropbox-Smart-Sync]] — dataless placeholder mechanism that caused the false-positive framing
- [[disk-audit]] — general pattern: verify actual vs apparent size before trusting cleanup/duplication claims
