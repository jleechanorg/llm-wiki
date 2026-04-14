# PR #2: Fix Claude ingestion to consume from message_queue

**Repo:** jleechanorg/bp-telemetry-core
**Merged:** 2025-11-29
**Author:** jleechan2015
**Stats:** +83/-73 in 17 files

## Summary
- Route Claude fast-path consumer to `telemetry:message_queue` (was `telemetry:events`) so it reads what hooks emit
- HTTP endpoint now enqueues into the same message queue to keep capture consistent
- AGENTS.md documents GH CLI PR workflow and notes CLAUDE.md defers here

## Raw Body
## Summary
- Route Claude fast-path consumer to `telemetry:message_queue` (was `telemetry:events`) so it reads what hooks emit
- HTTP endpoint now enqueues into the same message queue to keep capture consistent
- AGENTS.md documents GH CLI PR workflow and notes CLAUDE.md defers here

## Testing
- ./testing_integration/run_integration_tests.sh

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> Switch all producers/consumers from `telemetry:events` to `telemetry:message_queue`, update server/HTTP enqueue paths, and add minor robustness/logging/test tweaks.
> 
> - **Processing/Streams**:
>   - Route Claude and Cursor consumers/monitors to `TELEMETRY_MESSAGE_QUEUE_STREAM` (replacing `TELEMETRY_EVENTS_STREAM`) across `claude_code/event_consumer.py`, `cursor/event_consumer.py`, `cursor/session_monitor.py`, `cursor/database_monitor.py`, and `cursor/unified_cursor_monitor.py` (`EventQueuer`).
>   - Server initializes Claude consumer and HTTP endpoint to use `streams.message_queue`; `MessageQueueWriter` default `stream_type="message_queue"` used for hooks.
> - **Claude Consumer**:
>   - Minor loop enhancement with `iteration` counter for conditional backlog logging.
> - **Cursor Monitors**:
>   - More informative, non-fatal shutdown logging when closing DB connections (markdown/database monitors, workspace mapper).
> - **Tests/Integration**:
>   - Add/adjust integration tests for bug fixes and telemetry flows (`scripts/test_bug_fixes_integration.py`, `testing_integration/test_*`).
>   - Harden SQLite test helpers (validated table names, safer connects) and minor cleanup.
> - **Docs/Meta**:
>   - `AGENTS.md`: add GitHub CLI PR workflow; note `CLAUDE.md` defers here.
>   - `.beads/.gitignore`: clarify exclusion of merge artifacts.
>   - Minor cleanup in `queue_writer.py` (unused imports).
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit bba1930e83c5fdccc3fd2242b962261ab3603036. This will update automatically on new commits. Configure [here](https
