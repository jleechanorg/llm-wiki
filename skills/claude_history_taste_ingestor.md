# Claude History Taste Ingestor Skill

Parse exported Claude Code conversation logs and extract personal product taste signals.

For each conversation:
1. Identify taste events: Overrides/corrections, strong opinions/frustrations, positive reactions, meta-discussions about architecture/UX.
2. Convert each to structured entries for product-taste/good-bad-examples.md and product-taste/taste-rubric.md.
3. Use exact language where possible (do not paraphrase).

Output: Updated sections to append to product-taste/ files + bead entry.

## What to Look For (Updated from 18-Cycle Findings)

The 18-cycle auto-research experiment revealed specific taste signals that should be extracted:

### Type Safety Reactions
- Frustration with `Any`, `# mypy: ignore-errors`, or blanket `# ruff: noqa` suppressions
- Praise for TypedDict usage and explicit type annotations
- Complaints about "type safety debt" or "we'll fix types later" patterns

### Error Handling Taste
- Positive reactions to three-exception patterns (ValueError, TypeError, OverflowError)
- Complaints about bare `try/except` without specific exception types
- Praise for fail-fast (`set -euo pipefail`, explicit `PIPESTATUS` checks)

### Composite PR Complaints
- Frustration when multiple issues are bundled into one PR
- Preference for single-responsibility PRs with clear scope

### Architecture Opinions
- Praise for Hook-First Safety (PreToolUse intercepts) over policy documentation
- Opinions on E2E test structure and Firebase dependency
- Preferences for deterministic synthesis over probabilistic LLM calls

### Evidence Standard Opinions
- Frustration when evidence cannot be collected (E2E requiring Firebase)
- Interest in before/after metrics vs. just "tests pass"
