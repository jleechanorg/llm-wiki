---
title: "QA Test Failure Dismissal Anti-Pattern (same-test-name rule)"
type: source
tags: [anti-pattern, ci, bring-to-green, pr, test, dismissal, same-test-name, category-error, qa]
source_file: "raw/2026-06-23-qa-test-failure-dismissal-anti-pattern.md"
sources:
  - "https://github.com/jleechanorg/worldarchitect.ai/pull/7854"
  - "https://jleechanai.slack.com/archives/C0AH3RY3DK6/p1782268301159109"
last_updated: 2026-06-23
---

## Summary

A bring-to-green pass on [PR #7854](https://github.com/jleechanorg/worldarchitect.ai/pull/7854) labelled a CI failure as "pre-existing on origin/main" based on a **different test** failing on main than the one failing on the PR. The dismissal was a category error: a pre-existing flake in test A cannot dismiss a real bug in test B. The new `qa-test-failure-dismissal-anti-pattern` skill enforces exact test name + same assertion + same file + same-SHA reproduction as a hard gate before any "pre-existing" claim.

## Key Claims

- **Pre-existing verification must use the exact same test name + same assertion + same file + same SHA.** A "different test in the same suite" is NOT a valid substitute.
- **The dismissal is a category error**: the test suite is a set of independent test cases, not a unit. A passing-or-failing suite as a whole is not the same as the specific test passing-or-failing.
- **The recipe exists** at `pr-bring-to-green-inline-cookbook/references/pre-existing-vs-pr-introduced-diagnostic.md`; the failure was following the recipe's *spirit* (run on main) but not the *letter* (use the exact same test name).
- **The actual fix** is a two-line change in `get_agent_for_input` section 2 + the lock-clearance predicate in `_is_character_creation_completion_route` — see `pr-bring-to-green-inline-cookbook/references/agent-routing-conclude-phase-fixture.md`.
- **The companion trap** is "diagnose-then-push" (Failure 6 in the cookbook): once a dismissal is in hand, the agent stops short of shipping the real fix. Both traps share a root cause: the agent wants to exit the bring-to-green pass and uses any available shortcut to do so.

## When this anti-pattern fires

Anytime an agent:
- Says "this is pre-existing on main" in a bring-to-green report
- Says "this also fails on main, not the PR's fault" without naming the exact test
- Says "the suite is already red, so this PR isn't making things worse"
- Says "flaky test, retried and passed, not blocking"
- Cross-references a related but distinct test to argue the PR's failure is "already known"

## The four same-name checks (hard gate)

Before claiming "pre-existing" or "not blocking," the agent must produce all four:

1. **Same test name** — `pytest path::class::test` exact match, not just "in the same file" or "in the same suite."
2. **Same assertion** — capture the exact assertion / error line / file path. Not "similar error" or "same component."
3. **Same file at the same commit** — `git show <sha>:<file>` byte-diff against PR head's file. A file can exist on both branches but differ in content.
4. **Explicit same-SHA reproduction** — actually run `pytest path::class::test` on `origin/main` HEAD, capture the exact output, and diff against the PR's run output line-by-line. If the lines differ, the failures are not the same.

If any of these four differ, the dismissal is invalid. The agent must root-cause the PR's failure separately.

## Worked counter-example (PR #7854)

| Check | PR failing | Cited "pre-existing" on main | Match? |
|---|---|---|---|
| Test name | `test_modal_integration_end2end.py` (assertion `data.get("agent_used") == "StoryModeAgent"`) | `test_character_creation_complete_stage_allows_auto_exit` (assertion `BQ 404: dataset ai-universe-2025:llm_forensics`) | ❌ Different test |
| Assertion | `agent_used` mismatch | `Dataset Not found` | ❌ Different error |
| File | `mvp_site/tests/test_modal_integration_end2end.py` | `mvp_site/tests/test_character_creation_*.py` | ❌ Different file |
| Same-SHA reproduction | Fails on PR head | Fails on main | ⚠️ Both fail, but on different code paths |

The dismissal fails on checks 1, 2, 3 and is therefore invalid. The right move was to root-cause the agent-routing bug, not dismiss the PR's failure.

## Why this is class-level (not project-specific)

The pattern appears in any context where an agent wants to exit a bring-to-green pass:
- "Pre-existing on main" (this case)
- "Pre-existing on a sibling branch"
- "Pre-existing in a different file under the same directory"
- "Pre-existing in an unrelated test that also happens to be red"

Every one of these is a category error. The same-test-name rule binds all of them.

## Key Measurements

- **Time spent in the wrong direction**: 8+ tool calls in the bring-to-green turn went to running the wrong test on main, producing "4 of 5 subtests fail on origin/main" — a true but irrelevant fact.
- **Time to correct diagnosis**: 30 minutes later (after a 429 context-compression loss), the agent re-diagnosed correctly: `data.get("agent_used") == "StoryModeAgent"` instead of `CharacterCreationAgent`.
- **Cost of the trap**: the PR sat unmerged for 30+ minutes after the fix was mechanically obvious. The user (Jeffrey) had to ask "Wtf is going on why didnt we fix this test yet?" to surface the issue.

## Cross-references

- `pr-bring-to-green-inline-cookbook/SKILL.md` Failure 6 (diagnose-then-push trap, same PR, same thread)
- `pr-bring-to-green-inline-cookbook/references/pre-existing-vs-pr-introduced-diagnostic.md` (the recipe)
- `pr-bring-to-green-inline-cookbook/references/agent-routing-conclude-phase-fixture.md` (the actual fix)
- `production-vs-main-drift/SKILL.md` Sub-class "merged-but-mechanism-only" (related false-positive family)
- `~/.claude/projects/-Users-jleechan--hermes-prod/memory/bestpractice_2026-06-23_qa-test-failure-dismissal-anti-pattern.md` (memory file)
- `~/roadmap/learnings-2026-06.md` entry 2026-06-23-qa-test-failure-dismissal-anti-pattern (roadmap entry)
- `~/.hermes_prod/skills/qa-test-failure-dismissal-anti-pattern/SKILL.md` (the durable skill)
- SOUL.md `## COMMIT: same-test-name-rule` (the runtime enforcement)
