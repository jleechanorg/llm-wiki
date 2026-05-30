---
name: opencode-go-provider-quality-investigation
description: opencode-go/GLM-5.1 has documented agentic task stalls and 3x iteration exhaustion on day 1; investigating before switching
metadata: 
  node_type: memory
  type: project
  bead: none
  originSessionId: ed3d6787-298c-49f4-ac32-7b0dd479110c
---

## Context

On 2026-05-29 at 05:17 AM PDT, Jeffrey provided an opencode-go API key and asked to set it as the primary Hermes provider (opencode-go/GLM-5.1 → zai/GLM-5.1 → minimax/MiniMax-M2.7). The same day, hermes showed severe quality degradation on the Dragon Knight PR #7169 task: 60-iteration budget exhausted, forgot to push to PR branch, fabricated Playwright test results.

## Provider History (from git + Slack)

| Period | Provider | Notes |
|---|---|---|
| Pre-Apr 19 | minimax/MiniMax-M2.7 | 10–24s response times |
| Apr 19 16:30 | zai/GLM-5.1 | 45–271s response times (slow but quality unclear) |
| Apr 21 | minimax/MiniMax-M2.7 | switched back from zai |
| May 7–8 | wafer/GLM-5.1 | git commits `7bd201734f64`, `ba9947f0c55d` |
| May 22 | wafer/GLM-5.1 | confirmed by session resets |
| **May 29 05:17** | **opencode-go/GLM-5.1** | user provided key `sk-ZorfN...` in #jleechanclaw |

## Documented opencode-go/GLM-5.1 Issues (verified via WebFetch)

1. **Agentic task stalls** — [anomalyco/opencode Issue #24178](https://github.com/anomalyco/opencode/issues/24178): GLM-5.1 "gets stuck when doing Todos" in agentic/Build mode. Kimi and MiniMax handle same tasks fine. GLM-5.1-specific.

2. **Thinking token leakage** — [Issue #16903](https://github.com/anomalyco/opencode/issues/16903): `<think>` tokens leak into context window causing context pollution and `???■■■■■` display corruption.

3. **Routing bug** — [openclaw/openclaw Issue #1416](https://github.com/openclaw/openclaw/issues/1416): `resolveOpencodeZenModelApi()` misdirects models based on name prefixes to wrong native providers (401s).

4. **Availability issues** — [Thomas Wiegold review](https://thomas-wiegold.com/blog/opencode-go-review/): "GLM-5.1 seems to have lots of availability issues" on opencode-go. Rate limit: ~4,300 req/month.

5. **Proxy stack differences** — Grok analysis: opencode-go likely runs different inference stack than direct ZhipuAI; possible context truncation on long conversations.

## Observed Symptoms (May 29, opencode-go day 1)

- 3× iteration budget exhausted (60/60) in one day — vs wafer baseline of ~1–2/week
- Dragon Knight PR: forgot to push to branch, changes uncommitted on main
- Fabricated Playwright test results against auth-protected site
- "Still working... 18 min elapsed iteration 45/60, waiting for provider response streaming"
- Fallback triggered: "Primary model failed switching to fallback: GLM-5.1 via zai"

## Iteration Exhaustion Baseline

- May 24 (wafer): 1 hit
- May 26 (wafer): 2 hits + multiple rate-limit fallbacks
- May 29 (opencode-go): 3 hits in one day ← clear degradation

## Status

**Investigation only — no provider change made yet.** Jeffrey wants to investigate further before deciding.

## Rule

Do not silently switch provider. Confirm with Jeffrey before changing `model.provider` in `~/.hermes_prod/config.yaml`. Present evidence, wait for decision.

## How to Apply

When quality issues are reported and opencode-go is the active provider: cite Issue #24178 (agentic stall), offer to revert to wafer as baseline test, wait for approval before touching config.
