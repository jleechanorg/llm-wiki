# Wiki Daily Worker

Daily maintenance job for `~/llm_wiki`. Detects new files in `raw/*.md`, optionally ingests them via the local `claude` CLI, and logs entity/concept/source counts and ratios.

Cross-platform: runs as a **launchd LaunchAgent on macOS** or a **systemd user timer on Linux**. Installed as a **`uv` tool** (the `wiki-daily-worker` binary lives on `$PATH` at `~/.local/bin/`).

## Prerequisites

- [`uv`](https://docs.astral.sh/uv/) (Astral's Python package manager) — install with `curl -LsSf https://astral.sh/uv/install.sh | sh`
- `claude` CLI on `$PATH` (only required when ingest actually runs)
- **macOS**: nothing else (uses the built-in `launchd`)
- **Linux with systemd**: a user session that supports `systemd --user` (Ubuntu 16.04+ does)

## What it does

Each run:

1. Scans `<wiki_dir>/raw/*.md` and picks files newer than the mtime of `<wiki_dir>/wiki/sources/`.
2. For each new file, invokes `claude --dangerously-skip-permissions --model <model> --max-turns 5 --prompt "ingest <file>"` so the wiki can pick it up.
3. Logs entity/concept/source counts and the entity/concept and concept/source ratios to `~/Library/Logs/wiki-daily-worker.log` (macOS) or the systemd journal (Linux).

## Install

```bash
cd /path/to/llm_wiki
./tools/wiki-daily-worker/install.sh
```

The script will:
1. `uv tool install` the Python package (places `wiki-daily-worker` at `~/.local/bin/`).
2. Detect the OS and register a daily 08:00 scheduled job:
   - **macOS**: render the plist template into `~/Library/LaunchAgents/com.jleechan.wiki-daily-worker.plist` and `launchctl bootstrap` it.
   - **Linux**: copy the systemd unit and timer into `~/.config/systemd/user/`, then `systemctl --user enable --now` the timer.

## Uninstall

```bash
cd /path/to/llm_wiki
./tools/wiki-daily-worker/install.sh uninstall
```

This reverses both halves: stops the scheduled job (boots out the LaunchAgent or disables the timer) and `uv tool uninstall`s the package.

## Manual run

```bash
wiki-daily-worker --wiki-dir /path/to/llm_wiki --dry-run
```

Use `--dry-run` to verify what would be ingested without actually invoking `claude`. Drop `--dry-run` for a real run.

## Configuration

| Variable          | Default       | Notes |
|-------------------|---------------|-------|
| `LLM_WIKI_DIR`    | `~/llm_wiki`  | Wiki repo root. Override with `--wiki-dir` or the env var. |
| `MEMORY_WIKI_DIR` | `~/memory/wiki` | Memory wiki dir (logged each run; not used by ingest). |
| `--model`         | `MiniMax-M2.5` | Claude model to use for ingest. |
| `--log-file`      | `~/Library/Logs/wiki-daily-worker.log` | Per-run log (macOS default; journald on Linux). |

LaunchAgents do not load your shell profile, so `wiki-daily-worker` resolves the `claude` binary via the explicit `PATH` in `launchd/com.jleechan.wiki-daily-worker.plist.template`. The systemd unit sets the same `PATH` via `Environment=` in the service file.

## Repo layout

```
tools/wiki-daily-worker/
├── pyproject.toml                              # uv-installable package metadata
├── src/wiki_daily_worker/
│   ├── __init__.py
│   └── cli.py                                  # entry point (wiki-daily-worker)
├── install.sh                                  # install | uninstall
├── README.md                                   # this file
├── launchd/
│   ├── com.jleechan.wiki-daily-worker.plist.template
│   └── README.md
└── systemd/
    ├── wiki-daily-worker.service
    └── wiki-daily-worker.timer
```

## Troubleshooting

- **`wiki-daily-worker: command not found`** after install: uv installs the binary to `~/.local/bin/`, which may not be on your login `$PATH`. Add `export PATH="$HOME/.local/bin:$PATH"` to your `~/.bash_profile` (or `~/.zshrc`) and `source` it, or invoke `~/.local/bin/wiki-daily-worker` by full path.
- **Ingest silently does nothing**: the `claude` binary must be on the `PATH` the LaunchAgent / systemd unit sees. The shipped plist template and service file include `~/.local/bin`, `/opt/homebrew/bin`, `/usr/local/bin`, `/usr/bin`, `/bin`. If `claude` lives elsewhere, edit the template and re-run `install.sh`.
- **Logs on macOS**: `tail -f ~/Library/Logs/wiki-daily-worker.log` (or `.error.log`).
- **Logs on Linux**: `journalctl --user -u wiki-daily-worker.service --since today`.
- **Run the job now (macOS)**: `launchctl kickstart -k gui/$(id -u)/com.jleechan.wiki-daily-worker`.
- **Run the job now (Linux)**: `systemctl --user start wiki-daily-worker.service`.
