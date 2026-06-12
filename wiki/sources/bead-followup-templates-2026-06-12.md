---
title: Standard bead follow-up templates for executable review handoff
date: 2026-06-12
type: source
origin: worldarchitect.ai /learn
bead: rev-drhbu
tags: [beads, skills, pr-review, handoff, code-standards, evidence]
---

# Standard bead follow-up templates for executable review handoff

**Lesson:** Follow-up beads from PR/code-review work should be implementation handoffs, not vague TODOs. A future agent should be able to implement the bead by re-reading the named files and following the bead's explicit API/signature and acceptance-contract sections.

**Required bead content:**

- Source: PR URL, exact head SHA or commit URL, review/comment/thread URL, evidence path/log, and file/line references.
- Verified problem: one concrete paragraph explaining the blocker or gap.
- Implementation instructions: target files, module ownership, current API/function signatures copied from live code, expected call-site shape, constraints, non-goals, and forbidden paths.
- Acceptance criteria: exact `rg` checks, targeted tests, standards references, and `/es` evidence class when production `mvp_site/**` behavior is affected.
- Staleness note: signatures and file lines verified at a specific SHA; re-read before implementation.

**Durable skill:** `/Users/jleechan/.claude/skills/bead-followup-templates/SKILL.md`

**Codex pointer:** `/Users/jleechan/.codex/skills/bead-followup-templates`

**Related:** [[Beads]], [[AgentSkills]], [[WhatMakesAGitHubIssueReadyForCopilot]]
