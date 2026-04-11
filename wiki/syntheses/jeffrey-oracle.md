---
title: "jeffrey-oracle"
type: synthesis
tags: [jeffrey, oracle, synthesis, decision-framework]
sources: [user-preferences-patterns-learnings, github-patterns, ai-coding]
last_updated: 2026-04-11
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
Dependabot/security updates with CVE identifier satisfy evidence requirements. Pre-authorized auto-merge is acceptable. **Major version bumps (e.g., 4.x→5.x) need CVE — patch versions don't.**

### Large net-positive PRs fail minimal test
+1000+ lines on a single bug fix or feature is a red flag. Even if merged (CI passed), size alone fails Jeffrey's minimal-changes principle. The description should justify why it can't be smaller.

### Hook slimming PRs are ok
Net-negative PRs that trim hook chains (addressing context-bloat or similar) directly satisfy the minimal-changes principle. +6/-140 is the right direction.

### CI status required for open PRs
Before "ok" on OPEN PRs — verify `gh pr checks` shows green. Merged PRs = CI passed implicitly.

### Body-diff verification (Step 0)
Always compare PR body claims against actual `gh pr diff`. Mismatches are a direct reject — "no thats wrong."

### CHANGES_REQUESTED blocks "ok" unconditionally
Even if all oracle checks pass (CI green, minimal, caller verified), a CodeRabbit or human `CHANGES_REQUESTED` verdict blocks "ok." The PR must be re-reviewed after requested changes are resolved. This applies to OPEN PRs — merged PRs with outstanding changes are already blocked from merging.

### Body-diff mismatch: wrong operator/condition claimed
A specific variant of Step 0 failure: the body claims a specific code change (e.g., "`>` to `>=`") that contradicts the actual diff. The diff may contain the correct fix via a different mechanism (e.g., new `max_attempts <= 0` block) while the body describes a different operator change. This is a lie, not an omission — fix description to match actual diff.

### Preview model additions require explicit risk acknowledgment
Adding preview/nightly models to `MODELS_WITH_CODE_EXECUTION` or similar critical sets gets "conditional" even with all-CI-green and surgical +2/-1 changes. The risk is fail-open: preview model edge cases could silently route to wrong execution path. Jeffrey accepts "properly flagged medium risk" in the body but won't give unconditional "ok" on preview model additions.

### Cron janitor --all mode needs per-service PR-state verification
Automation scripts with `--all` mode running in cron path must re-verify per-service state at runtime — not rely on prior run's state checks. A service could become orphaned (PR closed/merged) between the last per-service check and the cron run. The `--pr-number` path may have proper guards; the `--all` cron path must independently verify each service's PR state before deletion.

### Sync PRs are their own category
Large sync PRs (e.g., user-scope to repo-scope .claude/ tree sync) are categorically different from feature/bug-fix PRs. Size discipline doesn't apply the same way — byte-level parity is the goal. Jeffrey accepts "sync necessary, tests green, medium risk flagged" as sufficient justification for large +N/-N sync PRs.

### Skill docs need callers — slash command definitions count
A skill doc IS the protocol definition; a slash command in `.claude/commands/` that invokes it IS a valid caller. Both being in the same repo satisfies the "who calls this?" criterion. The skill doc is not orphaned documentation.

### Body-diff omission: file modified but not listed
A Step 0 failure variant — not a lie about what changed, but incomplete enumeration: a file is modified in the diff but not listed in the PR body change summary (e.g., test-deployment.yml modified but not listed in Production Code Changes). Fix the body enumeration to list all modified files.

### CI automation extension requires visible wiring
When extending existing automation scripts (e.g., tool-cache bootstrap, evidence scripts) to new workflows, the caller must be visible in the diff — the workflow file must show the script invocation step. Adding scripts without visible workflow wiring is orphaned automation.

### PRODUCTION_MODE=true on preview = tightening (safe)
Adding `PRODUCTION_MODE=true` to a preview environment is a security tightening, not a bypass. This is fail-closed behavior and is safe. The concern would be removing it or setting it incorrectly.

### New automation script described as "fix existing code" — body-diff lie type 3
A body-diff lie variant: the PR body describes modifying/fixing EXISTING code (e.g., "remove broken redirect from existing spawn subshell"), but the diff shows ONLY new files with zero modifications to any existing file. The framing is actively misleading — it is a new automation script, not a fix to existing code. Step 0 catches this.

### settings.json modification in test PR — unlisted production code change
A test-only PR (body claims "Production Code Changes: None") that modifies `.claude/settings.json` in the diff. settings.json IS production configuration. Any changes to it must be disclosed in the PR body regardless of the PR's primary purpose.

### Recidivist body-diff liar: same PR, same lie, twice
If a PR has a body-diff mismatch flagged in a prior review and the same false claim persists after update/re-review, treat it as a pattern of deliberate misrepresentation. The author was informed and did not fix it. This is worse than a first offense — it suggests the mismatch is intentional.

### New automation scripts need body description AND visible caller
A bare new automation script file with no workflow wiring, no cron trigger, and no parent script invocation in the diff is not automation — it is orphaned code. New scripts require: (1) body must accurately describe what the script does, (2) the caller/trigger must be visible in the diff (workflow step, cron entry, or parent script that is itself auto-triggered).