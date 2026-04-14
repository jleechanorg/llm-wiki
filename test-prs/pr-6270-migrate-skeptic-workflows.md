# PR #6270: Infrastructure — Migrate to Reusable Skeptic Workflows

**URL:** https://github.com/jleechanorg/worldarchitect.ai/pull/6270
**Author:** jleechanorg
**State:** OPEN
**Date:** 2026-04-14

## Summary

Infrastructure refactor: extracts ~430-line inline script from `.github/workflows/skeptic-cron.yml` to a separate file `.github/scripts/skeptic-evaluate.sh`. Avoids GitHub Actions expression-length limits that can block workflow dispatch.

## Changes

- Deleted inline script from `skeptic-cron.yml` workflow
- Created `.github/scripts/skeptic-evaluate.sh` (standalone bash script)
- Uses `set -euo pipefail`, PIPESTATUS checking
- No functional behavior change — purely infrastructure reorganization

## Test Impact

No functional tests — workflow-only change. Shell script has inline error handling.

## Risk

Very low — purely structural refactor, no behavior change.

## Architecture

This PR demonstrates the **Hook-First Safety** pattern (H4 from auto-research): pre-tool-call intercepts are more reliable than policy documentation.
