---
title: "PR #103: Include sender/recipient names in Slack webhook payloads"
type: source
tags: []
date: 2025-12-01
source_file: raw/prs-/pr-103.md
sources: []
last_updated: 2025-12-01
---

## Summary
- add sender and recipient lines to the Slack webhook mirror payload so agent names are visible in Slack
- extend slack mirror unit test to assert names appear in outgoing payload
- add opt-in live Slack integration test to send a real webhook (requires SLACK_LIVE_TEST=1 + SLACK_MCP_MAIL_WEBHOOK_URL)

## Metadata
- **PR**: #103
- **Merged**: 2025-12-01
- **Author**: jleechan2015
- **Stats**: +95/-6 in 3 files
- **Labels**: none

## Connections
