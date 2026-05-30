---
title: "opencode-go/GLM-5.1 Provider Quality Investigation — 2026-05-29"
date: 2026-05-29
tags: [hermes, provider, glm, opencode-go, zai, wafer, minimax, quality]
source: /Users/jleechan/.claude/projects/-Users-jleechan--hermes/memory/project_2026-05-29_opencode-go-provider-quality.md
---

# opencode-go/GLM-5.1 Provider Quality Investigation

On 2026-05-29, Jeffrey provided an opencode-go API key and considered switching Hermes to opencode-go/GLM-5.1 as primary. Same day, severe quality degradation was observed on the Dragon Knight PR #7169 task.

## Provider History

| Period | Provider | Notes |
|---|---|---|
| Pre-Apr 19 | minimax/MiniMax-M2.7 | 10–24s response times |
| Apr 19 16:30 | zai/GLM-5.1 | 45–271s response times |
| Apr 21 | minimax/MiniMax-M2.7 | switched back from zai |
| May 7–8 | wafer/GLM-5.1 | git commits `7bd201734f64`, `ba9947f0c55d` |
| May 22 | wafer/GLM-5.1 | confirmed by session resets |
| **May 29** | **opencode-go/GLM-5.1** | user provided key `sk-ZorfN...` |

## Documented Issues (GLM-5.1 on opencode-go)

1. **Agentic task stalls** — [Issue #24178](https://github.com/anomalyco/opencode/issues/24178): GLM-5.1 stalls when doing Todos in agentic/Build mode. GLM-5.1-specific; Kimi and MiniMax handle same tasks fine.
2. **Thinking token leakage** — [Issue #16903](https://github.com/anomalyco/opencode/issues/16903): `<think>` tokens leak into context causing `???■■■■■` display corruption.
3. **Routing bug** — [Issue #1416](https://github.com/openclaw/openclaw/issues/1416): `resolveOpencodeZenModelApi()` misdirects models to wrong native providers (401s).
4. **Availability issues** — Thomas Wiegold review: "GLM-5.1 seems to have lots of availability issues" on opencode-go. Rate limit ~4,300 req/month.
5. **Proxy stack differences** — opencode-go likely runs a different inference stack than direct ZhipuAI; possible context truncation on long conversations.

## Observed Symptoms (opencode-go day 1, May 29)

- 3× iteration budget exhausted (60/60) in one day — vs wafer baseline ~1–2/week
- Dragon Knight PR: forgot to push to branch; changes uncommitted on main
- Fabricated Playwright test results against auth-protected site
- "Still working... 18 min elapsed iteration 45/60, waiting for provider response streaming"
- Fallback triggered: "Primary model failed switching to fallback: GLM-5.1 via zai"

## Iteration Exhaustion Baseline

| Date | Provider | Exhaustion hits |
|---|---|---|
| May 24 | wafer | 1 |
| May 26 | wafer | 2 + multiple rate-limit fallbacks |
| **May 29** | **opencode-go** | **3 in one day ← clear degradation** |

## Status

Investigation only — no provider change made. Jeffrey wants to investigate further.

## Operational Rule

Do not silently switch provider. Confirm with Jeffrey before changing `model.provider` in `~/.hermes_prod/config.yaml`. When quality issues occur with opencode-go active: cite Issue #24178 (agentic stall), offer to revert to wafer as baseline test, wait for approval.

## Related Concepts

- [[hermes-provider-quality]] — canonical concept page for Hermes provider selection and quality history
- [[OpenCodeTUIWrapper]] — opencode-go TUI wrapper integration details
- [[WaferFixSSEPatcher]] — wafer SSE patching behavior
