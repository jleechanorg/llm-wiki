# Resume Prompt — Autor Commit Workflow — 2026-04-23

## Context
On machine `llm-wiki-autor-phase3` (branch: `sr-matched-corpus-0417`), the autor workflow was modified to push commits to `jleechanorg/worldarchitect-autor-eval` instead of creating PRs on `worldarchitect.ai`.

**What was done this session:**
- Modified `scripts/run_autor_pr.py` and `scripts/run_autor_experiment.py` to push commits to autor-eval instead of creating/closing PRs
- Removed the PR lifecycle entirely (no draft PR, no close after score)
- Added `push_autor_commit()` that writes `autor_generated.py` to `~/worldarchitect-ai-autor` and pushes to `jleechanorg/worldarchitect-autor-eval`

**Current state:**
- Changes are uncommitted in `llm-wiki-autor-phase3`
- Score JSONs from SR-5iter and SR-metaharness runs are staged/unstaged but not committed
- `~/worldarchitect-ai-autor` is the local clone used for pushing to autor-eval

## How to Resume

### Step 1: Commit the modified scripts
```bash
cd /Users/jleechan/llm-wiki-autor-phase3
git add scripts/run_autor_pr.py scripts/run_autor_experiment.py
git commit -m "autor: push commits to autor-eval instead of PRs"
git push origin sr-matched-corpus-0417
```

### Step 2: Also push the autor-eval changes
The local clone `~/worldarchitect-ai-autor` should already have the autor-eval remote configured. Verify:
```bash
git -C ~/worldarchitect-ai-autor remote -v
# Should show: autor-eval https://github.com/jleechanorg/worldarchitect-autor-eval.git
```

### Step 3: Test end-to-end
```bash
cd /Users/jleechan/llm-wiki-autor-phase3
python scripts/run_autor_pr.py --technique SR --pr-number 6404
```
Expected: branch pushed to autor-eval, score JSON written, bandit updated.

### Step 4: Update autor-n15-loop.md skill (optional)
Update `.claude/skills/autor-n15-loop.md` to reference the commit-only workflow.

## Key Files
- `scripts/run_autor_pr.py` — single-run, commit-only
- `scripts/run_autor_experiment.py` — batch mode with commit push
- `technique_bandit/bandit_state.json` — all technique scores (n=15-31 per technique)
- `~/worldarchitect-ai-autor` — local clone used for autor-eval pushes

## Bandit State (current)
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
- Autor commits → `jleechanorg/worldarchitect-autor-eval` (not `worldarchitect.ai`)
- No PR created — just branch + score record
- Autor PRs (worldarchitect.ai) = evaluation artifacts, never merge candidates
- `/autor-n15-loop` = correct loop for technique research
