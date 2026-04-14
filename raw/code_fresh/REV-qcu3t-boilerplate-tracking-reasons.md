---
id: REV-qcu3t
title: "[Bug] copilot tracking reasons use boilerplate instead of preserving original"
description: |
  Despite Key Rule #4 explicitly banning boilerplate "Previously addressed in an earlier copilot run",
  the tracking table still has 17 rows using this phrase.

  Root cause: Step 2b (Filter Previously Resolved) was supposed to preserve original tracking reasons
  from the PR description, but used pre-existing responses.json with boilerplate instead of
  fetching original reasons from the tracking table.
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
- Added parse_existing_tracking_table() to read original reasons from PR description
- Replaced boilerplate fallback with descriptive message "[Original tracking reason not found...]"
- Boilerplate "Previously addressed in an earlier copilot run" no longer used

# Investigation

Step 2b of copilot.md says:
> 3. **Preserve their original tracking_reason** - store the reason text from the existing table row.
> Do NOT replace it with boilerplate like "Previously addressed in an earlier copilot run"

But the workflow used existing responses.json that already had boilerplate reasons.

# Fix Required

1. Modify Step 2b to parse existing tracking table from PR description
2. Store original tracking_reason for each Fixed/Acknowledged entry
3. When building responses.json for new run, merge with original reasons (not boilerplate)

# Solution

In `commentreply.py`, modify the tracking table parsing to:
1. Fetch PR description via `gh pr view --json body`
2. Extract rows between `COPILOT_TRACKING_START` and `COPILOT_TRACKING_END` markers
3. Parse each row: extract Comment ID, Status, and the Reason text
4. When building responses.json, use the parsed Reason as `tracking_reason` for carried-forward entries
5. Never use boilerplate - always preserve what was in the original tracking table

The key fix: **Read from PR description tracking table, not from old responses.json**
