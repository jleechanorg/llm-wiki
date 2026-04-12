---
title: "PR #6154: chore(deps): bump cryptography from 46.0.6 to 46.0.7"
type: source
tags: [dependencies, python:uv]
date: 2026-04-09
source_file: raw/prs-worldarchitect-ai/pr-6154.md
sources: []
last_updated: 2026-04-09
---

## Summary
Lockfile-only dependency update patching CVE-2026-39892 (non-contiguous buffer handling/buffer overflow risk). Updates cryptography from 46.0.6 to 46.0.7 via `uv.lock`. No application/runtime code changes. All CI checks passed.

## Key Claims
- Security fix: CVE-2026-39892 patched (buffer overflow risk in non-contiguous buffer handling)
- Lockfile-only change — 1 file modified
- All validation checks green (directory tests, ESLint, merge commit validation, coverage, Ruff, mypy, schema coverage guard, skeptic gate)

## Metadata
- **PR**: #6154
- **Merged**: 2026-04-09
- **Author**: app/dependabot
- **Stats**: +43/-42 in 1 files
- **Labels**: dependencies, python:uv

## Connections
