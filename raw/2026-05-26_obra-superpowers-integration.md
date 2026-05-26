---
name: obra superpowers integration into worldarchitect.ai
description: Enhanced code-standards skill with systematic-debugging, TDD, verification patterns from obra superpowers framework
type: feedback
bead: none
---

# Obra Superpowers Integration into worldarchitect.ai /code-standards

## Context

Reviewed obra superpowers prompts from wa-6292-fresh repo and identified integration opportunities for the worldarchitect.ai `/code-standards` skill.

## What Was Changed

Updated `.claude/skills/code-standards/SKILL.md` in worldarchitect.ai with four superpowers integrations:

1. **Iron Law**: "NO REVIEW LANE PASSES WITHOUT VERIFICATION EVIDENCE" - a lane returning PASS must include specific file/line evidence that proves compliance

2. **systematic-debugging four-phase process**: Integrated into review lanes (root cause investigation → pattern analysis → hypothesis → verification)

3. **verification-before-completion pattern**: From finishing-a-development-branch skill - each lane must run verification commands and cite actual grep/read evidence

4. **Test coverage gate (TDD enforcement)**: New production code requires tests; if tests don't exist, FAIL

5. **Anti-rationalization table**: Prevents "close enough to pass" dilution of FAILs

## Source Skills Used

- `~/.claude/skills/superpowers-systematic-debugging.md`
- `~/.claude/skills/superpowers-finishing-a-development-branch.md`
- `~/.claude/skills/superpowers-test-driven-development.md`
- `~/.claude/skills/superpowers-requesting-code-review.md`

## Verification

- Branch: `superpowers-code-standards-enhancement`
- Commit: `101c58c5ff`
- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/xxx

## Key Insight

The existing `/code-standards` skill was a dispatcher that ran 4 review lanes but had no enforcement mechanism. The superpowers framework brought the iron law discipline: rationalizations are not evidence, cite the exact file/line or the lane hasn't completed its work.

## References

- wa-6292-fresh superpowers skills at `~/.claude/skills/superpowers-*.md`
- worldarchitect.ai PR link to be added after creation