---
title: "Calibration Bias Verification"
type: concept
tags: [calibration, evidence, token-budgeting, real-service-verification]
sources: [gemini-token-ratio-real-calibration-2026-05-05]
last_updated: 2026-05-05
---

# Calibration Bias Verification

Calibration bias verification is the practice of validating a proposed estimator constant against the full representative calibration suite, not only the sample that exposed the bias.

## Rule

When changing a calibrated local estimator:

1. Identify whether the estimator should bias conservative or permissive.
2. Test the proposed value against every representative sample.
3. Reject values that fix one row but violate another threshold.
4. Choose the narrowest value that satisfies the intended bias direction and max-deviation envelope.
5. Record raw calibration rows, real service call counts, commit SHA, and checksums.

## Example

For the Gemini large structured token estimator, `3.45` fixed the PR #6809 1000-scene raw undercount but failed the Firestore compacted case at `5.003%`. The final `3.455` ratio kept the raw case conservative and kept max deviation at `4.852%`.

## Related

- [[TokenUtils]]
- [[GeminiProvider]]
- [[HarnessEvidenceRules]]
