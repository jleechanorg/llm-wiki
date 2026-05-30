---
title: "Hermes Provider Quality & Selection"
tags: [hermes, provider, glm, opencode-go, zai, wafer, minimax, quality, iteration-exhaustion]
updated: 2026-05-29
---

# Hermes Provider Quality & Selection

Canonical reference for Hermes LLM provider quality history, known failure modes, and selection discipline.

## Provider History (jleechan machine)

| Period | Provider | Quality Signal |
|---|---|---|
| Pre-Apr 19, 2026 | minimax/MiniMax-M2.7 | 10–24s response times; baseline quality |
| Apr 19–21, 2026 | zai/GLM-5.1 | 45–271s response times; slow but quality unknown |
| Apr 21, 2026 | minimax/MiniMax-M2.7 | Reverted from zai |
| May 7–22, 2026 | wafer/GLM-5.1 | Low iteration exhaustion (~1–2/week); stable |
| May 29, 2026 | opencode-go/GLM-5.1 | **Day 1: 3× budget exhaustion; severe quality degradation** |

## Iteration Exhaustion Baseline (quality proxy metric)

Iteration budget exhaustion (60/60 reached) is a strong signal of provider quality degradation.

| Date | Provider | Exhaustion hits |
|---|---|---|
| May 24 | wafer | 1 |
| May 26 | wafer | 2 + multiple rate-limit fallbacks |
| May 29 | opencode-go | **3 in one day ← clear degradation** |

Wafer baseline: ~1–2 exhaustion events per week. opencode-go: 3 in one day.

## opencode-go/GLM-5.1 Known Failure Modes

1. **Agentic task stalls** — [Issue #24178](https://github.com/anomalyco/opencode/issues/24178): GLM-5.1 stalls when doing Todos in agentic/Build mode. Kimi and MiniMax unaffected by same tasks. GLM-5.1-specific.
2. **Thinking token leakage** — [Issue #16903](https://github.com/anomalyco/opencode/issues/16903): `<think>` tokens leak into context, causing `???■■■■■` display corruption and context pollution.
3. **Routing bug** — [Issue #1416](https://github.com/openclaw/openclaw/issues/1416): `resolveOpencodeZenModelApi()` misdirects models to wrong native providers (401 errors).
4. **Availability** — Thomas Wiegold review: "GLM-5.1 seems to have lots of availability issues" on opencode-go. Rate limit ~4,300 req/month.
5. **Proxy stack differences** — opencode-go likely runs a different inference stack than direct ZhipuAI; possible context truncation on long conversations.

## May 29 Observed Symptoms (opencode-go day 1)

- 3× 60/60 iteration budget exhausted
- Dragon Knight PR task: forgot to push to PR branch; changes landed on main uncommitted
- Fabricated Playwright test results against auth-protected site
- Streaming stalls: "Still working... 18 min elapsed iteration 45/60, waiting for provider response streaming"
- Fallback triggered: "Primary model failed switching to fallback: GLM-5.1 via zai"

## Provider Change Discipline

**MANDATORY**: Do not silently change `model.provider` in `~/.hermes_prod/config.yaml`.

Protocol when quality issues occur with opencode-go active:
1. Cite Issue #24178 (agentic stall) as documented risk
2. Offer to revert to wafer/GLM-5.1 as baseline test
3. Wait for explicit Jeffrey approval before touching config

Source: [[opencode-go-provider-quality-2026-05-29]]

## Related

- [[OpenCodeTUIWrapper]] — opencode-go TUI integration patterns
- [[WaferFixSSEPatcher]] — wafer SSE stream patching (lean-body token estimation)
- `~/.hermes_prod/config.yaml` — live provider config
