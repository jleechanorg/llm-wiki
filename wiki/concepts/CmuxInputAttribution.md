---
title: "cmux Input Attribution"
type: concept
tags: [cmux, security, incident-response, terminal-control]
sources: [feedback-2026-06-25-cmux-unexpected-input-attribution]
last_updated: 2026-06-25
---

# cmux Input Attribution

## Summary

cmux prompt text should be attributed by route signature and corroborating artifacts, not by the visible text alone. `shortcut.routing reason=event_window` indicates local window keyboard-event routing; socket/API injection should have evidence from the `surface.send_text`, `surface.send_key`, or `cmux send` path.

## Protocol

- Check whether text was submitted to Claude/Hermes or only remained in the prompt buffer.
- Search `/Users/jleechan/Library/Logs/cmux-focus.log` for literal characters and surrounding `cmdn.route` records.
- Cross-check Claude transcripts, Hermes gateway logs, Hermes state DBs, Slack history, and cmux socket/API audit evidence.
- Treat installed remote-control tools as context only unless there is exact-time active-session proof.

## Related

- [cmux](../entities/cmux.md)
- [Security Analysis](SecurityAnalysis.md)
