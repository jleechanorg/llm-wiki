---
title: "PR #126: chore: rehome repo — ~/.openclaw/ as git root (ORCH-d6i)"
type: source
tags: []
date: 2026-03-14
source_file: raw/prs-worldai_claw/pr-126.md
sources: []
last_updated: 2026-03-14
---

## Summary
- Move \`openclaw-config/\` contents to repo root via \`git mv\` (history preserved)
- Clone target is now \`~/.openclaw/\` — files are live in place, no sync needed
- Remove \`scripts/sync-openclaw-config.sh\` (replaced by \`scripts/bootstrap.sh\`)
- Update \`.gitignore\`, \`tests/\`, \`scripts/doctor.sh\`, \`CLAUDE.md\`, \`AGENTS.md\` for new layout

## Metadata
- **PR**: #126
- **Merged**: 2026-03-14
- **Author**: jleechan2015
- **Stats**: +492/-1372 in 46 files
- **Labels**: none

## Connections
