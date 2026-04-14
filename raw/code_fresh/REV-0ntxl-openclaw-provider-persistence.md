# REV-0ntxl: OpenClaw Provider Persistence Guard

**Status:** IN_PROGRESS
**Priority:** High
**Component:** mvp_site/frontend_v1/js/settings.js, mvp_site/frontend_v1/tests/settings_listeners.test.js
**Created:** 2026-02-20
**Branch:** fix/openclaw-provider-persistence-indep

## Problem

Saved settings could send `llm_provider: "gemini"` when the provider radio state was not selectable/readable at save time, even when the persisted server setting was `openclaw`.

## Root Cause

- `readEntryValue()` fell back radio fields to `entry.defaultValue` (`gemini`) when no radio was selected.
- `saveSettings()` aborted only when no radio selected, but other callers could still produce provider flips via schema-driven payload construction.

## Fix

- Added `lastKnownProvider` tracking from loaded server settings (initialized to `null` to avoid false gemini fallback before settings load).
- Restored radio `readEntryValue` nullish-coalescing fallback (`?? entry.defaultValue`) for future radio type safety.
- In `saveSettings()`, resolved provider from:
  1) selected radio,
  2) last loaded setting (`window.__loadedSettings.llm_provider`),
  3) fallback `"gemini"`.
- Validated `resolvedProvider` against `SETTINGS_SCHEMA` allowed list before saving.
- Updated `window.__loadedSettings.llm_provider` and `lastKnownProvider` after each successful save so subsequent saves use the latest persisted value, not the stale load-time cache.
- Prevented auto-generation of `llm_provider` from schema default in payload assembly.
- Explicitly set `settingsToSave.llm_provider` from the resolved value.
- Added optional chaining (`settings?.llm_provider`) when reading loaded settings in `loadSettings()`.
- Backend: tightened `is_model_only_update` guard to prevent provider inference on mixed payloads.

## Validation

- Added regression tests in `mvp_site/frontend_v1/tests/settings_listeners.test.js`:
  - With all provider radios unchecked and loaded provider set to `openclaw`, save payload preserves `llm_provider: "openclaw"`.
  - After saving `openrouter`, subsequent save with radios unchecked still sends `openrouter` from updated cache.
  - Invalid cached provider value (`not-a-provider`) falls back to `"gemini"` via schema validation.
- Target tests run:
  - `node --test mvp_site/frontend_v1/tests/settings_listeners.test.js`
  - `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q mvp_site/tests/test_settings_api.py`

## Notes

- `pytest` without `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` crashes in this environment (segmentation fault), so the pytest run above uses plugin disable override.
