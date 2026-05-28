# Resilient MCP and Playwright video smoke test conflict resolution

- **Date:** 2026-05-28
- **Type:** Best Practice
- **PR:** [#7110](https://github.com/jleechanorg/worldarchitect.ai/pull/7110)
- **Bead:** `rev-2av80`

## Description
Clean merge conflict resolution in integration and video smoke tests requires blending branch-added environment cleanups/telemetry and Playwright browser check resiliency with main's refactored schemas. Pre-flight Playwright browser engine checks keep tests robust against environmental failures on self-hosted vs local runners.
