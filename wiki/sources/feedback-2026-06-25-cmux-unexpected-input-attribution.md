---
title: "Unexpected cmux Input Attribution Protocol"
type: source
date: 2026-06-25
tags: [cmux, hermes, security, incident-response, slack, remote-control]
source_path: "/Users/jleechan/.Codex/projects/-Users-jleechan-.hermes/memory/feedback_2026-06-25_cmux_unexpected_input_attribution.md"
---

# Unexpected cmux Input Attribution Protocol

## Summary

Unexpected text in a cmux/Claude prompt is not enough evidence to claim Hermes, Slack, socket injection, or external compromise. Attribute it by combining cmux focus-log route signatures, Claude transcript state, Hermes gateway/state artifacts, Slack search, and cmux socket/API evidence.

## Incident

On 2026-06-25 at about 21:39 PDT, `hello` appeared in the `.hermes` cmux workspace prompt. The cmux focus log showed per-character input at `2026-06-26T04:39:35Z` with `src=shortcut.routing reason=event_window`.

The investigation found:

- No submitted `hello` user message in the Claude transcript.
- No Hermes gateway inbound Slack/message event around the incident time.
- No Hermes state DB or session file matching a message around the incident.
- No relevant Slack-origin `hello`.
- No persisted socket/API audit entry for `surface.send_text`, `surface.send_key`, or `cmux send`.
- Remote-control tools were installed/running, but no exact-time active session proved the event.

## Rule

Classify `shortcut.routing reason=event_window` as local window keyboard-event evidence, not socket-send evidence. It may be physical keyboard input, remote-desktop input, or macOS synthetic key automation. Do not name a person or process without exact supporting evidence.

## Recurrence Protocol

1. Search `/Users/jleechan/Library/Logs/cmux-focus.log` for the exact prompt text.
2. Extract two minutes around the event, including `cmdn.route` records.
3. Cross-check Claude transcript submission state.
4. Cross-check Hermes gateway logs, Hermes state DBs, session files, and Slack search.
5. Search cmux socket/API logs or source-level audit records for `surface.send_text`, `surface.send_key`, and `cmux send`.
6. Preserve evidence before restarting cmux or rotating logs.

[[jeffrey-oracle]]: NO.
