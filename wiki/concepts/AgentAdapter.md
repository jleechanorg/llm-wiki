---
title: "Agent Adapter"
type: concept
tags: [configuration, integration, agents]
sources: []
last_updated: 2026-04-07
---

An agent adapter is a configuration component that maps orchestrator requests to specific AI agents. The benchmark revealed a critical issue with Ralph's codex adapter not being properly registered.

## Issue Details
- **Error**: `KeyError: 'codex'` in agent mapping
- **Root Cause**: Codex adapter created but not registered in agent mapping
- **Impact**: Ralph unable to use Codex for fair comparison
- **Workaround**: Claude fallback used for subsequent projects

## Lessons Learned
- Agent configuration validation required as pre-flight check
- Graceful fallbacks needed when primary agents fail
- Registration流程 must be validated before benchmark execution
