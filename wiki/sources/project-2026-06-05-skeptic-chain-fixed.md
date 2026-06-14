---
title: "Skeptic Chain agent-orchestrator Fixed (2026-06-05)"
type: source
tags: ["skeptic", "agent-orchestrator", "ao-config", "chain-fix"]
date: 2026-06-05
source_file: project_2026-06-05_skeptic_chain_fixed.md
---

## Summary
Skeptic chain for `agent-orchestrator` was silently broken. Fixed via two config changes: wrong reaction action (notify → skeptic-review) and missing SCM config.

## Key Claims
- Bug 1: `reactions.worker-signals-completion.action` was `notify` (only calls notifyHuman); fixed to `skeptic-review` to read skepticModel/skepticPostComment/skepticPrompt
- Bug 2: `projects.agent-orchestrator` had no `scm` stanza; `skeptic-cron-local.ts:153` returns silently with no PRs evaluated
- Both must be present for auto-skeptic to work; missing either causes silent failure

## Key Quotes
> if either is missing/wrong, skeptic silently does nothing — no error, no log entry

## Connections
- [[SkepticReview]] — concept page
- [[AgentOrchestrator]] — config
