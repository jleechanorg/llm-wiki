---
title: "Mobile Submit Blur Race and Dynamic CI Date Fixtures"
type: source
tags: [frontend, mobile, ci, fixtures, testing, beads]
date: 2026-09-10
source_file: raw/feedback_2026-09-10_mobile_submit_blur_race_and_dynamic_ci_fixtures.md
---

## Summary
Documents two critical engineering resolutions from PR #9762: (1) preventing mobile composer choices from re-expanding over streaming narrative by guarding onBlur with submit pending and input disabled states, and (2) preventing CI duration fixture test failures caused by static date expiration thresholds across calendar rollovers.

## Key Claims
- Disabling the composer textarea upon form submit triggers a synchronous blur event in browsers that can prematurely restore expanded choices if not guarded.
- Guarding onBlur with `!submitPending && !userInput.disabled` and clearing `collapsedByThisFocus` on actionable submit resolves the race.
- Hardcoded test date fixtures in tests enforcing age limits (`MAX_INPUT_AGE_DAYS = 14`) flake after 14 days; computing fixture dates dynamically relative to UTC now is mandatory.

## Connections
- [[worldarchitect.ai]] — Core web application frontend and CI pipeline.
- [[mobile-ux]] — Mobile composer behavior and focus collapse mechanics.
- [[ci-reliability]] — Dynamic test fixtures and avoiding brittle documentation-string assertions.
