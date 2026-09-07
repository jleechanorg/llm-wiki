---
title: "Fable missing from Claude Code /model picker is an upstream bug"
type: source
tags: [claude-code, model-picker, fable, upstream-bug]
date: 2026-09-06
source_file: raw/feedback_2026-09-06_fable_model_picker_upstream_bug.md
---

## Summary
Claude Code v2.1.259's interactive `/model` picker never listed `claude-fable-5-1`
even though `~/.claude/settings.json` had a syntactically correct `modelPicker.options`
entry for it and the model is real and fully entitled. Direct testing found the
picker only offers the fixed GA lineup plus whatever model the session was launched
with — `claude --model fable` works immediately, but `modelPicker.options` doesn't
inject rows for non-active models in this build. Confirmed as a known, unresolved
upstream defect via `gh api` against 8 real anthropics/claude-code GitHub issues.

## Key Claims
- `modelPicker.options` syntax was correct; `claude-fable-5-1` is a real,
  fully-registered catalog model (confirmed via binary `strings` search: Bedrock
  ids, Vertex region, pricing tier all present).
- Fresh tmux session reproduction ruled out session-cache staleness.
- `claude --model claude-fable-5-1` works immediately and the picker THEN lists
  it fully inside that session — proving the picker's list = GA lineup + launch-time
  active model, not `modelPicker.options` contents.
- 8 GitHub issues verified live via `gh api` (not WebSearch-summary text) confirm
  the same disconnect across different users, OSes, and Claude Code versions.

## Key Quotes
> "the server accepts Fable 5 requests, but the picker's client-side availability
> flag still reports it as disabled" — anthropics/claude-code#73423

> "My teammates do not have this problem and can choose fable" — anthropics/claude-code#73333
> (proves account/session-flag specificity, not a universal client bug)

> "When this file is manually edited to `allowed: true`, Claude Code reverts it
> back to `false` on restart — confirming it is server-controlled and cannot be
> overridden client-side." — anthropics/claude-code#66827

## Connections
- [[ClaudeCodeModelPickerEntitlementGap]] — the general pattern this instance belongs to
- [[VerifyUpstreamBugClaimsViaLiveAPI]] — the verification method used (`gh api` over WebSearch summary)
