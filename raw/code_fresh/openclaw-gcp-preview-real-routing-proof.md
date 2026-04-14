# OpenClaw real GCP preview routing proof

**Status:** UPDATED (latest PR 5879 evidence synced)
**Priority:** HIGH
**Created:** 2026-02-21
**Updated:** 2026-03-11
**Component:** GCP preview + OpenClaw + MCP

## Goal

Prove that GCP preview can route to local OpenClaw and complete real campaign creation/interaction for `jleechantest@gmail.com`, and keep a clear audit trail in PR evidence.

## Auth setup

- Set active world-architecture auth token to `jleechantest@gmail.com`:
  - `~/.ai-universe/auth-token-worldarchitecture-ai.json` (copied from `~/.worldarchitect-ai/auth-token.json`)
  - `~/.ai-universe/auth-token.json` also updated to `jleechantest@gmail.com`
  - Previous default `~/.ai-universe/auth-token.json` backed up to:
    - `~/.ai-universe/auth-token.json.pre-jleechantest-backup-20260221`

## Runtime config validated

- GCP preview service `mvp-site-app-s9` has `OPENCLAW_GATEWAY_TOKEN` set in Cloud Run environment variables.
- Environment: `WORLDAI_DEV_MODE=true`

## Latest evidence run (PR 5879)

Executed:

```
PREVIEW_URL=https://mvp-site-app-s9-i6xf2p72ka-uc.a.run.app

PYTHONPATH=/Users/jleechan/projects/worktree_openclaw \
WORLDAI_DEV_MODE=true \
AUTH_TOKEN_PATH=$HOME/.ai-universe/auth-token-worldarchitecture-ai.json \
OPENCLAW_TEST_USER_EMAIL=jleechantest@gmail.com \
./vpython testing_mcp/test_openclaw_gateway_url_preview.py --preview-url "$PREVIEW_URL"

TEST_BASE_URL="$PREVIEW_URL" \
OPENCLAW_PREVIEW_URL="$PREVIEW_URL" \
PYTHONPATH=/Users/jleechan/projects/worktree_openclaw \
./vpython testing_ui/test_openclaw_gcp_settings.py
```

Loop artifacts:
- `/tmp/pr5879_stabilize_20260311_123939/iter_1/testing_mcp.log`
- `/tmp/pr5879_stabilize_20260311_123939/iter_1/testing_ui.log`
- `/tmp/pr5879_stabilize_20260311_123939/iter_1/summary.txt`

MCP evidence bundle (latest):
- `/tmp/worldarchitectai/tailscale_pub/openclaw_gateway_url_preview/latest/run.json`
- `/tmp/worldarchitectai/tailscale_pub/openclaw_gateway_url_preview/latest/scenario_results_checkpoint.json`
- `/tmp/worldarchitectai/tailscale_pub/openclaw_gateway_url_preview/latest/test_console_output.txt`
- `/tmp/worldarchitectai/tailscale_pub/openclaw_gateway_url_preview/latest/request_responses.jsonl`

UI evidence bundle (latest):
- `/tmp/worldarchitect.ai/gcp_settings_test/run_1773258040/settings_proof.json`
- `/tmp/worldarchitect.ai/gcp_settings_test/run_1773258040/test_manifest.json`

Summary extracted from latest evidence:
- `testing_mcp`: exit 0, summary `5/5 passed (100%)`
- `testing_ui`: exit 0, `Success: PASS`
- `preview_url=https://mvp-site-app-s9-i6xf2p72ka-uc.a.run.app`
- `settings_saved=true`, `settings_persisted=true`
- `inference_hash_match=true`

## Skeptical validation note

- `testing_mcp` still records `e2e_gateway_routing` as `passed=true` while `skipped=true` when no tunnel provider is available.
- Treat this run as:
  - Strong evidence for preview surface/settings checks.
  - Not full remote->local routing execution proof for that skipped scenario.
- `testing_ui` latest run *did* execute preview proof call successfully and matched local hash.

## Prior-run cleanup

Older evidence references from prior PR runs (`feat_openclaw-gateway-url-setting`, `s10` preview URL, `2026-02-21` log slice) were removed from this doc and replaced with latest PR 5879 artifacts above.
