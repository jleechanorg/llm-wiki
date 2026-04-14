---
title: "Style Guide Compliance Gate"
type: concept
tags: [CI, visual-testing, evidence]
sources: []
last_updated: 2026-02-23
---

## Definition

A Style Guide Compliance Gate is an automated CI gate that scores visual conformance to a styleguide using computed style token checks, masked perceptual diffs against baselines, and contrast checks — replacing manual screenshot review with objective, repeatable metrics.

## Components

1. **Visual smoke tests**: Dual-theme test runs (`test_smoke_light.py`, `test_smoke_fantasy.py`)
2. **Compliance scorer**: Computes per-screen and per-theme compliance scores
3. **Baseline artifacts**: Stored reference images for diff comparison
4. **Machine-readable report**: `compliance_report.json` output
5. **Human-readable report**: Markdown summary with linked artifacts

## Scoring Dimensions

| Check | What it validates |
|---|---|
| Style token checks | CSS variable values match design tokens |
| Masked perceptual diff | Visual similarity to baseline (dynamic regions masked) |
| Contrast checks | WCAG compliance for text/background contrast |

## CI Integration

- PR fails when score drops below threshold OR critical checks fail
- Baseline refresh requires explicit manual approval (not implicit on test run)
- GitHub Actions workflow blocks merging on gate failure

## Dynamic Region Masking

Story text, timestamps, and account-specific content must be masked before diff comparison to avoid false positives from content-only changes.

## Sources

- BD-styleguide-compliance-gate: initial MVP implementation
