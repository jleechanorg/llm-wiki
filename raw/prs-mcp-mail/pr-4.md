# PR #4: Fix agent registration schema mismatch

**Repo:** jleechanorg/mcp_mail
**Merged:** 2025-11-09
**Author:** jleechan2015
**Stats:** +153/-5 in 6 files

## Summary
(none)

## Raw Body
## Problem

All agent registration attempts were failing with a misleading error message:
```
Error calling tool 'register_agent': Agent name 'X' is already in use globally (race condition detected). Please try again.
```

This occurred even for:
- Completely unique, randomly generated names
- Auto-generated names from the server
- Any new agent registration attempt

**Impact**: Codex and all other AI agents could not register with the MCP Agent Mail server, completely blocking multi-agent coordination.

## Root Cause

Schema mismatch between the database and source code:
- **Database**: Has `contact_policy` column (VARCHAR(16), NOT NULL)
- **Source Code**: The `Agent` SQLModel was missing the `contact_policy` field
- **Result**: SQLite raised `IntegrityError: NOT NULL constraint failed`, which was caught and incorrectly reported as a "race condition"

The error handling at `app.py:1272-1280` catches `IntegrityError` and assumes it's due to name conflicts, producing the misleading error message.

## Solution

Added the missing `contact_policy` field to the `Agent` model:
```python
# src/mcp_agent_mail/models.py:42
contact_policy: str = Field(default="auto", max_length=16)
```

## Testing

Verified fix with multiple scenarios:

**Test 1: Explicit name registration**
```
✅ SUCCESS! Agent ID: 127, Name: TestClaudeAgent
```

**Test 2: Auto-generated name**
```
✅ SUCCESS! Agent ID: 128, Name: LilacSnow
```

**Test 3: Codex registration scenario**
```
✅ SUCCESS! Agent ID: 126, Name: codexd
```

## Files Changed

- `src/mcp_agent_mail/models.py` - Added contact_policy field to Agent model
- `pyproject.toml` - Bumped version to 0.1.2
- `uv.lock` - Updated dependencies

## Notes

- This fix unblocks all agent registration
- Existing agents with NULL contact_policy values may need migration handling
- Consider improving error messages to distinguish between actual race conditions and schema issues

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SU
