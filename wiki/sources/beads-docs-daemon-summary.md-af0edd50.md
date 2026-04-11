---
title: "Beads Daemon: Technical Analysis and Architectural Guide"
type: source
tags: [beads, bd, daemon, architecture, sqlite, golang, background-process, sync]
sources: []
date: 2026-04-07
source_file: docs/daemon-analysis.md
last_updated: 2026-04-07
---

## Summary

The beads daemon (`bd daemon`) is a background process providing automatic synchronization between local SQLite database and git-tracked JSONL files. It follows an LSP-style model with one daemon per workspace, communicating via Unix domain sockets (or named pipes on Windows). The daemon automates `bd export` before git commits, provides multi-agent coordination through a single database access point, and enables real-time monitoring with sub-500ms latency in event-driven mode.

## Key Claims

- **LSP-style architecture**: One daemon per workspace, Unix domain sockets for communication, JSON-RPC protocol
- **Primary purpose**: Automates `bd export` before git commits (500ms debounce) — all else is secondary
- **Three primary goals**: Data safety (auto-export to JSONL), multi-agent coordination (single DB access point), team collaboration (auto-commit/push)
- **Memory footprint**: 30-35MB total — SQLite connection pool (12-20MB), WASM runtime (5-10MB), Go runtime (5-8MB), RPC buffers (0.4-12.8MB)
- **Event-driven mode**: Uses fsnotify for <500ms latency vs polling mode at ~5000ms with 2-3% continuous CPU
- **Platform-specific**: Unix domain sockets with flock on Unix, named pipes on Windows
- **Not a system monitor**: Explicitly excludes disk space, CPU monitoring, cron-like scheduling, or remote server functionality
- **WASM-based SQLite**: Uses ncruces/go-sqlite3 with wazero runtime for cross-platform compatibility without CGO

## Key Quotes

> "The daemon exists primarily to automate a single operation - `bd export` before git commits. Everything else is secondary."

> "Not a system monitor - Don't add disk space, CPU, or general health monitoring. Not a task scheduler - Don't add cron-like job scheduling. Not a server - It's a local process, not meant for remote access."

## Connections

- [[Beads Configuration System]] — daemon integrates with beads config for auto-commit/push settings
- [[GitHub Copilot Integration Guide]] — daemon provides persistent memory for coding agents via MCP

## Contradictions

- None identified — this document is purely technical analysis with no conflicting claims