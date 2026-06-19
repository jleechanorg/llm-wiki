---
title: "fix/mcp-daemon-keepalive branch (jleechanclaw)"
type: entity
tags: [branch, launchd, mcp-daemon, hermes, worktree-isolation]
last_updated: 2026-06-19
---

# fix/mcp-daemon-keepalive

Branch on `origin` (jleechanorg/jleechanclaw). Intent: add KeepAlive + template for mcp-daemon launchd plist. Branch name says mcp-daemon but the working tree has scope creep.

## Current state (2026-06-19 03:30Z)

- **2 commits pushed** to `origin/fix/mcp-daemon-keepalive`:
  - `16ecf2ab31` feat(launchd): add KeepAlive + template for mcp-daemon
  - `8eb29dd106` docs(slack): Layer 2 /es evidence bundle for 5e detector integration test
- **No PR exists** (`gh pr list --head fix/mcp-daemon-keepalive --state all` → `[]`)
- **11 uncommitted M + 7 untracked ?? files** in working tree
- **Merge-readiness 5-gate check: 5/5 FAIL**

## Scope creep in the working tree

- `D launchd/com.jleechan.mcp-daemon.plist.template` (the file the previous commit added — being deleted locally)
- `M workspace/SOUL.md` (live policy file — dangerous to carry uncommitted)
- `M agent-orchestrator.yaml`, `M scripts/deploy.sh`, `M scripts/install-launchagents.sh` (config drift)
- `?? launchd/ai.hermes.launchd-drift-audit.plist.template`, `?? scripts/audit-launchd-drift.sh`, `?? tests/test_example_placeholder_discipline.sh` (new scripts from today's work, not in any PR)
- `?? skills/worldarchitect/` (new skills tree)
- `?? roadmap/BROWSERCLAW_DEFERRED_SPEC.md` (deferred-spec doc)

## Recommended next steps

1. Decide on each uncommitted subset — land, discard, or stash
2. Split into scoped PRs:
   - `fix/mcp-daemon-keepalive` → just the KeepAlive plist (already committed)
   - `feat/launchd-drift-audit` → `audit-launchd-drift.sh` + plist + test
   - `feat/skills-worldarchitect` → `skills/worldarchitect/`
   - `docs/browserclaw-deferred-spec` → `BROWSERCLAW_DEFERRED_SPEC.md`
3. Drive each PR to 7-green
4. Type literal `MERGE APPROVED` per turn before any merge
5. After merge: `scripts/deploy.sh` to promote to prod

## Sources

- [[feedback-2026-06-19-hermes-liveness-and-merge-readiness]] — the 5-gate verification that flagged 5/5 failures on this branch
- [[WorktreeIsolation]] — the rule this branch violates (direct edits to `~/.hermes/` not via PR)
- [[MergeReadinessGate]] — the 5-gate protocol