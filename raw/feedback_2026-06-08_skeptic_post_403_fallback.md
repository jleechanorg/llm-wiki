---
name: skeptic post 403 fallback to CREATE
description: When patchComment 403s on cross-user comment edit, fall back to createComment — same pattern as 404
metadata:
  type: feedback
---

When posting a Skeptic verdict (or any PR comment) via PATCH-then-CREATE flow, treat both 404 (comment deleted) AND 403 (cross-user edit blocked) as recoverable conditions that fall back to creating a fresh comment. Only rethrow non-{404,403} errors (422 oversized body, 500, network).

**Why:** PR #654 (jleechanorg/agent-orchestrator) had a post step in `packages/cli/src/commands/skeptic/posting.ts:56-70` that only fell back to CREATE on 404. When the existing verdict comment was posted by `jleechan-af` and the current `gh` CLI is authenticated as `jleechan2015`, GitHub returns 403 on cross-user PATCH — the previous code rethrew, the error was suppressed somewhere in exec, and the CLI reported "Done!" while the verdict silently disappeared.

**How to apply:** When implementing PATCH-then-CREATE flows (skeptic verdicts, claim-verifier responses, AO worker comments), mirror the `isGhNotFoundError` + `isGhForbiddenError` pair in `packages/cli/src/commands/skeptic/posting.ts`. Test both fallback paths with mocked 404/403 responses. Rethrow only on truly fatal errors (422 oversized body, 500, network) so upstream retries/failures can do their job.

**Related:** [[project_2026-06-08_skeptic_post_fix_shipped]], [[project_2026-06-07_tilde_systemic]], [[project_2026-06-07_worldai_skeptic_conflation]]
