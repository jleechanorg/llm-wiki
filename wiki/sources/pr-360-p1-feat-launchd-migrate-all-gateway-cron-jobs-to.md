---
title: "PR #360: [P1] feat(launchd): migrate all gateway cron jobs to launchd with central installer"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-360.md
sources: []
last_updated: 2026-03-23
---

## Summary
- Migrate all 5 gateway cron jobs from ~/.openclaw/cron/jobs.json to tracked launchd plist templates
- Create central install entrypoint: scripts/install-openclaw-launchd.sh
- Fix broken CONFIG_DIR=openclaw-config/ references (directory doesn't exist)
- Fix unescaped & XML entities in ai.openclaw.lifecycle-manager.plist.template
- Convert hardcoded plists to templates: ai.agento.dashboard.plist, ai.openclaw.schedule.bug-hunt-9am.plist
- Document live-vs-tracked distinction in docs/CRON_MIGRATION

## Metadata
- **PR**: #360
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +1519/-142 in 19 files
- **Labels**: none

## Connections
