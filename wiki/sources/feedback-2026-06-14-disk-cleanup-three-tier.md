---
title: "2026-06-14 Disk Cleanup Three Tier"
type: source
tags: ["feedback", "disk-cleanup", "disk-magician", "automation", "pr686"]
date: 2026-06-14
source_file: raw/feedback_2026-06-14_disk_cleanup_three_tier.md
---

## Summary
After PR #686 (colima per-worker prevention) merged, a /diskm rerun surfaced three cleanup classes the existing auto-clean paths (cleanup_dev_caches, cleanup_tmp, cleanup_worktrees, cleanup_llm_inspector, cleanup_agent_artifacts) do not touch. Reclaiming them required explicit user approval per the 14-day mtime safety rule and produced 15.5 GB of new reclaim: 1.7 GB supervisor launchd log rotations (now automated via new cleanup_supervisor_logs.sh wired into disk_audit.sh, 7d retention), 9.8 GB ~/.ao-sessions/wa-* agent sessions (safety filter: skip wa-orchestrator, <100M, <30m old; includes the 2.7 GB wa-2327/.colima bootstrap artifact the PR prevents), 4.0 GB /private/tmp/wt-*/wa-* scratch worktrees (the existing cleanup_tmp and cleanup_worktrees both miss these — .git is a file pointing to parent's worktree, not a directory, and the worktrees root is not in any monitored path). Disk: 133 Gi → 147 Gi free.

## Key Claims
- The /diskm auto-clean paths are not exhaustive — supervisor log rotations are a 4.55 GB unmonitored rot class
- Tier A (launchd rotated logs) is always safe to automate; never-touch list = active log + stderr + state file
- Tier B (wa-* AO sessions) safety filter: skip wa-orchestrator, skip <100M, skip <30m old
- Tier C (/tmp wt-/wa- worktrees) miss both cleanup_tmp.sh (requires .git directory) and cleanup_worktrees.sh (only walks ~/.gemini/antigravity/worktrees/)
- ~/.ao-sessions is NOT in the disk_magician never-delete list — only ~/.codex/sessions, ~/.codex/sessions_archive, ~/.codex/state*.sqlite, ~/.codex/log, ~/.claude/projects are off-limits
- Pattern: classify any /diskm target by (1) is it in the never-delete list, (2) is it launchd-style rotated logs, (3) is it a worktree/session dir; apply tier-specific safety filter
- wa-2327 special note: 2.7 GB with 2.1 GB in .colima = per-worker colima bootstrap incident, now safe to clean post-PR-686

## Key Quotes
> "When /diskm audit shows growth on a path that no auto-clean script touches, classify by (1) is it in the never-delete list, (2) is it launchd-style rotated logs, (3) is it a worktree or session dir? Apply the tier-specific safety filter (orchestrator + < 100M + < 30m for wa-*/wt-* dirs; > 7d for rotated launchd logs) and ask the user for the explicit approval tier B/C require. Tier A is always safe to automate."

## Connections
- [[DiskMagician]]
- [[CleanupSupervisorLogs]]
- [[PR686ColimaFix]]
- [[PerWorkerColimaBootstrap]]
- [[DISKMagicSafetyConstraints]]
- [[LaunchdLogRotation]]
- [[AOSessionDirs]]
