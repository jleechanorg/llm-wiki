# Wiki Daily Worker

Automated daily job to improve the wiki using AO minimax workers.

## Files

- `wiki-daily-worker.sh` — Main worker script
- `launchd/` — LaunchAgent plist for macOS scheduling

## Usage

```bash
# Run manually
./wiki-daily-worker.sh

# Or use launchd (loads automatically if plist is in ~/Library/LaunchAgents/)
launchctl load ~/Library/LaunchAgents/com.jleechan.wiki-daily-worker.plist
```

## Schedule

Runs daily at 8:00 AM via launchd.

## What it does

1. Checks for new source files in `raw/`
2. Ingest new files via minimax (cost-effective)
3. Runs wiki-evolve pattern check
4. Reports entity/concept ratios

## Requirements

- `claude` CLI with `claudem()` function
- MiniMax API key (via ANTHROPIC_BASE_URL)