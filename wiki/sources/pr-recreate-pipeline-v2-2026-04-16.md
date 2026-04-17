---
title: "PR Recreate Pipeline v2 Results 2026-04-16"
type: source
tags: [worldarchitect.ai, auto-research, PRRecreatePipeline, technique-comparison, SelfRefine, ExtendedThinking]
date: 2026-04-16
---

## Summary

PR Recreate Pipeline v2 ran on 5 held-out merged PRs (#6279, #6273, #6267, #6266, #6269) using 3 techniques (SelfRefine, PRM, ET). Combined with v1 results (n=5), the ranking shifts significantly: SelfRefine emerges as more consistent than initially thought, while ET's high v1 average was inflated by an outlier.

## v2 Individual Results

| Source PR | Technique | Score | Delta | Outcome |
|-----------|----------|-------|-------|---------|
| #6279 | ET | 79 | +29 | PR #6311 created → closed (score low) |
| #6273 | ET | 74 | -1 | PR #6313 created → closed (delta negative) |
| #6267 | SelfRefine | 88.5 | +13.5 | PR #6312 (draft) |
| #6266 | SelfRefine | 90 | +15 | no PR (already merged) |
| #6269 | SelfRefine | — | 0 | no diff (already merged) |

## v2 Issues

- **recreator-6273 bug**: violated threshold rule (delta=-1 but created PR anyway). Fixed by closing #6313.
- PR #6311 closed (score 79 too low to warrant merge)
- PR #6313 closed (delta -1 means recreation was worse than original)

## Combined v1+v2 Ranking (n=8)

| Technique | PRs | Scores | Average | Notes |
|----------|-----|--------|---------|-------|
| SelfRefine | 2 | 90, 88.5 | **89.25** | Consistent across 2 PRs |
| ET | 2 | 79, 74 | **76.5** | Much lower than v1 avg of 90.2 |
| PRM | 0 | — | — | No v2 PRs |

## Key Insight: ET Inflated by v1 Outlier

v1 results showed ET at 90.2 average (n=5). But v2 shows ET at 76.5 average (n=2). The high v1 ET average was driven by PR #6277 which scored 100 — likely an outlier. SelfRefine's 89.25 (consistent across 2 PRs in v2) is more reliable than ET's 76.5.

**Conclusion**: Need n=15 total to confirm ranking. 5 PRs per technique still insufficient.

## Recommendations

- **Do NOT merge PRs #6293-#6307** until v3 validates or refutes the ranking
- **Next bead**: br-69k (Run v3 on more PRs to reach n=15)
- **SelfRefine**: Best choice for medium/complex PRs based on current evidence
- **ET**: Good for validation-style tasks but inconsistent for complex refactors

## Connections
- [[PRRecreatePipeline]] — v1 methodology
- [[SelfRefine]] — technique
- [[ExtendedThinking]] — technique
- [[ProcessRewardModel]] — technique
- [[cycle_pr-recreate-v1]] — v1 synthesis
