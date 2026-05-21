---
title: "setup-launchd.sh dry-run writes files bug"
type: source
date: 2026-05-19
tags: [hermes, launchd, bash, dry-run, plist, setup-launchd]
---

## Summary

`scripts/setup-launchd.sh` in hermes had a bug where `_install_plist()` ran `sed`
substitution and wrote the substituted plist to `~/Library/LaunchAgents/` before
the `DRY_RUN` check. Default mode is dry-run, so every invocation without `--apply`
silently overwrote managed plists without loading them.

## Bug Pattern

```bash
# WRONG — write happens before dry-run gate
sed ... "$src" > "$dest.tmp" && mv "$dest.tmp" "$dest"
if $DRY_RUN; then return; fi  # too late
```

## Fix Pattern

```bash
# CORRECT — gate first, write only when applying
if $DRY_RUN; then dry "would install: ..."; return; fi
sed ... "$src" > "$dest.tmp" && mv "$dest.tmp" "$dest"
```

## Additional fixes (same commit ab684908be)

- Created `launchd/ai.hermes-mem0-server.plist.template` (CORE_PLISTS referenced it but source was missing)
- Deleted duplicate `launchd/ai.hermes.schedule.harness-analyzer-9am.plist` (identical to `.template`)
- Corrected stale comments saying Phase 2 requires substitute-plists.sh

## References

- Commit: ab684908be on fix/setup-launchd-dryrun
- Bead: orch-ud0d
- Memory: feedback_2026-05-19_setup_launchd_dryrun_writes.md
