---
name: setup-launchd-dryrun-writes-files
description: setup-launchd.sh dry-run silently wrote substituted plists to LaunchAgents; sed ran before DRY_RUN check
metadata: 
  node_type: memory
  type: feedback
  bead: orch-ud0d
  originSessionId: 8740d484-1020-4e44-a28f-13a5a1a2eddd
---

## Learning: setup-launchd.sh dry-run was not read-only

**Date**: 2026-05-19
**Branch**: fix/setup-launchd-dryrun
**Commit**: ab684908be

### What went wrong

`_install_plist()` ran the `sed` substitution and wrote the result to `~/Library/LaunchAgents/<name>.plist` **before** the `DRY_RUN` check. Default invocation (no args) is dry-run. So every run of `./setup-launchd.sh` without `--apply` silently overwrote all managed plists on disk. `launchctl bootstrap` was not called (since DRY_RUN returned early), but the plist files on disk were replaced.

**Why it matters**: If the prod gateway plist was correctly installed by a prior deploy, a dry-run "status check" would silently replace it with a freshly substituted version, potentially from a different branch/state.

```bash
# WRONG (original) — substitution before DRY_RUN check
sed -e "s|@HOME@|$HOME|g" ... "$src" > "$dest.tmp" && mv "$dest.tmp" "$dest"
if $DRY_RUN; then
  dry "  would install: ..."
  return  # too late — file already written
fi
```

### Fix

Move all file I/O inside the `--apply` branch:

```bash
# CORRECT — check first, write only when applying
if $DRY_RUN; then
  dry "  would install: $src_file → $dest_file (label=$label)"
  return
fi
# substitution + write happen here
sed -e "s|@HOME@|$HOME|g" ... "$src" > "$dest.tmp" && mv "$dest.tmp" "$dest"
```

**How to apply**: Any bash script with dry-run mode: put ALL writes, moves, and deletes inside `if ! $DRY_RUN` blocks. Reading and reporting are OK in dry-run.

### Additional bugs fixed in same commit

1. **Missing template**: `ai.hermes-mem0-server.plist.template` was referenced in CORE_PLISTS but did not exist in `launchd/`. `_install_plist` silently warned "skip (template not found)". Installed plist had hardcoded `/Users/jleechan/` paths — created proper `@HOME@`-based template.

2. **Duplicate file**: `launchd/ai.hermes.schedule.harness-analyzer-9am.plist` was byte-for-byte identical to `ai.hermes.schedule.harness-analyzer-9am.plist.template`. setup-launchd.sh only installed from the `.template` version. Deleted the duplicate.

3. **Stale comments**: Header and Phase 2 comments still said "Phase 2 not automated — run substitute-plists.sh first." Updated to reflect inline substitution.

### Pattern

> When adding inline substitution to an install script, always verify that substitution happens AFTER the dry-run gate, not before it.

### References

- Commit: `ab684908be` on `fix/setup-launchd-dryrun`
- Files changed: `scripts/setup-launchd.sh`, `launchd/ai.hermes-mem0-server.plist.template` (new), `launchd/ai.hermes.schedule.harness-analyzer-9am.plist` (deleted)
- Related memory: [[feedback_2026-05-14_hermes_launchd_meta_pattern]]
