---
title: "Claude Code Version Stability Report v2.1.77–v2.1.92"
type: source
tags: [claude-code, version-stability, upgrades, compaction, hooks]
date: 2026-04-05
source_file: raw/claude-code-version-stability-2026-04-05.md
---

## Summary
Comprehensive stability analysis of Claude Code versions v2.1.77 through v2.1.92. Key recommendation: upgrade to v2.1.85 (GREEN) which includes all fixes from v2.1.78–v2.1.84 without regressions. Avoid v2.1.86 (RED — agent work destruction), v2.1.87 (RED — broken hotfix), and v2.1.90 (RED — --continue data loss). Compaction is a platform-wide issue across all versions. PreCompact/PostCompact hooks are NOT yet implemented despite multiple feature requests.

## Key Claims
- **v2.1.85** is the recommended upgrade target: GREEN, includes conditional hook filtering, transcript search, CwdChanged/FileChanged hooks, --resume fixes, without v2.1.86 destructive regression
- **v2.1.86** is critical: multiple reports of agent destroying user work (#40808, 20+ hour loss)
- **v2.1.90** introduces --continue data loss: `sessionKind` filter silently discards -p sessions on --continue
- Compaction threshold bug (~150K regardless of 1M window) is NOT version-specific — persists across all versions
- PreCompact/PostCompact hooks NOT IMPLEMENTED despite requests #17237, #33088, #36749, #38018, #40492, #43733, #43946
- Claude Code v2.1.89 has autocompact thrash loop fix (3 consecutive refill-to-limit cycle detection)
- .claude/ directory has special built-in protection that overrides user permission settings — architectural, not version-specific

## Stability Matrix
```
v2.1.77  [=====] GREEN   ← baseline (current)
v2.1.78  [===  ] YELLOW  ← .claude/ permission regression
v2.1.79  [=====] GREEN
v2.1.80  [===  ] YELLOW  ← acceptEdits Write regression (fixed)
v2.1.81  [=====] GREEN
v2.1.83  [=====] GREEN   ← CwdChanged/FileChanged hooks, transcript search
v2.1.84  [=====] GREEN
v2.1.85  [=====] GREEN   ← RECOMMENDED upgrade target
v2.1.86  [=    ] RED     ← agent work destruction
v2.1.87  [=    ] RED     ← broken hotfix
v2.1.88  [===  ] YELLOW  ← MCP tool result regression
v2.1.89  [===  ] YELLOW  ← big release, good fixes, some risk
v2.1.90  [=    ] RED     ← --continue data loss
v2.1.91  [===  ] YELLOW  ← pgrep crash, cache invalidation
v2.1.92  [===  ] YELLOW  ← multiple regressions, active fixes
```

## Connections
- [[ClaudeCode]] — the application under version analysis
- [[Compaction]] — platform-wide issue across all versions
- [[HookSystem]] — PreCompact hooks not implemented despite requests
- [[ClaudeCodePermissionIssues]] — .claude/ directory protection is architectural
