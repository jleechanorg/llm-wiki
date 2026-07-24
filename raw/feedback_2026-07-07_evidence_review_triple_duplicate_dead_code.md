---
name: evidence-review-triple-duplicate-dead-code
description: "/er silently loaded a stale evidence-review skill for months — three files shared the same frontmatter name, and the command's file-resolution script never checked the path where the newest content actually lived"
metadata: 
  node_type: memory
  type: feedback
  bead: rev-e70ll (repo copy still needs a PR fix)
  originSessionId: ed376cb6-f347-4237-a510-b404c88d46f0
---

**The bug:** three separate files all declared `name: evidence-review` in frontmatter: (1) `~/.claude/skills/evidence-review/SKILL.md` (directory form, stale), (2) `~/.claude/skills/evidence-review.md` (user-scope flat file, the NEWEST version — had a "Two-Tier Integration with /green (added 2026-07-02)" section critical to how `/green` gates merges), (3) a repo-tracked `worldarchitect.ai/.claude/skills/evidence-review.md` (also stale, same vintage as #1). The `/er` command's Step 2 file-resolution bash script only checked paths #1 (user-scope directory) and #3-equivalent (repo-scope flat file) — it never checked path #2, the actual location of the newest content. Since #1 always existed, `/er` ALWAYS loaded the stale directory version; the `/green` two-tier integration improvements written into the flat file were dead code from the day they were written until this was caught during an unrelated skill-usage audit.

**Why this matters generally:** a skill/command update that lives in the "wrong" file (relative to what the loader/resolver actually checks) is invisible-broken — no error, no warning, it just silently doesn't take effect. The usual signal that would catch this (someone testing the new behavior) can easily pass anyway if the OLD behavior is close enough to plausible, especially for a rarely-hit edge case like the PRODUCTION/NON_PRODUCTION tier distinction.

**Fix applied:** merged the newer flat-file content into the directory-form SKILL.md (matching this repo's dominant `<name>/SKILL.md` convention), archived the flat file. The repo-tracked stale copy (#3) needs a proper PR (not a dotfile edit) — tracked in bead `rev-e70ll`.

**How to apply:** when a command/skill has more than one file matching its declared name anywhere in scope (user-scope, repo-scope, plugin-scope), don't assume "the newest edit is the one being used" — trace the actual resolution/loader logic and confirm which physical path it reads. Two files claiming the same `name:` in frontmatter is itself a smell worth checking for whenever investigating "why doesn't this recent change seem to be taking effect."
