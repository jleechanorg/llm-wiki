---
name: design-exit-criteria-first-wiring
description: /design + superpowers brainstorming now do exit-criteria-first with batch-decision review; plugin-cache edit is volatile (bead jleechan-0bgw)
metadata: 
  node_type: memory
  type: feedback
  bead: jleechan-0bgw
  originSessionId: 8ae6304b-abed-40f7-af53-b55c903e8f67
---

**Context:** After the dark-factory cutover charter showed a rigorous-looking draft DoD had 20+
adversarially-findable loopholes, the user wired exit-criteria-first into the design toolchain
itself (2026-07-04, two parallel subagents, 6 files).

**What changed:**
- `~/.claude/commands/design.md` — new Phase 0: invoke `superpowers:brainstorming`, write exit
  criteria BEFORE any spec content. **Batch-decision mode (mandatory):** /design self-answers all
  brainstorming questions with recommended decisions (subagent or batched AskUserQuestion) and
  presents them ALL AT ONCE in one review table (decision | recommendation | rationale | rejected
  alternative) — zero one-by-one questioning.
- `~/.claude/skills/design-doc/SKILL.md` — same Phase 0 + batch mode; product-spec skeleton now
  leads with `## Exit Criteria`; old Phase 0 renamed Phase 0.5.
- `~/.claude/skills/design/SKILL.md` — Phase 0 (exit criteria + brainstorming), no batch mode.
- `~/.claude/skills/spec-design-docs/SKILL.md` — no-code spec's FIRST section must be Exit
  criteria; stage-1 adversarial gate must check criteria are game-proof (mock/dry-run/
  implementer-artifact satisfiability review); batch-review checkpoint is the gate's input.
- `~/.claude/plugins/cache/claude-plugins-official/superpowers/5.0.7/skills/brainstorming/SKILL.md`
  + `~/.claude/skills/tessl__brainstorming/SKILL.md` — exit criteria are a REQUIRED exploration
  area; resulting spec leads with Exit Criteria section.

**Exit-criteria bar (all files cite `~/projects/dark-factory/docs/cutover-exit-criteria.md`):**
binary, executable, externally anchored; implementer-authored artifacts corroborating never
sufficient; verifier reproduces rather than inspects; mock/dry-run satisfaction = FAIL; default
verdict FAIL.

**Volatility warning:** the superpowers plugin-cache path is version-keyed — an update to 5.0.8+
wipes the edit. Durable mirror: tessl__brainstorming. Re-apply per bead jleechan-0bgw.

**Why:** Goodhart — any spec written before its done-criteria optimizes proxies; and serial
question-asking wastes the operator's attention when the model can recommend and batch.

**How to apply:** any /design or brainstorming flow must produce the Exit Criteria section first;
if the plugin skill lacks the exit-criteria bullets after an update, re-apply from the mirror.
Related: [[cutover-exit-criteria-charter]], [[factory-lite-decommission-decision]].
