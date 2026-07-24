# Wiki Aggregator

Daily sync job that pulls log entries from per-project wikis (e.g. `~/worldarchitect.ai/wiki/`, `~/llm-wiki-autor-phase3/wiki/`, `~/worldarchitect-ai-autor/wiki/`, `~/worldarchitect-public-wiki/wiki/`) into `~/llm_wiki/wiki/log.md`. Each appended entry gets a `[from <source-wiki>]` attribution tag in the title.

This is the missing piece that ensures `/integrate` and `/learn` runs on any project land in the central llm_wiki repo (which has the auto-push to `origin/main`). Without this aggregator, per-project wikis accumulate entries that never make it to `jleechanorg/llm-wiki`.

Cross-platform: **launchd LaunchAgent on macOS** (daily 09:30) or **systemd user timer on Linux**. Installed as a **`uv` tool** at `~/.local/bin/wiki-aggregator`.

## Companion: ~/.wiki-default

This aggregator complements a forward-fix already applied to `~/.wiki-default`:

```
/Users/jleechan/llm_wiki/wiki
```

The `/wiki-ingest` skill reads this file and uses it as the default wiki for any session that doesn't have a project-local `.wiki-default`. Going forward, `/integrate` on any repo writes to llm_wiki by default.

## Prerequisites

- [`uv`](https://docs.astral.sh/uv/) — install with `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **macOS**: nothing else (uses built-in `launchd`)
- **Linux with systemd**: a user session that supports `systemd --user` (Ubuntu 16.04+ does)

## What it does

Each run:

1. Scans 5 per-project wiki log.md files (autor-phase3, worldarchitect.ai, worldarchitect-ai-autor, research-wiki, worldarchitect-public-wiki).
2. For each entry (matched by `date|title` signature) not already in llm_wiki, appends the full block to llm_wiki's log.md with `[from <source>]` prefix in the title.
3. Maintains a synced-signatures state file at `~/.cache/wiki-aggregator/synced.json` for belt-and-suspenders dedup.
4. Idempotent — re-running finds no new entries.

## Install

```bash
cd /path/to/llm_wiki
./tools/wiki-aggregator/install.sh
```

## Uninstall

```bash
./tools/wiki-aggregator/install.sh uninstall
```

## Manual run

```bash
# See what would be appended without writing:
wiki-aggregator --dry-run

# Real run:
wiki-aggregator
```

## Configuration

| Flag | Default | Notes |
|------|---------|-------|
| `--llm-wiki-log` | `~/llm_wiki/wiki/log.md` | Target wiki log.md to append to. |
| `--source PATH` | 5 built-in wikis | Override the source list (repeatable). |
| `--log-file` | `~/Library/Logs/wiki-aggregator.log` | Per-run log. |
| `--no-state-file` | (state on) | Skip `~/.cache/wiki-aggregator/synced.json` and rely on llm_wiki dedup only. |

## Repo layout

```
tools/wiki-aggregator/
├── pyproject.toml                              # uv-installable package metadata
├── src/wiki_aggregator/
│   ├── __init__.py
│   └── cli.py                                  # entry point (wiki-aggregator)
├── install.sh                                  # install | uninstall
├── README.md                                   # this file
├── launchd/
│   └── com.jleechan.wiki-aggregator.plist.template
└── systemd/
    ├── wiki-aggregator.service
    └── wiki-aggregator.timer
```

## Troubleshooting

- **`wiki-aggregator: command not found`** after install: uv installs the binary to `~/.local/bin/`, which may not be on your login `$PATH`. Add `export PATH="$HOME/.local/bin:$PATH"` to your `~/.bash_profile` (or `~/.zshrc`) and `source` it, or invoke `~/.local/bin/wiki-aggregator` by full path.
- **No new entries synced** on a re-run: that's the idempotent case. Check `~/.cache/wiki-aggregator/synced.json` for the synced-signature state. Delete it to force a re-sync.
- **Logs on macOS**: `tail -f ~/Library/Logs/wiki-aggregator.log` (or `.error.log`).
- **Logs on Linux**: `journalctl --user -u wiki-aggregator.service --since today`.
- **Run the job now (macOS)**: `launchctl kickstart -k gui/$(id -u)/com.jleechan.wiki-aggregator`.
- **Run the job now (Linux)**: `systemctl --user start wiki-aggregator.service`.