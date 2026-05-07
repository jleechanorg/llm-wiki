---
name: Real calibration must validate conservative Gemini token-ratio changes
description: When changing calibrated token ratios, rerun the full real-service calibration envelope because a safer-looking value can fail another edge case.
type: project
bead: rev-8min4
---

# Real calibration must validate conservative Gemini token-ratio changes

After PR #6809 merged, a review note identified that the new local Gemini large-structured token estimator had an underestimation bias on large raw payloads. The merged calibration evidence showed the 1000-scene raw case at local `115,327` vs real `120,618`, a `4.387%` undercount.

The suggested fix was to change `GEMINI_LARGE_STRUCTURED_CHARS_PER_TOKEN` from `3.62` to about `3.45`. Real calibration showed `3.45` was too aggressive: the Firestore compacted campaign `Z9zR8D0qq2gPlhMuHxZt` failed at `5.003%` deviation, exceeding the `5.0%` threshold. The final PR #6812 value `3.455` kept the 1000-scene raw case conservative while keeping the worst case at `4.852%`.

Rule: for calibrated token-budgeting constants, never accept a point-fix value because it fixes the sample that exposed the bias. Re-run the full real-service calibration envelope and choose the narrowest value that satisfies both the intended safety direction and the existing max-deviation threshold.

Evidence: commit `c1e02dfaf10deabacc5a6bd251dc079cfa4d3105`, PR #6812, bundle `/tmp/worldarchitect.ai/fix-gemini-token-estimator-conservative/c1e02dfaf10deabacc5a6bd251dc079cfa4d3105`, hosted gist `https://gist.github.com/jleechan2015/725770c262a76c01907eb5c6a8578199`, focused pytest `26 passed`, Ruff clean, real Gemini calibration `18` HTTP 200 `countTokens` calls.
