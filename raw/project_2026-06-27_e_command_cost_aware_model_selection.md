---
name: e-slash-command-now-encodes-cost-aware-model-routing-2026-06-27
description: PR
metadata: 
  node_type: memory
  type: project
  bead: none
  originSessionId: 169b8d9c-b8cb-4247-beff-46c5f2ecac37
---

The `/e` slash command in `.claude_reference/commands/e.md` was extended with a new `## 💰 MODEL SELECTION (cost-aware execution)` section on 2026-06-27. Before that change, `/e` delegated straight to `/execute` (planning → auto-approval → implementation) with no guidance on which model tier to use when fanning work out to subagents or pair-programming partners, so the default behavior was to reach for premium tiers (Opus for Claude, GPT-large for Codex) even for well-scoped tasks.

The new section establishes cheaper-model-by-default as the routing rule:

- **Claude family**: Haiku for quick reads / transforms / lint sweeps / deterministic mechanical edits; Sonnet for routine implementation / multi-file edits / test generation / conventional refactors; Opus reserved ONLY for genuinely hard architectural reasoning, cross-context synthesis, ambiguous debugging, or where Sonnet has demonstrably failed.
- **Codex family**: Codex Spark (or other GPT-medium variants) for fast code generation / scaffolding / mechanical edits; GPT-large reserved ONLY for hard architectural tasks where Codex Spark has demonstrably failed.
- **Other providers**: Cerebras / Gemini Flash / GLM-5.1 / wafer.ai preferred for high-volume mechanical code generation; premium tiers reserved for low-volume, high-stakes decisions.

The decision rule is explicit: "If the task is well-scoped (clear inputs, deterministic output, no architectural ambiguity, single-file or small blast radius), pick the cheapest model that can complete it. Use a more expensive model ONLY when (1) the cheaper tier has demonstrably failed (with evidence), OR (2) the task requires cross-context synthesis that cheaper tiers cannot handle." Plus a binding note: "This guidance is binding for `/e` execution: do not pick Opus / GPT-large by reflex."

**Why**: Recent memory entries (e.g., `feedback_2026-06-24_implicit_cache_advisor_review.md`, `feedback_2026-06-22_browserclaw_firefox_inverse_escape.md`) have shown that premium-tier reflex inflates cost without proportional quality gain on well-scoped tasks. Encoding the cheaper-by-default rule in `/e` itself ensures every `/e`-driven workflow inherits the preference.

**How to apply**:
- When `/e` is invoked, the executing model should now default to the cheapest coding tier that can complete the task correctly. Subagent selection (e.g., `claude-pair-coder` vs `cerebras-coder` vs `codex-pair-coder` vs `gemini-pair-coder`) should bias toward whichever provider's cheapest tier is available.
- The repo canonical copy is `.claude_reference/commands/e.md`; the user's active copy is `~/.claude/commands/e.md`. Both must stay in sync — after any future edit to the repo copy, copy to `~/.claude/commands/e.md`.
- The change is prompt-text (not application routing code), so the executing model retains discretion per the explicit exception conditions. This is by design — the section nudges behavior rather than hard-enforcing it.

**References**:
- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/7974
- Merge SHA on main: `f692d2184f73b4940b2126dd1d0a0e01a822e6a1`
- Pre-merge PR head: `bf6d5a46fcf9b5f5f16e12e5dfc9badc98ab41b2`
- File: `.claude_reference/commands/e.md` (+24 lines, additive, no deletions)
- Home copy verified: `diff -q .claude_reference/commands/e.md ~/.claude/commands/e.md` → no diff
- 7-green verification: Green Gate pass (run 28286834146), CodeRabbit pass, all CI checks pass, mergeable=MERGEABLE

**Verification (after merge)**:
```bash
git log origin/main -1 --format='%H %s'
# f692d2184f73b4940b2126dd1d0a0e01a822e6a1 chore(/e command): add cost-aware model selection guidance (#7974)
diff -q .claude_reference/commands/e.md ~/.claude/commands/e.md
# (no output = identical)
```
