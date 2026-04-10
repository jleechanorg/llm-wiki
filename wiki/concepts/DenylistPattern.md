---
title: "Denylist Pattern"
type: concept
tags: [denylist, configuration, github-variables]
sources: []
last_updated: 2026-04-07
---

## Definition
The denylist pattern is a configuration approach using GitHub repository variables to specify PRs or resources that should be excluded from automated operations. It provides a simple mechanism to override default behavior without changing code.

## Implementation
```bash
# Set denylist
gh variable set SKEPTIC_MERGE_DENYLIST -b 'PR1,PR2,PR3' -R owner/repo

# Clear denylist
gh variable delete SKEPTIC_MERGE_DENYLIST -R owner/repo
```

## Advantages
- No code changes required to update
- Atomic operations (merge/close no-ops on removed entries)
- Simple to manage via CLI
- Can be combined with global toggles (SKEPTIC_CRON_AUTO_MERGE)
