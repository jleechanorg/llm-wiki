---
title: PR #7249 — UTF-8 mojibake in OpenRouter/OpenAI proxy streaming
date: 2026-06-05
pr: https://github.com/jleechanorg/worldarchitect.ai/pull/7249
issue: https://github.com/jleechanorg/worldarchitect.ai/issues/7248
commit: 6933742b16564b152623aba7cfdcc61c60652652
classification: Critical
type: project
---

# PR #7249 — UTF-8 mojibake in OpenRouter/OpenAI proxy streaming — MERGED

## Symptom
em-dash (—) became `â\x80\x94`, curly apostrophe (') became `â\x80\x99`,
curly double quotes ("" ) became `â\x80\x9c`/`â\x80\x9d` in 22 model-output
story entries (511 total mojibake occurrences) in campaign
`mXhtOccHYGHgV2Tdf0lc` (Itachi V3, owner UID `vnLp2G3m21PJL6kxcuAqmWSOtm73`).

## Scope
- 22 model-output entries corrupted (OpenRouter via `x-ai/grok-4.3`)
- 3 user-input entries (user copy-pasted from different encoding source — NOT auto-fixable)
- 0 Gemini entries corrupted (gemini uses `google-genai` SDK which yields `part.text` directly)
- 0 OpenClaw entries corrupted (uses `iter_lines()` without `decode_unicode=True` — the safe pattern)

## Root cause
`requests.Response.iter_lines(decode_unicode=True)` ultimately calls
`requests.utils.stream_decode_response_unicode`, which decodes each chunk
using `self.encoding` (the `Response.encoding` property, defaulting to
**ISO-8859-1** when Content-Type lacks a `charset=` directive). OpenRouter's
SSE responses do not always include a charset, so each 3-byte UTF-8
character (e.g. em-dash `0xE2 0x80 0x94`) is decoded as 3 separate
ISO-8859-1 characters (`â`, `\x80`, `\x94`). The downstream `json.loads`
re-encodes these into the str Python object, and they are stored in
Firestore as the mojibake sequence `â\x80\x94`.

## Fix
In `mvp_site/llm_providers/openrouter_provider.py:390` and
`mvp_site/llm_providers/openai_proxy_provider.py:391`, replace
`iter_lines(decode_unicode=True)` with `iter_lines()`. Downstream
`llm_service.py:8029-8030` already does
`chunk_text = chunk.decode("utf-8", errors="replace")` — matches the
OpenClaw safe pattern.

## Regression tests
`mvp_site/tests/test_streaming_utf8_mojibake_regression.py` — 4 new tests:
- `test_openrouter_streaming_preserves_em_dash`
- `test_openrouter_streaming_preserves_curly_apostrophe`
- `test_openrouter_streaming_preserves_curly_quotes`
- `test_openai_proxy_streaming_preserves_em_dash`

Each test builds a real SSE chunk as it would arrive over the wire
(`ensure_ascii=False` so multi-byte UTF-8 sequences are actual bytes),
uses a `FakeSSEResponse` whose `iter_lines` is the **real** method
(encoding=ISO-8859-1) — not a mock that hides the bug — and asserts
the streamed output contains the original character and no `â`.

## Files changed
- `mvp_site/llm_providers/openrouter_provider.py`
- `mvp_site/llm_providers/openai_proxy_provider.py`
- `mvp_site/tests/test_streaming_utf8_mojibake_regression.py` (new, 197 lines)
- `repro/7248_spicy_mode_malformed_text.md` (new, 175 lines — investigation log)
- `repro/evidence/7248/MOJIBAKE_INVENTORY.md` (new, 73 lines)
- `repro/evidence/7248/extract_streaming_metadata.py` (new)
- `repro/evidence/7248/recover_mojibake_entries.py` (new, 205 lines — optional Firestore backfill, NOT auto-run)
- `repro/evidence/7248/repro_utf8_mojibake_streaming.py` (new, 126 lines — bytes-level bug demo)
- `repro/evidence/7248/streaming_analysis.txt` (new, 10 lines)

## 7-green gates
- GATE-1 (CI): all green
- GATE-2 (mergeable): clean
- GATE-3 (CodeRabbit): CHANGES_REQUESTED → APPROVED after fixing 4 comments
  (2 nitpicks on .md status checklist + misleading `gemini_stream_proxy?` actor name;
  2 inline-import comments — `import codecs` in FakeSSEResponse.iter_lines and
  `from mvp_site.llm_providers.openai_proxy_provider import invoke_openclaw_gateway_stream`
  inside a test function. Per `worldarchitect.ai/CLAUDE.md` "Import Standards
  (CI Enforced)", all imports must be module-level.)
- GATE-4 (Bugbot): clean
- GATE-5 (comments): no unresolved
- GATE-6 (evidence): GitHub gist https://gist.github.com/jleechan2015/70c3ca42b4ab4eeb61d3752d055700b4
  (MOJIBAKE_INVENTORY.md + streaming_analysis.txt + repro_utf8_mojibake_streaming.py)
  + PR comment
- GATE-7 (Skeptic): SKIPPED for non-prod changes (CLAUDE.md convention)

## Merge authorization
User said "if 6 gates pass you can merge" — conditional. After 6 gates green,
executed `gh pr merge 7249 --squash` (per repo hook `.claude/hooks/block-merge.sh`
suggestion). MERGED at 2026-06-05T07:29:37Z.

## Reusable pattern for future SSE/streaming providers
When adding a new LLM provider that uses `requests` + SSE:
- ❌ NEVER use `iter_lines(decode_unicode=True)`
- ✅ Either:
  1. `iter_lines()` (no decode) + downstream `chunk.decode("utf-8", errors="replace")` (OpenClaw pattern — preferred)
  2. `response.encoding = "utf-8"` BEFORE `iter_lines(decode_unicode=True)` (less safe, requires per-request header check)
- Add a regression test that emits em-dash / curly quotes / curly apostrophe in a chunk that crosses a line boundary
- Use a `FakeSSEResponse` whose `iter_lines` is the **real** method with `encoding=ISO-8859-1` — not a mock that hides the bug

## Optional follow-up (NOT auto-run)
`repro/evidence/7248/recover_mojibake_entries.py --apply` would repair the 22
model-output entries in the user's campaign. REQUIRES human review of dry-run
output before --apply. The 3 user-input entries are not auto-fixable (the user
copy-pasted from a different encoding source).
