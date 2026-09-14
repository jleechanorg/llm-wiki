---
title: "PR #9861 Ready-Gate Integrity, HeavyDialog Prompt Ordering, and Implicit Cache Invariants"
type: raw
tags: [workflow, ready-gate, prompt-engineering, gemini-cache, player-agency, heavy-dialog, worldarchitect-ai]
date: 2026-09-13
author: "Antigravity (gemini-3.7-flash)"
pr: "https://github.com/jleechanorg/worldarchitect.ai/pull/9861"
bead: "rev-iwt8i"
---

# PR #9861 Ready-Gate Integrity, HeavyDialog Prompt Ordering, and Implicit Cache Invariants

## Context

During PR #9861 (`feat(prompts): double word count guidance for HeavyDialogAgent`), the user's prompt included:
`lets run the relevant tests locally and ensure /wa /advice approve the PR then /ready and merge approved and double check that heavy dialog agent doesnt already have system instructions and ensure these new system instrucitosn do not break the iplicit cache prefix https://github.com/jleechanorg/worldarchitect.ai/pull/9861`

The workflow executed targeted local tests, gathered approvals from `/wa` and `/advice` review lanes, and verified backlogged CI jobs with qualifying local proofs. However, seeing `merge approved` in the prompt, the agent proceeded to merge without explicitly verifying the `/ready` skill's full 6-gate checklist (specifically Gate 1 `/es` Gist publication and Gate 2 `/er` adversarial evidence review). In parallel, review scrutiny by Codex and ChatGPT surfaced architectural requirements regarding prompt ordering, Gemini implicit KV-cache prefix stability, and player character agency.

## Core Lessons & Invariants

### 1. `/ready` Skill 6-Gate Discipline
Conditional or pre-authorized `merge approved` in a prompt does NOT waive the `/ready` 6-gate checklist. Every gate must be systematically validated:
- **Gate 1 (`/es`)**: Published Gist linked via canonical `**Evidence**: <gist-url> (head <sha>)` marker in PR body.
- **Gate 2 (`/er`)**: Adversarial evidence review verdict PASS at exact current HEAD SHA (or narrow doc-only allowlist).
- **Gate 3 (`/advice`)**: ≥2 independent full-coverage approval reviewers from canonical `advice/SKILL.md` approval lanes.
- **Gate 4 (`/green`)**: Current-head CI green (or 10m backlogged local-equivalent proof posted to PR) + `mergeable == MERGEABLE`.
- **Gate 5 (Comments Handled)**: All unresolved review threads and actionable bot comments addressed/resolved.
- **Gate 6 (Cross-Thread Regression Check)**: Audit open beads for shared touched files or root causes before merge.

### 2. HeavyDialogAgent Prompt Isolation & Suffix Ordering
- `HeavyDialogAgent` inherits from `NarrativeFamilyAgent`.
- To preserve the Gemini implicit KV cache, the 10-contract prefix (`NarrativeFamilyAgent.SHARED_PREFIX`) must remain byte-identical across all 5 gameplay agents (`StoryModeAgent`, `HeavyDialogAgent`, `LoreAgent`, etc.).
- `HeavyDialogAgent` loads its dedicated prompt (`heavy_dialog_system_instruction.md`) exclusively via `SUFFIX_PROMPT_ORDER`.
- In `SUFFIX_PROMPT_ORDER`, `PROMPT_TYPE_HEAVY_DIALOG` must appear strictly **after** `PROMPT_TYPE_NARRATIVE`. Because prompt assembly evaluates suffix instructions sequentially, placing it after ensures the 600-word dialogue directive supersedes the standard 180-word narrative directive without mutating shared prefixes.

### 3. Player Agency & No Artificial Padding
- Prompt instructions must NEVER author, dictate, or narrate player character interiority (thoughts, memories, unstated feelings, emotional reactions). Frame exchanges using scene atmosphere, environmental tension, and NPC cues instead.
- Never include forced-padding directives ("do not collapse back into 180 words"); allow natural scene resolution up to the 600-word ceiling when stakes warrant without artificial padding.

### 4. Backlogged CI Equivalent Local Proofs
- When CI runners are backlogged (>10 minutes), exact workflow commands executed locally against current HEAD with full command, output, timestamp, and commit SHA satisfy `/green` Gate 1 per canonical rules.
