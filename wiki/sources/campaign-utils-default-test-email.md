---
title: "Campaign Utils DEFAULT_TEST_EMAIL Behavior Tests"
type: source
tags: [python, testing, unittest, campaign-utils, testing-mcp]
source_file: "raw/test_campaign_utils_default_test_email.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest suite validating DEFAULT_TEST_EMAIL fallback behavior in campaign_utils.py functions. Tests ensure that when user_email is None, the X-Test-User-Email header is automatically set to a default test email, and that explicit user_email values are respected without override.

## Key Claims
- **Default Fallback**: When user_email is None, X-Test-User-Email header defaults to DEFAULT_TEST_EMAIL
- **Function Coverage**: Both collect_route_stream_events() and post_streaming_request() implement the fallback
- **Explicit Override**: When user_email is explicitly provided, it is used without fallback override
- **Header Propagation**: X-Test-User-Email header flows through urllib request headers

## Test Coverage
- test_collect_route_stream_events_uses_default_email_when_none
- test_post_streaming_request_uses_default_email_when_none  
- test_collect_route_stream_events_respects_explicit_email

## Connections
- [[TestingMCP]] — the library containing campaign_utils
- [[CampaignUtils]] — module with DEFAULT_TEST_EMAIL constant
