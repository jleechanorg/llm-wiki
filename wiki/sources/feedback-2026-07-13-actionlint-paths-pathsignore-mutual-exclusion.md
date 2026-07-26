---
title: "GH Actions paths + paths-ignore mutual exclusion workaround"
type: source
tags: [github-actions, actionlint, workflow, paths-filter, worldarchitect-ai]
date: 2026-07-13
source_file: feedback_2026-07-13_actionlint_paths_pathsignore_mutual_exclusion.md
---

## Summary

actionlint fails on `paths:` + `paths-ignore:` on the same event — they're mutually exclusive. Workaround: single `paths:` block with `!pattern` negations. PRs #8367 (presubmit) and #8370 (test.yml) both hit this bug; same fix applied to both.

## Key Claims

- actionlint explicitly says: "use '!' to negate patterns" — use that syntax verbatim.
- CodeRabbit correctly identified the bug on PR #8367 but was dismissed as "stylistic" — it was actually a real actionlint failure.
- The fix is small (3-6 line change) but easy to miss if not aware of the mutual-exclusion rule.
- The fix to PR #8367 came after the workflow-discipline lint failed; should have been caught at PR authoring time.

## Key Quotes

> "Both 'paths' and 'paths-ignore' filters cannot be used for the same event 'pull_request' (note: use '!' to negate patterns)"

## Connections

- [[WorldArchitectAI]] — PRs #8367, #8370 in this repo
- [[ActionlintTool]] — the validator that caught the bug
