---
title: "Documentation as Infrastructure"
type: concept
tags: ["documentation", "infrastructure", "claude", "agents"]
sources: ["harness-engineering-philosophy"]
last_updated: 2026-04-07
---

The principle that CLAUDE.md, AGENTS.md, and SOUL.md are not documentation but infrastructure — they are read by agents on every turn and directly control agent behavior.

## Key Quote
> "From the agent's perspective, anything it can't access in-context doesn't exist."

## Implication
These files must be treated with the same rigor as production config. Changes take effect immediately because the repo root IS ~/.openclaw/.

## Related Artifacts
- SOUL.md — agent personality, goals, decision-making rules
- TOOLS.md — tool allow/deny list and usage policy
- CLAUDE.md — project rules, coding style, safety rails
- AGENTS.md — agent-specific guidelines and conventions

## Related Concepts
- [[Harness Engineering]] — overall discipline
- [[Agent Environment]] — layer 1 of harness
