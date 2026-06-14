---
name: pr-7249-utf-8-mojibake-streaming-fix-merged
description: "requests.Response.iter_lines(decode_unicode=True) silently defaults to ISO-8859-1 when Content-Type lacks charset, corrupting multi-byte UTF-8 in OpenRouter/OpenAI proxy SSE streams. Fix: remove decode_unicode=True + downstream explicit utf-8 decode (OpenClaw safe pattern). 4 regression tests, GATE-6 gist, --squash merge at 6933742b16."
metadata: 
  node_type: memory
  type: project
  bead: rev-c4dmt
  originSessionId: 82ffcc9f-0edd-4305-9b06-d3d9a2d56b24
---

# PR #7249: UTF-8 mojibake in OpenRouter/OpenAI proxy streaming — MERGED

**Status:** MERGED at `6933742b16564b152623aba7cfdcc61c60652652` on 2026-06-05 via `--squash`
**PR:** https://github.com/jleechanorg/worldarchitect.ai/pull/7249
**Issue:** https://github.com/jleechanorg/worldarchitect.ai/issues/7248
**Campaign affected:** mXhtOccHYGHgV2Tdf0lc (Itachi V3)
**Symptoms:** em-dash (—) became `â\x80\x94`, curly apostrophe (') became `â\x80\x99` in 22 model-output story entries (511 total mojibake occurrences)
**Cause:** Gemini path was clean (0 mojibake). All corruption in OpenRouter (`x-ai/grok-4.3`) and OpenAI proxy model output.

## Root cause (proven)

`requests.Response.iter_lines(decode_unicode=True)` ultimately calls
`requests.utils.stream_decode_response_unicode`, which decodes each chunk
using `self.encoding` (the `Response.encoding` property, defaulting to
**ISO-8859-1** when Content-Type lacks a `charset=` directive). OpenRouter's
SSE responses don't always include a charset, so each 3-byte UTF-8
character (e.g. em-dash `0xE2 0x80 0x94`) is decoded as 3 separate
ISO-8859-1 characters (`â`, `\x80`, `\x94`). The downstream `json.loads`
re-encodes these into the str Python object, and they are stored in
Firestore as the mojibake sequence `â\x80\x94`.

## Why some Grok turns are clean (seq=1008, seq=1124)

A turn is mojibake-free when the model's emitted text happens to contain
no multi-byte UTF-8 characters in the chunk that crosses a line boundary.
If a chunk boundary lands **between** the 3 bytes of an em-dash,
`iter_lines(decode_unicode=True)` corrupts them. If the chunk boundary
is at a single-byte ASCII character, the em-dash passes through cleanly.
Bug is **non-deterministic at the per-turn level**.

## Why Gemini is not affected

`mvp_site/llm_providers/gemini_provider.py:1175` uses the official
`google-genai` SDK (`client.models.generate_content_stream`). Yields
`part.text` directly — no `iter_lines`, no `decode_unicode`, no manual
byte→str decoding.

## Why OpenClaw is not affected (safe pattern reference)

`mvp_site/llm_providers/openclaw_provider.py:291` uses
`response.iter_lines()` **without** `decode_unicode=True`. Bytes pass
through un-decoded; the consumer in `llm_service.py:8029-8030` then
does `chunk_text = chunk.decode("utf-8", errors="replace")`. **This is
the correct pattern that the OpenRouter and OpenAI proxy providers now
match.**

## Fix (option 1, 1-line per call site)

In `mvp_site/llm_providers/openrouter_provider.py:390` and
`mvp_site/llm_providers/openai_proxy_provider.py:391`, replace
`iter_lines(decode_unicode=True)` with `iter_lines()`. The downstream
`llm_service.py` consumer already does explicit UTF-8 decode.

## Files changed

- `mvp_site/llm_providers/openrouter_provider.py` — removed `decode_unicode=True`
- `mvp_site/llm_providers/openai_proxy_provider.py` — removed `decode_unicode=True`
- `mvp_site/tests/test_streaming_utf8_mojibake_regression.py` — 4 new tests
  - test_openrouter_streaming_preserves_em_dash
  - test_openrouter_streaming_preserves_curly_apostrophe
  - test_openrouter_streaming_preserves_curly_quotes
  - test_openai_proxy_streaming_preserves_em_dash
- `repro/7248_spicy_mode_malformed_text.md` — investigation log
- `repro/evidence/7248/MOJIBAKE_INVENTORY.md` — 25-entry inventory with 511 occurrences
- `repro/evidence/7248/recover_mojibake_entries.py` — optional one-time Firestore backfill (NOT run, requires human review)
- `repro/evidence/7248/extract_streaming_metadata.py` — per-seq model/encoding/char-count
- `repro/evidence/7248/repro_utf8_mojibake_streaming.py` — bytes-level bug demo

## CodeRabbit review resolution

- 2 nitpicks (status checklist in repro/.md, misleading `gemini_stream_proxy?` actor name)
- 2 inline-import comments (`import codecs` in FakeSSEResponse.iter_lines; `from mvp_site.llm_providers.openai_proxy_provider import invoke_openclaw_gateway_stream` inside test function)
- All 4 fixed → CHANGES_REQUESTED → APPROVED
- Module-level imports are MANDATORY per CLAUDE.md (`/Users/jleechan/projects/worldarchitect.ai/CLAUDE.md` "Import Standards (CI Enforced)")

## 7-green gates workflow that worked

- GATE-1 (CI): all green
- GATE-2 (mergeable): clean
- GATE-3 (CodeRabbit): CHANGES_REQUESTED → APPROVED after fixing 4 comments
- GATE-4 (Bugbot): not applicable / clean
- GATE-5 (comments): no unresolved
- GATE-6 (evidence): GitHub gist https://gist.github.com/jleechan2015/70c3ca42b4ab4eeb61d3752d055700b4 + PR comment
- GATE-7 (Skeptic): SKIPPED for non-prod changes (CLAUDE.md "Skeptic gate (Codex) - SKIPPED for non-prod changes")
- User authorization: "if 6 gates pass you can merge" (conditional)
- Merge method: `--squash` per repo hook `.claude/hooks/block-merge.sh` suggestion

## PR head ref retarget — GitHub API limitation

Tried to retarget PR #7249 head from `repro/7248-spicy-mode-malformed-text` to `fix/utf8-mojibake-streaming`:
- `gh pr edit --head` not supported
- `gh api -X PATCH /repos/.../pulls/7249` with `head` body — rejected (head ref is immutable)
- GraphQL `updatePullRequest` mutation with `headRefName` — rejected
- **Resolution:** force-push `fix/utf8-mojibake-streaming` with the merged content using `--force-with-lease` after getting user explicit in-thread approval

## Optional follow-up: Firestore backfill of 25 already-corrupted entries

`repro/evidence/7248/recover_mojibake_entries.py` exists. Has `--apply` flag.
- 22 model-output entries: `â\x80\x94`/`â\x80\x99`/`â\x80\x9c`/`â\x80\x9d` → `—`/`'`/`"`/`"`
- 3 user-input entries: NOT auto-fixable (user copy-pasted from different encoding source)
- **REQUIRES human review of dry-run output before --apply** — never run --apply without user explicitly typing approval

## Reusable pattern for future SSE/streaming providers

When adding a new LLM provider that uses `requests` + SSE:
- ❌ NEVER use `iter_lines(decode_unicode=True)`
- ✅ Either:
  1. `iter_lines()` (no decode) + downstream `chunk.decode("utf-8", errors="replace")` (OpenClaw pattern)
  2. `response.encoding = "utf-8"` BEFORE `iter_lines(decode_unicode=True)`
- Add a regression test that emits em-dash / curly quotes / curly apostrophe in a chunk that crosses a line boundary

## References

- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/7249
- Issue: https://github.com/jleechanorg/worldarchitect.ai/issues/7248
- Gist: https://gist.github.com/jleechan2015/70c3ca42b4ab4eeb61d3752d055700b4
- Commit: 6933742b16564b152623aba7cfdcc61c60652652
- Prior commits: 1bba34da7a45d1314bda3dcdc2815eee843268b5 (clean tip), aa1010ad5f (pre-merge main)
- Campaign: mXhtOccHYGHgV2Tdf0lc (owner UID vnLp2G3m21PJL6kxcuAqmWSOtm73)
- Worktree: /Users/jleechan/projects/wt-utf8-mojibake (used during PR work)
- Skills referenced: ~/.claude/skills/evidence-standards/, ~/.claude/skills/pr-green-definition
- Mandatory import rule: worldarchitect.ai/CLAUDE.md "Import Standards (CI Enforced)"
