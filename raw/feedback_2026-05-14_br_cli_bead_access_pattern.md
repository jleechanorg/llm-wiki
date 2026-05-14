---
name: br-cli-bead-access-pattern
description: Always use br CLI (show/search/list) for bead lookups — never Read .beads/*.jsonl; beads.left.jsonl is 5MB and equally dangerous
metadata: 
  node_type: memory
  type: feedback
  bead: rev-1ivmd
  originSessionId: c508ff6e-e323-4bd8-be06-6e3e58a53894
---

Never read `.beads/issues.jsonl` or `.beads/beads.left.jsonl` raw. Use `br` CLI which queries `beads.db` (SQLite) directly.

**Why:** Research session (2026-05-14) measured issues.jsonl at 1.0MB and discovered `beads.left.jsonl` at **5.0MB, 15,447 lines** — a git-tracked legacy export that is 5× more dangerous. Both files fill context immediately when read without offset/limit, causing autocompact thrashing (see [[large-file-read-triggers-autocompact-thrashing]]).

**`br` CLI is complete — no JSONL read is ever necessary:**
- `br show <id>` — single bead detail
- `br search <term> --status open` — full-text search with filters
- `br list --status open --json` — filtered lists
- `br stats --json` — summary counts
- All queries hit `beads.db` (SQLite 5.7MB) which has all 1,208 beads

**Size breakdown of issues.jsonl (2026-05-14):**
- Total: 1.0MB, 1,239 records
- Open: 658 beads / 556.7KB
- Closed: 508 beads / 429.6KB (41% — archivable)
- In-progress: 32 beads / 31.2KB
- Other (tombstone/done/superseded): 41 / 34.6KB

**Why compaction is blocked:** `br sync --flush-only` re-exports the full DB including closed beads, so closed-bead archival would require a custom filter script. Not implemented.

**How to apply:**
- In any agent session: replace `Read .beads/issues.jsonl` with `br show <id>` or `br search`
- Never Read `.beads/beads.left.jsonl` — treat as unreadable legacy artifact
- If checking file size first: `wc -c .beads/issues.jsonl` returns ~1MB; `wc -c .beads/beads.left.jsonl` returns ~5MB

**References:**
- Root cause bead: rev-wgtju (unguarded Read proof from GLM-5.1 session)
- This learning bead: rev-1ivmd
- CLAUDE.md: `~/.claude/CLAUDE.md` — "Known large files — NEVER read whole" section
- Session JSONL: `~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/c508ff6e-e323-4bd8-be06-6e3e58a53894.jsonl`
