# PR #5: docs: add OpenClaw context-window ASCII diagram

**Repo:** jleechanorg/smartclaw
**Merged:** 2026-03-30
**Author:** jleechan2015
**Stats:** +54/-0 in 1 files

## Summary
(none)

## Raw Body
## Summary\n- add a new markdown doc with an OpenClaw-vs-AO ASCII context-window comparison\n- replace the original Zoe/Codex framing with Jeffrey's real OpenClaw stack\n- include system-relevant elements: SOUL/AGENTS/TOOLS, memory files, launchd/cron, AO dispatch, and merge-gate targets\n\n## File\n- docs/OPENCLAW_CONTEXT_WINDOW_COMPARISON.md\n\n## Notes\n- this is documentation-only (no runtime behavior changes)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Documentation-only change with no impact to runtime behavior, APIs, or data handling.
> 
> **Overview**
> Adds a new doc, `docs/OPENCLAW_CONTEXT_WINDOW_COMPARISON.md`, with an ASCII side-by-side “context window” comparison of **OpenClaw** vs **AO workers**.
> 
> It also maps the split to `worldarchitect.ai` (business prioritization vs PR/CI execution) and documents strengths/risk zones plus a naming shift to *OpenClaw* (not Zoe).
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit 723dc031a7e2d589d6aa0bbe366c304a2d6d57a2. This will update automatically on new commits. Configure [here](https://cursor.com/dashboard?tab=bugbot).</sup>
<!-- /CURSOR_SUMMARY -->

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->
## Summary by CodeRabbit

* **Documentation**
  * Added a side-by-side comparison document outlining responsibilities and workflows for OPENCLAW (business orchestrator) vs AO WORKERS (execution agents).
  * Describes business vs delivery contexts, decision vs implementation roles, memory/operating history vs code/quality targets, and automation vs operational limits.
  * Lists capability strengths and risk zones for each system, includes a business–execution mapping with feedback loop and a naming/positioning note.
<!-- end of auto-generated comment: release notes by coderabbit.ai -->
