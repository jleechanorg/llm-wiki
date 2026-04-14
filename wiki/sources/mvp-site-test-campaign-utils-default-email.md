---
title: "test_campaign_utils_default_email.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Unit tests for campaign_utils DEFAULT_TEST_EMAIL behavior. Tests that when user_email is None, the X-Test-User-Email header is set to DEFAULT_TEST_EMAIL.

## Key Claims
- collect_route_stream_events uses DEFAULT_TEST_EMAIL when user_email is None
- post_streaming_request uses DEFAULT_TEST_EMAIL when user_email is None

## Connections
- [[campaign_utils]] — the module being tested