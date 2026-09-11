---
name: Mobile Submit Blur Race and Dynamic CI Date Fixtures
description: Prevent mobile input focus collapse blur races by checking submit state and disabled flag, and use dynamic UTC dates in CI duration fixtures
type: feedback
bead: rev-sbvtx
---

# Mobile Submit Blur Race and Dynamic CI Date Fixtures

## Context
During PR #9762 (branch `fix/mobile-planning-block-submit-reexpand`), users reported in Slack thread 1788752311.570149 (video F0BV7CVH883) that after manually expanding the planning block and typing into the composer textarea on mobile, submitting a turn caused the planning choices to immediately re-expand over the incoming streaming narrative.

Additionally, after pushing the initial fix, CI workflows `Directory tests (scripts)` and `Directory tests (core-tests)` unexpectedly failed on `test_ci_duration_observations.py` and `test_ci_test_duration_sharding.py` due to static date fixtures `2026-08-24` crossing the `MAX_INPUT_AGE_DAYS = 14` threshold upon UTC calendar rollover to `2026-09-08`.

## Technical Details

### 1. Mobile Submit Blur Race
In `mvp_site/frontend_v1/app.js`:
- Disabling the textarea (`userInputEl.disabled = true`) on submission fires a synchronous `blur` event in modern browsers.
- If `onBlur` unconditionally clears focus state or restores prior expansion when `collapsedByThisFocus` is true, it re-expands choices right as the LLM stream begins.
- Solution:
  - Guard `onBlur`: only restore prior expansion if `!submitPending && !userInput.disabled`.
  - In form `submit` listener: reset `collapsedByThisFocus = false` on actionable submissions before disabling `userInputEl`.
  - In `submitBtn`: wire deferred restoration (`restoreIfBlurredWithoutSubmit`) on `pointerup` and `pointercancel` with `setTimeout(0)` so empty submits or cancelled taps do not get permanently stuck collapsed.

### 2. Dynamic CI Date Fixtures
- Tests with expiration thresholds (e.g. `MAX_INPUT_AGE_DAYS = 14`) that use hardcoded date strings (e.g. `"2026-08-24"`) will inevitably fail when calendar time advances past `14` days from the test authoring date.
- Solution: Compute dates dynamically relative to `dt.datetime.now(dt.UTC).date()` in both production helpers (`scripts/ci_duration_observations.py`) and test fixtures (`tests/scripts/test_ci_duration_observations.py`, `tests/test_ci_test_duration_sharding.py`).

### 3. Brittle Documentation Assertions
- Unit tests asserting literal header strings or exact section titles in markdown documentation (e.g. `test_agents_md_documents_no_campaign_hardcoding`) cause spurious CI failures during documentation refactoring. Functional behavioral invariant tests should test the actual code paths rather than markdown text.

## Verification
- Headless Chromium Playwright test (`testing_ui/test_mobile_planning_block_submit_collapse.py`): 10/10 PASS across mobile viewport 375x812.
- Node unit tests (`mvp_site/frontend_v1/tests/submit_expand_scroll_bugs.test.js`): 12/12 PASS.
- Full CI suite: all required checks passed green.
- PR #9762 merged into main as commit `719cd96efa8a1c1a4ee47f8df56b5bb5a50f26b6`.
