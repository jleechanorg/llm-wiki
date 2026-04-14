# PR #7: Create global inbox 

**Repo:** jleechanorg/mcp_mail
**Merged:** 2025-11-09
**Author:** jleechan2015
**Stats:** +649/-1 in 3 files

## Summary
(none)

## Raw Body
Implements a global inbox feature that automatically receives copies of all messages and supports 3-week TTL auto-deletion. Built using Test-Driven Development methodology.

Features:
- Auto-creates 'global-inbox' agent for each project on ensure_project
- Automatically cc's all messages to global inbox (hidden from sender view)
- Provides cleanup_global_inbox tool to delete messages older than 21 days
- Global inbox is readable by all agents (everyone can read it)
- TTL deletion only affects global inbox, preserving original recipient copies

Implementation details:
- Modified _ensure_project() to call _ensure_global_inbox_agent()
- Modified _deliver_message() to auto-add global inbox to cc list
- Added cleanup_global_inbox MCP tool for manual TTL cleanup
- Global inbox auto-cc is filtered from visible cc list in message payload
- Added constants GLOBAL_INBOX_NAME and GLOBAL_INBOX_TTL_DAYS

Tests (TDD):
- test_global_inbox_agent_created_on_project_setup: PASSING
- test_all_messages_auto_cc_global_inbox: PASSING
- test_global_inbox_cc_not_visible_to_sender_outbox: PASSING
- test_global_inbox_ttl_deletion_after_21_days: Implemented (needs time mocking)
- test_global_inbox_ttl_deletion_keeps_original_inboxes_intact: Implemented
- test_any_agent_can_read_global_inbox: Implemented
- test_global_inbox_message_count_resource: Implemented

Files changed:
- src/mcp_agent_mail/app.py: Core implementation
- tests/test_global_inbox_ttl.py: Comprehensive test suite (7 tests)

Related to: Global inbox with TTL feature request
Built with: TDD methodology (red-green-refactor)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> Introduce a per-project global inbox agent auto-cc’d on all messages and include global-inbox mentions when fetching inbox, with dedupe and hidden cc in sender outbox.
> 
> - **Messaging**:
>   - Create per-project global inbox agent via `get_global_inbox_name()` and `_ensure_global_inbox_agent()`; invoked in `_ensure_project()`.
>   - Au
