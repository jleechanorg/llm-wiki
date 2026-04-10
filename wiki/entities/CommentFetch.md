---
title: "Commentfetch"
type: entity
tags: [python, data-collection, copilot-tool]
sources: [clean-architecture-rules-python-files-prohibition]
last_updated: 2026-04-08
---

## Description
The ONLY allowed Python file for pure data collection in the copilot system. Used for fetching data (e.g., GitHub comments) and outputting to JSON for Claude to process.

## Role
Data collection only - no intelligence, decision-making, or response generation.

## Connections
- [[CleanArchitectureRules]] — governed by clean architecture policy
- [[CommentReplyWorkflow]] — consumes data from commentfetch output
