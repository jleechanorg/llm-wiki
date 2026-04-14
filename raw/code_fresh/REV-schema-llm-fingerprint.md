# Bead: LLM Prompt Fingerprint Is Not Comparable Between Main and Branch (Schema MCP Runs)

**Status:** OPEN
**Priority:** HIGH
**Component:** testing_mcp, mvp_site/agent_prompts.py, evidence capture
**Created:** 2026-02-21

## Problem

The schema MCP regression artifacts do not contain a comparable LLM request stream for origin/main.
Branch runs include `llm_request_responses.jsonl`, but origin/main runs do not.

That means we cannot verify that the exact LLM request payload (including `system_instruction_text` and related schema instructions) is identical between `main` and `branch`.

## Evidence

- `~/Downloads/schema_prompt_regression_20260221_010824/REPORT.md` shows `main` `schema_validation_real_api` as PASS and branch `schema_validation_real_api` as OOM-killed; `schema_validation_extended` is `N/A` on main.
- `/tmp/worldarchitectai/main` contains only `campaign_pagination_mcp` and `github-mcp-smoke-mock` evidence directories.
- `llm_request_responses.jsonl` files are present only in `schema_followup` paths under `/tmp/worldarchitectai/schema_followup/`.
- Main branch logs still report: `Missing llm_request_responses.jsonl` and `Strict trace validation failed: MCP trace file has no process_action pairs`.

## Impact

- We cannot claim "same schema sent to LLM" from current artifacts.
- The current evidence only proves branch payload capture exists, not parity against main.

## Recommendation

- Re-run comparable `schema_validation_*` MCP tests on origin/main with trace capture enabled.
- Use the branch capture files in `/tmp/worldarchitectai/schema_followup/` as the canonical branch baseline.
- Diff normalized request envelopes (`system_instruction_text`, tool contract sections, and JSON schema snippets) after rerun.

## Update from supplied paths

- `main` sample path `.../unknown/schema_validation_real_api/http_request_responses_1771665151953.jsonl` only includes `/mcp` HTTP calls and ends with `create_campaign` failure (`GEMINI_API_KEY environment variable not found`); it does **not** include direct Gemini `generateContent` traffic.
- `branch` sample path `/schema_followup/schema_validation_extended/iteration_001/gemini_http_request_responses.jsonl` is a direct Gemini `generateContent`/`streamGenerateContent` request including full `systemInstruction` + user content.
- Therefore, these two are not comparable as the "same llm side request" even though both are marked PASS in different contexts.

## Update from GH Actions run 22254378586 / job 64383602612

- I checked `https://github.com/jleechanorg/worldarchitect.ai/actions/runs/22254378586`.
- This job (`Harness autonomy checks (fallback)`) is unrelated to the schema prompt regression suite.
- Its logs are from harness autonomy checks + prompt/tool contract hash validation and do not contain MCP schema LLM request/response fingerprints.
- So, this run does not satisfy the schema LLM fingerprint comparison you are asking about.

## Next Step

Open a follow-up tracking item once rerun artifacts are available, and compare request fingerprints directly.
