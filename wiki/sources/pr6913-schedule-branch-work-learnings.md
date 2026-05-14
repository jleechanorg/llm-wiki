# PR #6913 schedule_branch_work.sh — Learnings

**Source type**: feedback / engineering learnings
**Date**: 2026-05-13
**PR**: https://github.com/jleechanorg/worldarchitect.ai/pull/6913
**Branch**: chore/schedule-branch-work-wrappers

## Learning 1: Bash ANSI-C quoting inside double quotes

`$'\n'` ANSI-C sequences inside `"..."` are literal text, not newlines.

```bash
# WRONG
MSG="$MSG$'\n\n'suffix"   # produces literal $'\n\n'

# CORRECT
MSG+=$'\n\nsuffix'
MSG+=$'\n'"$VAR"
```

Bead: `rev-bmo6q` | Fix commit: `5d3c8c412`

## Learning 2: CodeRabbit evaluates stale SHA not current HEAD

CR may post CHANGES_REQUESTED based on an older commit when multiple commits land close together.
Always check which SHA CR's review mentions. Trigger re-review with `@coderabbitai review`.

Green Gate Gate-3 uses `ping-coderabbit` CI check status (not formal review state).
Gate-3 can PASS even when `reviewDecision=CHANGES_REQUESTED`.

Bead: `rev-3jjro`

## Learning 3: Beads issues.jsonl corruption modes

**Mode 1 (Doubling):** `br` auto-flush re-appends all records when `export_hashes` table stale after git merge.
Detected by `test_beads_issue_ids_are_unique` CI gate. Fixed via dedup in `b1fc0f4ee`.

**Mode 2 (Shrinking):** `orchestrated_pr_runner.py` uses `git checkout --ours .beads/issues.jsonl`
during conflict resolution. PR branch version (fewer entries) wins over main.

Fix for Mode 2: replace `--ours` with union merge + ID-based dedup.

Bead: `rev-teygr`
