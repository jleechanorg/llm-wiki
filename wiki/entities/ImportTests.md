---
title: "Import Tests"
type: entity
tags: [testing, module-validation]
sources: []
last_updated: 2026-04-08
---

Import tests are unit tests that verify module dependencies are available and properly structured. These tests catch missing imports, module API inconsistencies, and dependency issues early in the development cycle.

## Purpose
- Validate all application modules can be imported
- Verify expected attributes/classes exist in each module
- Prevent runtime ImportError exceptions
- Serve as a smoke test for the application stack

## Test Coverage
- [[FirestoreService]] — add_story_entry, create_campaign
- [[LLMService]] — continue_story
- [[Main]] — create_app (Flask factory)
- [[GameState]] — GameState class
- [[Constants]] — structured field constants
- [[StructuredFieldsUtils]] — extract_structured_fields
- [[NarrativeResponseSchema]] — NarrativeResponse
- [[LLMResponse]] — LLMResponse
