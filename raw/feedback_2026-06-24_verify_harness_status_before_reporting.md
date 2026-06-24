---
name: ""
metadata: 
  node_type: memory
  originSessionId: 119226a9-d30b-4b43-93af-9857792505eb
---

**Context (2026-06-24):** During this session's `/learn` for the prompt-cleanup learning, my own bash probe checked `[ -z "${OPENAI_API_KEY:-}${MEM0_API_KEY:-}" ]` and reported `mem0 unavailable: helper present but no OPENAI_API_KEY/MEM0_API_KEY in env`. That was the `/learn` SKILL.md instruction from the pre-Ollama era. **Mem0 itself worked perfectly** — verified by feeding a Stop-hook fixture to `~/.hermes/.claude/hooks/mem0_save.py` and observing 508 points in Qdrant `hermes_mem0` plus an appended `mem0_extractions.md`. The skill's negative status string was a **hypothesis**, not a fact.

**Failure class:** mislabeled artifact (status string from a skill) + silent degradation (no test caught the false-negative, so it ran for ~2 months after PR #7178 / bead `rev-1cmaj` switched mem0 to local Ollama embedder + Groq LLM in May 2026).

**FIX (apply on every "X unavailable" report):**

1. **Rewrite the probe to use the helper's own gate, not the env vars the helper USED TO gate on.** For mem0 the real gates are: (a) `python3 -c "from mem0 import Memory"` import resolves, (b) helper script exists at `~/.hermes/.claude/hooks/mem0_save.py` or repo-local fallback, (c) `mem0_config.py:mem0_hooks_enabled()` returns `True`. **Do NOT** hard-code `OPENAI_API_KEY` / `MEM0_API_KEY` checks — those are pre-Ollama-era gates.
2. **Mandatory verification step before reporting "mem0 unavailable":** run the helper with a tiny Stop-hook fixture and confirm a Qdrant-side delta or markdown append. If the helper persists successfully, report `mem0 saved (<N> facts)` and **fix the SKILL.md probe**.
3. **Generalized CLAUDE.md rule (now in `~/.claude/CLAUDE.md` "Verify before reporting"):** treat any "X unavailable" / "X failed" status string a skill emits as a hypothesis, not a fact. Skills get stale. Run the underlying mechanism before reporting.

**Verification (2026-06-24):**
- Direct invocation of `mem0_save.py` with a Stop-hook fixture persisted to Qdrant (`hermes_mem0`, user_id=jleechan, count=508) and markdown.
- `/learn` SKILL.md rewritten — `OPENAI_API_KEY` no longer the gate; references `mem0_hooks_enabled()` + import probe + verification step.
- Re-ran the verification step after the SKILL.md fix; Qdrant count updated, markdown appended.

**Why this pairs with `feedback_2026-06-24_prompt_cleanup_drops_load_bearing_clauses.md`:** Both are the same root cause — I trusted the harness instead of verifying reality. There, I trusted the contract hash green; here, I trusted the SKILL.md status string. The general rule is: **don't paraphrase a skill's output as ground truth without running the mechanism**. The `~/.claude/CLAUDE.md` "Verify before reporting" rule now states this explicitly.

**Reusable pattern:** When a skill says "X unavailable because Y is missing," check whether the helper actually checks for Y. If the helper doesn't, the probe is the bug, not the helper. Helper script > skill text. See [[prompt-cleanup-drops-load-bearing-clauses]] for the same shape.
