# Disk Cleanup Coverage

Disk cleanup coverage is the guarantee that a monitored disk-growth path has a corresponding cleanup path or an explicit manual-risk policy.

## Pattern

Monitoring answers "what is growing?" Cleanup coverage answers "what prevents this from growing forever?"

These are separate. A path can appear in `disk_snapshot.sh` and still be absent from all scheduled cleanup scripts.

## 2026-05-29 Example

Loaded launchd cleanup agents did not clean the paths that refilled the disk:

- Docker Desktop `Docker.raw`
- `/private/tmp/wt-*` AO worker clones
- Antigravity generated worktrees
- Antigravity browser recordings
- broader rebuildable cache dirs under `~/.cache`

## Rule

For every high-growth path, assign one status:

- scheduled safe cleanup,
- manual cleanup only because state can be lost,
- monitor only with an alert and an owner.

`~/.worktrees` belongs in the manual category because it may include registered and locked worktrees. Docker raw cleanup also belongs in the manual category because it discards local Docker Desktop VM state.
