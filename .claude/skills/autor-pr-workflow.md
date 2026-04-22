# Autor PR Workflow Skill

**Skill**: `.claude/skills/autor-pr-workflow.md`
**Date**: 2026-04-21
**Trigger**: Any time you create an autor-generated PR on jleechanorg/worldarchitect.ai

## Core Rule

**Autor PRs are evaluation artifacts, NEVER merge candidates.** The purpose is a scorable diff — not production code.

## Required Lifecycle (every autor PR, without exception)

### 1. Create as draft with autor label
```bash
gh pr create --draft \
  --repo jleechanorg/worldarchitect.ai \
  --title "[autor] <technique> <brief-description>" \
  --label "autor" \
  --body "Autor evaluation PR — technique: <SR|ET|PRM>"
```

### 2. Apply the technique
Use the specified technique (SelfRefine, Extended Thinking, or PRM) to generate a real code fix. The fix must:
- Actually compile / pass syntax checks
- Be a genuine attempt to solve the issue
- NOT be a simulated prediction — must produce real code

### 3. Score the diff
Use the 6-dimension rubric on the actual diff:
```
python layer/score_pr.py <pr_number>
```

### 4. Record evidence
Write score JSON and log:
- `research-wiki/scores/<tech>_<pr>_<ts>.json`
- `wiki/syntheses/et_logs/<tech>_<pr>_<ts>.log`

### 5. Update bandit state
```
python technique_bandit/technique_selector.py --update \
  --PR <pr_number> --score <score> --technique <tech>
```

### 6. Close the PR (most critical step)
```bash
gh pr close <pr_number> \
  --repo jleechanorg/worldarchitect.ai \
  --comment "autor eval: <tech> score=<score>. Closing — evaluation artifact, not a merge candidate."
```

## Anti-patterns (NEVER do these)

| Anti-pattern | Why |
|---|---|
| Open as ready-for-review | Signals production intent — autor PRs are eval artifacts |
| Leave PR open after scoring | Open = incomplete evaluation |
| Merge an autor PR | Policy violation — never merge evaluation artifacts |
| Simulate a PR without real code | User explicitly said "I never want any simulated ones" |
| Score from memory instead of live run | Evidence must be freshly generated |

## Quick Reference

```
OPEN  = gh pr create --draft --label autor
SCORE = python layer/score_pr.py <pr>
CLOSE = gh pr close <pr> --comment "autor eval: <tech> score=N"
```

## Skill interactions
- `autor-n15-loop` skill: Uses this workflow for each iteration
- `CLAUDE.md` Autor PR Lifecycle section: Has the full policy rationale
