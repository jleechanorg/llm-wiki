---
title: Skillify Always Calls Learn — Chain Rule
created: 2026-06-23
updated: 2026-06-23
type: source
tags: [wa-skillify, wa-learn, wa-soul, wa-process]
sources: [~/.hermes_prod/SOUL.md, ~/.claude/projects/-Users-jleechan--hermes-prod/memory/bestpractice_2026-06-23_skillify-always-calls-learn.md]
contradictions: []
---

# Skillify Always Calls Learn — The Chain Rule

A SOUL.md `## COMMIT` that enforces the `/skillify` + `/learn` chain. The
rule is the durable contract; this wiki page is the human-readable
explanation.

## What the rule says

When a session invokes `/skillify` (or `/sk`) to create or patch a skill, the
**same turn** MUST also run `/learn` to produce four additional artifacts:

1. A memory file at
   `~/.claude/projects/-Users-jleechan--hermes-prod/memory/<type>_YYYY-MM-DD_<slug>.md`
   (types: `bestpractice_`, `feedback_`, `project_`, `reference_`, `prompt_`,
   `tribal_`).
2. A roadmap entry appended to
   `~/roadmap/learnings-YYYY-MM.md` with the
   `- **Type**: feedback` and `- **Classification**: ✅ Best Practice`
   metadata block.
3. A `br` bead (default P4) tracking the learning, closed when the artifacts
   are in place.
4. A wiki source page at
   `~/llm_wiki/wiki/sources/<slug>.md` (Source Page Format) plus
   `index.md` and `log.md` entries under `~/llm_wiki/wiki/`.

The skill itself is item 0 — it is the `/skillify` output. The four items
above are the `/learn` output. Both halves land in the same turn.

## Why the chain exists

The skillify SKILL.md (Phase 0.5) explicitly distinguishes the two output
targets:

- **`/skillify` output** — the skill itself, routable, tested, auditable.
  Lives at `~/.hermes_prod/skills/<name>/`. The user (or another session)
  can invoke the skill by trigger phrase.
- **`/learn` output** — the durable record of the lesson. Lives in the
  memory file, the roadmap, the bead, the wiki source page. Future sessions
  can find the lesson by searching these artifacts without re-deriving it.

Prior sessions ran `/skillify` as the final step and treated the SKILL.md
as the sole durable record. The `/learn` half was silently dropped. The
result: future sessions searching `~/llm_wiki/sources/` or
`~/roadmap/learnings-*.md` found nothing about the lesson and re-derived it
from scratch. The fix is a SOUL.md `## COMMIT` so the chain fires on every
session via the session-init scan.

## The order rule

From `~/.hermes_prod/skills/skillify/SKILL.md` Phase 0.5:

- **`/learn` first, `/skillify` second** — when the lesson is class-level
  enough to be a skill. Capture the durable record first (so it exists even
  if the skillify pass later hits a tool-budget wall), then make the
  reusable shortcut.
- **`/skillify` first, `/learn` second** — when the user invokes
  `/skillify` explicitly. Do the skill first, then run `/learn` immediately
  in the same turn. Do not wait for the next turn.

Either order is acceptable. The rule is "both halves in the same turn, not
one-half-now-one-half-next-session."

## Verification

The closure summary of any `/skillify` invocation MUST include a `/learn`
checklist line showing all five outputs landed (or four + "deferred — user
opt-out"), with `ls` / `grep` / `br show` evidence in the same turn. This is
the "verification in the same turn as the claim" rule from
`~/.hermes_prod/skills/skillify/SKILL.md` (the "Claiming DONE" anti-pattern).

A paste-able verification block:

```bash
echo "1. SOUL.md COMMIT:  $(grep -c '^## COMMIT: skillify-always-calls-learn' ~/.hermes_prod/SOUL.md)/1"
echo "2. memory file:     $(test -f ~/.claude/projects/-Users-jleechan--hermes-prod/memory/bestpractice_2026-06-23_skillify-always-calls-learn.md && echo PRESENT || echo MISSING)"
echo "3. roadmap entry:   $(grep -c '/skillify always calls /learn' ~/roadmap/learnings-2026-06.md) match"
echo "4. wiki source:     $(test -f ~/llm_wiki/wiki/sources/skillify-always-calls-learn.md && echo PRESENT || echo MISSING)"
echo "5. br bead:         $(br show jleechan-7ncj --json 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin).get(\"status\",\"?\"))')"
```

If any of those returns MISSING, the `/learn` half is incomplete and the
skillify pass is not done. Close the bead (`br close jleechan-7ncj`) only
when all five return PRESENT.

## Sources

- `~/.hermes_prod/SOUL.md` `## COMMIT: skillify-always-calls-learn` (added
  2026-06-23)
- `~/.hermes_prod/skills/skillify/SKILL.md` Phase 0.5 (the canonical
  output-target contract this COMMIT enforces)
- `~/.claude/projects/-Users-jleechan--hermes-prod/memory/bestpractice_2026-06-23_skillify-always-calls-learn.md`
  (the memory file for this lesson)
- `~/roadmap/learnings-2026-06.md` 2026-06-23 entry (the roadmap entry)
- `br` bead `jleechan-7ncj` (the tracking bead)
- `~/.hermes_prod/skills/_learn/slack-mcp-routing-loop-2026-06-09-to-2026-06-11.md`
  (the format reference for new `/learn` outputs)
