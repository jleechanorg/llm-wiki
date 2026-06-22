#!/usr/bin/env python3
"""CLI entry point for wiki-aggregator.

Scans a configured set of per-project wiki log.md files, finds entries not
yet present in ~/llm_wiki/wiki/log.md, and appends them with a `[from
<source-wiki>]` attribution tag in the title. Idempotent: re-running
finds no new entries to sync.

Default source wikis (overridable via --source PATH):
- ~/llm-wiki-autor-phase3/wiki/log.md      → autor research
- ~/worldarchitect.ai/wiki/log.md          → worldarchitect.ai game
- ~/worldarchitect-ai-autor/wiki/log.md    → autor worktree
- ~/research-wiki/wiki/log.md              → research notes
- ~/worldarchitect-public-wiki/wiki/log.md → public mirror

Dedup uses two layers:
1. llm_wiki log.md signature set (date|title) — prevents re-appending.
2. ~/.cache/wiki-aggregator/synced.json — belt-and-suspenders if entries
   in llm_wiki get edited or removed between runs.
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from datetime import datetime
from pathlib import Path

LOG = logging.getLogger("wiki-aggregator")

DEFAULT_LLM_WIKI_LOG = Path.home() / "llm_wiki" / "wiki" / "log.md"
STATE_DIR = Path.home() / ".cache" / "wiki-aggregator"
STATE_FILE = STATE_DIR / "synced.json"

DEFAULT_SOURCES = [
    Path.home() / "llm-wiki-autor-phase3" / "wiki" / "log.md",
    Path.home() / "worldarchitect.ai" / "wiki" / "log.md",
    Path.home() / "worldarchitect-ai-autor" / "wiki" / "log.md",
    Path.home() / "research-wiki" / "wiki" / "log.md",
    Path.home() / "worldarchitect-public-wiki" / "wiki" / "log.md",
]

# Matches a header line like "## [2026-06-22] ingest | Cancelled PR..."
ENTRY_HEADER_RE = re.compile(
    r"^## \[(\d{4}-\d{2}-\d{2})\]\s+(.+?)\s*$",
    re.MULTILINE,
)
# Splits on header lines, keeping them in the resulting chunks.
ENTRY_SPLIT_RE = re.compile(
    r"(?=^## \[\d{4}-\d{2}-\d{2}\])",
    re.MULTILINE,
)


def parse_entries(log_path: Path) -> list[dict]:
    """Return list of {date, title, block, signature} dicts from a log.md."""
    if not log_path.exists():
        return []
    text = log_path.read_text(encoding="utf-8", errors="replace")
    entries: list[dict] = []
    for chunk in ENTRY_SPLIT_RE.split(text):
        if not chunk.startswith("## ["):
            continue
        m = ENTRY_HEADER_RE.search(chunk)
        if not m:
            continue
        date = m.group(1)
        title = m.group(2).strip()
        signature = f"{date}|{title}"
        entries.append({
            "date": date,
            "title": title,
            "block": chunk.rstrip(),
            "signature": signature,
        })
    return entries


def existing_signatures(log_path: Path) -> set[str]:
    return {e["signature"] for e in parse_entries(log_path)}


def load_synced_state() -> set[str]:
    if not STATE_FILE.exists():
        return set()
    try:
        return set(json.loads(STATE_FILE.read_text()))
    except Exception:  # noqa: BLE001
        LOG.warning("State file %s unreadable; treating as empty", STATE_FILE)
        return set()


def save_synced_state(state: set[str]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(sorted(state)))


def prefix_title(block: str, source_name: str) -> str:
    """Inject `[from <source_name>]` into the first header line of a block.

    Idempotent: a block whose header already carries the prefix is
    returned unchanged.
    """
    first_line = block.split("\n", 1)[0]
    if f"[from {source_name}]" in first_line:
        return block
    return re.sub(
        r"^(## \[[^\]]+\]\s+)(.+)$",
        lambda m: f"{m.group(1)}[from {source_name}] {m.group(2)}",
        block,
        count=1,
        flags=re.MULTILINE,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--llm-wiki-log",
        default=str(DEFAULT_LLM_WIKI_LOG),
        help=f"Path to the central llm_wiki log.md (default: {DEFAULT_LLM_WIKI_LOG}).",
    )
    parser.add_argument(
        "--source",
        action="append",
        default=None,
        help="Path to a per-project wiki log.md (repeatable). Defaults to the built-in list.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be appended without writing.",
    )
    parser.add_argument(
        "--log-file",
        default=str(Path.home() / "Library" / "Logs" / "wiki-aggregator.log"),
        help="Path to the run log (default: ~/Library/Logs/wiki-aggregator.log).",
    )
    parser.add_argument(
        "--no-state-file",
        action="store_true",
        help="Skip the per-signature state file (rely on llm_wiki dedup only).",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M",
        handlers=[
            logging.FileHandler(args.log_file),
            logging.StreamHandler(sys.stdout),
        ],
    )

    llm_log = Path(args.llm_wiki_log)
    if not llm_log.exists():
        LOG.error("llm_wiki log %s does not exist", llm_log)
        return 1

    source_paths = (
        [Path(p) for p in args.source] if args.source else DEFAULT_SOURCES
    )

    LOG.info("=== Wiki Aggregator Starting ===")
    LOG.info("target=%s sources=%d", llm_log, len(source_paths))

    existing = existing_signatures(llm_log)
    synced_state = set() if args.no_state_file else load_synced_state()
    LOG.info(
        "llm_wiki has %d entries; %d previously synced by aggregator",
        len(existing),
        len(synced_state),
    )

    new_entries: list[tuple[str, str, str]] = []  # (source_name, signature, block)
    for src_log in source_paths:
        if not src_log.exists():
            LOG.info("skip (missing): %s", src_log)
            continue
        source_name = src_log.parent.parent.name
        src_entries = parse_entries(src_log)
        added = 0
        for entry in src_entries:
            sig = entry["signature"]
            if sig in existing or sig in synced_state:
                continue
            block = prefix_title(entry["block"], source_name)
            new_entries.append((source_name, sig, block))
            added += 1
        LOG.info("source %s: %d entries, %d new", source_name, len(src_entries), added)

    if not new_entries:
        LOG.info("=== Wiki Aggregator Done (nothing to sync) ===")
        return 0

    # Sort by date descending so newest entries appear at the top of the appended block
    new_entries.sort(key=lambda x: x[1].split("|", 1)[0], reverse=True)

    if args.dry_run:
        LOG.info("--dry-run: would append %d new entries:", len(new_entries))
        for source_name, sig, _block in new_entries[:10]:
            LOG.info("  [%s] %s", source_name, sig)
        if len(new_entries) > 10:
            LOG.info("  ... and %d more", len(new_entries) - 10)
        LOG.info("=== Wiki Aggregator Done (dry-run) ===")
        return 0

    header = (
        f"\n\n## Aggregated from per-project wikis "
        f"({datetime.now().strftime('%Y-%m-%d %H:%M')})\n\n"
    )
    with llm_log.open("a", encoding="utf-8") as f:
        f.write(header)
        for _source_name, _sig, block in new_entries:
            f.write(block.rstrip() + "\n\n")

    if not args.no_state_file:
        save_synced_state(synced_state | {sig for _, sig, _ in new_entries})

    LOG.info("Appended %d new entries to %s", len(new_entries), llm_log)
    LOG.info("=== Wiki Aggregator Done ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())