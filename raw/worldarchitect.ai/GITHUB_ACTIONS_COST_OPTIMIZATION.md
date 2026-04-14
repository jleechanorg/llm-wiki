# GitHub Actions Cost Optimization

**Analysis Period:** Feb 1-18, 2026 (18 days)
**Total Cost:** $671.66 (Net)
**Projected Annual Cost:** ~$13,617/year

---

## Cost Breakdown

| Workflow | Cost | % of Total |
|----------|------|------------|
| test.yml | $356.24 | 53% |
| presubmit.yml | $83.22 | 12% |
| pr-preview.yml | $81.44 | 12% |
| coverage.yml | $47.30 | 7% |
| Other workflows | $103.46 | 16% |

---

## What Was Already Implemented ✅

The following optimizations were already in place:

- **Path filtering** on test.yml (`paths-ignore: '**/*.md', 'docs/**', 'roadmap/**'`)
- **Path filtering** on pr-preview.yml (runs only on `mvp_site/**`, `infrastructure/**`, etc.)
- **Caching** for pip, venv, and testmon data in test.yml
- **Directory-based test execution** to only run tests for changed code

---

## Implemented Changes 🆕

### Concurrency Limits

Added concurrency groups to top workflows to cancel redundant runs when new commits are pushed:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

**Applied to:**
- test.yml
- presubmit.yml
- pr-preview.yml
- coverage.yml

**Not applied to:**
- test-deployment.yml (Cloud Build - cancellation can orphan builds)

**Estimated savings:** ~$30/month (10-15% reduction)

---

## Potential Future Optimizations

### 1. Limit cursor[bot] Workflows

**Problem:** cursor[bot] runs 43 workflows totaling $81.86/month

**Solution:** Restrict to specific paths:
```yaml
on:
  pull_request:
    paths:
      - 'mvp_site/**'
```

### 2. Reduce Test Run Duration

Currently averaging 2,239 minutes/run on test.yml. Consider:
- Further test parallelization
- Faster test selection with testmon (already in use)

---

## Verification

Check current workflow configurations:
```bash
grep -r "paths-ignore\|paths:\|concurrency" .github/workflows/
```
