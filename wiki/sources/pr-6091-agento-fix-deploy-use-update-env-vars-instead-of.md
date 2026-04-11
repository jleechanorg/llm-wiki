---
title: "PR #6091: [agento] fix(deploy): use --update-env-vars instead of --set-env-vars when --remove-env-vars is also set"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldarchitect-ai/pr-6091.md
sources: []
last_updated: 2026-04-04
---

## Summary
- **Root cause**: `gcloud run deploy` rejects simultaneous `--set-env-vars` and `--remove-env-vars` as mutually exclusive
- **Symptom**: `ERROR: (gcloud.run.deploy) argument --set-env-vars: At most one of --clear-env-vars | --env-vars-file | --set-env-vars | --remove-env-vars --update-env-vars can be specified.`
- **Fix**: when `REMOVE_ENV_VARS` is set (dev/preview), use `--update-env-vars` instead of `--set-env-vars`. `--update-env-vars` adds/overrides only the specified vars and is compatible

## Metadata
- **PR**: #6091
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +13/-2 in 2 files
- **Labels**: none

## Connections
