---
title: "Claude Code Quota Cost Analysis — May 5 2026"
type: source
date: 2026-05-06
tags: [claude-code, quota, cost, hooks, skeptic, tokens]
raw: raw/project_2026-05-06_claude-quota-cost-analysis.md
---

## Summary

Total May 5 spend: **$2,832/day** across 481 sessions.

- Automation (384 sessions, 37%): Skeptic QA $963 · /fake hook $51 · file-justification $35
- Normal work (97 sessions, 63%): AO workers $882 · Interactive $902

## Token cost drivers

| Token type | Cost | % |
|---|---|---|
| input_tokens ($3/MTok) | $1,518 | 54% |
| cache_read ($0.30/MTok) | $718 | 25% |
| cache_creation ($3.75/MTok) | $380 | 13% |
| output_tokens ($15/MTok) | $216 | 8% |

**Counterintuitive**: output is 50× more expensive per token than cache_read, but input volume dominates. Skeptic alone sends 225M input tokens/day.

## Actions (all taken 2026-05-06)

1. `~/.agent-orchestrator.yaml` → `worker-signals-completion: auto: false`
2. `~/.hermes_prod/agent-orchestrator.yaml` → same (was still `auto: true`)
3. `~/.claude/settings.json` → removed `detect_speculation_and_fake_code.sh`, `smart_fake_code_detection.sh`, `post_file_creation_validator.sh`
4. PR [#6822](https://github.com/jleechanorg/worldarchitect.ai/pull/6822) — removes GH Actions cron `*/30 * * * *` from `skeptic-cron.yml`

## Bead

rev-8cubl

## See also

- [[ClaudeCodeHooks]] — hook cost patterns
- [[ClaudeCodeQuotaCost]] — new concept introduced by this learning
