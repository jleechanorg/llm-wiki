---
title: "Hardened Virtualenv Bootstrap"
type: concept
tags: [CI, virtualenv, reproducibility]
sources: []
last_updated: 2026-02-24
---

## Definition

Hardened Virtualenv Bootstrap is a CI infrastructure pattern where the virtual environment bootstrap logic favors correctness and determinism over speed. It minimizes silent fallback behavior so that bootstrap issues surface clearly in CI rather than being hidden by cache reuse.

## Hardened vs Current Bootstrap

| Aspect | Current (Non-Hardened) | Hardened |
|---|---|---|
| Cache reuse | Reuse potentially unhealthy cached venv | Treat unhealthy cache as hard failure |
| Health check failure | Silent fallback | Hard failure or forced full rebuild |
| Bootstrap timeout | Falls back to fresh venv | Timeout = failure (no silent fallback) |
| Priority | Speed (cache hits) | Correctness and determinism |

## Decision Criteria

1. CI stability and flake rate — no regressions vs current path
2. End-to-end test runtime — within agreed CI budget
3. Reproducibility — local and CI environments match
4. Security — reduced supply-chain risk in dependency installation
5. Operational complexity — ease of debugging and maintenance

## CI Bootstrapping Layers

```
Venv creation (hardened)
  └── Health check (hardened — hard fail on failure)
        └── Dependency pinning verification
              └── Tool cache (host-specific, separate)
```

## Sources

- BD-pair_followup3-ci-test-hardened-venv-bootstrap.md: PR #5751 hardened bootstrap decision
