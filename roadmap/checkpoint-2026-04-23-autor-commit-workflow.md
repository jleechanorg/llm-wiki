# Checkpoint — Autor Commit Workflow — 2026-04-23

## What This Is
Modified autor scripts to push commits directly to `jleechanorg/worldarchitect-autor-eval` instead of creating PRs.

## Repo
`/Users/jleechan/llm-wiki-autor-phase3` (branch: `sr-matched-corpus-0417`)

## Current State

### Changes Made This Session

**`scripts/run_autor_pr.py`** — single-run mode, converted to commit-only:
- Removed: `open_draft_autor_pr()`, `close_after_score()`, PR lifecycle entirely
- Removed: `_import_autor_pr()` helper (no longer needed)
- Removed: `run_tests_via_api()` fork test runner
- Removed: test result embedding in score
- New flow: generate → write `autor_generated.py` → commit → `git push -u autor-eval` → score → update bandit
- Pushes to `jleechanorg/worldarchitect-autor-eval` (not `worldarchitect.ai`)
- Uses `~/worldarchitect-ai-autor` (already has `autor-eval` remote configured)
- Output: `DONE: {technique} on PR #{pr} → score={score} branch={autor-{tech}-{pr}-{ts}}`

**`scripts/run_autor_experiment.py`** — batch mode, added commit push:
- Added `REPO_LOCAL = ~/worldarchitect-ai-autor`
- Added `run_git()` helper
- Added `push_autor_commit()` — writes `autor_generated.py`, commits, pushes to `autor-eval`
- Integrated into `run_cell()` between generate and score steps
- No PR created — just branch push + score record

### Bandit State (checked 2026-04-23)
| Technique | n | mean |
|----------|---|------|
| SR-multi-exemplar | 31 | 80.4 |
| PRM | 29 | 78.7 |
| SR | 21 | 75.0 |
| SR-fewshot | 20 | 81.6 |
| ET | 16 | 78.4 |
| SR-prtype | 16 | 84.4 |
| SR-metaharness | 15 | 84.0 |
| SR-adversarial | 15 | 79.2 |
| SR-5iter | 15 | 82.4 |

### autor-eval Repo State
- `~/worldarchitect-ai-autor` has `autor-eval` remote → `jleechanorg/worldarchitect-autor-eval`
- Recent branches: `autor-et-*`, `autor-sr-metaharness-*`, `autor-sr-5iter-*`
- Latest commit: `6a9010f87 autor: SR-metaharness fix for PR #6409`

### Git Status (uncommitted)
```
M scripts/run_autor_experiment.py   (+36/-0 lines)
M scripts/run_autor_pr.py         (+49/-121 lines)
?? research-wiki/scores/SR-5iter_*.json  (11 files)
?? research-wiki/scores/SR-metaharness_*.json  (14 files)
?? wiki/syntheses/et_logs/SR-5iter_*.log  (11 files)
?? wiki/syntheses/et_logs/SR-metaharness_*.log  (14 files)
```
Beads DB also modified but not staged.

## What Needs Doing

### MUST: Commit and push changes to autor-eval
These script changes must be committed to `sr-matched-corpus-0417` and pushed to autor-eval so they're available for the next machine.

### MUST: Test the new workflow
Run one of the modified scripts to verify:
```bash
cd /Users/jleechan/llm-wiki-autor-phase3
python scripts/run_autor_pr.py --technique SR --pr-number 6404
```
Verify: branch pushed to autor-eval, score JSON written, bandit updated.

### SHOULD: Update autor-n15-loop.md skill
The skill should reference `run_autor_pr.py` (commit-only) not the old PR lifecycle.

## Key Rules
- `/autor-n15-loop` = correct loop for technique research
- Autor commits go to `worldarchitect-autor-eval`, NOT `worldarchitect.ai`
- No PR created — just remote branch + score record
- Autor PRs (worldarchitect.ai) = evaluation artifacts, never merge candidates
- SWE-bench Verified ≠ Lite

## Resume Prompt
See `roadmap/resume-autor-commit-workflow.md`
