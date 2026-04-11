---
title: "Debug Events Export Tests"
type: source
tags: [python, testing, export, debug, campaign]
source_file: "raw/test_debug_events_export.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating that all debug events are properly included in campaign exports. Tests `_format_debug_events` and `format_story_entry` functions for comprehensive coverage of background_events, faction_updates, rumors, scene_events, and complications.

## Key Claims
- **Background events formatting**: Both dict and string format background_events are properly formatted with appropriate icons
- **Comprehensive debug sections**: All debug event types (background_events, faction_updates, rumors, scene_event, complications) are included in exports
- **Mixed content handling**: Tests verify handling of mixed string/dict background_events arrays
- **Empty handling**: Empty debug_info returns empty string, preserving export format integrity

## Key Test Cases
| Test | Scenario | Expected |
|------|----------|----------|
| test_format_debug_events_with_background_events | background_events with dict entries | All fields formatted with icons |
| test_format_debug_events_comprehensive | All debug event types | All sections present in output |
| test_format_debug_events_with_string_events | Mixed string/dict events | String events get ⏳ icon |
| test_format_debug_events_empty | Empty/None debug_info | Empty string returned |
| test_format_debug_events_empty_background_events | Empty background_events array | Empty string returned |

## Connections
- [[DocumentGenerator]] — module containing `_format_debug_events`
- [[CampaignExport]] — feature this test validates
- [[LivingWorldDebugging]] — related to debug event handling
