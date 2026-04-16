---
title: "Technique Selection Oracle — Thompson Sampling Bandit"
type: concept
tags: [auto-research, technique-selection, bandits, thompson-sampling, reinforcement-learning]
last_updated: 2026-04-16
---

## Concept

A **Thompson Sampling bandit** that selects the best coding technique (SelfRefine, ET, PRM) for each PR by balancing exploration vs exploitation using posterior sampling over score outcomes.

## How It Works

1. **Prior**: Each technique starts with a weak Beta(2,2) prior
2. **Update**: After each PR result, update the posterior: `α += normalized_score, β += 1 - normalized_score`
3. **Selection**: Sample from each technique's posterior; pick the highest sample
4. **Result**: Over time, the system converges to using the best technique more often

## Usage

```bash
# Get technique recommendation for a PR
python3 technique_bandit/technique_selector.py --suggest <PR_number>

# After a PR is scored, record the result
python3 technique_bandit/technique_selector.py --update \
    --PR <n> --technique <ET|SelfRefine|PRM> --score <score>

# Check current posterior state
python3 technique_bandit/technique_bandit/technique_selector.py --rank

# View recent history
python3 technique_bandit/technique_selector.py --history
```

## State

Current posterior state (as of 2026-04-16):

| Technique | Posterior Mean | n | α | β |
|-----------|--------------|---|---|---|
| ET | 83.7 | 11 | 10.1 | 4.9 |
| SelfRefine | 83.0 | 12 | 10.6 | 5.4 |
| PRM | 81.1 | 4 | 5.0 | 3.0 |

**Note**: At n=23 total observations, all 3 techniques have converged to ~81-84 mean. This is consistent with the finding that all 3 converge to ~87 at higher n — initial differences were noise.

## Integration Points

- **Pre-PR selection**: Run `--suggest <PR>` before applying a technique
- **Post-scoring**: Run `--update` after each PR is scored to update beliefs
- **Pipeline integration**: `technique_bandit/technique_selector.py` can be imported as a module

## Relationship to PR Recreate Pipeline

The Technique Selection Oracle is the **online learning layer** on top of the PR Recreate Pipeline:

```
PR Recreate Pipeline → scores per (PR, technique) → bandit update → next suggestion
```

The pipeline generates the training signal; the oracle uses it to select techniques dynamically.

## See Also

- [[SelfRefine]] — technique
- [[ExtendedThinking]] — technique
- [[ProcessRewardModels]] — technique
- [[PRRecreatePipeline]] — experiment methodology
- [[AutoResearchLoop]] — the broader research loop
