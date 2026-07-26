---
title: "Harness-surface consistency — sidekick team-only migration (2026-07-19)"
type: source
tags: [harness, skills, sidekick, agent-teams, process]
date: 2026-07-19
source_file: raw/feedback_2026-07-19_harness_surface_consistency_sidekick.md
---

## Summary

A week of "improper /sidekick" behavior traced to a single root cause: the user's 2026-07-11 team-only directive was encoded in the command-file header and a never-activated draft hook, while the Skill-tool-loaded SKILL.md still taught the opposite (tmux-first). Agents obey whichever surface actually loads, so the stale surface won until a 2026-07-18 audit reconciled every surface in one pass — command, skill, sibling swarm files, repo contract tests, and the claude-commands export mirror ([PR #337](https://github.com/jleechanorg/claude-commands/pull/337), merged `6462b69`).

## Key Claims

- An unenforced directive spread across inconsistent harness surfaces is indistinguishable from no directive; the Skill-loaded file is the one that wins in practice.
- Fix pattern: enumerate ALL teaching surfaces (`grep -rl <topic>` across commands/, skills/, export repo), edit in the SAME pass, simulate the repo's doc contract tests locally (literal-glyph regexes like `≤5 min`, slash-token sweeps), then grep every surface for the banned pattern as the done-check.
- `~/.claude` and `~/.claude-wa` command/skill files are hardlinked on this machine — one write updates both; verify with md5, don't double-edit.
- A PR can be built and merged entirely via GitHub contents API + REST merge (no local checkout), which also sidesteps GraphQL-bucket rate exhaustion since REST and GraphQL quotas are separate.
- Disk-checkpoint durability (STATE.md ≤5-min cadence + resumption bead) bounds work LOST, not DOWNTIME — passive state needs an active respawn trigger to be truly crash-recoverable (unanimous 3/3 /advice verdict; watcher deferred as bead jleechan-tn4h).

## Key Quotes

> "Agents obey whichever surface actually loads; the Skill tool loads SKILL.md, so the stale surface won for a week." — root-cause statement

> "Durable state is not continuous execution." — /advice Opus reviewer, PR #337

## Connections

- [[HarnessEngineering]] — this is a concrete instance of harness-surface auditing done reactively; the lesson argues for same-pass surface sync as a standing rule
- [[SkillStaleness]] — sibling failure class: there the probe was stale, here the whole skill contradicted the newer command surface
- [[EvidenceHarnessDiscipline]] — contract tests over harness docs (claude-commands contract-tests) are the enforcement layer that caught wording drift
- [[HarnessSurfaceConsistency]] — the generalized rule distilled from this incident
