# PR #9: Add smoke campaign test and trace coverage

**Repo:** jleechanorg/worldai_claw
**Merged:** 2026-02-22
**Author:** jleechan2015
**Stats:** +54/-37 in 5 files

## Summary
(none)

## Raw Body
Implements 3-action smoke test for campaign/session workflow with full turn-envelope checks and evidence trace capture.

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Changes affect integration test harness behavior and strict trace gating, which may cause previously-passing local runs to fail if trace env vars or server-start assumptions differ; no production runtime logic is modified.
> 
> **Overview**
> Adds a new `test_smoke_campaign_3_actions` integration smoke test that creates a campaign + session, submits 3 `/turn` actions, validates a stricter turn-response envelope (no mock markers, no character-creation/[STORY MODE], and bans legacy keys), and writes richer evidence including capped JSONL trace excerpts.
> 
> Updates test harness trace handling by (1) capturing OpenClaw/Gemini HTTP traces under `GEMINI_HTTP_REQUEST_RESPONSE_CAPTURE_PATH` in `running_backend`, and (2) tightening `MCPTestBase` strict trace validation to only require full trace logs when the test runner **actually started** the local server (not when connecting/reusing an existing server).
> 
> Documentation (`AGENTS.md`, `CLAUDE.md`) is updated to explicitly forbid mock/fallback flags (including `WORLDCLAW_FORCE_MOCK_OPENCLAW`) and fake local gateways in `testing_mcp/` and `testing_ui/`.
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit a94f035251254ecb2092b93e39db6e7c5a349d19. This will update automatically on new commits. Configure [here](https://cursor.com/dashboard?tab=bugbot).</sup>
<!-- /CURSOR_SUMMARY -->

<!-- COPILOT_TRACKING_START -->
## Copilot Tracking

| Comment ID | Status | Summary |
|------------|--------|---------|
| 2837210104 | Not Done | Comment references code at lines 668-669 that no longer exists in the current version. |
| 2837210108 | Not Done | Comment references line 1385 with redundant assignment that no longer exists. |
| 2837210117 | Not Done | Similar to above, code no longer exists. |
| 2837210124 | Already 
