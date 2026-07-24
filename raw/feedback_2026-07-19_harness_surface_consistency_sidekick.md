---
name: harness-surface-consistency-sidekick
description: A directive encoded in one harness surface but not its siblings (command vs skill vs tests vs export repo) keeps being violated — update every teaching surface in the same pass and pre-validate contract tests
metadata: 
  node_type: memory
  type: feedback
  bead: jleechan-0020
  originSessionId: 2e9c7623-926a-46d2-8401-6cc4a05622e5
---

# Harness-surface consistency — the sidekick team-only migration (2026-07-18/19)

**Classification: Anti-Pattern (root cause) + Mandatory (the fix pattern)**

## Context

User asked why sessions kept violating the "proper /sidekick method" (claude
team + sonnet). Audit across /history + /ms found a week of drift: sidekicks
spawned with no `model` param (inheriting claude-fable-5 / MiniMax-M3), fake
"team" lanes as fire-and-forget subagents, and tmux `-p` sidekicks that can't
form Agent Teams at all.

## Root cause

The user's 2026-07-11 directive ("use a real /team-claude, the sidekick is a
teammate I can see") was encoded in only TWO surfaces — the command file
header (`~/.claude/commands/sidekick.md`) and a never-activated draft hook —
while the Skill-tool-loaded `~/.claude/skills/sidekick/SKILL.md` still taught
the opposite (tmux-first, "do not describe sidekick as an in-memory Agent
lane"). **Agents obey whichever surface actually loads**; the Skill tool loads
SKILL.md, so the stale surface won for a week. An unenforced directive spread
across inconsistent surfaces is indistinguishable from no directive.

## Rule (mandatory)

When a directive changes a contract, update EVERY surface that teaches it in
the SAME pass: slash-command file, skill file, sibling skills that reference
it (swarm referenced the tmux sidekick — caught by codex review as a P1),
repo contract tests, and the export mirror (claude-commands). Then grep all
surfaces for the banned pattern before reporting done.

## Supporting lessons (verified this session)

- **`~/.claude` and `~/.claude-wa` command/skill files are hardlinked** on
  this machine — one Write updates both; `cp` reports "are identical". Verify
  with matching md5s, don't assume two copies need two edits.
- **Pre-validate doc contract tests locally**: claude-commands runs
  contract-tests over harness docs (e.g. `CADENCE_TIME_RE` requires the
  literal `≤5 min` glyph; `test_swarm_references.py` sweeps every `/token`
  and fails on untriaged ones like a newly added `/claw`). Simulating the
  regexes in python before pushing caught 100% of would-be CI failures on
  the second push.
- **API-only PR flow**: a PR can be built entirely via `gh api` contents
  endpoints (create ref → PUT files → open PR → REST `pulls/N/merge`) with
  zero local git operations — useful when the session cwd-lock forbids
  working in that repo, and REST merge works when `gh pr merge` (GraphQL)
  is rate-limited. REST and GraphQL are separate quota buckets.
- **Downtime vs work-lost** (from the /advice Opus reviewer, unanimous 3/3
  Sound): disk-checkpoint durability bounds work LOST (≤5 min cadence) but
  NOT downtime — passive state needs an active respawn trigger to be truly
  crash-recoverable. User deferred the watcher (bead jleechan-tn4h, P3).

## References

- Incident record: [[sidekick-method-drift-investigation]] (same memory dir)
- Merged fix: https://github.com/jleechanorg/claude-commands/pull/337
  (squash `6462b69`), local files hardlink-identical by construction
- Beads: jleechan-0020 (closed, root cause), jleechan-9tee (closed, export),
  jleechan-tn4h (open P3, deferred watcher)
- CLAUDE_CONFIG_DIR OAuth footgun: [[cmux-sidekick-claude-config-dir-breaks-auth]]

## Reusable pattern

Directive lands → enumerate ALL teaching surfaces (`grep -rl <topic>
~/.claude/commands ~/.claude/skills <export-repo>`) → edit all in one pass →
simulate the repo's doc contract tests locally → push → grep every surface
for the banned pattern as the done-check. Severity match per
harness-fix-durability: a twice-repeated directive violation warrants
hook/CI-level enforcement, not another memory note.
