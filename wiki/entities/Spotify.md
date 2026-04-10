---
title: "Spotify"
type: entity
tags: ["company", "engineering", "orchestration"]
sources: ["orchestration-architecture-research"]
last_updated: 2026-04-07
---

Engineering team behind the Honk System for AI coding agents. Production lessons include "reduced flexibility increases predictability" — agents heavily constrained to read codebase, edit files, execute verifiers. Push ops, user comms, and prompt authoring handled by surrounding infrastructure. Implemented LLM-as-Judge pattern where secondary LLM evaluates diffs before merge, vetoing ~25% of sessions.

## See Also
- [[Orchestration Architecture Research]] — Honk System detailed in research
- [[LLM-as-Judge Pattern]] — concept page for the pattern Spotify uses
