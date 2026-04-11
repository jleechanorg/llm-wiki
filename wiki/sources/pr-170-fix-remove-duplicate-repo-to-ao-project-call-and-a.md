---
title: "PR #170: fix: remove duplicate repo_to_ao_project call and add author notification tests"
type: source
tags: []
date: 2026-03-15
source_file: raw/prs-worldai_claw/pr-170.md
sources: []
last_updated: 2026-03-15
---

## Summary
- Remove redundant duplicate `repo_to_ao_project` call in github-intake.sh (was called at both lines 116 and 155 with no code in between modifying repo_name)
- Add test coverage for `reason=author` notification classification

## Metadata
- **PR**: #170
- **Merged**: 2026-03-15
- **Author**: jleechan2015
- **Stats**: +152/-3 in 5 files
- **Labels**: none

## Connections
