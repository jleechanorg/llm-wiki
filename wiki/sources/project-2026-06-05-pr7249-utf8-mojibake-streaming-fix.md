---
title: "PR #7249 — UTF-8 Mojibake in OpenRouter/OpenAI Proxy Streaming (MERGED)"
type: source
tags: [streaming, utf-8, mojibake, openrouter, openai-proxy, openclaw, sse, requests]
sources: [pr7249-utf8-mojibake-streaming-fix-2026-06-05.md]
last_updated: 2026-06-05
source_file: raw/project_2026-06-05_pr7249_utf8_mojibake_streaming_fix.md
---

## Summary
PR #7249 fixed UTF-8 mojibake corruption in OpenRouter (`x-ai/grok-4.3`) and OpenAI proxy streaming. Root cause: `requests.Response.iter_lines(decode_unicode=True)` silently defaults to ISO-8859-1 when Content-Type lacks `charset=`, corrupting multi-byte UTF-8 (em-dash, curly apostrophe, curly quotes) into 3 separate ISO-8859-1 characters that get stored in Firestore. Fix: remove `decode_unicode=True` from `openrouter_provider.py:390` and `openai_proxy_provider.py:391` (matches OpenClaw safe pattern). MERGED at `6933742b16564b152623aba7cfdcc61c60652652` on 2026-06-05 via `--squash`.

## Key Claims
- Bug affected 22 model-output story entries in campaign `mXhtOccHYGHgV2Tdf0lc` (Itachi V3, owner UID `vnLp2G3m21PJL6kxcuAqmWSOtm73`), 511 total mojibake occurrences. 3 user-input entries are not auto-fixable (user copy-pasted from a different encoding source).
- Gemini path was clean (0 mojibake) — uses `google-genai` SDK which yields `part.text` directly with no `iter_lines` / `decode_unicode` / manual byte→str decoding.
- OpenClaw was not affected — uses `iter_lines()` WITHOUT `decode_unicode=True`; consumer in `llm_service.py:8029-8030` does explicit `chunk.decode("utf-8", errors="replace")`. This is the safe pattern.
- Why some Grok turns are clean: when the chunk boundary doesn't fall between the 3 bytes of an em-dash. Bug is non-deterministic at the per-turn level.
- Fix is a 1-line change per call site: replace `iter_lines(decode_unicode=True)` with `iter_lines()`.
- 4 regression tests in `mvp_site/tests/test_streaming_utf8_mojibake_regression.py`:
  - `test_openrouter_streaming_preserves_em_dash`
  - `test_openrouter_streaming_preserves_curly_apostrophe`
  - `test_openrouter_streaming_preserves_curly_quotes`
  - `test_openai_proxy_streaming_preserves_em_dash`
- Tests use `FakeSSEResponse` whose `iter_lines` is the **real** method (encoding=ISO-8859-1) — NOT a mock that hides the bug. Each test builds a real SSE chunk as it would arrive over the wire (`ensure_ascii=False` so multi-byte UTF-8 sequences are actual bytes).
- CodeRabbit review: 2 nitpicks (status checklist in repro/.md, misleading `gemini_stream_proxy?` actor name) + 2 inline-import comments (`import codecs` in FakeSSEResponse.iter_lines; `from mvp_site.llm_providers.openai_proxy_provider import invoke_openclaw_gateway_stream` inside test function). All 4 fixed. Module-level imports are MANDATORY per `worldarchitect.ai/CLAUDE.md` "Import Standards (CI Enforced)".
- 7-green workflow: GATE-1 CI green, GATE-2 mergeable clean, GATE-3 CodeRabbit CHANGES_REQUESTED → APPROVED, GATE-4 Bugbot clean, GATE-5 comments resolved, GATE-6 evidence (GitHub gist https://gist.github.com/jleechan2015/70c3ca42b4ab4eeb61d3752d055700b4 + PR comment), GATE-7 Skeptic SKIPPED for non-prod changes. User authorized "if 6 gates pass you can merge".
- Optional follow-up: `repro/evidence/7248/recover_mojibake_entries.py --apply` would repair the 22 model-output entries. **REQUIRES human review of dry-run output before --apply** — never run --apply without user explicitly typing approval.
- Reusable pattern for future SSE/streaming providers: ❌ NEVER use `iter_lines(decode_unicode=True)`. ✅ Either: (1) `iter_lines()` + downstream `chunk.decode("utf-8", errors="replace")` (preferred — OpenClaw pattern), or (2) `response.encoding = "utf-8"` BEFORE `iter_lines(decode_unicode=True)`. Always add a regression test that emits multi-byte UTF-8 in a chunk that crosses a line boundary.

## Key Quotes
> "`requests.Response.iter_lines(decode_unicode=True)` ultimately calls `requests.utils.stream_decode_response_unicode`, which decodes each chunk using `self.encoding` (the `Response.encoding` property, defaulting to **ISO-8859-1** when Content-Type lacks a `charset=` directive)." — project_2026-06-05_pr7249_utf8_mojibake_streaming_fix

> "When adding a new LLM provider that uses `requests` + SSE: ❌ NEVER use `iter_lines(decode_unicode=True)`. ✅ Either: `iter_lines()` (no decode) + downstream `chunk.decode('utf-8', errors='replace')` (OpenClaw pattern), or `response.encoding = 'utf-8'` BEFORE `iter_lines(decode_unicode=True)`." — project_2026-06-05_pr7249_utf8_mojibake_streaming_fix

## Connections
- [[pr7249-utf8-mojibake-streaming-fix-2026-06-05]] — the existing pre-upgrade page (sibling)
- [[Streaming-Evidence-Standards]] — evidence requirements for streaming chunks
- [[CodeRabbit-Import-Standards]] — module-level imports are CI-enforced
- [[7-Green-Proof-Artifact]] — VERDICT PASS workflow
- [[PR-6896-Location-Inline-Resolve]] — earlier fix that establishes inline-resolve pattern
