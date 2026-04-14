# PR #9: fix: enhance metadata-updater hook with guardrails and parsing

**Repo:** jleechanorg/smartclaw
**Merged:** 2026-04-03
**Author:** jleechan2015
**Stats:** +91/-27 in 3 files

## Summary
- Add hook_event detection to distinguish PreToolUse vs PostToolUse hooks
- Strip leading cd and env variable prefixes from commands
- Add [agento] prefix guardrail on gh pr create titles
- Add gh pr merge guardrail to block agent-triggered merges by default
- Fix sed escaping bug

🤖 Generated with Claude Code

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Adds enforcement that can deny `gh pr create`/`gh pr merge` executions and changes merge-detection parsing, which could block wo

## Raw Body
## Summary
- Add hook_event detection to distinguish PreToolUse vs PostToolUse hooks
- Strip leading cd and env variable prefixes from commands
- Add [agento] prefix guardrail on gh pr create titles
- Add gh pr merge guardrail to block agent-triggered merges by default
- Fix sed escaping bug

🤖 Generated with Claude Code

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Adds enforcement that can deny `gh pr create`/`gh pr merge` executions and changes merge-detection parsing, which could block workflows if patterns misfire; otherwise changes are localized to hook scripts and docs.
> 
> **Overview**
> Strengthens the `.claude/metadata-updater.sh` hook by adding **PreToolUse enforcement**: denies `gh pr create` unless the title starts with `[agento]`, and blocks agent-triggered `gh pr merge` by default (with improved detection even when commands are chained via `&&`/`;`).
> 
> Improves robustness of metadata writing by fixing `sed` escaping for `|` in values and updating merge-status marking to run **PostToolUse only** after a detected successful merge. Updates `.claude/settings.json` to run the hook on **both** `PreToolUse` and `PostToolUse`, and expands `README.md` with documentation for a daily harness analyzer and updated repo overview copy.
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit 9b6a353ea64f31cd56a00c7a443da6efa9f07501. This will update automatically on new commits. Configure [here](https://cursor.com/dashboard?tab=bugbot).</sup>
<!-- /CURSOR_SUMMARY -->

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->
## Summary by CodeRabbit

* **Chores**
  * Added a new pre-execution hook and adjusted the post-execution hook configuration and formatting for metadata handling.

* **Bug Fixes**
  * Tightened merge detection and blocking to catch merged commands in chained positions and prevent merges during pre-execution.
  * Metadata marking now runs only after execution.
  * Improved metadat
