---
title: "Luke"
type: entity
tags: [user, tester]
sources: ["main-user-scenario-fix-god-mode-json"]
last_updated: 2026-04-08
---

Test user whose god mode scenario (scene 116) exposed raw JSON leakage issue. The test `test_luke_scenario_scene_116_type_issue` reproduces the exact type of malformed JSON that caused the original user-facing bug where raw JSON keys were displayed in god mode.

## Related Tests
- [[Main User Scenario Fix — No Raw JSON in God Mode]] — contains the reproducing test
