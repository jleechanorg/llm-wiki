---
title: "Evidence Skeptical Review"
type: concept
tags: [testing, task-pattern, automation]
sources: []
last_updated: 2026-04-13
---

## Description

The evidence skeptical review pattern applies skepticism when reviewing test evidence, avoiding overstated pass claims. Evidence review should validate consistency between logs and JSON artifacts, not just accept the presence of evidence.

## Why It Matters

When stabilizing remote-preview reruns via iterative test loops, evidence must be scrutinized. A test that passes evidence review but has inconsistent logs vs JSON artifacts is a false positive. The pattern emphasizes validating evidence bundle consistency.

## Key Technical Details

- **Validation**: Check consistency between logs and JSON artifacts
- **Scope**: `testing_mcp/test_openclaw_gateway_url_preview.py`, `testing_ui/test_openclaw_gcp_settings.py`
- **Key insight**: Evidence review should be skeptical and avoid overstated pass claims

## Related Beads

- BD-pr5879-rerun-stability-loop
