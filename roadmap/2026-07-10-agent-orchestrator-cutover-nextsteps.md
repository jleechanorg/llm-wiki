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

Generic `ao` remains the TypeScript CLI. `ao-go` is the Go binary. Repointing generic `ao` is explicitly deferred until the Go PR actions fail closed and every consumer has been classified.

## Verified live state

| Surface | Canonical identity | Runtime evidence |
|---|---|---|
| TypeScript GitHub | https://github.com/jleechanorg/agent-orchestrator-ts | Repository ID `1176698268`; reference migration PR https://github.com/jleechanorg/agent-orchestrator-ts/pull/757 |
| Go GitHub | https://github.com/jleechanorg/agent-orchestrator | Repository ID `1183912784`; fork parent preserved |
| Mac TypeScript | `/Users/jleechan/project_agento/agent-orchestrator-ts` | Dashboard launchd PID `94609`; `http://127.0.0.1:3020/` returned HTTP 200 with 14,440 bytes |
| Mac Go | `/Users/jleechan/projects/agent-orchestrator` | Go AO launchd implementation is being proven by https://github.com/jleechanorg/jleechanclaw/pull/756 |
| Linux TypeScript | `/home/jleechan/project_agento/agent-orchestrator-ts` | `ao-orchestrator.service` active with PID `3446`, unchanged since 2026-07-10 12:39:22 PDT |
| Linux Go | `/home/jleechan/projects/agent-orchestrator` | Canonical checkout migrated; legacy `ao-daemon.service` PID `3461` intentionally still executes the separately tracked `agent-orchestrator-golang` checkout |

Unrelated dirty files and untracked files in all source checkouts were preserved. Linked git worktrees were repaired after each move.

## Compatibility bridges still present

- `/Users/jleechan/project_agento/agent-orchestrator` -> `/Users/jleechan/project_agento/agent-orchestrator-ts`: retain until the Mac dashboard supervisor is reloaded from its canonical-path template during a controlled handoff.
- `/Users/jleechan/projects/agent-orchestrator-mirror` -> `/Users/jleechan/projects/agent-orchestrator`: remove after the launchd export evidence worker releases the old source path.
- `/home/jleechan/project_agento/agent-orchestrator` -> `/home/jleechan/project_agento/agent-orchestrator-ts`: retain until `ao-orchestrator.service` is restarted from its updated canonical path. Its unchanged PID proves the move did not interrupt the live daemon.

The Linux Go bridge was removed after verification because no running consumer depended on it.

## Capability gaps and durable follow-ups

- P0 fail-closed PR actions: https://github.com/jleechanorg/agent-orchestrator/issues/14 and bead `jleechan-k4i`.
- Explicit TypeScript YAML to Go SQLite migration: https://github.com/jleechanorg/agent-orchestrator/issues/15 and bead `jleechan-odk`.
- Correct stale tracker-intake status documentation: https://github.com/jleechanorg/agent-orchestrator/issues/16 and bead `jleechan-awc`.
- Reconcile the separate legacy Go fork and Linux daemon: https://github.com/jleechanorg/agent-orchestrator/issues/17 and bead `jleechan-gbz`.

Current-source inspection showed that Go tracker intake is wired; the contrary `docs/STATUS.md` text is stale. The blocking functional gap is PR action integrity: merge and resolve-comments currently report success without confirmed SCM behavior.

## Remaining closeout

1. Finish the real black-box AO recovery evidence in https://github.com/jleechanorg/jleechanclaw/pull/756, including worker-completion observation and the configured fallback harness.
2. Remove the Mac Go compatibility bridge after that worker confirms it no longer holds the old path.
3. Restart the Mac dashboard and Linux TypeScript daemon from canonical paths only during controlled supervisor handoffs, verify health immediately, then remove their bridges.
4. Merge repository-reference PR https://github.com/jleechanorg/agent-orchestrator-ts/pull/757 only after its normal review gates pass. No merge was performed during this cutover.
5. Implement issue 14 before considering any generic `ao` cutover to Go.

Historical roadmap entries, session transcripts, caches, evidence bundles, and archived policy copies intentionally retain their original names for provenance.
