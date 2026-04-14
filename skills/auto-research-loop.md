# Auto-Research Loop (Self-Discovering Meta-Research)

You are running a grounded, self-discovering research experiment on your personal codebase.

## Phase 0 — Hypothesis Generation

Analyze patterns across your historical PRs and canonical repos.
Generate 1–3 novel, testable hypotheses for improving code quality, architecture, or harness efficiency.

Each hypothesis must be:
- Specific and falsifiable
- Grounded in observed patterns from your codebase
- Different from existing papers in raw/

Output format:
```
Hypothesis 1: [short title]
Rationale: [observed patterns]
Predicted improvement: [expected gain]
Test plan: [how to test on next PR]
```

## Phase 1 — Selection

Choose the next historical PR from test-prs/ or test one of the generated hypotheses.

## Phase 2 — Implementation

Implement the selected paper's technique OR the generated hypothesis using the [[SelfCritiqueVerificationLoop]] skill (with real sandboxed test execution).

## Phase 3 — Evaluation

Run baseline (direct generation) and improved version.
Score both using the [[CanonicalCodeScorer]] skill.
Record full results in the wiki (pass rate, iterations, token usage, rubric breakdown, diff similarity).

## Phase 4 — Update

Update the relevant wiki page with "Results on My Codebase" section.
Create a bead for every experiment run.

## Always Use

The [[SelfCritiqueVerificationLoop]] skill when applicable.

## Integration

- [[SelfCritiqueVerificationLoop]] — called in Phase 2
- [[CanonicalCodeScorer]] — called in Phase 3
- [[ProductJudge]] — called alongside CanonicalCodeScorer in Phase 3 (full master system only)
- [[AutoProductMasterSystem]] — directory structure (raw/, canonical-repos/, test-prs/)

## Tags

#agent-harness #llm-wiki #self-research #meta-learning
