# PR #9: docs: clarify OpenClaw git backup scope

**Repo:** jleechanorg/user_scope
**Merged:** 2026-03-11
**Author:** jleechan2015
**Stats:** +1/-0 in 1 files

## Summary
(none)

## Raw Body
## Summary\n- document current OpenClaw git backup scope\n- clarify that  is markdown-only in git\n- clarify that , , sqlite, and sensitive token/manifests stay out of git\n\n## Why\n- makes the backup policy explicit for review and CI workflows\n- reduces accidental re-introduction of runtime/private artifacts\n

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Low risk: documentation-only change that clarifies what gets included/excluded in git backups, with no functional or runtime impact.
> 
> **Overview**
> Clarifies the documented OpenClaw git backup policy by explicitly stating that `workspace/` is markdown-only (`*.md`) and that runtime/private artifacts (e.g., `memory/`, `media/`, `*.sqlite*`, tokens, manifests) are excluded from git backups.
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit fc3075d84e55590d21223aa4df573d69d1865b0f. This will update automatically on new commits. Configure [here](https://cursor.com/dashboard?tab=bugbot).</sup>
<!-- /CURSOR_SUMMARY -->
