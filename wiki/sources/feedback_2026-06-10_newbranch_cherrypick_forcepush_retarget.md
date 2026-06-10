---
type: source
slug: feedback_2026-06-10_newbranch_cherrypick_forcepush_retarget
ingested: 2026-06-10
source: ~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-10_newbranch_cherrypick_forcepush_retarget.md
---

# Source: /newb + cherry-pick + force-push retarget recipe

Trigger condition: `gh pr diff <N> --stat` shows >>2× expected files, `git diff origin/main -- <expected-files>` is empty (file changes are merge pollution, not real work).

Recipe:
1. `/newb <clean-name>` (script normalizes `/` → `-`)
2. `git cherry-pick <sha1>..<shaN>` (or auto-detected by script)
3. Commit refactor closure (e.g., shared-module extraction)
4. `git push --force-with-lease origin <clean>:<old-polluted>` (REQUIRES explicit human approval; lease form fails safely on concurrent force-push)

`gh pr edit --head` does NOT exist — force-push is the ONLY retarget path. Result: clean 7-file diff on the OLD branch name; PR #, review history, issue link preserved.

See memory file for the PR #7386 case study (36-file → 7-file).
