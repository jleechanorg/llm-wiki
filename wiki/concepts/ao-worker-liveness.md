# AO Worker Liveness

**Type**: concept
**Created**: 2026-05-14

## Definition

Agent Orchestrator (AO) workers operate in a turn-based execution model: the orchestrator dispatches a prompt → the worker executes tool calls → the worker returns to idle at the `❯` prompt, waiting for the next orchestrator prompt. Between-turn idle is the expected steady state, NOT an error condition.

## Key Distinctions

| State | Indicator | Action |
|-------|-----------|--------|
| **Active turn** | `[Tool use: ...]` in scrollback | Wait, don't interrupt |
| **Between turns** (healthy) | `❯` prompt, possibly with pre-filled text | Do nothing — it's waiting for orchestrator |
| **Actually stuck** | Stack trace, error, or mid-call silence >10 min | Investigate, possibly kill |
| **Exited** | `tmux list-panes` returns "pane not found" | Confirm work complete |

## Anti-Pattern

Misinterpreting between-turn idle as "frozen" or "stuck" leads to:
- Incorrect kill recommendations
- Unnecessary restart loops
- Loss of worker context (completed work in scrollback)

## Related

- [[hermes-launchd-meta-pattern]] — Liveness ≠ Functionality applies broadly
- Source: `sources/ao-worker-tmux-reading.md`
