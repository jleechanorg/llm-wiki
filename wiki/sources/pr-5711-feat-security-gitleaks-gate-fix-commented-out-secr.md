---
title: "PR #5711: feat(security): gitleaks gate + fix commented-out secret filter in backup_dotfiles"
type: source
tags: []
date: 2026-02-22
source_file: raw/prs-worldarchitect-ai/pr-5711.md
sources: []
last_updated: 2026-02-22
---

## Summary
- Fix `filter_sensitive_data()` to redact commented-out `# export TOKEN=...` lines — previously these slipped past all sed patterns due to the `#` prefix
- Add `run_gitleaks_gate()` that runs `gitleaks detect --no-git --redact` on the backup output directory **before** any `git add/commit`, aborting if secrets are found
- Refresh `scripts/dotfiles_backup/bashrc_macbook.txt` from current `~/.bashrc` (clean scan confirmed)

**Key themes:** secret hygiene hardening, defense-in-depth for dotfile bac

## Metadata
- **PR**: #5711
- **Merged**: 2026-02-22
- **Author**: jleechan2015
- **Stats**: +200/-82 in 3 files
- **Labels**: none

## Connections
