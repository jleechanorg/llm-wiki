---
name: Unexpected cmux input attribution protocol
description: Unexpected text in a cmux/Claude prompt must be attributed from cmux focus logs, transcript submission state, gateway logs, Slack search, and socket evidence before claiming compromise.
type: feedback
bead: none
---

# Unexpected cmux input attribution protocol

On 2026-06-25 at about 21:39 PDT, `hello` appeared in a Claude prompt inside the `.hermes` cmux workspace. The investigation found per-character cmux focus-log input at `2026-06-26T04:39:35Z`, route signature `src=shortcut.routing reason=event_window`, no submitted `hello` in the Claude transcript, no Hermes gateway inbound event, no Hermes state/session record, no relevant Slack-origin `hello`, and no persisted socket/API audit entry tying `surface.send_text` or `cmux send` to the text.

Rule: treat `shortcut.routing reason=event_window` as local window keyboard-event evidence, not socket-send evidence. It supports physical keyboard, remote desktop, or macOS synthetic key event as possible classes, but not a named person/process without additional proof.

Recurrence protocol: search `/Users/jleechan/Library/Logs/cmux-focus.log` for the exact prompt text and surrounding `cmdn.route` records; cross-check Claude transcript, Hermes gateway logs, Hermes state DBs, Slack search, and cmux socket/API audit evidence. Preserve 2 minutes of cmux focus log around the event.
