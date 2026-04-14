---
title: "Agento Proactive Recovery Design"
type: source
tags: [agento, proactive-recovery, session-respawn, ao-backfill, merge-completed, lifecycle-hook]
date: 2026-03-14
source_file: /home/jleechan/project_jleechanclaw/jleechanclaw/roadmap/AGENTO_PROACTIVE_RECOVERY_DESIGN.md
---

## Summary
The Agento Proactive Recovery Design addresses four recurring session failure modes: (1) sessions running after PR merges, (2) dead sessions blocking respawn, (3) stuck sessions with no respawn action available, (4) reactions not firing for pre-existing review comments. The recommended solution is a layered approach: ao-backfill.sh polling as immediate fallback, openclaw gateway /ao-notify webhook handler for event-driven recovery, and an upstream AO respawn action type as the long-term fix.

## The Four Failure Modes

| # | Symptom | Root cause |
|---|---|---|
| 1 | Sessions run for hours after PR merges | ao-backfill.sh only spawns, never stops |
| 2 | Killed/stuck sessions block respawn | Backfill skips PRs with any session, even dead ones |
| 3 | Stuck sessions abandoned after 3 nudges | AO has no `respawn` action; `requiresManualIntervention: true` is terminal |
| 4 | Reactions fire for new events only | Pre-existing review comments don't trigger bugbot-comments on newly spawned sessions |

## The Four Options

**Option A — External scripts (ao-backfill.sh)**
Extend `~/.openclaw/scripts/ao-backfill.sh` to:
- Cleanup: for each project, check if PR merged/closed → `ao stop`
- Liveness: for projects with stuck/killed sessions older than 30min → force `ao spawn`

Pros: zero AO repo changes, fits 15-min cron cadence, shell script
Cons: up to 15min lag, bash complexity grows, `ao session ls` output parsing is brittle

**Option B — AO Plugin (new `lifecycle-hook` plugin slot)**
Propose new `lifecycle-hook` plugin slot in AO's plugin registry for custom reaction action handlers.

Pros: clean integration, upstreamable to ComposioHQ
Cons: plugins statically compiled into CLI, no dynamic loading, requires TypeScript build + npm publish

**Option C — openclaw gateway /ao-notify handler (recommended)**
Extend the existing `agento-notifier.py` (Python `http.server` on port 18800) to handle `merge.completed` and `session.stuck` events:
- `merge.completed` → `ao stop <project>`
- `session.stuck` + PR still open → `ao spawn --fresh`

Pros: event-driven (<60s reaction vs 15min poll), entirely outside AO repo, uses existing infrastructure
Cons: gateway must be up (no queue, fire-and-forget), risk of event loops

**Option D — Fork AO + add `respawn` action type**
In jleechanorg/agent-orchestrator fork, add `respawn` action type in lifecycle-manager.ts.

Pros: cleanest UX, declarative config, inside AO lifecycle loop
Cons: requires fork build, TypeScript compile step, fork diverges from upstream

## Recommended: Layered Approach

```
Layer 1 (immediate, polling fallback):  ao-backfill.sh — cleanup + liveness
Layer 2 (event-driven, <60s reaction):    openclaw /ao-notify webhook handler
Layer 3 (declarative config, upstream):  respawn action type in AO fork → PR to ComposioHQ
```

## Layer 1: ao-backfill.sh Extensions

**Pass 1 — Merged PR cleanup:**
```bash
while IFS=' ' read -r REPO PROJECT_ID DEFAULT_BRANCH; do
    state=$(gh pr list --repo "$REPO" --head "$DEFAULT_BRANCH" \
              --json state,merged --jq '.[0] | "\(.state) \(.merged)"' 2>/dev/null || echo "")
    if [[ "$state" == "MERGED true" || "$state" == "CLOSED"* ]]; then
        "$AO_BIN" stop "$PROJECT_ID" 2>/dev/null || true
    fi
done <<< "$MAPPINGS"
```

**Pass 2 — Force-respawn dead sessions:**
Read session metadata files directly at `~/.agent-orchestrator/<machine-id>-<project>/sessions/<session-id>` (format: `key=value` plain text). Compare `createdAt` — if session created >30min ago AND status=stuck, respawn candidate.

## Layer 2: /ao-notify Handler

Existing `agento-notifier.py` (port 18800, Python `http.server`) already handles `/ao-notify`. Extend `Handler.do_POST` with dispatch table:

```python
RECOVERY_HANDLERS = {
    "merge.completed": handle_merge_completed,
    "session.stuck":   handle_session_stuck,
    "session.killed":  handle_session_killed,
}
```

Use `subprocess.Popen` (non-blocking) for ao stop/spawn calls — `http.server` is single-threaded, blocking subprocess calls would block the next request.

Guard against loops: `_ao_respawn_cooldown` per project, 60s minimum between respawns.

## Resolved Open Questions

**Q1: Does the openclaw gateway have an HTTP server we can add routes to?**
Yes — `agento-notifier.py` (`~/project_jleechanclaw/worktree_agento/scripts/agento-notifier.py`), Python `http.server` on port 18800, already handles `/ao-notify`. Extends via dispatch table in `do_POST`.

**Q2: Parse `ao session ls` or session metadata files?**
Read session metadata files directly at `~/.agent-orchestrator/<machine-id>-<project>/sessions/<session-id>` (plain `key=value` format). `ao session ls` is formatted for humans, requires fragile regex.

**Q3: Kill stuck tmux before respawning?**
No — just run `ao spawn <project> --claim-pr <N>`. AO handles deduplication. Caveat: `STALE_PR_OWNERSHIP_STATUSES` doesn't include `stuck`/`killed`, so before respawning, clear `pr` field from stuck session metadata: `sed -i '' 's/^pr=.*/pr=/' "$STUCK_META"`.

**Q4: Raise escalation ceiling (currently `escalateAfter: 3`)?**
Yes — raise to 20 as immediate workaround. With 10min intervals, gives ~3.3 hours of autonomous recovery attempts. Long-term fix is respawn action type (Option D).

## What Does NOT Need an AO Repo Change
- Merged-PR session cleanup → ao-backfill.sh
- Liveness respawn of killed sessions → ao-backfill.sh
- Event-driven cleanup/respawn → openclaw /ao-notify handler
- agent-stuck + agent-needs-input nudges → already fixed via yaml reactions config
- Orchestrators persisting across reboots → install-agento-orchestrators.sh launchd job

Only genuine gap requiring AO code: a `respawn` action type (problem 3). Everything else is config + external script.

## Related Concepts
- [[ProactiveSessionRecovery]]
- [[LayeredRecoveryArchitecture]]
- [[AutonomousAgentLoop]]