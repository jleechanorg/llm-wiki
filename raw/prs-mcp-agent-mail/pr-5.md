# PR #5: feat: Implement Phase 2 lazy loading meta-tools

**Repo:** jleechanorg/mcp_agent_mail
**Merged:** 2025-11-05
**Author:** jleechan2015
**Stats:** +377/-14 in 5 files

## Summary
(none)

## Raw Body
This commit implements Phase 2 of the lazy loading roadmap, adding meta-tools for dynamic tool discovery and invocation.

Changes:
- Add list_extended_tools tool to list all 19 extended tools with metadata
- Add call_extended_tool tool to dynamically invoke extended tools by name
- Populate _EXTENDED_TOOL_REGISTRY with all 19 extended tool functions
- Add MCP_TOOLS_MODE environment variable support to config.py
- Create comprehensive integration tests in tests/test_lazy_loading.py
- Update docs/LAZY_LOADING.md to reflect Phase 2 completion

Implementation details:
- list_extended_tools returns total count, tools by category, and full tool list
- call_extended_tool validates tool names and arguments, provides clear error messages
- Registry populated using post-registration approach (Option B from roadmap)
- All 27 tools remain exposed (no context savings yet - that's Phase 3)
- Zero breaking changes, fully backward compatible

Phase 2 Success Criteria (all met):
✅ list_extended_tools returns 19 tools with metadata ✅ call_extended_tool can invoke any extended tool
✅ All 19 extended tools in _EXTENDED_TOOL_REGISTRY ✅ Environment variable support added
✅ Integration tests created
✅ Documentation updated

Next: Phase 3 will implement conditional registration for actual context savings

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> Adds `list_extended_tools`/`call_extended_tool`, a registry for dynamic invocation, and runtime core vs extended tool exposure controlled by `MCP_TOOLS_MODE`, with docs and tests.
> 
> - **Server (FastMCP)**:
>   - **Meta-tools**: Add `list_extended_tools` (discovery) and `call_extended_tool` (proxy invocation) with instrumentation.
>   - **Dynamic registry**: Populate `_EXTENDED_TOOL_REGISTRY` for all 19 extended tools.
>   - **Lazy loading**: Conditionally expose tools based on `settings.tools_mode` (`core` hides extended tools via `mcp.remove_tool`; still accessible through meta-tools; `extended` exposes all).
> - **Config
