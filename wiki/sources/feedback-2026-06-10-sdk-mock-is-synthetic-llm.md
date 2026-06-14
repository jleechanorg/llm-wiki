---
title: "Feedback 2026 06 10 Sdk Mock Is Synthetic Llm"
type: source
tags: [memory, ao-worker, codex-worker, 2026-06]
date: 2026-06-10
source_file: .claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-10_sdk_mock_is_synthetic_llm.md
---

## Summary

**Date**: 2026-06-10 (PR #7439 BQ logging fix verification)
**Trigger**: User: *"why did we make syhnethic payloads? I almsot never want that /harness use /history i believe i asked many times for real llm real BQ proof"*



Verify script `scripts/verify_bq_logging.sh` drove production streaming code with a mocked Gemini client:

```python
class _FakeClient:
    models = _FakeModelsAPI()
gp.get_client = lambda api_key=None: _FakeClient()
```

This substituted the entire `google.genai` SDK with a...

## Original

# SDK mock ≠ external API boundary — `get_client = lambda: _FakeClient()` is SYNTHETIC LLM

**Date**: 2026-06-10 (PR #7439 BQ logging fix verification)
**Trigger**: User: *"why did we make syhnethic payloads? I almsot never want that /harness use /history i believe i asked many times for real llm real BQ proof"*

## What happened

Verify script `scripts/verify_bq_logging.sh` drove production streaming code with a mocked Gemini client:

```python
class _FakeClient:
    models = _FakeModelsAPI()
gp.get_client = lambda api_key=None: _FakeClient()
```

This substituted the entire `google.genai` SDK with a hand-rolled fake. BQ HTTP inserts were real (4 production-driven rows at 09:30:14-16 with production-set `execution_path`/`path` fields), but the **streamed chunks flowing through production code were fabricated** — they were not real Gemini responses.

The 4 /er dispatches in this session treated "real BQ HTTP inserts" as Layer 2 proof and passed the bundle. The user correctly identified the gap: "real BQ" and "real LLM" are orthogonal axes, and the LLM axis was synthetic.

## Why this is the SAME failure class as prior entries

| Memory entry | Failure mode | Same root cause? |
|---|---|---|
| `feedback_2026-05-29_factory_synthetic_evidence_real_repro` | "Hand-feeding bad values to SUT" | Different surface, same idea: RED/EVIDENCE built from a synthetic source the gate itself reads |
| `feedback_2026-06-09_unit_only_proof_not_allowed` | "Unit-only" | Parent rule; the SDK-mock case is a sub-case that the parent rule was *meant* to cover but didn't enumerate |
| `feedback_2026-06-10_forensic_llm_captures_must_be_committed` | "Raw LLM payloads must be committed" | Symmetric: you can't *commit* a real payload if you never captured one |
| **THIS ENTRY** | "In-process SDK mock ≠ external API boundary" | Names the specific gap in the parent rule |

## The rule that was missing

The parent rule says: *"mocks only at external API boundaries (network, third-party services)"*. The user-facing intent is "real network call to the third party." But the wording leaves room for agents to claim "external API boundary" was satisfied by an in-process function override (`get_client = lambda: ...`).

The corrected rule: **the external API boundary is the network socket, not the in-process wrapper.** Specifically:

| Mocked boundary | Layer | Allowed for LLM-behavior claim? |
|---|---|---|
| `mock.patch("google.genai.GenerativeModel")` in a unit test | Layer 1 | ✅ as Layer 1, ❌ as Layer 2 |
| `gemini_provider.get_client = lambda: _FakeClient()` (in-process) | Layer 1 (synthetic LLM) | ❌ NOT acceptable as Layer 2 |
| `httpx.MockTransport` / `responses` / `respx` at HTTP layer | Layer 2 boundary | ✅ IF the body is recorded from a real prior call |
| Real `https://generativelanguage.googleapis.com/...` POST | Layer 2 (real LLM) | ✅ Required for LLM-behavior claims |

## How to apply

**Before claiming an LLM-behavior change is proven:**

1. **Find the in-process wrapper override.** Search the verify script for any line that does `module.<func> = lambda ...` or `monkeypatch.setattr(module, "<func>", ...)`. If the override is between your code and a third-party SDK (Gemini, OpenAI, Anthropic, Firebase, Dice), the LLM is synthetic.
2. **Demand per-claim layer labels.** Every /er verdict claim must end with `[Layer N source]`. A claim missing the label is non-compliant and the verdict must be downgraded to PARTIAL.
3. **Re-run with real network calls when the LLM is in scope.** For PR #7439, the missing piece is: drive `_continue_story_streaming_impl` (or at minimum `gemini_provider.generate_content_stream_sync` + downstream BQ helper) with a real `GOOGLE_API_KEY` and a real network POST. The BQ row will then carry a real Gemini response (real `candidates[0].content.parts[0].text`).
4. **If real LLM is too expensive or slow for one PR**, scope the PR to "production code paths wire to BQ correctly" and explicitly state in the PR description "Known Limitations: Layer 2 BQ proof only — streamed payload is synthetic, real-Gemini capture is a follow-up bead." Don't claim PASS on LLM-behavior when the LLM is mocked.

## Related harness changes

- `~/.claude/skills/evidence-standards/SKILL.md` — added "SDK Mock ≠ External API Boundary (NAMED ANTI-PATTERN)" section and "Per-Claim Layer Label (MANDATORY in /er verdicts)" section.
- PR #7439 — needs PR description update: reclassify the Layer 2 BQ proof as `Layer 1 synthetic-LLM + Layer 2 real-BQ` and explicitly add "real-Gemini capture" as a Known Limitation with a follow-up bead.
- Bead needed: `rev-<next>` — "Capture real-Gemini streamed response and BQ row for the 4 streaming/repair paths."

## Why this matters

The user has flagged "synthetic" or "real LLM" in at least 3 sessions (2026-04-28, 2026-05-29, 2026-06-10). The harness now has an explicit named anti-pattern + detection signal + per-claim layer label requirement. Future /er dispatches should auto-catch this.
