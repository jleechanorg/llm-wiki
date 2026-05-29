# Disk Cleanup Coverage Gap - 2026-05-29

## Summary

The 2026-05-29 disk emergency showed that user-scope disk monitoring covered more paths than scheduled cleanup. The launchd cleanup agents were loaded, but the actual regrowth paths were outside their cleanup rules.

## Incident

`/System/Volumes/Data` reached 100% capacity with about 7.4 GiB free. Emergency cleanup raised free space to about 104 GiB.

Confirmed reclaimed sources:

- Docker Desktop `Docker.raw`: 88G physical allocation before cleanup, about 11G physical after Docker recreated the sparse file.
- `/private/tmp`: AO scratch clones/logs removed, down to about 21M.
- `~/.cache`: rebuildable cache entries removed, down to about 85M.
- Antigravity generated worktrees and browser recordings removed, leaving `~/.gemini/antigravity` around 4.2G.

## Scheduled Cleanup Coverage

Installed and loaded launchd agents:

- `com.jleechan.cleanup-ao-tmp`
- `com.jleechan.cleanup-llm-inspector`
- `com.jleechan.cleanup-dev-caches`
- `com.jleechan.cleanup-apfs-snapshots`

Coverage gaps:

- `cleanup-ao-tmp.sh` did not cover `/private/tmp/wt-*`, `/private/tmp/wt_*`, or `/private/tmp/ao-restore`.
- `cleanup-dev-caches.sh` did not cover `~/.cache/cmux`, `~/.cache/zig`, `~/.cache/firebase`, `~/.cache/gh`, `~/.cache/fastembed`, or `~/.cache/node`.
- No loaded cleanup agent covered `~/.gemini/antigravity-cli/brain/*/.system_generated/worktrees`, `~/.gemini/antigravity/worktrees`, or Antigravity `browser_recordings`.
- No cleanup agent should blindly remove `~/.worktrees`; it contains registered/locked worktrees.
- Docker raw growth is monitored by snapshot logic but not automatically cleaned; deleting it discards Docker Desktop local VM state.

## Reusable Rule

Disk monitoring coverage is not cleanup coverage. When a path is added to disk snapshots, add one of three outcomes:

- scheduled safe cleanup,
- explicit manual cleanup procedure,
- explicit risk note that it is monitored only.

## References

- `/Users/jleechan/projects_other/user_scope/scripts/install-auto-cleanup-launchd.sh`
- `/Users/jleechan/projects_other/user_scope/scripts/cleanup-ao-tmp.sh`
- `/Users/jleechan/projects_other/user_scope/scripts/cleanup-dev-caches.sh`
- `/Users/jleechan/projects_other/user_scope/scripts/cleanup-ao-sessions.sh`
- `/Users/jleechan/projects_other/user_scope/scripts/disk_snapshot.sh`
- Bead: `bd-t9f`
- Related bead: `bd-wz0`
