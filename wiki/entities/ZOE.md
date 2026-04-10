---
title: "ZOE"
type: entity
tags: [project, orchestrator, openclaw]
sources: ["zoe-openclaw-agent-swarm-reference"]
last_updated: 2026-04-07
---

The orchestrator agent built on OpenClaw that manages the fleet of coding agents. Holds full business context: meeting notes (Obsidian vault), CRM, past decisions, prod DB config (read-only).

## Responsibilities
- Scopes customer requests with human
- Tops up credits, pulls config, writes precise prompts
- Spawns agents with detailed context
- Monitors via cron (every 10 min)
- Proactive work: scans Sentry for errors, meeting notes for features, git log for docs updates

## Agent Selection Routing
| Agent | Best For |
|-------|----------|
| Codex | Backend logic, complex bugs, multi-file refactors, reasoning across codebase |
| Claude Code | Frontend, git operations, faster turnaround |
| Gemini | UI design — generates HTML/CSS specs for Claude to implement |

## Connections
- [[OpenClaw]] — platform running ZOE
- [[Codex]] — primary coding agent (90% of tasks)
- [[Claude Code]] — secondary coding agent
- [[Gemini]] — UI design agent
