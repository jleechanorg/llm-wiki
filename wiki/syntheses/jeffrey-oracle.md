---
title: "jeffrey-oracle"
type: synthesis
tags: [jeffrey, oracle, synthesis, decision-framework]
sources: [user-preferences-patterns-learnings, github-patterns, ai-coding]
last_updated: 2026-04-09
---

# The Jeffrey Oracle: What Would Jeffrey Say?

The crown jewel. Synthesizes everything to predict: what would Jeffrey say or do?

## The Decision Framework

### Step 1: What category?

| Category | Response |
|----------|----------|
| AI output / code | Real or speculative? Cite file:line or flag fake |
| PR / review | Green? CodeRabbit? Evidence cited? |
| Automation | Safety limit hit? Who owns it? |
| Tool question | Use gh. Minimax if cost matters. |
| Context question | Check mem0. Check git. Check PR state. |
| Unknown / confused | "what does it prove?", "is this true?" |

### Step 2: What would Jeffrey do?

1. Inspect first: gh pr view, check Pr now, ao status, check context
2. Issue direct command: "fix it", "merge", "run /fake", "investigate and root cause"
3. Iterate until satisfied
4. Move on — no pleasantries, no wrap-up

### Step 3: What would Jeffrey NOT do?

- Say "let me check" (he checks himself)
- Accept speculative code
- Push to main
- Skip tests
- Create a new file if existing works
- Waste money (minimax for routine tasks)

## Situation → Prediction

| Situation | Jeffrey's Response |
|-----------|-------------------|
| AI produces code | Cite file:line? Run /fake? |
| PR failing CI | Fix it, push, confirm green |
| New automation script | Who calls this? Auto-trigger? |
| New tool suggested | Does task require it? |
| Git commit vague | Explain why, not what |
| Hook prevents action | Fix the hook or comply |
| Model choice | Minimax for routine, Anthropic for complex |
| Code review comment | Fix every item, push, don't run /er until resolved |
| New skill doc proposed | Who calls this? Integrate into existing instead? |
| Large net-negative PR | Verify it's simplification, not just bloat — net deletion is ok |
| Security concern | Production safety over speed |

## Communication Style Predictions

| If Jeffrey... | He says |
|---------------|--------|
| Likes what you did | "ok" or "continue" or 🦾 (silence = approval) |
| Disagrees | "no thats wrong" — direct |
| Is confused | "what does this prove?", "is this true?" |
| Wants inspection | "check Pr now", "ao status" |
| Wants action | "investigate and fix", "run /fake", "fix the stuck ones" |
| Wants control | "Reply with exactly OK." |

## Jeffrey's Priorities

1. Production safety — auth, validation, fail-closed
2. Evidence over assertion — cite file:line or fake
3. Tests must pass — no claiming done until green
4. Minimal changes — surgical, existing files first
5. Automation with callers — scripts need triggers
6. Cost consciousness — minimax over anthropic when appropriate
7. Worktree isolation — one PR per worktree

## The Jeffrey Test

Before acting, ask:
1. **Body matches diff?** → Step 0: verify PR description matches actual code changes
2. Real or speculative? → /fake first if unsure
3. Tests passing? → Check CI status (gh pr checks) before claiming "ok" on open PRs
4. Minimal? → Could it be smaller? **Note: net-negative PRs (pure deletion) are ok**
5. Caller? → Who triggers automation? **Skill docs need callers too**
6. Safe? → Fail-closed, no auth bypass

All yes → Jeffrey says "ok" or "continue" 🦾

## Additional Patterns Observed

### Net-negative deletion is ok
Pure deletion of unused/obsolete code (+0/-N) satisfies minimal-changes principle. Removing dead code is the right direction.

### Skill docs need callers too
New skill documents (e.g., `bypass-claims.md`) need integration into existing skills/hooks or they are just documentation. Ask "who calls this?"

### Evidence cross-reference fails evidence standards
Citing "reviewed in PR #X" or "audit PASS" without actual Bead + timestamps is not sufficient evidence. Must show: Bead identifier, per-chunk UTC timestamps, latency metrics table.

### Bot-authored dependency PRs
Dependabot/security updates with CVE identifier satisfy evidence requirements. Pre-authorized auto-merge is acceptable.

### CI status required for open PRs
Before "ok" on OPEN PRs — verify `gh pr checks` shows green. Merged PRs = CI passed implicitly.

### Body-diff verification (Step 0)
Always compare PR body claims against actual `gh pr diff`. Mismatches are a direct reject — "no thats wrong."