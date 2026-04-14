# Make mock-mode smoke tests target and report the same preview MCP URL

**Type:** bug
**Priority:** 1
**Status:** open
**Labels:** testing, ci, mcp, preview, mock-mode

## GOAL

Ensure `MCP_TEST_MODE=mock` smoke tests in preview CI use the same GCP preview MCP endpoint that `real` mode uses, and make the exact URL used observable in logs/comment artifacts.

## MODIFICATION

- Update the PR/workflow-run smoke path so when running mock mode it receives the resolved preview `MCP_SERVER_URL` and runs against that URL, not a local default.
- In mock-mode smoke execution, include evidence of the effective stream endpoint (for example `.../api/campaigns/<campaign>/interaction/stream`).
- Ensure the PR workflow comment receives and prints the non-empty service URL used by the mock run.

## NECESSITY

- Current behavior can run mock-mode checks against the wrong target after preview deploys, making CI feedback not representative of the deployed preview service.
- PR comments currently can miss the actual service URL, reducing traceability when failures are reported.

## INTEGRATION PROOF

- In CI smoke runs, mock and real modes should both report the same preview `https://...a.run.app` base URL (without localhost) in comments and debug output.
- Mock-mode streaming contract failures should include request evidence showing the final stream URL path for campaign interaction.
