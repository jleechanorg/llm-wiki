# Codebase Statistics

**Last Updated:** 2026-01-30

## Overview

This document provides comprehensive statistics about the WorldArchitect.AI codebase, including lines of code breakdown, test coverage, and development metrics.

## Lines of Code Analysis

### Summary

- **Total Code:** 431,264 lines
  - Production: 205,262 lines
  - Test: 226,002 lines
  - **Test Coverage: 52.4%** (more test code than production!)

### Code by Language

| Language | Production | Test | Total | Test % |
|----------|------------|------|-------|--------|
| 🐍 Python (.py) | 145,054 | 207,829 | 352,883 | 58.9% |
| 🐚 Shell (.sh) | 40,626 | 10,995 | 51,621 | 21.3% |
| 🌟 JavaScript (.js) | 11,730 | 5,341 | 17,071 | 31.3% |
| 🎨 CSS (.css) | 4,322 | 0 | 4,322 | 0% |
| 🌐 HTML (.html) | 1,584 | 1,837 | 3,421 | 53.7% |
| ✨ JavaScript Modules (.mjs) | 1,916 | 0 | 1,916 | 0% |
| 📦 CommonJS (.cjs) | 30 | 0 | 30 | 0% |

### Config/Data Files (Excluded from Code Count)

| Type | Lines |
|------|-------|
| 🧾 TOML (.toml) | 29,818 |
| 🧾 JSON (.json) | 3,691 |
| 🧾 YAML (.yml) | 2,992 |
| 🧾 YAML (.yaml) | 670 |
| 🧾 INI (.ini) | 153 |
| 🧾 Config (.conf) | 138 |
| **Total** | **37,462** |

### Production Code by Functionality

| Functional Area | Lines | Primary Languages |
|----------------|-------|-------------------|
| Core Application (mvp_site/) | 70,890 | py:57,001, js:8,672, css:4,322 |
| Automation Scripts | 31,763 | py:21,686, sh:9,059, mjs:1,018 |
| AI Assistant (.claude/) | 21,165 | py:16,063, sh:4,204, mjs:898 |
| Task Management | 8,904 | py:8,264, sh:640 |
| Test Infrastructure | 13,788 | py:12,591, html:731, sh:466 |

## Development Metrics (Last 30 Days)

### Commit Statistics
- Total commits: 903
- Days with commits: 30
- Average commits/day: 30.1
- Fix commits: 255 (28.2%)
- Feature commits: 226 (25.0%)
- Other commits: 422 (46.7%)

### Pull Request Statistics
- Total merged PRs: 273
- Average PRs/day: 9.1
- Features: 84 (30.8%)
- Fixes: 106 (38.8%)
- Other: 62 (22.7%)
- Documentation: 5 (1.8%)
- Tests: 8 (2.9%)
- Refactoring: 8 (2.9%)

### DORA Metrics
- **Deployment Frequency:** 9.1 deployments/day
- **Lead Time for Changes:** 2.9 hours (0.1 days) median
- **Mean Time to Recovery:** 2.9 hours (0.1 days)

### PR Timing Metrics
- Average time to merge: 28.6 hours (1.2 days)
- Median time to merge: 2.9 hours (0.1 days)
- 95th percentile: 173.0 hours (7.2 days)
- Fastest merge: 0.0 hours
- Slowest merge: 625.8 hours (26.1 days)

### DORA Metrics by PR Size

| Size | PRs | Avg Lines | Deploy Freq | Lead Time |
|------|-----|-----------|-------------|-----------|
| 0-50 lines | 65 | 19 | 2.2/day | 0.3h |
| 50-100 lines | 27 | 78 | 0.9/day | 1.5h |
| 100-1000 lines | 114 | 469 | 3.8/day | 3.5h |
| 1000-10000 lines | 63 | 3,092 | 2.1/day | 28.2h |
| 10000+ lines | 4 | 20,012 | 0.1/day | 1.4h |

## Exclusions

The following are excluded from code counts:
- Documentation and processing data (docs/)
- Virtual environment (venv/)
- Planning documents (roadmap/)
- Prototypes (prototype*/)
- Package lock files (package-lock.json, yarn.lock)
- Node modules, git files
- Config/data files (JSON, YAML, TOML, INI) - shown separately above

## Key Insights

1. **Exceptional Test Coverage:** Python has 143% more test code than production code (207,829 test vs 145,054 production)
2. **High Development Velocity:** 9.1 PRs merged per day over the last 30 days
3. **Fast Lead Time:** Median of 2.9 hours from PR creation to merge
4. **Low Noise Ratio:** Only 3.1% of changes are vendor/generated files
5. **Multi-Language Stack:** Primarily Python (82% of code), with JavaScript, Shell, and web technologies

## How to Generate These Stats

Run the LOC analysis script:

```bash
# Full analysis (last 30 days)
./loc.sh

# Specific date range
./loc.sh 2025-01-01

# Skip LOC analysis, only git stats
./loc.sh --no-loc

# Include config files in code count
./loc.sh --include-config
```

The script uses `/Users/jleechan/projects/worktree_loc/scripts/analyze_git_stats.py` which provides:
- Lines of code breakdown by language
- Test vs production code analysis
- Functional area analysis
- Git commit statistics
- Pull request metrics
- DORA metrics (Deployment Frequency, Lead Time, MTTR)

## Historical Trends

### Weekly Breakdown (Last 5 Weeks)

| Week | PRs | Commits | Deploy Freq | Lead Time | Avg PR Size |
|------|-----|---------|-------------|-----------|-------------|
| 1 | 69 | 75 | 9.9/day | 1.7h | 478 lines |
| 2 | 60 | 183 | 8.6/day | 7.9h | 1,342 lines |
| 3 | 88 | 564 | 12.6/day | 3.6h | 1,164 lines |
| 4 | 32 | 54 | 4.6/day | 0.8h | 1,603 lines |
| 5 | 24 | 27 | 3.4/day | 4.4h | 2,682 lines |

### Trends (First Half vs Second Half)
- 📉 Deployment Frequency: declining (-25.6%)
- 📈 Lead Time: improving (-39.3%)
- 📉 Average PR Size: declining (+99.6%)
