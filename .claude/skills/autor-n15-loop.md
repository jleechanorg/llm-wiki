# autor-n15-loop — Continuous autor PR evaluation loop

**Loop interval**: 30m | **Max duration**: 12h (24 iterations)

## Purpose
Generate real draft PRs on worldarchitect.ai using 9 techniques (SelfRefine, ET, PRM, SR-5iter, SR-fewshot, SR-adversarial, SR-metaharness, SR-prtype, SR-multi-exemplar) and score them against the 6-dim rubric. All 9 techniques have n≥15 in bandit — continuous evaluation mode.

## Entry conditions (all must be true to continue)
- Branch `sr-matched-corpus-0417` is pushed and not detached
- No merge conflicts on the branch
- CI is not stuck (>30min queue with no progress)

## Each iteration

### 1. Check bandit state
```
python technique_bandit/technique_selector.py --rank
```
Print: `[iter N] SelfRefine n=X | ET n=Y | PRM n=Z | elapsed=Thh:mm`

### 2. Thompson-suggest next technique
```
python technique_bandit/technique_selector.py --suggest <PR#>
```
Use the suggested technique for the next run.

### 3. Pick an open PR on worldarchitect.ai
Pick the open PR with fewest existing samples across all techniques:
```
gh pr list --repo jleechanorg/worldarchitect.ai --state open --json number,title --jq '.[] | "\(.number) \(.title)"' | head -30
```

### 4. Generate autor PR using run_autor_pr.py
Local clone: `~/worldarchitect-ai-autor` (private repo, do NOT fork — forking is disabled)
```
cd ~/llm-wiki-autor-phase3
python scripts/run_autor_pr.py --technique <TECH> --pr-number <PR>
```
Where `<TECH>` is any of: SelfRefine, ET, PRM, SR-5iter, SR-fewshot, SR-adversarial, SR-metaharness, SR-prtype, SR-multi-exemplar. This script:
- Fetches diff of the target PR
- Generates fix using MiniMax-M2.7
- Creates a draft PR labeled `autor`
- Scores the generated diff against the 6-dim rubric
- Writes score JSON to `research-wiki/scores/`
- Updates `technique_bandit/bandit_state.json`
- **Closes the draft PR** (never merges)

### 5. Verify score JSON was written
Check `research-wiki/scores/<tech>_<pr>_s1_<ts>.json` exists before continuing.

### 6. Commit + push evidence
```
cd ~/llm-wiki-autor-phase3
git add -A && git commit -m "autor: <tech> on PR#<n> score=<score>" && git push
```

### 7. Check time budget
If elapsed > 12h since first iteration → STOP.

## Stop conditions
- 12 hours elapsed → PARTIAL (note final n for each technique)
- Error on 3 consecutive iterations → FAIL (notify)

## Output
After each iteration, print:
```
[iter N] SelfRefine n=X | ET n=Y | PRM n=Z | elapsed=Thh:mm
```

## Key files
- `scripts/run_autor_pr.py` — the autor PR workflow script
- `scripts/autor_pr.py` — helper module (open_draft_autor_pr, close_after_score)

## Output
After each iteration, print:
```
[iter N] SelfRefine n=X | ET n=Y | PRM n=Z | elapsed=Thh:mm
```
