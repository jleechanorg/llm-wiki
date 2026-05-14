# Ruff Pre-Commit Checks Whole File, Not Just Diff

**Ingested**: 2026-05-10  
**Type**: feedback / tooling behavior  
**Classification**: Best Practice

## Summary

The ruff pre-commit hook scans **entire staged files**, not just the changed lines. If a file has pre-existing violations, your commit fails even when your added lines are clean.

## Key Rule

Before staging a file: `ruff check <file>`. If violations exist, fix them first or skip staging that file for this commit.

## Incident Reference

2026-05-10: 9 lines added to `mvp_site/llm_providers/gemini_provider.py` — commit blocked by 13 pre-existing ruff errors (PLR0912, PIE810, ARG002, etc.).
