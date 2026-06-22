#!/usr/bin/env python3
"""CLI entry point for wiki-daily-worker.

Runs once per day (via launchd on macOS, systemd user timer on Linux) and:
1. Detects new files in <wiki_dir>/raw/*.md newer than <wiki_dir>/wiki/sources/.
2. Optionally ingests them via the local `claude` CLI (skipped when --dry-run).
3. Logs entity/concept/source counts and ratios.

Configuration is read from CLI flags, with environment variables as fallback:
- LLM_WIKI_DIR     → --wiki-dir
- MEMORY_WIKI_DIR  → --memory-wiki
"""
from __future__ import annotations

import argparse
import logging
import os
import subprocess
import sys
from pathlib import Path

LOG = logging.getLogger("wiki-daily-worker")

DEFAULT_MODEL = "MiniMax-M2.5"
DEFAULT_WIKI_DIR = str(Path.home() / "llm_wiki")
DEFAULT_MEMORY_WIKI = str(Path.home() / "memory" / "wiki")


def find_new_sources(wiki_dir: Path) -> list[Path]:
    """Return raw/*.md files newer than the wiki/sources/ directory mtime."""
    sources_dir = wiki_dir / "wiki" / "sources"
    if not sources_dir.exists():
        LOG.warning("wiki/sources/ not found under %s", wiki_dir)
        return []
    sources_mtime = sources_dir.stat().st_mtime
    raw = wiki_dir / "raw"
    if not raw.exists():
        return []
    return sorted(p for p in raw.glob("*.md") if p.stat().st_mtime > sources_mtime)


def ingest(sources: list[Path], model: str) -> None:
    """Invoke the local `claude` CLI for each new source."""
    for src in sources:
        LOG.info("Ingesting %s via claude (%s)...", src.name, model)
        subprocess.run(
            [
                "claude",
                "--dangerously-skip-permissions",
                "--model", model,
                "--max-turns", "5",
                "--prompt", f"ingest {src}",
            ],
            check=False,
        )


def log_ratios(wiki_dir: Path) -> None:
    """Log entity/concept/source counts and ratios to the run log."""
    wiki = wiki_dir / "wiki"
    counts = {
        name: len(list((wiki / name).glob("*.md")))
        for name in ("sources", "entities", "concepts")
    }
    entities = counts["entities"]
    concepts = counts["concepts"]
    sources = counts["sources"]
    LOG.info(
        "Ratios: sources=%d entities=%d concepts=%d e/c=%.3f c/s=%.3f",
        sources,
        entities,
        concepts,
        entities / max(concepts, 1),
        concepts / max(sources, 1),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--wiki-dir",
        default=os.environ.get("LLM_WIKI_DIR", DEFAULT_WIKI_DIR),
        help="Path to the llm_wiki repo (default: $LLM_WIKI_DIR or ~/llm_wiki).",
    )
    parser.add_argument(
        "--memory-wiki",
        default=os.environ.get("MEMORY_WIKI_DIR", DEFAULT_MEMORY_WIKI),
        help="Path to the memory wiki dir (default: $MEMORY_WIKI_DIR or ~/memory/wiki).",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Claude model to use for ingest (default: {DEFAULT_MODEL}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Detect new sources and log ratios but do not invoke claude.",
    )
    parser.add_argument(
        "--log-file",
        default=str(Path.home() / "Library" / "Logs" / "wiki-daily-worker.log"),
        help="Path to the log file (default: ~/Library/Logs/wiki-daily-worker.log).",
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

    wiki_dir = Path(args.wiki_dir)
    if not wiki_dir.exists():
        LOG.error("Wiki dir %s does not exist", wiki_dir)
        return 1

    LOG.info("=== Wiki Daily Worker Starting ===")
    LOG.info("wiki_dir=%s memory_wiki=%s model=%s", wiki_dir, args.memory_wiki, args.model)

    new_sources = find_new_sources(wiki_dir)
    LOG.info("New source files found: %d", len(new_sources))
    if new_sources and not args.dry_run:
        ingest(new_sources, args.model)
    elif new_sources and args.dry_run:
        LOG.info("--dry-run set: skipping claude ingest for %d file(s)", len(new_sources))

    log_ratios(wiki_dir)
    LOG.info("=== Wiki Daily Worker Done ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
