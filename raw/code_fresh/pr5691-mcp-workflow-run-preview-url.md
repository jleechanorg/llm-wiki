# Ensure MCP workflow_run smoke tests use preview server URL in PR comments

**Type:** bug
**Priority:** 1
**Status:** open
**Labels:** testing, ci, mcp, preview

## Summary

The MCP smoke test comment on `origin/main` shows `N/A` for service URL because the `workflow_run` path of `.github/workflows/mcp-smoke-tests.yml` runs mock smoke tests against local defaults and does not resolve/post a preview service URL.

## Context

- PR comment observed: https://github.com/jleechanorg/worldarchitect.ai/pull/5691#issuecomment-3941476773
- Title: `## ✅ [Mock] MCP Smoke Tests Passed`
- `SERVICE_URL` in workflow action output is blank in that run.

## Problem

- `workflow_run` trigger is used after preview deploy completion, but mock smoke test job still executes `scripts/mcp_smoke_test.sh` without explicitly setting `MCP_SERVER_URL` to the deployed preview endpoint.
- The comment formatter for `post-workflow-run-comment` is invoked without a `service_url` input in this path.
- Result: logs and comment can indicate local server behavior instead of preview deployment behavior.

## Desired outcome

- Resolve deployed preview service URL during `workflow_run` and export `MCP_SERVER_URL` before running mock tests.
- Pass the resolved URL through to comment output (`service_url`) in `post-workflow-run-comment`.
- Keep behavior deterministic across self-hosted and fallback jobs.

## Acceptance criteria

- `workflow_run` smoke test jobs in `mcp-smoke-tests.yml` populate service URL for PR comment payload.
- Mock MCP smoke test run after preview deploy points at the preview endpoint, not localhost.
- PR comment includes a non-empty preview `Server URL:` field.
- Regression check against `origin/main` does not reproduce `N/A` preview service display.

## Related

- PR #5691
- `.github/workflows/mcp-smoke-tests.yml`
