---
title: "cmux"
type: entity
tags: [terminal, tool, ai-productivity, open-source, yc]
sources: [stellar-work-ep57-eng-mgmt-ai, feedback-2026-06-25-cmux-unexpected-input-attribution]
last_updated: 2026-06-25
---

# cmux

**Type**: Terminal application
**Website**: cmux ux (mentioned in podcast)
**Stage**: Early-stage, YC-backed

## Summary

cmux is a terminal application designed for AI-augmented workflows. It features vertical tabs/workspaces, horizontal splitting, and terminal-ready notifications (e.g., "this tab is ready"). Jeff Lee-Chan ([JeffreyChan](JeffreyChan.md)) gave it a prominent shoutout on Stellar Work EP57, calling it "the best terminal I've ever used, especially for AI."

## Key Features

- **Vertical tabs/workspaces** — organize multiple AI agent sessions side-by-side
- **Horizontal splitting** — view multiple terminals simultaneously
- **Smart notifications** — alerts when a terminal tab or process is ready (critical for async AI agent workflows)
- **AI-optimized UX** — designed from the ground up for workflows involving AI coding agents

## Operational Notes

- **Input attribution** — unexpected prompt text should be attributed from cmux focus-log route signatures and corroborating artifacts. `shortcut.routing reason=event_window` is local window keyboard-event evidence; socket/API injection needs separate `surface.send_text`, `surface.send_key`, or `cmux send` evidence.

## Origin

Built by "young guys in their early 20s" with Y Combinator backing. Jeff mentioned talking to their founder directly.

## Why It Matters

Traditional terminals (Warp, Ghostty, etc.) "didn't exactly hit it" for AI workflows. cmux solves the specific notification problem: when you have multiple AI agents running in parallel, you need to know which terminal is ready for input without constant context-switching.

## Shoutout Timeline

- **2026-04-27**: Stellar Work EP57 — Jeff gives ~90 seconds of unprompted praise for cmux, calling it the best terminal for AI work

## Connections

- [JeffreyChan](JeffreyChan.md) — advocate and early adopter
- [StellarWorkPodcast](StellarWorkPodcast.md) — where the shoutout occurred
- [AgentOrchestrator](AgentOrchestrator.md) — mentioned in same podcast segment as another young-builder exemplar
- [cmux Input Attribution](../concepts/CmuxInputAttribution.md) — operational incident-response pattern for unexpected prompt text
