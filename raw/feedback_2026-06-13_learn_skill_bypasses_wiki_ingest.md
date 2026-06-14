---
name: learn-skill-bypasses-wiki-ingest
description: "/learn skill step 6 caused agents to direct-Write wiki files instead of calling Skill(\"wiki-ingest\"); fixed 2026-06-13"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3853b8e4-b066-4445-8e0a-01431a88d4fa
---

# /learn skill step 6 was a manual-write trap

## What broke

`/learn` step 6 instructed the agent to "follow the wiki-ingest workflow"
with a 6-step manual procedure (copy to raw, create source page, update
index, append log, update concept/entity, oracle impact). The agent
treated this as license to write files directly via `Write` / `Edit` /
`cp` / `python3 <<EOF`.

When called from `/integrate` in non-llm_wiki worktrees, the agent knew
the global rule "Never write files directly to wiki/sources/" but
could not invoke `/wiki-ingest` as a slash command, so it fell back to
direct `Write`. The fallback violates the global rule AND skips the
entity/concept extraction that the real `wiki-ingest` skill performs.

## Evidence

- `~/.claude/history.jsonl` — `/wiki-ingest` invoked 0 times; `/integrate`
  21 times; `/learn` 2 times (one of which was inside a dark-factory
  session with no wiki activity)
- Session `73be4e82` at `2026-06-13T20:10:09.543Z`:
  > "Now writing the source pages directly. Per the global rule 'Never
  > write files directly to wiki/sources/ ... Always route through the
  > /wiki-ingest workflow' — but `/wiki-ingest` is a slash command I can
  > [not] invoke:"
- 8 of 9 wiki source files written in June 2026 came from `/learn`
  post-`/integrate` cycles that did direct `Write` instead of
  `Skill("wiki-ingest")`. Only `alexiel-larion.md` came from a proper
  skill invocation.

## Fix applied

`~/.claude/skills/learn/SKILL.md` step 6 now:

1. Calls `Skill("wiki-ingest", args="<abs path to memory file>")`
   instead of describing manual steps.
2. Lists the four required side-effects so the agent can verify.
3. **Explicitly forbids the direct-Write fallback** — if the skill
   errors, surface to user and stop.
4. Documents the working-directory caveat: pass absolute path; do not
   `cd ~/llm_wiki` first.

## Why it matters

Karpathy wiki pattern requires entity + concept extraction on every
ingest. Direct `Write` skips that. A 6-week audit of the 8 bypass
sessions showed 0 new entity pages and 0 new concept pages were
created — only flat source stubs. Entity/concept ratio dropped
measurably.

## How to apply

- If you ever see a session `Write` to `~/llm_wiki/wiki/sources/`
  directly (no `Skill("wiki-ingest")` call in the same turn), that's
  the same bug. Surface it; do not let the agent proceed.
- When spawning `/integrate` workers, tell them `/learn` step 6 now
  requires `Skill("wiki-ingest", args="...")` — no manual fallback.
- Verification: `grep -l '"wiki-ingest"' /Users/jleechan/.claude/projects/*/session.jsonl`
  should never be zero after an `/integrate` runs `/learn`.

## Backfill (2026-06-13, post-fix)

After fixing /learn step 6, dispatched 4 parallel subagents to backfill
24 memory files that should have been wiki-ingested during their
respective /integrate + /learn sessions:

- `aa3d24cb` (5 files, 6/12 + 6/13 worktree_level_quick)
- `a92b7c73` (5 files, 6/13 worktree_runner23423 claw/colima)
- `ab82ca8c` (5+1 files, 6/13 worktree_runner23423 runner/claw)
- `a10dd752` (9 files, 5/24 + 5/28 + 6/5 + 6/13 venv)

Result: 24 ingested, 1 skipped (already canonical), 0 errors. 4 prior
stubs (mikey-routing, colima-completed, pr7048, pr7249, pr7522) were
upgraded to canonical pages with proper frontmatter and `[[wikilinks]]`.
Wiki source count: 28,351 → 28,374 (+23 net new pages).

**Why:** 2026-06-13 audit, 8 sessions, 0 entity/concept pages created
via the bypass. Manual `Write` doesn't trigger the karpathy
extraction pipeline.

**How to apply:** See [[wiki-ingest-must-be-skill-invocation]] and
[[karpathy-wiki-pattern-enforcement]].
