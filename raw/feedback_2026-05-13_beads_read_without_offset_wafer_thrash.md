---
name: large-file-read-triggers-autocompact-thrashing
description: Reading files >100K bytes on context floors >80K triggers autocompact thrashing; .beads/issues.jsonl confirmed read without offset in GLM-5.1 session
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8fa5ad17-b269-4b9c-a078-3ec3124a921a
  bead: rev-wgtju
---

Reading files >100K bytes (~25K+ tokens) when context floor is already ~90K triggers autocompact thrashing: context fills to 180K → auto-compact → refills within 3 turns → repeat. Observed in BOTH regular Claude sessions AND wafer/GLM-5.1 (`claudew`) sessions. NOT backend-specific.

**Smoking gun #1:** `mvp_site/tests/test_rewards_engine.py` is 188,647 bytes (~47K tokens). One Read consumes 26% of the 180K window on top of the ~90K floor.

**Smoking gun #2 (confirmed 2026-05-13):** `.beads/issues.jsonl` at **1,044,983 bytes** read with NO `offset` or `limit` in a GLM-5.1 (wafer) session on the `worktree-location-freeze` project. Evidence:
- Session: `~/.claude/projects/-Users-jleechan-projects-worktree-location-freeze/c03c7cd8-ad2a-4107-b27b-6ef0a5fd4635.jsonl`
- Model confirmed: `GLM-5.1` (`<synthetic>`)
- Read call: `{"name": "Read", "input": {"file_path": ".../.beads/issues.jsonl"}}` — no offset, no limit
- Also unguarded: `test_freeze_time_choices.py` at 45,318 bytes in same session

**Why:** 90K floor + 1MB issues.jsonl = instant overflow on any context window. GLM-5.1's smaller window makes this worse than Anthropic models.

**How to apply:** Always use `offset`/`limit` parameters when reading files >50K bytes. Known large files that must NEVER be read whole:
- `.beads/issues.jsonl` — grep by bead ID or use offset/limit
- `mvp_site/world_logic.py` — 421KB/9890 lines; use Grep to locate function first
- Any `test_rewards_engine.py` or similar large test files

Check `wc -c <file>` before reading if file size is unknown. This applies to ALL Claude Code backends (claude, claudew/wafer, codex).
