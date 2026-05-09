---
name: PR 6842 Root Cause — Flawed Dual-Condition CC Modal Guard
description: PR #6225 introduced cc_in_progress AND cc_completed guard that never fires for templates
type: feedback
bead: rev-kpm5u
---

PR #6842: Character creation modal soft-locked for God Mode/template campaigns. The backend correction guard required BOTH `character_creation_in_progress=True` AND `character_creation_completed=True`, but templates start with `completed=False` (they skip the manual creation flow), so the guard never fired.

**Breaking PR**: #6225 (Skip character creation modal for pre-populated templates). This PR introduced the flawed dual-condition while trying to fix template initialization, accidentally breaking the exit path.

**Lesson**: Modal exit guards must use OR logic, not AND, when one condition alone proves the modal should dismiss. `cc_in_progress=True` alone should be sufficient to clear the modal — adding `cc_completed=True` as a conjunct creates an impossible state for templates.

**How to apply**: When writing modal exit guards, always ask: "Is there a valid state where one condition is true but the other is false?" If yes, use OR. AND is only correct when both conditions are always simultaneously true.

**Verification**: PR #6842 adds `testing_mcp/core/test_godmode_cc_modal_exit_real_e2e.py` (Layer 3 MCP test).
