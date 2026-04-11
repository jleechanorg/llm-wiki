---
title: "GitHub Actions Cost Optimization"
type: source
tags: [github-actions, ci-cd, cost-optimization, workflows]
date: 2026-04-07
source_file: /Users/jleechan/repos/worldarchitect-ai/.github/workflows/cost-analysis.md
last_updated: 2026-04-07
---

## Summary
Analysis of GitHub Actions costs over 18 days (Feb 1-18, 2026) reveals $671.66 total cost with projected annual cost of ~$13,617/year. Test.yml dominates at 53% of costs. Already implemented optimizations include path filtering, caching, and directory-based test execution. New concurrency limits provide ~10-15% monthly savings. Future optimization opportunities include limiting cursor[bot] workflows and reducing test run duration.

## Key Claims
- **Total Cost**: $671.66 over 18 days, projected ~$13,617/year
- **Cost Distribution**: test.yml ($356.24, 53%), presubmit.yml ($83.22, 12%), pr-preview.yml ($81.44, 12%), coverage.yml ($47.30, 7%)
- **Existing Optimizations**: Path filtering, pip/venv/testmon caching, directory-based test execution already in place
- **New Concurrency Limits**: Added to test.yml, presubmit.yml, pr-preview.yml, coverage.yml — cancels redundant runs on new commits
- **Estimated Savings**: ~$30/month (10-15% reduction) from concurrency limits
- **Future Opportunity**: cursor[bot] runs 43 workflows totaling $81.86/month — could restrict to specific paths
- **Test Duration**: test.yml averages 2,239 minutes/run — potential for further parallelization

## Key Quotes
> "test.yml | $356.24 | 53%" — dominant cost driver
> "cursor[bot] runs 43 workflows totaling $81.86/month" — optimization target
> "concurrency: group: ${{ github.workflow }}-${{ github.ref }}, cancel-in-progress: true" — prevents redundant runs

## Connections
- [[GitHub Development Statistics]] — related DORA metrics showing 12.5/day deployment frequency
- [[GitHub Actions Auto-Deployment]] — deployment workflow this cost analysis applies to

## Contradictions
- None identified
