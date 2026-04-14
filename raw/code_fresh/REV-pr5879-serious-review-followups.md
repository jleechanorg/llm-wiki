# REV-pr5879-serious-review-followups

## Goal
Land the serious PR 5879 follow-ups that can cause false failures or incorrect tunnel side effects.

## Scope
- Harden `OPENCLAW_*` numeric env parsing in `testing_mcp/test_openclaw_gateway_url_preview.py`
- Skip persistent Serveo setup when `--public-url` is already explicit
- Add Cloud Build poll headroom above the 15 minute build timeout

## Status
Completed on branch `tailscale_pub`.

## Verification
- `WORLDAI_DEV_MODE=true python3 -m unittest testing_mcp.test_openclaw_gateway_url_preview_helpers`
- `python3 -m py_compile testing_mcp/test_openclaw_gateway_url_preview.py testing_mcp/test_openclaw_gateway_url_preview_helpers.py`
- YAML parse of `.github/workflows/pr-preview.yml`
- Latest rerun stabilization loop:
  - `/tmp/pr5879_stabilize_20260311_123939/iter_1/testing_mcp.log`
  - `/tmp/pr5879_stabilize_20260311_123939/iter_1/testing_ui.log`
  - `/tmp/pr5879_stabilize_20260311_123939/iter_1/summary.txt`
- Latest evidence bundles:
  - `/tmp/worldarchitectai/tailscale_pub/openclaw_gateway_url_preview/latest/`
  - `/tmp/worldarchitect.ai/gcp_settings_test/run_1773258040/`

## Notes
- `bd` / beads MCP writes are currently blocked because the configured Dolt server at `127.0.0.1:3308` is unreachable in this worktree.
- Fallback tracking is recorded in this tracked `.beads/` note so the PR still carries issue context.
