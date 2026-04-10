---
title: "Input Validation"
type: concept
tags: [security, validation, sanitization]
sources: [worldai-tools-mcp-proxy-tests]
last_updated: 2026-04-08
---

## Description
Security practice of sanitizing user inputs to prevent injection attacks. The MCP proxy validates:

1. **Service names**: Rejects characters like AND, OR, >= that could be used in injection
2. **Severity values**: Must be in known set (DEBUG, INFO, WARNING, ERROR, CRITICAL)
3. **Deploy tokens**: Format must be DEPLOY-{target}-{timestamp} with matching target

## Security Rationale
Prevents command injection in gcloud log queries and ensures deployment operations use properly formed confirm tokens.
