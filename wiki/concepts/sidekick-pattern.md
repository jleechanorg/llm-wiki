---
title: "Sidekick Pattern"
type: concept
tags: [orchestration, sidekick, swarm, durability]
date: 2026-07-07
---

## Definition

The Devin-sidekick pattern: one persistent, restartable background teammate owns a long-running mission, checkpointing state to disk (`STATE.md`) so a fresh session can respawn and resume with zero conversation-context re-derivation. Used for swarm-style multi-agent missions in Claude Code.

## Known gap

Reusing the same teammate `name` to start a new mission before a prior `shutdown_request` is confirmed via `shutdown_approved` can race, producing two concurrent workers on the same mission scratch files. See [[feedback-2026-07-07-sidekick-same-name-respawn-race]].

## Related

- [[feedback-2026-07-07-sidekick-same-name-respawn-race]]
