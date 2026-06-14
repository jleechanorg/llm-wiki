---
title: "Skeptic post fix shipped 2026-06-08 (PR #654)"
type: source
tags: [skeptic, 403, fallback, create-comment, pr-654, agent-orchestrator]
date: 2026-06-08
source_file: raw/project_2026-06-08_skeptic_post_fix_shipped.md
---

## Summary
Subagent a6194e0e16bd939e0 completed the skeptic post fix on 2026-06-08. The bug: packages/cli/src/commands/skeptic/posting.ts:56-70 rethrew 403 errors from cross-user comment PATCH, causing the verdict to silently disappear while the CLI reported 'Done!'. Fix shipped (commit fca0cc322): added isGhForbiddenError() alongside isGhNotFoundError(); 403 now falls back to createComment. TDD: Red (1 failing test) → Green (5/5 posting.test.ts) → 696/696 full suite (no regressions). E2E verified on PR #654 with both idempotent PATCH and fresh CREATE comments carrying all required markers.

## Key Claims
- Bug: 403 on cross-user PATCH (jleechan-af comment, jleechan2015 auth) was rethrown; error suppressed somewhere in exec, CLI reported 'Done!' while verdict disappeared
- Fix: added isGhForbiddenError() alongside isGhNotFoundError(); 403 falls back to createComment (same pattern as 404); other errors (422, 500, network) still rethrow
- TDD: 1 failing test for 403 fallback → 5/5 posting.test.ts pass → 696/696 full suite (no regressions)
- E2E verified on PR #654: comment 4644588084 (idempotent PATCH on existing comment matching SHA 97b51e6ff) + comment 4644642181 (fresh CREATE for new SHA fca0cc322); both have all required markers

## Connections
- [[feedback_2026-06-08_skeptic_post_403_fallback]]
- [[project_2026-06-07_worldai_skeptic_conflation]]
- [[project_2026-06-07_tilde_systemic]]
- [[SkepticPost403Fallback]]
