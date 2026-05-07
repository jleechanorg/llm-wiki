---
title: "Claude Code Quota Cost"
type: concept
tags: [claude-code, quota, cost, tokens, hooks, skeptic, optimization]
sources: [claude-quota-cost-analysis-2026-05-06]
last_updated: 2026-05-06
---

## Token pricing (claude-sonnet-4-6)

| Token type | Rate |
|---|---|
| output_tokens | $15.00/MTok |
| cache_creation | $3.75/MTok |
| input_tokens | $3.00/MTok |
| cache_read | $0.30/MTok |

## Cost driver reality (May 5 2026 measurement)

Output tokens are the most expensive rate but usually only 7–8% of total cost. The actual cost leaders are:

1. **input_tokens (54%)** — Large context blobs sent on every call. Skeptic agent sends 225M/day; AO workers send 237M/day. Each session re-sends the full conversation context.
2. **cache_read (25%)** — Cheap per token ($0.30) but interactive sessions accumulate 2.4B tokens/day.
3. **cache_creation (13%)** — Hooks that spawn fresh sessions (no cache warmth) create new cache each invocation.
4. **output_tokens (8%)** — High rate but low volume.

## PostToolUse hooks that spawn Claude sessions

Hooks that call `claude` or spawn subprocesses with `claude --dangerously-skip-permissions` create a full new Claude session per invocation. Each Write tool call fires all PostToolUse `Write` hooks sequentially.

**Known expensive hooks (disabled 2026-05-06):**
- `detect_speculation_and_fake_code.sh` — fired on every tool call (PostToolUse `*`); spawned ~75-message session
- `smart_fake_code_detection.sh` — fired on every Write
- `post_file_creation_validator.sh` — fired on every Write; ~13-message session

**Pattern:** A session with 50 Write operations → 50 × (hook session cost). With avg $0.89/hook session = $44.50 in hook overhead per interactive session.

## Skeptic QA agent

The AO `worker-signals-completion` reaction fires a skeptic review whenever a worker signals PR completion. With `skepticModel: claude`, each review spawns a full Claude Code session (~145 messages, avg $4.56).

At 211 reviews/day = **$963/day**. This was the single largest cost driver.

**To switch to non-quota model:**
```yaml
worker-signals-completion:
  auto: true
  action: skeptic-review
  skepticModel: codex    # does not consume Claude quota
  skepticPostComment: true
```

**Both configs must be updated:**
- `~/.agent-orchestrator.yaml`
- `~/.hermes_prod/agent-orchestrator.yaml`

## See also

- [[ClaudeCodeHooks]] — hook configuration patterns
- [[ContextBloatFromMetadataHooks]] — related hook overhead problem
