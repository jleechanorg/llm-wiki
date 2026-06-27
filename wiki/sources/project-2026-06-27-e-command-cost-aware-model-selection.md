---
title: "/e slash command now encodes cost-aware model routing (2026-06-27)"
type: source
tags: [slash-command, model-selection, cost-optimization, claude-code, worldarchitect-ai]
date: 2026-06-27
source_file: ../../raw/project_2026-06-27_e_command_cost_aware_model_selection.md
---

## Summary

On 2026-06-27, PR #7974 added a `## 💰 MODEL SELECTION (cost-aware execution)` section to `.claude_reference/commands/e.md` (and the mirror copy at `~/.claude/commands/e.md`) so every `/e` invocation biases subagent selection toward the cheapest coding tier that can complete the task correctly. Premium tiers (Opus / GPT-large) are reserved for hard architectural reasoning, ambiguous debugging, or where cheaper tiers have demonstrably failed. Both repo and home copies are in sync at main SHA `f692d2184f`.

## Key Claims

- The `/e` slash command previously delegated to `/execute` with no model-tier guidance, so the default behavior was to reach for premium tiers (Opus / GPT-large) even for well-scoped tasks.
- The new MODEL SELECTION section establishes cheaper-model-by-default as the routing rule with explicit per-family guidance: Haiku / Sonnet / Opus for Claude; Codex Spark / GPT-medium / GPT-large for Codex; Cerebras / Gemini Flash / GLM-5.1 / wafer.ai for high-volume work.
- The decision rule is explicit: "well-scoped task → cheapest tier that can complete it; expensive tier ONLY when (1) cheaper tier demonstrably failed with evidence, OR (2) task requires cross-context synthesis cheaper tiers cannot handle."
- The change is prompt-text (not application routing code), so the executing model retains discretion per the explicit exception conditions. This is by design — the section nudges behavior rather than hard-enforcing it.
- Both `.claude_reference/commands/e.md` (repo canonical) and `~/.claude/commands/e.md` (user active) must stay in sync after any future edit.

## Key Quotes

> "If the task is well-scoped (clear inputs, deterministic output, no architectural ambiguity, single-file or small blast radius), pick the cheapest model that can complete it. Use a more expensive model ONLY when (1) the cheaper tier has demonstrably failed (with evidence), OR (2) the task requires cross-context synthesis that cheaper tiers cannot handle."

> "This guidance is binding for `/e` execution: do not pick Opus / GPT-large by reflex."

## Connections

- [[SlashCommandArchitecture]] — `/e` is part of the project's slash-command system; cost-aware routing is a behavioral nudge baked into a slash command, not application routing code.
- [[ModelTierRouting]] — Generic concept of routing between model tiers based on task complexity; this PR instantiates the principle in a specific slash command.
- [[CostAwareDevelopment]] — Project-wide effort to reduce token spend by avoiding premium-tier reflex on well-scoped tasks.
- [[WorldarchitectAiWorkflow]] — The repo in which this guidance lives (`.claude_reference/commands/e.md`) and the home mirror (`~/.claude/commands/e.md`).
- [[MergeSafetyPolicy]] — The change was driven through the full /goal → PR #7974 → /green → MERGE APPROVED → merge → copy-to-~/.claude cycle, which exercises the explicit-trigger merge safety policy.

## Verification

```bash
git log origin/main -1 --format='%H %s'
# f692d2184f73b4940b2126dd1d0a0e01a822e6a1 chore(/e command): add cost-aware model selection guidance (#7974)
diff -q .claude_reference/commands/e.md ~/.claude/commands/e.md
# (no output = identical)
```

7-green verification: Green Gate pass (run 28286834146), CodeRabbit pass, all CI checks pass, mergeable=MERGEABLE at pre-merge head `bf6d5a46fc`.
