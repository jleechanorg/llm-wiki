# Disk cleanup coverage gap for Docker and Antigravity regrowth

On 2026-05-29, `/System/Volumes/Data` refilled to 100% capacity with only about 7.4 GiB free. Emergency cleanup reclaimed space by deleting Docker Desktop's physically allocated `Docker.raw`, clearing `/private/tmp` AO scratch clones/logs, clearing rebuildable `~/.cache` entries, and deleting Antigravity generated worktrees and browser recordings.

The installed cleanup agents were loaded: `com.jleechan.cleanup-ao-tmp`, `com.jleechan.cleanup-llm-inspector`, `com.jleechan.cleanup-dev-caches`, and `com.jleechan.cleanup-apfs-snapshots`.

The gap was that those scheduled scripts did not cover the regrowth paths:

- Docker Desktop `~/Library/Containers/com.docker.docker/Data/vms/0/data/Docker.raw` grew to 88G physical allocation.
- `/private/tmp/wt-*` AO worktrees and `/private/tmp/ao-restore` were not covered by `cleanup-ao-tmp.sh`.
- `~/.cache/cmux`, `~/.cache/zig`, `~/.cache/firebase`, `~/.cache/gh`, `~/.cache/fastembed`, and `~/.cache/node` were not covered by `cleanup-dev-caches.sh`.
- `~/.gemini/antigravity-cli/brain/*/.system_generated/worktrees`, `~/.gemini/antigravity/worktrees`, and `~/.gemini/antigravity*/browser_recordings` were not covered by any installed cleanup agent.
- `~/.worktrees` remains a registered/locked worktree tree and must not be blindly deleted.

Rule: disk monitoring coverage is not cleanup coverage. If a path appears in `disk_snapshot.sh`, confirm it is either safely cleaned by a scheduled agent or explicitly tracked as a manual-risk item.

Beads: `bd-t9f`, related `bd-wz0`.
