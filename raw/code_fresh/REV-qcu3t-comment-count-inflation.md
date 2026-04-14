---
id: REV-qcu3t-counting
title: "[Bug] copilot comment count inflation - inconsistent across surfaces"
description: |
  Comment counting is inconsistent:
  - API: 84 total comments
  - Consolidated: 52 analyzed, 40 distinct issues
  - Tracking: 52 entries
  - Coverage: 74 requires_response (because already_replied is 84)

  The counting logic varies across workflow components.
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
- commentcheck.md now reads responses.json for standardized counts
- Added standardized count stages: Total Issues, Fixed, Acknowled Not Done
-ged, Deferred, All copilot files now use /tmp/{repo}/{branch}/copilot/ directory

# Investigation

Different parts of the workflow count differently:
- API returns raw comments (84)
- commentfetch marks requires_response based on deduplication logic
- coverage check uses requires_response vs already_replied

# Fix Required

1. Standardize comment counting in commentfetch module
2. Document expected count at each stage
3. Add validation that counts are consistent

# Solution

Standardize the counting in `commentfetch.py`:

```python
# All raw API comments
ALL_COMMENTS = total from API

# Deduplicated (unique by comment_id)
UNIQUE_COMMENTS = len(set(c['id'] for c in comments))

# Requires response (unique minus [AI responder])
REQUIRES_RESPONSE = unique - ai_responder_count

# Already replied (comments that have our response)
ALREADY_REPLIED = comments where already_replied=true
```

Key fix: **Single source of truth for counts - store in comments.json metadata**
