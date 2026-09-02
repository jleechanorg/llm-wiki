---
name: disk-audit-apparent-vs-actual-size
description: Always verify disk/storage duplication claims with st_blocks (actual) not st_size (apparent) on cloud-sync mounts before trusting a report
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 74473364-f31b-4db0-9ecf-63a1836762fa
  modified: 2026-09-01T06:46:53.749Z
---

A disk-usage audit reported "~220GB used in Dropbox, ~55GB wasted on duplicate top-level vs nested `codex_conversations`/`claude_conversations` folders." That framing was **false** for local disk space: `du -sh` (actual disk blocks) showed the same directories consumed **0 bytes** locally (all `stat -f "blocks=%b"` = 0, flagged `compressed,dataless` — macOS FileProvider/Dropbox Smart Sync placeholders). Whole-Dropbox actual local usage was **10GB**, not 220GB; the 294GB figure was Dropbox's cloud/apparent size (`st_size`), which any tool without `-A`/blocks awareness will conflate with real disk pressure.

**Why:** Dropbox Smart Sync (and macOS CloudStorage FileProvider generally) keeps most files as "dataless" online-only placeholders — `ls`/`find`/naive `du` report full logical size even when zero bytes are actually on the local SSD. A disk-cleanup recommendation based on apparent size will wildly overstate local disk savings and can lead to needless "cleanup" actions that reclaim ~0 local bytes.

**However**, verifying "is this duplication real" surfaced a genuinely different, still-real problem: `scripts/backup-home.sh` has two backup legs (rsync/FileProvider `DROPBOX_TARGET` at line 49, correctly prefixed with `conversation-backups/`; and rclone `dst_remote` at line ~1220, `dst_remote="dropbox:${rel_norm%/}"`, NOT prefixed) writing the same `BACKUP_ITEMS` source data to two different Dropbox root locations every 2 hours (`StartInterval=7200` in `org.jleechan.user-scope-backup.plist`). That's a real ~55GB **Dropbox cloud-quota** duplication (not local disk), caused by an actual one-line code bug, not stale cache. Fix identified but NOT yet applied (needs explicit approval since it changes a live launchd-scheduled automation's destination): change line ~1220 to `dst_remote="dropbox:${DROPBOX_BACKUP_SUBDIR:-conversation-backups}/${rel_norm%/}"`.

**How to apply:** Any time a disk/storage audit (self-generated, subagent, or pasted from elsewhere) reports large duplication or waste numbers on a Dropbox/iCloud/OneDrive/CloudStorage-backed path, cross-check with `stat -f "blocks=%b" <file>` or `du` (real blocks, no `-A`) vs `du -A` or `ls` (apparent/cloud size) before accepting the claim or recommending cleanup. Distinguish "local disk waste" from "cloud quota waste" — they require different actions (local: nothing to do if dataless; cloud: fix the write path or delete the extra cloud copy). See also [[user-scope-stack-consolidation]] for the general "don't trust a report's headline number without checking the underlying primitive" pattern in this repo.
