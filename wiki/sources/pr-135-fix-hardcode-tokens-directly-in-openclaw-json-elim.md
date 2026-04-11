---
title: "PR #135: fix: hardcode tokens directly in openclaw.json, eliminate all ${ENV_VAR} placeholders"
type: source
tags: []
date: 2026-03-14
source_file: raw/prs-worldai_claw/pr-135.md
sources: []
last_updated: 2026-03-14
---

## Summary
The gateway was using \`\${ENV_VAR}\` placeholders in \`openclaw.json\` that were resolved from launchd plist \`EnvironmentVariables\` at runtime. When the plist and \`~/.bashrc\` drifted (after token rotation), Slack Socket Mode crashed with \`invalid_auth\`.

**Fix: delete all \${ENV_VAR} indirection — hardcode real tokens directly in \`openclaw.json\`.**

## Metadata
- **PR**: #135
- **Merged**: 2026-03-14
- **Author**: jleechan2015
- **Stats**: +134/-1327 in 16 files
- **Labels**: none

## Connections
