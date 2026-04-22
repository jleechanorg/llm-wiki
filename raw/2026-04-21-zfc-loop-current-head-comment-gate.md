# ZFC Loop Current-Head Comment Gate — 2026-04-21

## Summary

The level-up ZFC loop supervision hit a concrete failure on PR `#6431`: the normal GitHub check surface looked green, but a real-E2E smoke failure comment still existed on the PR head SHA. The worker lane did not reconcile that contradiction before disappearing. The supervision rule must therefore be: current-head `/smoke`, `/er`, and bot-failure comments block worker parking and must be reconciled before a lane is considered done.

## Key claims

- Green checks and mergeability are insufficient when current-head issue comments still report gate failures.
- PR `#6431` had a real smoke failure at comment `4291382771` tied to head SHA `c1a865d68c38aef2b02a252f8d4bfb7c0fefedcd`.
- A loop that counts such a lane as parked/done is overstating progress.
- Worker accounting must use current-head comment-gate truth plus tmux evidence, not only AO inventory or check-rollup summaries.

## Operational consequence

The loop should fail closed: if the latest `/smoke`, `/er`, or bot-generated failure comment names the current PR head SHA, the owning worker may not park or be counted as complete until the failure is fixed, rebutted with proof, or superseded by a newer successful run.
