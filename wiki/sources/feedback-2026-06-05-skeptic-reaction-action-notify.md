---
title: "Skeptic Reaction Action Must Be `skeptic-review`, not `notify`"
type: source
tags: ["skeptic", "ao-config", "reactions", "silent-failure", "feedback"]
date: 2026-06-05
source_file: feedback_2026-06-05_skeptic_reaction_action_notify.md
---

## Summary
`worker-signals-completion` reaction action must be `action: skeptic-review`, not `action: notify`. `notify` silently discards the skeptic trigger; the `skepticModel`/`skepticPostComment`/`skepticPrompt` fields are only read by `skeptic-review` case.

## Key Claims
- `action: notify` fires on every PR state transition but only calls `notifyHuman()`
- Invisible because: manual `ao skeptic verify` still worked, no error logged, lifecycle-worker log showed reaction fired correctly
- Diagnostic chain: grep action + scm config; only check logs if both are correct

## Key Quotes
> When skeptic is not auto-running on new PRs, check `reactions.worker-signals-completion.action` FIRST

## Connections
- [[SkepticReview]] — concept
- [[AgentOrchestrator]] — config
