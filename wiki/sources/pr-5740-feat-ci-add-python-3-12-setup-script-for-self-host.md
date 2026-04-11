---
title: "PR #5740: feat(ci): add Python 3.12 setup script for self-hosted runners"
type: source
tags: []
date: 2026-02-23
source_file: raw/prs-worldarchitect-ai/pr-5740.md
sources: []
last_updated: 2026-02-23
---

## Summary
- Adds `scripts/setup-python-runner.sh` to bootstrap Python 3.12 with venv and pip on self-hosted runners
- Adds `scripts/RUNNER_DEPLOYMENT.md` with deployment guide (SSH, GitHub Actions workflow, and direct command options)
- Eliminates "ensurepip not available" errors on self-hosted runners
- Removes need for GitHub-hosted runner fallbacks

## Metadata
- **PR**: #5740
- **Merged**: 2026-02-23
- **Author**: jleechan2015
- **Stats**: +281/-0 in 2 files
- **Labels**: none

## Connections
