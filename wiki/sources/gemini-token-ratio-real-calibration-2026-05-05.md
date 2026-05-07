---
title: "Real calibration must validate conservative Gemini token-ratio changes"
type: source
date: 2026-05-05
bead: rev-8min4
source: raw/project_2026-05-05_gemini_token_ratio_real_calibration.md
---

# Real calibration must validate conservative Gemini token-ratio changes

## Summary

PR #6812 fixed a real follow-up issue from PR #6809: the large structured Gemini token estimator undercounted the 1000-scene raw calibration sample. The important lesson is that a proposed conservative ratio must be validated against the entire real-service calibration suite, not just the row that exposed the bias.

## Key Facts

- PR #6809 merged the calibrated local Gemini estimator.
- The large raw 1000-scene sample undercounted at local `115,327` vs real `120,618`.
- A suggested ratio of `3.45` made that row conservative but failed the Firestore compacted row at `5.003%`.
- Final ratio `3.455` kept the 1000-scene raw row conservative and kept max deviation at `4.852%`.
- PR #6812 commit: `c1e02dfaf10deabacc5a6bd251dc079cfa4d3105`.
- Evidence gist: https://gist.github.com/jleechan2015/725770c262a76c01907eb5c6a8578199

## Reusable Rule

For calibrated constants that replace provider calls, verify candidate values using the full real-service calibration envelope. A value that fixes one exposed bias can break another representative case.

## Links

- [[CalibrationBiasVerification]]
- [[TokenUtils]]
- [[GeminiProvider]]
