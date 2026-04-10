---
title: "Structured Fields"
type: concept
tags: [ui, structured-data, responses]
sources: [ui-verification-screenshots-test]
last_updated: 2026-04-08
---

Structured fields are UI elements that display AI response metadata: session headers, planning blocks, dice rolls, resources, and system warnings. Hidden by default, exposed via debug mode.

## Fields Tested
- `.session-header` — session progress indicators
- `.planning-block` — AI planning content
- `.dice-rolls` — dice roll results
- `.resources` — resource changes
- `.system-warnings` — warnings and alerts

## Connections
- [[DebugMode]] — enables visibility
- [[UIVerificationScreenshotsTest]] — verifies display
- [[StateUpdateFlow]] — data source for fields
