---
title: "Standard Bead Follow-up Templates (PR/Code Review → Beads)"
type: source
tags: [bead-followup, pr-review, code-standards, handoff, worldarchitect-ai, pr-7467]
date: 2026-06-12
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-worktree_level_quick/memory/feedback_2026-06-12_bead_followup_templates.md
---

## Summary
PR/code-review findings turned into beads should be actionable implementation handoffs, not just issue summaries. Each bead should include exact PR/head/file-line evidence, severity and safe-fix ranking, module ownership boundary, exact implementation instructions, API/function signatures with call-site examples, and objective acceptance criteria. Created user-scope skill at `~/.claude/skills/bead-followup-templates/SKILL.md`.

## Key Claims
- Each bead must include: PR/head/file-line evidence, severity and safe-fix ranking, module ownership boundary, exact implementation instructions, API/function signatures, call-site examples, acceptance criteria (`rg` checks, targeted tests, `/es` evidence when production `mvp_site/**` behavior is affected).
- Created user-scope skill: `/Users/jleechan/.claude/skills/bead-followup-templates/SKILL.md`.
- Created Codex-visible pointer: `/Users/jleechan/.codex/skills/bead-followup-templates` → `/Users/jleechan/.claude/skills/bead-followup-templates`.
- In worktrees, use `br --no-auto-flush` and avoid shared `--external-ref` collisions by putting PR URLs in the body when multiple beads come from the same PR.
- Triggered by: make beads for follow-ups, blockers, safe fixes, `/code-standards` violations, or implementation handoff.

## Key Quotes
> "When PR/code-review findings are turned into beads, the beads should be actionable implementation handoffs, not just issue summaries."

## Connections
- [[BeadFollowupTemplates]] — durable skill for follow-up beads
- [[CodeStandards]] — review findings → safe-fix ranking
- [[PRReviewDiscipline]] — review evidence chain
- [[WorktreeWorkflow]] — `br --no-auto-flush` in worktrees
