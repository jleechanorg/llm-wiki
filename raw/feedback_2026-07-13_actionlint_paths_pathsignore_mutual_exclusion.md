---
name: gh-actions-paths-paths-ignore-mutual-exclusion-workaround
description: "actionlint blocks paths: + paths-ignore: on the same event — use !pattern negation inside a single positive paths: block. PRs #8367 and #8370 both hit this; fixed in the same commit by switching to !pattern syntax."
metadata: 
  node_type: memory
  type: feedback
  bead: rev-6vf3c
  originSessionId: 6d6509e7-ea7b-44a2-8aa5-e0699e99ba2c
---

# GH Actions paths + paths-ignore mutual exclusion — use !pattern negation

## Context
- 2026-07-13 round 3: PR #8367 (presubmit positive paths filter) initially combined BOTH `paths:` and `paths-ignore:` blocks on the same `pull_request:` trigger
- actionlint failed with: `both "paths" and "paths-ignore" filters cannot be used for the same event "pull_request" (note: use '!' to negate patterns)`
- 2026-07-13 round 5: PR #8370 (test.yml positive paths filter) hit the same bug — driver didn't learn from the #8367 fix
- CodeRabbit review (the original author dismissed it) actually caught the right issue

## The bug pattern
```yaml
# WRONG — actionlint fails
on:
  pull_request:
    paths:
      - 'mvp_site/**'
      - 'tests/**'
    paths-ignore:
      - 'roadmap/**'
      - '.github/ISSUE_TEMPLATE/**'
```

## The fix
```yaml
# RIGHT — single paths: block with !pattern negations
on:
  pull_request:
    paths:
      - 'mvp_site/**'
      - 'tests/**'
      - '!roadmap/**'
      - '!.github/ISSUE_TEMPLATE/**'
```

## Why this happens
GitHub Actions does NOT allow `paths:` AND `paths-ignore:` on the same event — they're mutually exclusive. The ONLY workaround is to combine into a single positive `paths:` block and prefix the items you want to exclude with `!`.

## Rule for future trigger filter work
- **Always use a single `paths:` block** with `!pattern` negations for items to exclude.
- **NEVER combine `paths:` + `paths-ignore:` on the same event** — actionlint will fail at parse time.
- **actionlint's error message says it explicitly**: "use '!' to negate patterns" — copy that syntax verbatim.

## References
- PRs: #8367 (presubmit), #8370 (test.yml) — both had this bug, both fixed in follow-up commits
- Commit fixes: `debb99eb58` (PR #8367), `c4db0cbb2c` (PR #8370)
- CodeRabbit review (the user dismissed it as "stylistic" — actually CORRECT)
- Round 4 Lane D research: full per-job dorny/paths-filter is the larger follow-up if simple paths filter is insufficient

## Verification
- actionlint: passes after fix
- `python3 -c "import yaml; yaml.safe_load(...)"`: passes
- Triggers fire correctly per `!pattern` semantics
- No regression on previously-working events
