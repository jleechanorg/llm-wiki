---
title: "ThemeManager JavaScript Class"
type: source
tags: [theme, javascript, localStorage, migration, frontend]
source_file: "raw/theme-manager.js"
sources: []
last_updated: 2026-04-08
---

## Summary
JavaScript class that manages theme selection, persistence, and switching in the WorldAI frontend. Supports default and fantasy themes with localStorage-based preferences, migration from legacy storage keys, URL parameter overrides for testing, and custom event dispatching on theme changes.

## Key Claims
- **Theme Options**: Default (☀️) and Fantasy (⚔️) themes, with fantasy only enabled when `__WORLDAI_FANTASY_THEME_ENABLED` is not explicitly false
- **Persistence**: Theme preference stored in localStorage under 'theme' key with migration path from deprecated 'preferred-theme' and 'light' keys
- **Testing Support**: URL parameter `test_theme` allows theme override during development/testing
- **Event System**: Dispatches 'themeChanged' custom event when theme updates, enabling other components to react
- **Bootstrap Integration**: Respects `__WORLDAI_THEME_BOOTSTRAP_THEME` as bootstrap-provided fallback theme

## Connections
- [[ThemeSystem]] — the overall theme architecture
- [[LocalStorageMigration]] — pattern for migrating deprecated storage keys
- [[CustomEventPattern]] — event-driven communication between components

## Contradictions
- []
