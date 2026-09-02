---
title: "Disk audits: apparent size vs actual disk usage"
type: concept
tags: [disk-audit, dropbox, filesystem, verification]
---

## Definition
On cloud-sync mounts (Dropbox Smart Sync, macOS CloudStorage/FileProvider, iCloud Drive), `ls`, `find`, and `du` without a blocks-based flag report the *apparent* (logical/cloud) size of a file — the size it would be if fully downloaded — even when the file is a "dataless" online-only placeholder consuming zero bytes on the local disk. Standard `du -sh` (no `-A`) on macOS reports real disk blocks and correctly shows 0B for dataless directories; but any tool, script, or subagent that uses `du -A`, sums file sizes from `ls`/`find`, or reads `st_size` instead of `st_blocks` will report the cloud size as if it were local disk usage.

## Verification method
```bash
stat -f "blocks=%b size=%z %N" <file>   # blocks=0 → dataless/online-only, no local disk cost
ls -lO <file>                            # flags column shows "compressed,dataless" for placeholders
du -sh <dir>                             # actual disk blocks (macOS default, no -A)
du -sh -A <dir>                          # apparent/cloud size — do NOT treat this as local disk usage
```

## Why it matters
A disk-cleanup or duplication report that uses apparent size will wildly overstate local disk savings. Deleting a "duplicate" that's actually a 0-byte-local placeholder frees no local disk space — it only affects cloud storage quota, which is a separate concern with separate remediation (fix the write path, or explicitly delete the cloud copy).

## Instance
[[disk-audit-apparent-vs-actual-size-2026-08-31|2026-08-31 case]]: a Dropbox report claimed ~220GB local / ~55GB wasted duplication; real local disk usage was 10GB total. The duplication claim was still partially right, but for cloud quota, not local disk — traced to a real bug in [[backup-home-sh]].

## Connections
- [[backup-home-sh]] — the script whose dual-target bug produced real (cloud-only) duplication
- [[Dropbox-Smart-Sync]] — the placeholder mechanism
