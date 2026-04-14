---
title: "PR #6269: [antig] Port CR fallback logic to Skeptic Gates in worldarchitect.ai"
type: test-pr
date: 2026-04-14
pr_number: 6269
files_changed: [skeptic-evaluate.sh, green-gate.yml, skeptic-cron.yml, skeptic-gate.yml]
---

## Summary
Ports the CodeRabbit fallback logic to the Skeptic Gates in worldarchitect.ai to fix a PR gating deadlock. Allows Skeptic Gates to pass if a formal `APPROVED` review state is missing but CodeRabbit posts an `[approve]` comment. Unifies approval detection across workflows with resilient error handling.

## Key Changes
- **skeptic-evaluate.sh**: Updated CR approval comment regex from exact line match to "match anywhere" pattern, wrapped pipelines with `set +e -o pipefail` and explicit exit-code handling
- **green-gate.yml**: Added CR fallback logic - checks formal APPROVED review first, then falls back to (status=success AND post-head `[approve]` comment)
- **skeptic-cron.yml**: Same dual-condition fallback logic as green-gate
- **skeptic-gate.yml**: Broader CR signal detection, loosened approve-comment regex

## Diff Snippets
```bash
# skeptic-evaluate.sh - regex change for CR approve comment
-        | jq -rs --arg since "$HEAD_COMMITTED_AT" 'add | [.[] | select((.user.login == "coderabbitai[bot]" or .user.login == "coderabbitai") and .created_at >= $since and (.body | test("(?m)^\\s*\\[approve\\]\\s*$"; "i")))] | sort_by(.created_at) | last | if . then "APPROVED" else "none" end' \
+        | jq -rs --arg since "$HEAD_COMMITTED_AT" 'add | [.[] | select((.user.login == "coderabbitai[bot]" or .user.login == "coderabbitai") and .created_at >= $since and (.body | test("\\[approve\\]"; "i")))] | sort_by(.created_at) | last | if . then "APPROVED" else "none" end' \
```

## Motivation
PR #6266 was blocked because the Skeptic Gate couldn't detect CodeRabbit approval. The fallback logic was already validated in the Antig codebase - this ports the same pattern to worldarchitect.ai to unblock the merge queue.