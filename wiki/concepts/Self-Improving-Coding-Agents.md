---
title: "Self-Improving Coding Agents"
type: concept
tags: ["agents", "self-improvement", "coding", "llm"]
sources: ["orchestration-architecture-research"]
last_updated: 2026-04-07
---

LLM coding agents that can autonomously edit themselves and improve performance on benchmark tasks. Key patterns: loop halts on red flags (failed tests, type errors, linting failures) and re-prompts; for human feedback, open PRs rather than auto-merge; developers update AGENTS.md with corrections for persistent preference records.

## Production Lessons
- **Context bloat kills performance** — summarize older logs, archive obsolete guidance
- **Monitoring essential** — tail progress logs, inspect diffs, set hard stops
- **Safeguards**: feature branches, whitelisted operations, sandboxed environments, emergency stops
- Use different models for different roles (planning vs coding)

## See Also
- [[Nested Agent Loops]]
- [[Ralph Loop Method]]
- [[Context Bloat]]
- [[Planner-Worker Hierarchies]]
- [[Orchestration Architecture Research]]
- [[AutoResearchExperiment]] — full 18-cycle autonomous meta-research experiment combining self-critique loops, canonical scoring, and product taste evaluation
- [[SelfCritiqueVerificationLoop]] — 3-iteration-cap verification loop used in AutoResearchExperiment Phase 2
