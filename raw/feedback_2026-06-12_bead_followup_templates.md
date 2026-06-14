# Feedback: Standard Bead Follow-up Templates

Date: 2026-06-12
Project: `/Users/jleechan/projects/worktree_level_quick`
Source PR: https://github.com/jleechanorg/worldarchitect.ai/pull/7467

## Learning

When PR/code-review findings are turned into beads, the beads should be actionable implementation handoffs, not just issue summaries. Each bead should include:

- the exact PR/head/file-line evidence that motivated the finding
- severity and safe-fix ranking
- the module ownership boundary
- exact implementation instructions
- actual API/function signatures and call-site examples
- objective acceptance criteria, including `rg` checks, targeted tests, and `/es` evidence when production `mvp_site/**` behavior is affected

## Durable Skill

Created user-scope Claude skill:

- `/Users/jleechan/.claude/skills/bead-followup-templates/SKILL.md`

Created Codex-visible pointer:

- `/Users/jleechan/.codex/skills/bead-followup-templates` -> `/Users/jleechan/.claude/skills/bead-followup-templates`

## Pattern

Use this skill when the user asks to make beads for follow-ups, blockers, safe fixes, `/code-standards` violations, or implementation handoff. In worktrees, create/update beads with `br --no-auto-flush` and avoid shared `--external-ref` collisions by putting PR URLs in the body when multiple beads come from the same PR.
