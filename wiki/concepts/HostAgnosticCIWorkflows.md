---
title: "Host-Agnostic CI Workflows"
type: concept
tags: [CI, self-hosted, infrastructure]
sources: []
last_updated: 2026-02-24
---

## Definition

Host-Agnostic CI Workflows is an infrastructure principle where CI logic defaults to portable assumptions (Linux-like environments) rather than runner-specific paths, with explicit host-specific jobs only for runner infrastructure verification.

## Problem

Non-portable CI assumptions cause runner fragility. Notably, non-interactive `sudo` calls on self-hosted runners fail unpredictably.

## Decision Record

1. **Default**: host-agnostic workflows for CI logic (keep Linux-like assumptions)
2. **Exception**: host-specific jobs only for runner infrastructure verification (e.g., runner binary checks)
3. **Defer**: full containerization of all self-hosted jobs to a dedicated follow-up PR

## Pattern

```
CI Workflow Layer (host-agnostic)
  └── Tool cache / runner setup (host-specific, separate job)
        └── Binary verification (host-specific)
```

## Related Patterns

- [[Style Guide Compliance Gate]] — uses GitHub Actions for automated gates
- [[Defensive Field Normalization]] — defensive programming principles applied to infrastructure

## Sources

- BD-runner-hosting-strategy: decision record for self-hosted runner strategy
