---
name: token-burn-investigation-anti-patterns
description: Anti-patterns caught during 2026-08-12 token-burn investigation — three wrong conclusions in one session, plus the dominant token source (cmux-resume-watchdog with LLM fallback). Use /advice as a hard gate and JSONL→worktree/PR/commit attribution as the default work-investigation pattern.
metadata:
  type: feedback
---

# Token-Burn Investigation Anti-Patterns (2026-08-12)

Three wrong conclusions in one session. The third was caught by `/advice` Reviewer A (sonnet subagent) before it shipped. Memory captures the anti-patterns + the meta-rule that should have triggered /advice earlier.

## The dominant token source (the actual answer)

The biggest single token consumer this week was **the cmux-resume-watchdog**, not user-driven sessions. Specifically:

- `projects-user-scope` bucket: **94.8 MB across 6,505 JSONL files in 7 days**
- Each watchdog tick invokes `classify_with_llm()` which spawns `codex` (gpt-5.3-codex-spark) or `claude` CLI as a subprocess with 12s timeout
- The watchdog runs at 600-second intervals via `--daemon --interval 600` (the launchd plist's `StartInterval=120` is the kickstart interval)
- Even at a fraction of ticks invoking LLM, this is by far the largest JSONL source

**Fix applied 2026-08-14:** `~/.claude/skills/cmux-resume-watchdog/scripts/cmux_resume_watchdog.py:526` — `llm_predict = None` always. Ambiguous surfaces now default to "clear" (no resume) instead of falling through to the LLM subprocess. The `classify_with_llm()` function is kept as dead code for easy revert. Fastembed-only classification is sufficient — the anchor phrases already cover QUOTA/NETWORK/CLEAR with confidence threshold 0.65.

**Expected token reduction:** ~94.8 MB/week of JSONL → near zero for the watchdog bucket.

## Anti-Pattern 1: Treating ccusage cost column as actual billing

**What I did wrong:** Read ccusage's `Cost (USD)` column showing $4,189.43 and initially concluded the user was being billed that amount on their custom API key.

**Truth:** ccusage uses LiteLLM pricing data, not the Anthropic billing API. Anthropic's own docs state the JSONL `costUSD` field "may differ from your actual bill." For Max subscribers, the figure is a theoretical conversion at standard list rates.

**Cheap check that would have caught it FIRST:** `~/.claude.json` → `oauthAccount.hasExtraUsageEnabled`. If `false`, the user is on Max flat fee and no overage billing is possible. `billingType=stripe_subscription` + `organizationType=claude_max` → flat fee only.

**Rule:** When reporting cost, NEVER cite ccusage's cost column without also showing the auth source check. Default to "theoretical, not billed" until proven otherwise.

## Anti-Pattern 2: Assuming "uses MiniMax" = "is free"

**What I did wrong:** Saw that ccusage showed MiniMax-M3 at $0.00 cost. Concluded claudem is "free." Recommended routing heavy investigation work to claudem to "save money."

**Truth (caught by /advice Reviewer A):** MiniMax API is metered per-token like any other LLM provider. The `MINIMAX_API_KEY` in `~/.bashrc:290` is a pay-as-you-go key, not a free-tier key. ccusage shows $0 only because it lacks MiniMax pricing data — NOT because MiniMax is free. Routing to claudem **shifts spend from Max flat-fee → MiniMax per-token**, doesn't eliminate it.

**Rule:** "X tool shows Y model at $0" ≠ "Y model is free." Cost = 0 in any aggregator is a missing-data signal until proven otherwise. For recommendations that swap providers, ALWAYS measure the destination's per-token cost vs origin's marginal value.

## Anti-Pattern 3: Citing file:line without grep verification

**What I did wrong:** Cited `~/.bashrc:936` for `unset ANTHROPIC_API_KEY`. Missed line 829 (also `unset ANTHROPIC_API_KEY`). Reviewer A caught: "the investigator cited line 936 only; line 829 is also valid."

**Rule:** When citing file:line for evidence, ALWAYS run `grep -n` first to find ALL occurrences. Citing one occurrence when there are multiple is incomplete evidence and will be caught by adversarial review.

## Meta-Rule: /advice as gate after 2 pushbacks

**Trigger:** When the user has pushed back TWICE on the same investigation, dispatch `/advice` BEFORE the next "verified" claim. Three reviewers (Opus subagent + /research + /secondo) catch intra-model blind spots.

**What /advice caught for me (third wrong conclusion):** Reviewer A's `THIRD_ERROR` field surfaced the "MiniMax is free" mistake before it shipped in a memory entry that future sessions would have inherited.

**Cost of skipping:** Three wrong conclusions in one session. User trust erosion. ~$0 direct cost (Max is flat fee) but lots of rework + a memory entry that would have perpetuated the error.

**Operational pattern that works:**
1. After 2 user pushbacks on a single investigation → STOP claiming "done"
2. Dispatch `/advice` with three reviewers in parallel
3. Spot-check the most concrete finding yourself (rule 12 of swarm skill)
4. Only then claim "verified"

## Anthropic bug #32286 — silent API billing mode

**The bug:** If `~/.claude/.credentials.json` has `claudeAiOauth.subscriptionType: null` or `rateLimitTier: null`, the CLI silently enters API billing mode and charges usage credits EVEN on Max. Documented at anthropics/claude-code issue #32286.

**User's status (verified 2026-08-12):** subscriptionType=`"max"`, rateLimitTier=`"default_claude_max_20x"` → bug NOT active.

**Recommended hook:** Alert when either field goes null. Bead: `jleechan-6iu` covers the claudem auto-route hook but a SEPARATE bead should cover the credentials-null watch.

## /sidekick idle ≠ work done

When `/sidekick` teammate sends "available" notification immediately after spawn without updating STATE.md, it's idle — it hasn't done the work you asked for. Either:
1. `SendMessage` with explicit task instructions, OR
2. Do the work yourself (the sidekick is same-model, no diversity benefit)

Don't trust "sidekick spawned successfully" alone — verify STATE.md Progress Log advances within the first checkpoint window.

## Verification by /secondo was blocked

AI Universe auth token expired 2026-08-10 17:00 UTC. /secondo (multi-model consensus) was unavailable for this review. Refresh requires OAuth browser login outside Claude Code. **2/3 reviewers instead of 3/3** — gap should be acknowledged when reporting validation.

## Verification (this memory entry)

- Captured during `/learn` invocation 2026-08-12 after /advice validated findings
- /advice reviewers: A (sonnet subagent, PARTIALLY CONFIRMED, caught Anti-Pattern 2), B (/research, CONFIRMED, found bug #32286), C (/secondo, UNAVAILABLE on auth expiry)
- Spot-check by main session: directly read `~/.claude/.credentials.json` confirming `subscriptionType: "max"`
- Memory entry `feedback_2026-08-12_route_classifier_claudem_vs_max.md` updated with corrected recommendation (don't enshrine claudem routing before measuring MiniMax cost)

## Related memories

- [[feedback_2026-08-12_route_classifier_claudem_vs_max]] — companion memory with verified routing facts
- [[feedback_2026-06-13_dont_second_guess_working_setup]] — bashrc wrappers user-owned
- [[feedback_2026-06-10_aipulse_ccusage_flood]] — earlier ccusage-related history

## Work attribution lesson (the user had to push back to get this)

When asked "what work used up my tokens?", the wrong answer was a vague list of slash commands. The right answer requires actually mapping **JSONL files → worktree → PR → git commits**. Use:

```python
# Pseudo-pattern:
for jsonl in glob.glob('~/.claude/projects/*/*.jsonl'):
    wt = extract_worktree_from_path(jsonl)
    first_user_msg = parse_first_user_message(jsonl)
    pr_refs = re.findall(r'#(\d{3,5})', content)
    commits = run_git_log(worktree_meta[wt])  # git log --since="7 days ago"
```

Then group by worktree + present PRs + commits + first task. **Work attribution FIRST, cost framing SECOND.** Per CLAUDE.md /harness rule: never attribute without file evidence.

## Bead

`jleechan-7rl` (P3, learning) — to be created