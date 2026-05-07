---
title: "Evidence Skeptical Review"
type: concept
tags: [testing, task-pattern, automation]
sources: [pr-review-live-head-verdict-discipline-2026-05-07]
last_updated: 2026-05-07
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
- rev-awmxd

## 2026-05-07 Update — Live-Head PR Review

When reviewing a PR handoff, skeptical evidence review includes live GitHub
state, not only bundle internals. Verify the current `headRefOid`, bundle
`git_head`, post-bundle runtime deltas, Green Gate logs, and PR body evidence
text before answering whether issues are fixed. Report serious code/product
blockers separately from strict green process gaps.
