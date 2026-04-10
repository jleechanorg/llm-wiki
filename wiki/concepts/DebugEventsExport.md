---
title: "Debug Events Export"
type: concept
tags: [export, debugging, campaign, feature]
sources: [debug-events-export-tests]
last_updated: 2026-04-08
---

## Description
Feature in document_generator module that formats debug events for campaign exports. Exports background_events, faction_updates, rumors, scene_events, and complications.

## Implementation
- `_format_debug_events(debug_info)` — main formatting function
- `format_story_entry()` — uses debug events in story export
- Handles both dict and string format background_events
- Returns empty string for empty/None debug_info

## Event Types
| Type | Icon | Description |
|------|------|-------------|
| background_events | 📜 | Actor, action, event_type, status |
| faction_updates | 🏛️ | Faction objectives, progress, resources |
| rumors | 💬 | Rumor content and accuracy |
| scene_event | 🎭 | Scene type, actor, description |
| complications | ⚠️ | Type, severity, description |

## Connections
- [[DocumentGenerator]] — contains export functions
- [[CampaignExport]] — uses debug events in exports
- [[LivingWorldDebugging]] — debug event generation
