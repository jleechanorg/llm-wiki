---
title: "test_basic_validation.py"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/test_basic_validation.py
---

## Summary
Basic validation test for Real-Mode Testing Framework integration. Tests core functionality without external dependencies: service provider creation, mode switching (mock/real), global provider management, backward compatibility, and mock service operations (Firestore, Gemini, Auth).

## Key Claims
- Testing framework should create mock and real service providers
- Service providers expose firestore, gemini, and auth services
- Mock mode should have is_real_service = False
- Global provider should return same instance until reset
- get_test_client_for_mode() provides backward compatibility
- Integration_utils provides fallback when unavailable
- Mock Firestore operations work without errors
- Mock Gemini operations generate content without errors

## Key Connections
- [[mvp-site-testing-framework]] — Test factory module
- [[mvp-site-testing-factory-fixtures]] — Test client helpers
- [[mvp-site-integration-utils]] — Integration utilities

## Test Structure
- TestBasicFramework: service provider creation, mode switching, global provider management
- TestBackwardCompatibility: get_test_client_helper, integration_utils import
- TestServiceOperations: mock Firestore, Gemini, and Auth operations

## Related Sources
- [[mvp-site-test-base-test-provenance]] — MCPTestBase provenance tests
- [[mvp-site-mvp-site-testing-mcp]] — Testing MCP system