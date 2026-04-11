---
title: "Testing MCP Agent Instructions"
type: source
tags: [worldarchitect-ai, testing, mcp, infrastructure, tdd]
sources: []
date: 2026-04-07
source_file: raw/testing_mcp-agents.md
last_updated: 2026-04-07
---

## Summary
Defines mandatory testing standards for the WorldArchitect AI testing infrastructure. Enforces connection to real servers/Firebase/LLMs (no mocks), required use of MCPTestBase class, and loud failure signals. Establishes test file placement patterns and documents prohibited anti-patterns.

## Key Claims

- **NO MOCKS Rule**: All tests must connect to real servers, real Firebase, real LLMs. Introducing mocks invalidates tests.
- **LLM Trace Capture**: MCPTestBase automatically captures `llm_request_responses.jsonl`, `http_request_responses.jsonl`, and `gemini_http_request_responses.jsonl`.
- **MCPTestBase Required**: Every test using the MCP server must inherit from `testing_mcp.lib.base_test.MCPTestBase`. Standalone scripts are legacy.
- **Real Failure Signal**: Tests must fail loudly with specific assertion messages. Never catch exceptions silently or return `passed=True` on partial success.
- **No Utility Code Duplication**: If a helper exists in `testing_mcp/lib/`, use it. Do not reimplement `create_campaign`, `process_action`, `get_evidence_dir`, etc.

## Key Patterns

### Required Test Pattern

```python
class MyFeatureTest(MCPTestBase):
    TEST_NAME = "my_feature"
    MODEL = "gemini-3-flash-preview"
    DESCRIPTION = "Prove that X works correctly end-to-end"

    def run_scenarios(self, ctx: TestContext) -> list[dict[str, Any]]:
        errors: list[str] = []
        campaign_id = ctx.create_campaign(title="Test Campaign")
        # ... test logic ...
        return [{"name": "scenario", "passed": not errors, "errors": errors}]
```

### RED Test Pattern (TDD)

```python
if equipped_weapon and equipped_weapon not in display_names:
    errors.append(
        f"BUG: equipped_items.main_hand='{equipped_weapon}' not in "
        f"equipment_display"
    )
```

## File Placement

| Test Type | Location |
|---|---|
| Campaign creation/init | `testing_mcp/creation/` |
| Dice / RNG | `testing_mcp/dice/` |
| Faction minigame | `testing_mcp/faction/` |
| Schema validation | `testing_mcp/schema/` |
| Streaming | `testing_mcp/streaming/` |
| General integration | `testing_mcp/test_*.py` (root) |

## Prohibited Anti-Patterns

- Do NOT add `TESTING_AUTH_BYPASS=true` to run commands
- Do NOT import from `mvp_site/tests/` (wrong infrastructure)
- Do NOT use `unittest.mock`, `MagicMock`, or `patch()`
- Do NOT use `TEST_MODE=mock` or any mock env var
- Do NOT create new campaign_utils helpers without checking lib/ first
- Do NOT add `__init__.py` that imports test code (causes collection issues)

## Connections
- [[TestingMcpLib]] — base_test.py and helper modules
- [[WorldArchitectAI]] — the platform this testing infrastructure supports

## Contradictions
- None identified — this is foundational infrastructure documentation.