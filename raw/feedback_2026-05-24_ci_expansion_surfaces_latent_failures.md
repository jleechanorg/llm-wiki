---
name: PRs that expand CI coverage will surface latent test failures
description: This PR's CI-inclusion commits exposed 9 pre-existing test failures that were latent on main; pattern means CI-expansion PRs must budget for fixing those failures too
type: feedback
bead: rev-igs3c
---

PR #7048's own commits `44cef3e22 "ci: include end2end in core-mvp directory-based test runs"`
and `e7ef154c2 "ci: run mvp end2end tests in self-hosted shards"` added end2end
tests to self-hosted CI shards. Those tests were never running in CI before.
This surfaced 9 pre-existing failures (continue_story injector ZFC violation,
debug_mode planning_block contract drift, god_mode placeholder leak, cooldown
strip refactor delta, level_up scrub gap, etc.) — none of which the PR's own
production code regressed.

**How to apply:** When proposing a CI-coverage-expansion PR (adding tests to
self-hosted runners, enabling end2end on PRs, widening test-matrix coverage,
etc.):
1. Run the newly-included tests **locally first** to enumerate latent failures.
2. Budget the same PR (or a same-day prerequisite PR) for fixing those failures.
3. If failures are out-of-scope, either xfail with bead-tracked rationale or
   revert the CI inclusion commit until they're addressed separately.
4. Do not assume "the new tests will pass because I didn't touch that area".

**Specific failures fixed in this PR's scope:**
- `test_continue_story_end2end::test_campaign_upgrade_choice_injected`
  (deleted injector + renamed test)
- `test_debug_mode_end2end::test_backend_strips_game_state_fields_when_debug_off`
  (updated seed for post-PR-6958 dict planning_block contract)
- `test_god_mode_end2end::test_god_mode_returns_god_mode_response_field`
  (added is_god_mode kwarg + placeholder-skip)
- `test_non_streaming_cooldown_strip_end2end::test_non_streaming_cooldown_calls_normalize_lw_for_persist`
  (wired centralized normalize_lw_for_persist call into world_logic)
- `test_non_streaming_cooldown_strip_end2end::test_non_streaming_cooldown_strip_tracks_canonical_lw_field_list`
  (replaced hardcoded LW tuple with live module attribute lookup)
- `test_continue_story_end2end::test_level_up_modal_scrubs_character_creation_finish_choices`
  (extended scrub predicate to include _CHARACTER_CREATION_EXIT_CHOICES)

Related: [[7green-proof-artifact]]
