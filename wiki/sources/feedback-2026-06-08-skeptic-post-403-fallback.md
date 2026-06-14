---
title: "Skeptic post 403 fallback to CREATE"
type: source
tags: [skeptic, 403, fallback, patch-then-create, agent-orchestrator]
date: 2026-06-08
source_file: raw/feedback_2026-06-08_skeptic_post_403_fallback.md
---

## Summary
When posting a Skeptic verdict (or any PR comment) via PATCH-then-CREATE flow, treat both 404 (comment deleted) AND 403 (cross-user edit blocked) as recoverable conditions that fall back to creating a fresh comment. Only rethrow non-{404,403} errors (422 oversized body, 500, network). PR #654 (agent-orchestrator) had the post step in packages/cli/src/commands/skeptic/posting.ts:56-70 that only fell back to CREATE on 404; when existing verdict was posted by jleechan-af and current gh CLI is jleechan2015, GitHub returns 403 on cross-user PATCH — verdict silently disappeared.

## Key Claims
- PATCH-then-CREATE flows must treat 404 AND 403 as recoverable fallback conditions
- Only rethrow non-{404,403} errors (422 oversized body, 500, network) so upstream retries/failures can do their job
- Mirror the isGhNotFoundError + isGhForbiddenError pair from packages/cli/src/commands/skeptic/posting.ts in any PATCH-then-CREATE implementation (skeptic verdicts, claim-verifier responses, AO worker comments)

## Connections
- [[project_2026-06-08_skeptic_post_fix_shipped]]
- [[project_2026-06-07_tilde_systemic]]
- [[project_2026-06-07_worldai_skeptic_conflation]]
- [[PatchThenCreateFallback]]
