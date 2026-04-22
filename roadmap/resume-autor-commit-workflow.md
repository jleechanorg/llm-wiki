# Resume Prompt — Autor Commit Workflow — 2026-04-23

## What Was Done
Modified `scripts/run_autor_pr.py` and `scripts/run_autor_experiment.py` to push commits directly to `jleechanorg/worldarchitect-autor-eval` instead of creating draft PRs on `worldarchitect.ai`. The scripts now:
1. Generate fix via MiniMax
2. Write `autor_generated.py` to `~/worldarchitect-ai-autor`
3. Commit and `git push -u autor-eval <branch>`
4. Score against 6-dim rubric
5. Write score JSON + log
6. Update bandit state
No PR created — just remote branch + score record.

## What Changed
- `scripts/run_autor_pr.py` — removed PR lifecycle (open/close), removed `_import_autor_pr()`, removed `run_tests_via_api()`
- `scripts/run_autor_experiment.py` — added `REPO_LOCAL`, `run_git()`, `push_autor_commit()` helpers; integrated into `run_cell()`

## Current State
- Commit `6480d891` merged to `main` on `jleechanorg/llm-wiki`
- Research branch `sr-matched-corpus-0417` is behind main; resync from main on next session in `llm-wiki-autor-phase3`
- `~/worldarchitect-ai-autor` is the working clone for pushing to autor-eval

## How to Resume on Another Machine

### Step 1: Pull latest main
```bash
git clone https://github.com/jleechanorg/llm-wiki.git ~/llm-wiki
cd ~/llm-wiki
```

### Step 2: Ensure autor-eval remote is available
```bash
git remote add autor-eval https://github.com/jleechanorg/worldarchitect-autor-eval.git
# OR if already cloned:
git remote -v  # should show autor-eval
```

### Step 3: Verify scripts
```bash
ls scripts/run_autor_pr.py          # should exist
ls scripts/run_autor_experiment.py # should exist
```

### Step 4: Clone/create autor working directory for autor-eval pushes
```bash
git clone https://github.com/jleechanorg/worldarchitect-autor-eval.git ~/worldarchitect-ai-autor
```

### Step 5: Run a test
```bash
cd ~/llm-wiki
python scripts/run_autor_pr.py --technique SR --pr-number 6404
```
Expected output: `DONE: SR on PR #6404 → score=XX branch=autor-sr-6404-YYYYMMDDHHMMSS`

### Step 6: Check autor-eval push
```bash
git -C ~/worldarchitect-ai-autor log --oneline -3
# Should show new branch pushed
```

## Bandit State
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

## Key Rules
- Autor commits → `jleechanorg/worldarchitect-autor-eval` (NOT `worldarchitect.ai`)
- No PR created — just branch push + score record
- `/autor-n15-loop` = correct loop for technique research
- Autor PRs (worldarchitect.ai) = evaluation artifacts, never merge candidates
