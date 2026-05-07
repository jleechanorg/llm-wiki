---
name: Claude Code quota cost analysis — May 5 2026
description: $2,832/day total; automation 37% ($1,049), normal work 63% ($1,783); skeptic was #1 driver at $963/day; all 3 disabled
type: project
bead: rev-8cubl
---

## Finding

Claude Code weekly quota hit 40% in one day (2026-05-05). Analysis of all 481 sessions with May 5 API activity revealed a $2,832/day spend split 37% automation / 63% normal work.

## Cost breakdown by category

| Category | Sessions | Est Cost | Avg/session |
|---|---|---|---|
| (A) Skeptic QA auto-reaction | 211 | **$963** | $4.56 |
| (A) /fake hook | 57 | $51 | $0.89 |
| (A) file-justification hook | 116 | $35 | $0.30 |
| **Automation subtotal** | 384 | **$1,049** | |
| (B) AO workers (PR work) | 9 | $882 | $97.97 |
| (B) Interactive user sessions | 88 | $902 | $10.25 |
| **Normal work subtotal** | 97 | **$1,783** | |
| **GRAND TOTAL** | 481 | **$2,832** | |

## Token type cost breakdown (grand total)

| Token type | Rate | Volume | Cost | % |
|---|---|---|---|---|
| input_tokens | $3/MTok | 505.9M | $1,518 | 54% |
| cache_read | $0.30/MTok | 2,393M | $718 | 25% |
| cache_creation | $3.75/MTok | 101M | $380 | 13% |
| output_tokens | $15/MTok | 14.4M | $216 | 8% |

**Key insight**: Output is the most expensive per-token ($15/MTok) but only 8% of cost. The real driver is **input token volume** — Skeptic sends 225M input tokens/day, AO workers send 237M. Cache reads are cheap but 2.4B tokens = $718.

## Root cause: Skeptic ran in BOTH configs

`~/.agent-orchestrator.yaml` AND `~/.hermes_prod/agent-orchestrator.yaml` both had:
```yaml
worker-signals-completion:
  auto: true
  action: skeptic-review
  skepticModel: claude
```

Every time an AO worker signaled completion, a full Claude skeptic session was spawned. With 211 sessions at avg 145 messages each, this was the dominant cost driver.

## Actions taken (2026-05-06)

1. **~/.agent-orchestrator.yaml** — `worker-signals-completion: auto: false`
2. **~/.hermes_prod/agent-orchestrator.yaml** — `worker-signals-completion: auto: false`
3. **~/.claude/settings.json** — removed PostToolUse hooks:
   - `detect_speculation_and_fake_code.sh` (from `*` matcher)
   - `smart_fake_code_detection.sh` (from `Write` matcher)
   - `post_file_creation_validator.sh` (from `Write` matcher)
4. **GH Actions cron** — PR [#6822](https://github.com/jleechanorg/worldarchitect.ai/pull/6822) removes `*/30 * * * *` schedule from `skeptic-cron.yml`

## Savings

Estimated $1,049/day saved (37% of total). Normal work ($1,783/day) is the remaining spend.

## How to re-enable skeptic selectively

```yaml
# ~/.agent-orchestrator.yaml and ~/.hermes_prod/agent-orchestrator.yaml
worker-signals-completion:
  auto: true
  action: skeptic-review
  skepticModel: codex   # use codex, not claude, to avoid Claude quota
  skepticPostComment: true
```

Switching `skepticModel: codex` would run skeptic sessions via Codex instead, which doesn't consume Claude quota.
