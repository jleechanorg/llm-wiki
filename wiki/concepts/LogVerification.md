---
title: "Log Verification"
type: concept
tags: [testing, debugging, logs]
sources: [real-browser-settings-game-integration-test]
last_updated: 2026-04-08
---

Testing technique of validating behavior through server log inspection. The test verifies model switching works by:
1. Making requests with different model settings
2. Reading server logs
3. Asserting the correct model name appears in logs

This approach catches bugs where settings are persisted but not actually used at runtime.

## Wiki Connections
- [Real Browser Settings Game Integration Test] uses log verification
- Uses [logging_util] to get consistent log file paths
