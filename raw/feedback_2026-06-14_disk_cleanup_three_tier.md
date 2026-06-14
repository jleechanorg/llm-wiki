---
name: three-tier-disk-cleanup-playbook-15-5gb-reclaimed
description: "Tiered cleanup classification for /diskm targets beyond what auto-clean covers — supervisor launchd logs, AO wa-* sessions, /private/tmp scratch worktrees"
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: cc9c3759-7030-436a-a3d5-7e356d65b412
---

## Context

After PR [#686](https://github.com/jleechanorg/agent-orchestrator/pull/686) merged (per-worker colima bootstrap prevention), a /diskm rerun on 2026-06-13 surfaced three cleanup tiers that the existing auto-clean paths (cleanup_dev_caches, cleanup_tmp, cleanup_worktrees, cleanup_llm_inspector, cleanup_agent_artifacts) did not touch. Reclaiming them required user approval per the disk_magician safety constraints (14-day mtime rule for worktrees/agent sessions) and produced **15.5 GB of new reclaim** with a small new automation.

## The three tiers (and safety filters)

### Tier A — `~/.claude/supervisor` rotated launchd logs (~1.95 GB, no approval risk)

- **Symptom**: 91 × 50 MB rotated log files = 4.55 GB across 19 days.
- **Why it grows**: `cmux-codex-launchd` plist rotates stdout at 50 MB cap; nothing prunes the rotations.
- **Pattern**: `cmux-codex-launchd.YYYYMMDDTHHMMSS.log` (timestamped rotation). NEVER touch `cmux-codex-launchd.log` (active), `cmux-codex-launchd.stderr.log` (active stderr), or `cmux-codex-launchd-state.json` (state file).
- **Cleanup script**: `scripts/cleanup_supervisor_logs.sh` (added in this session). Defaults to dry-run; `--clean` applies. Pattern-matches only timestamped rotations older than 7 days; post-checks the three never-touch files are still present.
- **Wired into**: `scripts/disk_audit.sh` line 263-266, between `cleanup_llm_inspector.sh` and `cleanup_agent_artifacts.sh`. Now every `./disk_magician.sh clean` runs it.
- **New floor**: ~7 × 50 MB = 350 MB indefinitely (7-day retention).

### Tier B — `~/.ao-sessions/wa-*` AO session dirs (~9.8 GB, required WORKTREE APPROVED for < 14d)

- **Sizes**: range from 48M (fresh worker) to 2.7G (per-worker colima bootstrap artifact, the very thing PR #686 prevents going forward).
- **Safety filter applied** (the one we used; refine if you re-derive):
  1. **Skip `wa-orchestrator`** — that's the live orchestrator, must preserve.
  2. **Skip dirs < 100M** — small ones (48M) are likely fresh or just-completed workers; not worth the risk.
  3. **Skip dirs < 30 min old** — likely in-flight; never kill active work.
  4. The rest: `rm -rf` cleanly.
- **wa-2327 special note**: 2.7G with 2.1G in `.colima` = the per-worker colima bootstrap incident. Now safe to clean since PR #686 prevents the bootstrap pattern.
- **The never-delete list does NOT include `~/.ao-sessions`** — only `~/.codex/sessions`, `~/.codex/sessions_archive/`, `~/.codex/state*.sqlite`, `~/.codex/log`, `~/.claude/projects` are off-limits.

### Tier C — `/private/tmp/wt-*` and `/private/tmp/wa-*` scratch worktrees (~4.0 GB, lower risk than Tier B)

- **What they are**: agent worktree checkouts for completed PR/agent runs. Most are 264-277 MB. They are NOT full git clones (`.git` is a file pointing to parent's `.git/worktrees/`, not a directory), so `cleanup_tmp.sh` (which requires `.git` folder) does not touch them. `cleanup_worktrees.sh` only walks `~/.gemini/antigravity/worktrees/`, so it also misses them.
- **Safety filter applied**:
  1. **Skip < 100M** — small briefs/notes (`wa-XXXX-brief.md` 4-16K) are often in-flight evidence; not safe to delete.
  2. **Skip < 30 min old** — likely active agent work.
  3. The rest: `rm -rf`.
- **Total cleaned**: 15 dirs (8 wt-* + 7 wa-* of the 264M+ size).

## Verification

```
Before:  133 Gi free, 12% used on 926 Gi
After:   147 Gi free, 11% used
Delta:   +14 Gi (matches 15.5 GB reclaimed minus APFS overhead)
```

`./disk_magician.sh audit` post-cleanup shows zero regressions on monitored paths.

## References

- Commit: `5b3e3a6` on branch `dev1781402943` (feat(supervisor-logs): add cleanup_supervisor_logs.sh + wire into disk_audit)
- Files: `scripts/cleanup_supervisor_logs.sh` (new, 80 lines), `scripts/disk_audit.sh` (3-line wiring), `README.md` Section E
- Original PR: https://github.com/jleechanorg/agent-orchestrator/pull/686 (the prevention pattern that made wa-2327 safe to clean)

## Reusable pattern: classify any disk-cleanup target by asking

1. **Is it in the never-delete list?** (`~/.codex/*`, `~/.claude/projects`) → NEVER touch.
2. **Is it > 14 days old?** → auto-clean OK via existing /diskm paths.
3. **< 14 days + outside the never-delete list** → needs explicit user approval, then safety-filter by size+age.
4. **For launchd-style rotated logs**: write a small dedicated cleanup with explicit never-touch list (active log, stderr, state file). Default threshold: 7 days.
5. **For agent worktree scratch dirs in /tmp**: minimum size (≥ 100M) + minimum age (≥ 30 min) filters are sufficient for safety.
