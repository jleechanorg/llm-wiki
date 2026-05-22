"title: "Lifecycle Reactions"
type: concept
tags: ["orchestration", "lifecycle", "events"]
sources: ["smartclaw-ao-exhaustive-audit-findings-file-level-sweep.md"]
last_updated: 2026-04-07
---

System for handling lifecycle events and reactions in orchestration.

## AO Implementation
- `packages/core/src/lifecycle-manager.ts`

## Current Stack
Lifecycle logic exists in `jleechanclaw/src/orchestration/lifecycle_reactions.py` but narrower on parity behaviors.

## Gap Closure
Bead ORCH-twf: Lifecycle reaction parity hardening (retry/escalation/all-complete)

## Injection mechanism (send-to-agent)

When an AO session is `agent-stuck` or `agent-needs-input`, lifecycle-manager calls
`sessionManager.send()` → `runtimePlugin.sendMessage()` → `tmux send-keys` to inject
the `reactions:` message template into the Claude pane. This happens every poll cycle
(75 s default). These injected messages appear in Claude as "Stop hook feedback:" text
even when no stop hook is active — the messages come from AO, not from a Claude hook.

To silence: `ao stop <project>` or `ao session kill <sessionId>` before a manual session.

See: `sources/ao-ralph-lifecycle-worker-respawn-2026-05-21.md` (2026-05-21), bead rev-3ey45.

## Connections
- [[AgentOrchestrator]] — reference
- [[jleechanclaw]] — existing implementation
- [[Ralph-Loop-Method]] — do not confuse AO lifecycle-worker ralph with ralph-wiggum plugin
