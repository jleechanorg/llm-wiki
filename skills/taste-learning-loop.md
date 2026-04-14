# Taste Learning Loop

Whenever I manually reject, heavily edit, or comment on a PR:

1. **Extract my feedback** — Pull your comment + the original PR description/diff
2. **Add to product-taste/good-bad-examples.md** — Label as Good or Bad Example with your reasoning
3. **Update product-taste/taste-rubric.md** — If new principles emerge from the feedback, add them
4. **Create a bead** — Record the learning event with the feedback and outcome
5. **Auto-incorporation** — [[ProductJudge]] will now reference the updated wiki on future PRs

This loop turns every correction you make into permanent institutional knowledge.

## Trigger Conditions

- You manually reject a PR verdict
- You heavily edit generated code before accepting
- You leave substantive comments explaining *why* something was wrong beyond technical accuracy
- You override [[ProductJudge]]'s verdict with your own reasoning

## What to Record

For each learning event, record:
- The original PR / generated code
- Your feedback (exact words if possible)
- Why the generated code didn't match your taste
- What principle from [[ProductPrinciples]] was violated (or what new principle emerged)

## Key Findings from 18 Cycles

Based on auto-research experiment results (Cycles 1–18, 2026-04-14):

### Type Safety Is a Taste Issue, Not Just a Technical Issue

The 18-cycle experiment revealed that pervasive `Any` is not just a type-safety FAIL — it is a product taste failure. Code with `# mypy: ignore-errors` or `dict[str, Any]` without TypedDict signals:
- Low craft standards
- Technical debt being accumulated
- Future refactoring cost being offloaded onto future maintainers

This should be reflected in [[ProductJudge]] scoring under "Long-term Maintainability & Vision Fit". A PR that introduces `Any` without justification should receive a lower score on this dimension.

### The 3-Exception `_parse_numeric` Pattern Is a Taste Positive

The `_parse_numeric` pattern (ValueError, TypeError, OverflowError) from PR #6233 represents good taste:
- Defensive: assumes LLM output will be malformed
- Minimal: falls through to 0 silently
- General-purpose: worth extracting to module level

This should be surfacing in taste-rubric.md as a positive example of defensive LLM-output handling.

### Composite PRs Violate Simplicity

PRs fixing 6 issues at once (#6241 SixRegressionFixes, #6259 PRRegressionResolution) scored 70-73 vs 77-80 for single-focus PRs. This is a taste violation — each regression deserved its own PR with clear scope. Record this as a negative taste example.

### Shell CI Scripts Model Good Error Handling Taste

The shell scripts in PRs #6269 (SkepticGateCodeRabbit) and #6248 (RepoLevelMergeGuard) scored 86/100. Key taste signals:
- `set -euo pipefail` — fail-fast by default
- Explicit `PIPESTATUS` checking — no silent pipe failures
- Fail-closed evidence gates — safety by default
- Inline comments explaining TOCTOU and security decisions

These should be positive examples in good-bad-examples.md under "Error Handling Taste".

### Hook-First Safety Is Better Than Policy Documentation

PR #6248 (PreToolUse hook blocking `gh pr merge`) scored 86/100. This validates that intercepting dangerous operations at the tool-call layer is more tasteful than CLAUDE.md policy documentation (which scored 53/100). Record this contrast in taste-rubric.md as a structural principle.

## Integration

- Reads from [[ProductJudge]] verdicts (to detect when you overrule the agent)
- Updates [[ProductTasteLayer]] wiki pages (good-bad-examples.md, taste-rubric.md)
- Creates beads for each learning event
- [[ProductJudge]] consumes the updated wiki for future verdicts

## Tags

#agent-harness #product-judgement #llm-wiki #self-improvement
