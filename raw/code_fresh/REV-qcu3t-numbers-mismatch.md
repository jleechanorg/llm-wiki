---
id: REV-qcu3t-numbers
title: "[Bug] copilot responses.json not single source of truth - numbers mismatch"
description: |
  Three different numbers from three different sources:
  - Consolidated reply: 16 FIXED, 24 ACKNOWLEDGED (40 issues)
  - Tracking table footer: 33 Fixed, 19 Ignored (52 entries)
  - Summary: 40 responses, 74/74 coverage

  Violates Key Rule #7: "The consolidated reply metrics AND the tracking table MUST both derive
  from responses.json"
status: resolved
priority: 2
issue_type: bug
owner: jleechan@gmail.com
created_by: claude
labels: [copilot, workflow-bug]
resolved: 2026-02-17
---

# Resolution

Fixed in PR #5597:
- Added compute_metrics() function that handles both single-issue and multi-issue responses
- Both tracking table and consolidated reply now use compute_metrics for ALL counts (response types AND categories)
- Single source of truth for all metrics

# Investigation

- Consolidated reply counts unique issues (40)
- Tracking table counts all comment entries including duplicates from multiple reviewers (52)

# Fix Required

1. responses.json should be authoritative for both outputs
2. Tracking table should derive count directly from responses.json
3. Consolidated reply should derive metrics from responses.json
4. Ensure deduplication logic is consistent across both outputs

# Solution

In `commentreply.py`, create a single function that computes all metrics:
```python
def compute_metrics(responses):
    fixed = sum(1 for r in responses if r.get('response') == 'FIXED')
    acknowledged = sum(1 for r in responses if r.get('response') == 'ACKNOWLEDGED')
    deferred = sum(1 for r in responses if r.get('response') == 'DEFERRED')
    ignored = sum(1 for r in responses if r.get('response') == 'IGNORED')
    return {
        'total': len(responses),
        'fixed': fixed,
        'acknowledged': acknowledged,
        'deferred': deferred,
        'ignored': ignored
    }
```

Then use this same function for both:
- Generating tracking table footer
- Generating consolidated reply metrics

Key fix: **DRY - compute metrics once, use everywhere**
