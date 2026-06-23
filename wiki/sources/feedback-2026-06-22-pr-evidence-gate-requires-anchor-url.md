---
title: "PR evidence gate requires anchor URL; gh pr edit body quoting wipes body"
type: source
tags: [feedback, worldarchitect, ci-gate, green-gate, pr-description, gh-cli, pr-7815]
date: 2026-06-22
source_file: raw/feedback_2026-06-22_pr_evidence_gate_requires_anchor_url.md
---

## Summary
WorldArchitect Green Gate GATE-6 requires a real media/gist/loom/attachment URL in the PR body — plain "N/A — no UI" text fails even when the change is test-infra. Companion gotcha: `gh pr edit --body "$()"` silently wipes a long body to ~100 chars; use `--body-file` instead. Both surfaced while driving PR #7815 (Mobile Auth Same-Origin Regression test timeout fix) to 7-green.

## Key Claims
- **GATE-6** (`green-gate.yml:451`) greps the PR body + comments for: `https?://[^ ]*\.(mp4|gif|cast)` OR `gist.github.com/` OR `asciinema.org/a/` OR `loom.com/share/` OR `user-attachments.githubusercontent.com/`
- The "EVIDENCE_REQUIRED" check fires when the PR touches `testing_(mcp|ui)/|mvp_site/|deploy.sh|.github/workflows/evidence-gate.yml`
- A run URL like `https://github.com/.../actions/runs/27992975784` does **NOT** match any of those patterns → gate fails even when the test passed
- **GATE-6b** runs `.github/scripts/pr_description_gate.py` which requires each evidence section to contain a real URL or a backticked code block of ≥80 chars (`_section_has_anchor` at line 266, anchor requirement at lines 475-496)
- `## Non-Unit Test Evidence` always requires an anchor; `## Real LLM Evidence` only requires one if `touches_prompts` is true
- For test-infra PRs (`testing_ui/**` or `testing_mcp/**`): add a gist with the test pass output and link it in BOTH the relevant `## *Test Evidence` section AND a trailing `## Evidence` link line
- For backend PRs: link a `/end2end-testing` payload or a raw LLM HTTP response in `## Non-Unit Test Evidence`
- Never rely on `## Real LLM Evidence: N/A` to pass on its own unless the PR really doesn't touch `mvp_site/prompts/**` — the gate still wants a URL/code block in the other two evidence sections

## Key Quotes
> "Symptom: GATE-6b reports ~5 sections as 'section header missing' simultaneously." — observed in PR #7815 cycle
> "Fix: write the new body to a temp file and use `gh pr edit --body-file /tmp/body.md`." — verified

## Connections
- [[GATE6bDescriptionGate]] — same gate family
- [[SelfHostedRunnerInfraFlakeVsRealFailure]] — same PR cycle
- [PR #7815](https://github.com/jleechanorg/worldarchitect.ai/pull/7815) (merged 2026-06-23T02:21:20Z) — fix shipped with a public gist at `https://gist.github.com/jleechan2015/becd90fd7afe670d16b9f80c95df00d3`
- Gate logic: `green-gate.yml:451` + `pr_description_gate.py:266` + `:475-496`
- Bead: rev-m5obm
