---
title: "test_campaign_clicks.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Tests for campaign list click functionality - verifies CSS and JavaScript click handler improvements.

## Key Claims
- Campaign items have data attributes for clicking
- CSS file `campaign-click-fix.css` exists with `.campaign-title-link`, `cursor: pointer`, `.list-group-item[data-campaign-id]`
- JavaScript has click handler with `e.stopPropagation()`, opacity change, and `handleRouteChange()`
- index.html includes the campaign click fix CSS with `data-async-css`

## Connections
- [[frontend_v1]] — frontend components being tested