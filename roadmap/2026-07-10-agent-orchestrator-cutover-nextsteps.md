---
type: nextsteps
status: active
date: 2026-07-10
bead: jleechan-lgm
---

# Agent Orchestrator Cutover: Evidence and Next Steps

## Executive summary

The remote identity cutover is complete. The original TypeScript repository is now `jleechanorg/agent-orchestrator-ts` with immutable repository ID `1176698268`. The Go upstream mirror is now the canonical `jleechanorg/agent-orchestrator` with immutable repository ID `1183912784` and parent `AgentWrapper/agent-orchestrator`.

The canonical Mac and Linux checkout paths and remotes are updated. Existing services stayed available through old-path symlink bridges. Those bridges are compatibility controls, not duplicate repositories, and must be removed only after their long-running consumers restart from canonical paths.

Generic `ao` remains the TypeScript CLI. Stable explicit launchers are available as `ao-ts` and `ao-go` on both Mac and Linux. Repointing generic `ao` is explicitly deferred until the Go PR actions fail closed and every consumer has been classified.

## Verified live state

| Surface | Canonical identity | Runtime evidence |
|---|---|---|
| TypeScript GitHub | https://github.com/jleechanorg/agent-orchestrator-ts | Repository ID `1176698268`; reference migration PR https://github.com/jleechanorg/agent-orchestrator-ts/pull/757 |
| Go GitHub | https://github.com/jleechanorg/agent-orchestrator | Repository ID `1183912784`; fork parent preserved |
| Mac TypeScript | `/Users/jleechan/project_agento/agent-orchestrator-ts` | Dashboard launchd PID `94609`; `http://127.0.0.1:3020/` returned HTTP 200 with 14,440 bytes |
| Mac Go | `/Users/jleechan/projects/agent-orchestrator` | Go AO launchd implementation and real evidence are at https://github.com/jleechanorg/jleechanclaw/pull/756; live REST state on 2026-07-10 20:26 PDT was open, non-draft, mergeable/clean at `37005244644ab4783aec070e4e4a1a6d696cf877` |
| Linux TypeScript | `/home/jleechan/project_agento/agent-orchestrator-ts` | `ao-orchestrator.service` active with PID `3446`, unchanged since 2026-07-10 12:39:22 PDT; `/home/jleechan/.local/bin/ao-ts --version` returned `0.1.3` |
| Linux Go | `/home/jleechan/projects/agent-orchestrator` | Canonical checkout migrated; legacy `ao-daemon.service` PID `3461` intentionally still executes the separately tracked `agent-orchestrator-golang` checkout |

Unrelated dirty files and untracked files in all source checkouts were preserved. Linked git worktrees were repaired after each move.

## Compatibility bridges still present

- `/Users/jleechan/project_agento/agent-orchestrator` -> `/Users/jleechan/project_agento/agent-orchestrator-ts`: retain until the Mac dashboard supervisor is reloaded from its canonical-path template during a controlled handoff.
- `/home/jleechan/project_agento/agent-orchestrator` -> `/home/jleechan/project_agento/agent-orchestrator-ts`: retain until `ao-orchestrator.service` is restarted from its updated canonical path. Its unchanged PID proves the move did not interrupt the live daemon.

The Mac and Linux Go bridges were removed after verification because no running consumer depended on them. The TypeScript bridges remain intentional availability controls for long-running Node processes; removing them is a separate controlled supervisor handoff, not a repository-identity blocker.

## Capability gaps and durable follow-ups

- P0 fail-closed PR actions: https://github.com/jleechanorg/agent-orchestrator/issues/14 and bead `jleechan-k4i`.
- Explicit TypeScript YAML to Go SQLite migration: https://github.com/jleechanorg/agent-orchestrator/issues/15 and bead `jleechan-odk`.
- Correct stale tracker-intake status documentation: https://github.com/jleechanorg/agent-orchestrator/issues/16 and bead `jleechan-awc`.
- Reconcile the separate legacy Go fork and Linux daemon: https://github.com/jleechanorg/agent-orchestrator/issues/17 and bead `jleechan-gbz`.
- Retry clean local-ahead export commits after recovery exhaustion: https://github.com/jleechanorg/jleechanclaw/issues/758 and bead `jleechan-4fw`.

Current-source inspection showed that Go tracker intake is wired; the contrary `docs/STATUS.md` text is stale. The blocking functional gap is PR action integrity: merge and resolve-comments currently report success without confirmed SCM behavior.

## Remaining closeout

1. Re-query https://github.com/jleechanorg/jleechanclaw/pull/756 through REST before acting; it was already open and non-draft at head `37005244644ab4783aec070e4e4a1a6d696cf877` when last verified. Obtain CodeRabbit and skeptic review at whatever head is current, and merge only after the repository's normal gates pass.
2. Install the combined tracked LaunchAgent from the stable canonical `jleechanclaw` checkout after that reviewed change lands. Keep the existing `llm_wiki` exporters loaded until the new label is verified, then retire only the two explicitly superseded labels. This is the remaining deployment step for `roadmap`.
3. Restart the Mac dashboard and Linux TypeScript daemon from canonical paths only during controlled supervisor handoffs, verify health immediately, then remove their TypeScript bridges.
4. Merge repository-reference PR https://github.com/jleechanorg/agent-orchestrator-ts/pull/757 only after its normal review gates pass. No merge was performed during this cutover.
5. Implement issue 14 before considering any generic `ao` cutover to Go.

## AO spawn safety correction

The stale `~/.claude/skills/ao-spawn-safety/SKILL.md` text was corrected. The current policy is:

- pause when a target channel exceeds its `kanban.max_spawn` setting (default 8);
- refuse at 20 active AO workers total;
- spawn at most 5 workers per batch;
- never use system load average as the gate.

The old value `15` was a superseded per-batch upper bound, not a session-count safety gate.

Historical roadmap entries, session transcripts, caches, evidence bundles, and archived policy copies intentionally retain their original names for provenance.
