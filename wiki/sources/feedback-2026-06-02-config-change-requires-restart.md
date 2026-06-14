---
title: "Feedback 2026-06-02 Config Change Requires Restart"
type: source
tags: [feedback, project, hermes, memory-file]
date: 2026-06-02
source_file: raw/memory_backfill_2026_06_13/feedback_2026-06-02_config_change_requires_restart.md
---

## Summary

Config file writes are cached at gateway startup and NOT hot-reloaded. A change to with no restart is a silent no-op — the running process continues with the old values indefinitely. : 2026-06-02 incident — hermes updated both and to (switching from M2.7) but never restarted the gateway.

## Key Claims

- (See raw memory file for full content)

## Key Quotes

_(No blockquotes in source)_

## Connections

_(No prior wiki links detected)_
