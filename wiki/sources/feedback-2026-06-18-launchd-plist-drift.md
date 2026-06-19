---
title: "Hermes ecosystem breaks from launchd plist drift (scripts moved/deleted)"
type: source
tags: [feedback, launchd, macos, hermes, anti-pattern, infra-resilience]
date: 2026-06-18
source_file: ../../raw/feedback_2026-06-18_launchd_plist_drift.md
---

## Summary

The Hermes ecosystem (gateway, qdrant, sync, mem0-server, /history, /ms) "always keeps breaking" because of **launchd plist drift**: plists reference scripts at hardcoded paths that get moved/deleted during refactors, but the plists never get updated. Exit code 127 silently accumulates. On 2026-06-18, audit found 13 plists at exit 127, 11 at exit 1, 6 at exit 78. The structural defense is the `~/.claude/skills/launchd/SKILL.md` 6-step protocol — most importantly step 4 (commit template to owning repo), which was skipped for the broken plists today.

## Key Claims

- launchd plist drift is a **systemic root cause**, not incidental. Same pattern recurs across many services.
- The `/launchd` skill exists precisely to prevent this; today's drift happened because the canonical 6-step protocol was not followed for several plists.
- Hand-authored plists drift; template-rendered plists (using `@HOME@` placeholders + commit-to-repo) cannot.
- When the gateway crashes, every dependent service degrades simultaneously — user perceives this as "everything is broken again" but it's one structural failure manifesting across many surfaces.
- Permanent fix proposed: nightly audit cron (`jleechan-vuh` / GH #709) that catches exit-127 plists before they accumulate.

## Key Quotes

> "Plists reference scripts at hardcoded paths that get moved/deleted during refactors, but the plists never get updated. Exit code 127 silently accumulates."

> "Hand-authored launchd plists drift. The `launchd-plist-template` rule exists precisely to prevent this — every plist must have a template in `~/.hermes/launchd/` and the installed copy must be rendered from that template."

## Connections

- [[LaunchdPlistTemplate]] — the rule this finding reinforces
- [[HermesMem0Qdrant]] — mem0-specific qdrant container setup (today's fix)
- [[MacOsLaunchd]] — `/launchd` skill content (the canonical 6-step protocol)
- [[JleechanVuh]] — bead / GH issue for the nightly audit cron
- [[AO_Session_Accumulation]] — sister finding (CPU overload from worker accumulation)
