---
title: "PRs That Expand CI Coverage Will Surface Latent Test Failures"
type: source
tags: [ci, end2end-tests, latent-failures, pr-workflow]
sources: []
last_updated: 2026-05-24
source_file: raw/feedback_2026-05-24_ci_expansion_surfaces_latent_failures.md
---

## Summary
CI-coverage-expansion PRs (adding tests to self-hosted runners, enabling end2end on PRs, widening test-matrix coverage) will surface pre-existing latent failures that were never running in CI. PR #7048's commits adding end2end tests to self-hosted CI shards exposed 9 pre-existing failures — none of which the PR's own production code regressed. Such PRs must budget time to fix those failures in the same PR or a same-day prerequisite PR.

## Key Claims
- PR #7048's CI-inclusion commits (`44cef3e22` and `e7ef154c2`) added end2end tests to self-hosted CI shards. Those tests were never running in CI before, which surfaced 9 pre-existing failures.
- The 9 latent failures (all fixed in-scope): continue_story injector ZFC violation, debug_mode planning_block contract drift, god_mode placeholder leak, cooldown strip refactor delta, level_up scrub gap, etc.
- When proposing a CI-coverage-expansion PR: (1) run newly-included tests locally first to enumerate latent failures, (2) budget the same PR (or a same-day prerequisite PR) for fixing those failures, (3) if out-of-scope, xfail with bead-tracked rationale or revert the CI inclusion commit, (4) don't assume "the new tests will pass because I didn't touch that area".
- Specific test files affected: `test_continue_story_end2end::test_campaign_upgrade_choice_injected`, `test_debug_mode_end2end::test_backend_strips_game_state_fields_when_debug_off`, `test_god_mode_end2end::test_god_mode_returns_god_mode_response_field`, `test_non_streaming_cooldown_strip_end2end::*`, etc.

## Key Quotes
> "When proposing a CI-coverage-expansion PR (adding tests to self-hosted runners, enabling end2end on PRs, widening test-matrix coverage, etc.): Run the newly-included tests **locally first** to enumerate latent failures. Budget the same PR (or a same-day prerequisite PR) for fixing those failures." — feedback_2026-05-24_ci_expansion_surfaces_latent_failures

> "Do not assume 'the new tests will pass because I didn't touch that area'." — feedback_2026-05-24_ci_expansion_surfaces_latent_failures

## Connections
- [[7-Green-Proof-Artifact]] — PR #7048 reached 7-green despite the 9 latent failures
- [[PR-7048-Location-Centralization-Merged]] — the PR that surfaced the latent failures
- [[End2End-Testing-Architecture]] — end2end test patterns
- [[CI-Worktree-Runner-Infra]] — self-hosted runner infra
