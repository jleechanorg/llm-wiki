---
title: "DefaultTestEmailFallback"
type: concept
tags: [testing, headers, fallback]
sources: []
last_updated: 2026-04-08
---

Pattern in campaign_utils where X-Test-User-Email header defaults to DEFAULT_TEST_EMAIL when user_email parameter is None, ensuring test requests always have a valid test user email header.
