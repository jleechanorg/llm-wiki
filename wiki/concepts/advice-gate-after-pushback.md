---
title: "AdviceGateAfterPushback"
type: concept
tags: [validation, advice, swarm, anti-pattern, harness]
last_updated: 2026-08-12
---

# /advice Gate After Two User Pushbacks

When the user pushes back twice on the same investigation, dispatch `/advice` BEFORE the next "verified" claim. Three reviewers (Opus subagent + /research + /secondo) catch intra-model blind spots that same-model reviews structurally cannot.

**Trigger:** 2 user pushbacks on a single investigation → STOP claiming "done" → dispatch `/advice` → spot-check the most concrete finding yourself (rule 12 of swarm skill) → only then claim "verified".

**Why:** The 2026-08-12 token-burn investigation produced three wrong conclusions in one session:
1. Treated ccusage cost as actual billing
2. Assumed MiniMax = free because ccusage showed $0
3. Cited file:line without `grep -n` verification

The third error was caught by `/advice` Reviewer A's `THIRD_ERROR` field before it shipped in a memory entry that future sessions would have inherited. Without the gate, all three errors would have been memorialized as correct.

**Cost of skipping:** User trust erosion + rework + a memory entry perpetuating the error across sessions. ~$0 direct cost (Max is flat fee) but lots of compounding downside.

**Pattern:** `/advice` = token-efficient second opinion (~5K tokens vs ~80-140K for advisor()). Three reviewers in parallel. Survive on ≥2/3 non-refutations (rule 2 of swarm skill). Cross-model cold review is MANDATORY for any "verified" claim (rule 12).

**Sources:** [[feedback-2026-08-12-token-burn-investigation-learnings]], ~/.claude/skills/advice/SKILL.md, ~/.claude/skills/swarm/SKILL.md rule 12.