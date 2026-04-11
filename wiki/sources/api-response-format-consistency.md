---
title: "API Response Format Consistency Tests"
type: source
tags: [python, testing, unittest, api, response-format, backward-compatibility, frontend]
source_file: "raw/api-response-format-consistency.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest file ensuring all API endpoints maintain consistent response formats between legacy (main branch) format, new MCP format, and frontend expectations. Tests /api/campaigns endpoint for array vs object wrapper formats.

## Key Claims
- **Legacy Array Format**: GET /api/campaigns must return array directly for backward compatibility with JavaScript forEach
- **Object Format**: GET /api/campaigns/<id> returns {campaign, story, game_state} structure
- **Creation Format**: POST /api/campaigns returns {success, campaign_id} format
- **Firebase Mocking**: Uses FakeFirestoreClient for testing without real Firebase credentials
- **Auth Bypass**: Uses X-Test-Bypass-Auth header for test authentication

## Connections
- [[API Backward Compatibility Tests]] — related testing for legacy frontend compatibility
- [[FakeFirestoreClient]] — test infrastructure for Firebase mocking

## Contradictions
- None identified
