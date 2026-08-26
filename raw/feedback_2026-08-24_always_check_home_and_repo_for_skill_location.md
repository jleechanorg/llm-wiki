---
name: feedback-always-check-home-and-repo-for-skill-location
description: "When researching where a skill/command's real content lives, always check both ~/.claude/ (global canonical source) and the active repo's .claude/skills/ — a skill can be canonical-only in one location with no mirror in the other"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0cbd82d5-3c2c-49df-a555-91dd9e4cda6d
  modified: 2026-08-24T19:02:43.832Z
---

Discovered while building a jleechan-skills README (2026-08-24): `/research`'s
command file pointed to `~/.claude/skills/research/SKILL.md` (global, canonical),
but the jleechan-skills repo had NO copy at the standard `.claude/skills/research/`
location every other referenced skill uses — only a differently-named mirror at
`hermes/skills/research/SKILL.md`. A parallel research pass that checked only the
repo would have wrongly concluded the skill "doesn't exist in a standard location";
a pass that checked only `~` would have missed that the repo's own copy was
missing/inconsistent with the rest of the repo's skills.

**Why:** the user caught this directly ("where does it live? it should be in ~.
Remember to always check ~ and .claude") after I initially treated the repo's
absence of a standard-location copy as a full explanation, without confirming the
global source was in fact the correct, expected owner.

**How to apply:** whenever locating where a skill, command, or config actually
lives — especially before asserting "X doesn't exist" or "X is missing" — check
BOTH `~/.claude/` (or the relevant global home-directory location) AND the active
repo's own mirror location before concluding. A canonical source in one with a
missing or stale mirror in the other is a normal, easy-to-miss state, not a sign
the thing doesn't exist. Persisted as a standing rule in `~/.claude/CLAUDE.md`
under "Verify before reporting" via `/up --global` the same day this was learned.
