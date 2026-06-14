---
name: cr-unresolved-orphan
description: "CodeRabbit issue-summary comment can include outdated/unresolved counts; check each comment's body for \"✅ Addressed\" before acting on summary"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 11b18814-6b01-49a8-a167-12c66b99835e
---

CodeRabbit's PR-level issue summary comment (e.g. https://github.com/jleechanorg/worldarchitect.ai/pull/7467#issuecomment-4685201983) lists "X open comments" with severity. **This number can be stale** — comments may have been marked "✅ Addressed" by a follow-up review but not removed from the open count.

**Pattern to verify before dispatching fix subagents:**

1. List all PR comments with `gh api repos/.../pulls/N/comments`
2. Filter `c.user.login == "coderabbitai[bot]"` AND `c.in_reply_to_id is None` (top-level only)
3. Check each body for `✅ Addressed in commit <sha>` marker
4. Comments with that marker are resolved — do NOT act on them
5. Comments without it that are on files the PR didn't modify are **stale orphans** (CodeRabbit reused an old review thread)

**Concrete PR #7467 example (2026-06-11):**
- Issue comment said: "8 open review comments" with 4 Major in agents.py/rewards_engine.py/world_logic.py
- Reality: 7 of 8 are marked `✅ Addressed` in commits f8a6a97/57b25cf/eca8ad5/13b2dac
- 1 remaining (scripts/test_determine_smoke_mode.sh:20) is a stale orphan from PR #7242 — #7467 doesn't touch that file
- All 5 actual code issues genuinely fixed; 914 tests pass, 7 skipped, 0 failed

**Why:** Issue-summary comments are not auto-refreshed when CodeRabbit re-reviews. Acting on the summary count wastes subagent time re-fixing already-fixed code.

**How to apply:** When user says "handle with subagents" + links to a CR issue comment, run the 5-step verification above FIRST. If most comments are marked Addressed, skip subagent dispatch and report the resolution status to the user.
