---
title: "Theme Migration"
type: concept
tags: [localStorage, migration, pattern]
sources: ["theme-manager"]
last_updated: 2026-04-08
---

Pattern for migrating deprecated localStorage keys to new keys while preserving user preferences. In ThemeManager, 'preferred-theme' is migrated to 'theme', and 'light' is converted to 'default' to maintain backwards compatibility with older storage formats.
