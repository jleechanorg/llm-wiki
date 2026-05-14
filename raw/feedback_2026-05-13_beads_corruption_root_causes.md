---
name: beads-corruption-root-causes
description: Two modes of .beads/issues.jsonl corruption — doubling (br auto-flush) and shrinking (--ours conflict resolution)
type: feedback
bead: rev-teygr
---

`.beads/issues.jsonl` corruption has two distinct modes:

**Mode 1 — Doubling:** `br` CLI auto-flush appends all DB records when `export_hashes`
table is stale after a git merge changes the JSONL hash. All records get re-appended,
causing duplicates. The `test_beads_issue_ids_are_unique` CI test catches this.
Fix: `b1fc0f4ee` deduped 1234 duplicate entries in PR #6913.

**Mode 2 — Shrinking:** `automation/jleechanorg_pr_automation/orchestrated_pr_runner.py`
uses `git checkout --ours .beads/issues.jsonl` during conflict resolution. The PR branch
version of `issues.jsonl` typically has fewer entries than main, causing data loss.

**Root cause:** `issues.jsonl` is git-tracked; `beads.db` (SQLite) is not. Git merges
create conflicts; conflict resolution strategies determine which version wins.

**Recommended fix for Mode 2:** Replace `--ours` strategy in orchestrated_pr_runner.py
with a union merge or a script that deduplicates by ID after merge.

**References:**
- PR #6913: https://github.com/jleechanorg/worldarchitect.ai/pull/6913
- Dedup fix commit: `b1fc0f4ee`
- Mode 2 source: `automation/jleechanorg_pr_automation/orchestrated_pr_runner.py`
