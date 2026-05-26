---
title: Gmail Access via gog CLI
date: 2026-05-26
tags: [gmail, gog, cli, email, tooling]
source: ~/.claude/skills/gmail/SKILL.md
---

# Gmail Access via gog CLI

Use `gog gmail search -a jleechan@gmail.com "<query>"` to read/search Gmail.

Binary: `/opt/homebrew/bin/gog` — auth stored in macOS keychain.

**Anti-patterns**: browser automation, mcp-agent-mail (inter-agent messaging), @gongrzhe/server-gmail-autoauth-mcp.

**Slash command**: `/gmail`
