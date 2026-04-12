---
title: "SkepticGatePaginationBug"
type: concept
tags: [skeptic, pagination, CI, green-gate, worldarchitect]
sources: [930ed371d6]
last_updated: 2026-04-12
---

## Summary

`SkepticGatePaginationBug` is a bug in the green-gate CI pagination loop where `--jq` and `--paginate` flags are incompatible. The pagination logic cannot handle skeptic output formatted with `--jq` filters.

## The Bug

The green-gate CI script uses pagination to iterate through PR checks. When `--jq` is applied to format output, the pagination loop's line-counting logic breaks because `--jq` produces JSON that doesn't match the expected single-line-per-item format.

## Code Pattern (buggy)

```bash
# Paginate with jq filter — breaks pagination loop
gh run list --jq '.[] | .name' | while read item; do
    process "$item"
done
```

## Correct Fix

Either use `--paginate` OR `--jq`, not both in the same pipeline. Or use a different pagination approach that handles JSON streams.

## Related

- [[PRWatchdog]] — PR monitoring
- [[SkepticGate]] — Skeptic gate system
- [[SkepticGatePaginationLoop]] — Pagination loop concept
