---
title: "GitHub Actions Cost Optimization"
type: source
tags: [worldarchitect-ai, github-actions, cost-optimization, ci/cd]
sources: []
date: 2026-04-07
source_file: raw/github-actions-cost-optimization.md
last_updated: 2026-04-07
---

## Summary
Analysis of GitHub Actions costs for WorldArchitect.AI over 18 days (Feb 1-18, 2026), totaling $671.66 with projected annual cost of ~$13,617/year. Documents existing optimizations and newly implemented concurrency limits with estimated 10-15% monthly savings.

## Key Claims
- **Total cost:** $671.66 (18 days), projected ~$13,617/year
- **test.yml is dominant cost:** $356.24 (53% of total)
- **Already implemented:** Path filtering, pip/venv/testmon caching, directory-based test execution
- **New optimization:** Concurrency groups to cancel redundant runs (~10-15% / ~$30/month savings)
- **cursor[bot] opportunity:** 43 workflows/month costing $81.86 — could restrict to `mvp_site/**` paths
- **Test duration bottleneck:** 2,239 minutes/run average on test.yml

## Cost Breakdown

| Workflow | Cost | % of Total |
|----------|------|------------|
| test.yml | $356.24 | 53% |
| presubmit.yml | $83.22 | 12% |
| pr-preview.yml | $81.44 | 12% |
| coverage.yml | $47.30 | 7% |
| Other workflows | $103.46 | 16% |

## Applied Concurrency Groups

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

Applied to: test.yml, presubmit.yml, pr-preview.yml, coverage.yml

Not applied to: test-deployment.yml (Cloud Build - cancellation can orphan builds)

## Connections
- [[WorldArchitect.AI]] — the project this cost optimization applies to
- [[WorldArchitect.AI GitHub Actions Auto-Deployment]] — related CI/CD infrastructure