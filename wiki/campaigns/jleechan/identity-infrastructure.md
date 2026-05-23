---
title: "jleechan Infrastructure Profile"
type: concept
tags: [identity, infrastructure, setup, tools, workflow]
sources: []
last_updated: 2026-04-13
---

# jleechan Infrastructure Profile

Hardware, software stack, automation systems, and operational setup. Built from local filesystem analysis.

---

## Hardware

**Mac16,7** — Mac with 48 GB RAM.

**The OOM Problem:** Running multiple concurrent AI agent sessions (Claude Code, Codex, tmux/cmux orchestration) can consume all RAM in seconds, causing kernel panics. Jeffrey experienced two kernel panics in one hour on March 5, 2026.

**Solution: mem-watchdog** (launchd LaunchAgent):
- Scans all processes every 5 seconds
- Kills any `rg`, `Python`, `codex`, or `node` process exceeding 8 GB RSS
- Keeps a kill log at `/tmp/mem-watchdog.log`
- Script at `~/bin/mem-watchdog.sh`

---

## MCP Servers (Configured)

Available MCP tools in Claude Code:
- **worldarchitect** — worldarchitect.ai API (game state, campaigns)
- **mcp-agent-mail** — agent coordination via SQLite mailboxes
- **slack** — Slack integration (workspace messaging)
- **memory-mcp** — vector memory (Qdrant + Ollama 768-dim embeddings)
- **perplexity-ask** — Perplexity AI search
- **context7** — context management
- **serena** — custom agent tool
- **chrome-devtools** — browser automation
- **playwright-mcp** — browser testing
- **filesystem** — local file access
- **ddg-search** — DuckDuckGo search
- **gemini-cli-mcp** — Gemini integration
- **grok-mcp** — Grok integration
- **ios-simulator-mcp** — iOS simulator control
- **thinclaw** — thin MCP server bridge

**Not configured:** Google Drive, Gmail, Google Calendar, Dropbox MCP.

---

## Cloud Infrastructure

### GCP (Google Cloud Platform)
- **Cloud Run** — containerized worldarchitect.ai deployment
- **Artifact Registry** — ~$252/month container storage
- **Firebase/Firestore** — worldarchitect.ai database
- **GCS buckets** — campaign storage, logs
- **Service accounts** — credential files in `~/.config/gcloud/`

### GitHub
- **jleechanorg** org — 23+ repos under management
- **PR numbers in 6,000s** as of April 2026
- Multiple runners: `actions-runner`, `actions-runner-2`, `actions-runner-aub`, `actions-runner-aub2`

---

## Automation Cron Jobs

Managed by `install_cron_entries.sh` via crontab:

| Job | Frequency | Purpose |
|-----|-----------|---------|
| `pr-monitor` | Every 2 hours | Monitor PRs, comment-only mode |
| `fix-comment` | Every hour at :45 | Fix comment workflows with MiniMax |
| `comment-validation` | Every 30 min | Validate PR comments |
| `codex-update` | Every hour at :15 | Codex automation for PRs |
| `codex-api` | Every hour at :30 | Codex API apply-and-push |

Logs at: `~/Library/Logs/worldarchitect-automation/`

---

## Multi-Agent Orchestration Stack

### Core Tools
- **tmux / cmux** — terminal session management for concurrent agents
- **Claude Code CLI** — primary coding agent
- **Claude CLI + MiniMax API** — parallel batch work via `claudem()` function
- **Codex (OpenAI)** — secondary coding, session parsing
- **MiniMax M2.7** — production gateway, Slack routing

### Custom Wrappers
- `~/bin/rg` — wrapper for ripgrep that skips VMs, caches, system dirs
- `~/.rgignore` — extensive ignore patterns for performance
- `AO novel.txt` — architectural notes for agent orchestrator

### Session Management
- `cmux` — Claude multiplexer for parallel CLI sessions
- Worktrees per branch isolation
- Multiple simultaneous tmux sessions

---

## WorldArchitect.AI Stack

From source code analysis:

- **Firebase/Firestore** — user data, campaign state, game state
- **`rewards_box`** — XP/rewards tracking system
- **`world_logic.py`** — core game mechanics, canonicalizers
- **`game_state.py`** — state management
- **`agents.py`** — agent orchestration (Story Agent, Rewards Agent)
- **`mcp_api.py`** — MCP tool definitions
- **`narrative_system_instruction.md`** — system prompt for narrative
- **Firestore user profiles** — email lookup, rate limiting, API keys

### Rate Limiting
Exempt users configured via `RATE_LIMIT_EXEMPT_EMAILS` env var. Jeffrey's own account is likely exempt.

---

## Dropbox Backup

**Path:** `~/Library/CloudStorage/Dropbox/`

Contains:
- `conversation-backups/` — rsync backup of Claude, Codex, Cursor, Gemini, OpenClaw conversations
- `Wedding/` — married (to Cindil)
- `2015 Questionnaire.xls` — pre-marriage questionnaire
- `4 day intermediate advanced building workout.*` — fitness program
- `intp.pdf` — INTP personality type document
- `My_True_Type.mobi` — Kindle ebook format
- `claude_backup_jeffpc_linux` — Linux machine backup

---

## Personal Files (~/Documents)

Key documents:
- **`openclaw log.txt`** — cmux/Claude Code session log showing multi-agent PR workflow
- **`machine-setup-oom-guard.md`** — OOM guard setup documentation
- **`agent_orchestrator.txt`** — architectural decisions for agent orchestrator (Python, Slack-Bolt, MCP config)
- **`codex_push.txt`** — GitHub automation notes, dual-agent /pair flow
- **`rewards.txt`** — worldarchitect.ai PR review about rewards latency fix
- **`crontab.txt`** — automation cron entries
- **`scratchpad.txt`** — multi-stream work notes, 5-workstream summaries
- **`michele fried chicken.txt`** — restaurant note (possibly personal)

---

## Financial / Health

From Dropbox:
- `cvsc caremark auth form.tif` — health insurance
- `Confirmation (1).pdf` — unclear origin, possibly financial

No direct access to: bank accounts, health records, personal budget spreadsheets.

---

## Google credentials

Found: `client_secret_*.apps.googleusercontent.com.json` — Google OAuth client for what appears to be worldarchitect.ai integration. No Gmail API or Google Calendar MCP configured.

---

## What Was NOT Accessible

- **Gmail** — no MCP server, credentials not configured for API access
- **Google Drive** — no MCP server, no API access
- **Google Calendar** — no MCP server
- **Firebase/Firestore** — live production data requires authentication; no local export found
- **worldarchitect.ai production** — cannot read user data without being logged in as user
- **Health records** — not digitized in accessible form
- **Financial accounts** — bank/brokerage not accessible

---

## What Was Added

This page documents Jeffrey's operational infrastructure — the machine, cloud accounts, automation, and tooling that underlies the AI orchestration practice. It complements `identity-synthesis.md` which covers professional history and psychological profile.
