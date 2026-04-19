#!/usr/bin/env python3
"""Search across the documented memory sources with a 1-hour disk cache.

This is the executable behind the llm_wiki memory-search skill. It resolves the
previous design/implementation gap where the skill documented cache behavior but
never actually wired cache reads or writes into execution.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import Callable

CACHE_DIR = Path.home() / "llm_wiki" / ".cache" / "memory-search"
DEFAULT_TTL_SECONDS = 3600
MAX_MATCHES_PER_SOURCE = 20
SECTION_TITLES = {
    "roadmap": "Roadmap",
    "beads": "Beads",
    "claude_memories": "Claude Memories",
    "hermes_sqlite": "Hermes SQLite (audit log)",
    "hermes_briefings": "Hermes Briefings",
    "hermes_index": "Hermes Index",
    "openclaw": "OpenClaw",
    "wiki": "Wiki",
    "history": "History",
}


def canonicalize_query(query: str) -> str:
    return " ".join(query.strip().lower().split())


def query_hash(canonical_query: str) -> str:
    return hashlib.sha256(canonical_query.encode("utf-8")).hexdigest()


def _utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _parse_timestamp(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def cache_file_for(query: str, cache_dir: Path = CACHE_DIR) -> Path:
    return cache_dir / f"{query_hash(canonicalize_query(query))}.json"


def load_cached_result(
    query: str,
    *,
    cache_dir: Path = CACHE_DIR,
    ttl_seconds: int = DEFAULT_TTL_SECONDS,
    now: dt.datetime | None = None,
) -> dict[str, object] | None:
    now = now or _utc_now()
    canonical_query = canonicalize_query(query)
    cache_file = cache_file_for(query, cache_dir)
    if not cache_file.exists():
        return None
    try:
        payload = json.loads(cache_file.read_text())
    except json.JSONDecodeError:
        return None
    if payload.get("canonical_query") != canonical_query:
        return None
    created_at = _parse_timestamp(payload.get("created_at"))
    if created_at is None:
        return None
    age = (now - created_at).total_seconds()
    if age < 0 or age > ttl_seconds:
        return None
    cached = dict(payload)
    cached["cache_status"] = "hit"
    cached["cache_path"] = str(cache_file)
    cached["cache_age_seconds"] = int(age)
    return cached


def write_cached_result(
    query: str,
    results: dict[str, str],
    *,
    cache_dir: Path = CACHE_DIR,
    ttl_seconds: int = DEFAULT_TTL_SECONDS,
    now: dt.datetime | None = None,
) -> dict[str, object]:
    now = now or _utc_now()
    canonical_query = canonicalize_query(query)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_file_for(query, cache_dir)
    payload: dict[str, object] = {
        "query": query,
        "canonical_query": canonical_query,
        "query_hash": query_hash(canonical_query),
        "created_at": now.isoformat(),
        "expires_at": (now + dt.timedelta(seconds=ttl_seconds)).isoformat(),
        "ttl_seconds": ttl_seconds,
        "results": results,
    }
    cache_file.write_text(json.dumps(payload, indent=2, sort_keys=True))
    payload["cache_status"] = "miss"
    payload["cache_path"] = str(cache_file)
    payload["cache_age_seconds"] = 0
    return payload


def _snippet(text: str, query: str, *, radius: int = 80) -> str:
    lower_text = text.lower()
    lower_query = query.lower()
    idx = lower_text.find(lower_query)
    if idx < 0:
        return text[: radius * 2].replace("\n", " ").strip()
    start = max(0, idx - radius)
    end = min(len(text), idx + len(query) + radius)
    return text[start:end].replace("\n", " ").strip()


def _search_filesystem(
    query: str,
    *,
    roots: list[Path],
    allowed_suffixes: set[str] | None = None,
    max_matches: int = MAX_MATCHES_PER_SOURCE,
) -> str:
    needle = query.lower()
    matches: list[str] = []
    for root in roots:
        expanded = root.expanduser()
        if not expanded.exists():
            continue
        if expanded.is_file():
            candidates = [expanded]
        else:
            candidates = [p for p in expanded.rglob("*") if p.is_file()]
        for candidate in candidates:
            if allowed_suffixes and candidate.suffix.lower() not in allowed_suffixes:
                continue
            try:
                text = candidate.read_text(errors="ignore")
            except OSError:
                continue
            if needle not in text.lower():
                continue
            relative = str(candidate)
            for line_no, line in enumerate(text.splitlines(), start=1):
                if needle in line.lower():
                    matches.append(f"- {relative}:{line_no} — {_snippet(line, query)}")
                    break
            if len(matches) >= max_matches:
                return "\n".join(matches)
    return "\n".join(matches) if matches else "— no matches"


def _search_sqlite(query: str) -> str:
    db_path = Path.home() / ".hermes" / "memory.db"
    if not db_path.exists():
        return "— no matches"
    sql = (
        "SELECT memory_id, action, created_at, new_value FROM memory_history "
        "WHERE lower(coalesce(new_value, '')) LIKE ? ORDER BY created_at DESC LIMIT 20"
    )
    rows: list[str] = []
    try:
        with sqlite3.connect(db_path) as conn:
            for memory_id, action, created_at, new_value in conn.execute(sql, (f"%{query.lower()}%",)):
                rows.append(
                    f"- {memory_id} [{action}] {created_at} — {_snippet(str(new_value or ''), query)}"
                )
    except sqlite3.Error as exc:
        return f"— sqlite error: {exc}"
    return "\n".join(rows) if rows else "— no matches"


def _search_wiki(query: str) -> str:
    script = Path.home() / "llm_wiki" / "scripts" / "memory_search.py"
    if not script.exists():
        return "— no matches"
    wiki_root = Path.home() / "llm_wiki" / "wiki"
    return _search_filesystem(query, roots=[wiki_root], allowed_suffixes={".md"})


def build_search_sources() -> dict[str, Callable[[str], str]]:
    return {
        "roadmap": lambda q: _search_filesystem(
            q,
            roots=[Path.home() / "roadmap"],
            allowed_suffixes={".md", ".txt", ".json", ".jsonl"},
        ),
        "beads": lambda q: _search_filesystem(
            q,
            roots=[Path.home() / ".claude" / "projects", Path.home() / ".beads" / "issues.jsonl"],
            allowed_suffixes={".md", ".txt", ".json", ".jsonl"},
        ),
        "claude_memories": lambda q: _search_filesystem(
            q,
            roots=[Path.home() / ".claude" / "projects"],
            allowed_suffixes={".md"},
        ),
        "hermes_sqlite": _search_sqlite,
        "hermes_briefings": lambda q: _search_filesystem(
            q,
            roots=[Path.home() / ".hermes" / "memory"],
            allowed_suffixes={".md"},
        ),
        "hermes_index": lambda q: _search_filesystem(
            q,
            roots=[Path.home() / ".hermes" / "MEMORY.md"],
            allowed_suffixes={".md"},
        ),
        "openclaw": lambda q: _search_filesystem(
            q,
            roots=[Path.home() / "openclaw-repo" / "MEMORY.md"],
            allowed_suffixes={".md"},
        ),
        "wiki": _search_wiki,
        "history": lambda q: _search_filesystem(
            q,
            roots=[Path.home() / ".claude" / "projects"],
            allowed_suffixes={".jsonl"},
        ),
    }


def run_memory_search(
    query: str,
    *,
    cache_dir: Path = CACHE_DIR,
    ttl_seconds: int = DEFAULT_TTL_SECONDS,
    now: dt.datetime | None = None,
    search_sources: dict[str, Callable[[str], str]] | None = None,
) -> dict[str, object]:
    cached = load_cached_result(query, cache_dir=cache_dir, ttl_seconds=ttl_seconds, now=now)
    if cached is not None:
        return cached

    sources = search_sources or build_search_sources()
    results: dict[str, str] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(sources) or 1) as executor:
        future_to_name = {executor.submit(func, query): name for name, func in sources.items()}
        for future in concurrent.futures.as_completed(future_to_name):
            name = future_to_name[future]
            try:
                value = future.result()
            except Exception as exc:  # pragma: no cover - defensive reporting
                value = f"— error: {exc}"
            results[name] = value or "— no matches"

    ordered_results = {name: results.get(name, "— no matches") for name in sources}
    return write_cached_result(
        query,
        ordered_results,
        cache_dir=cache_dir,
        ttl_seconds=ttl_seconds,
        now=now,
    )


def format_markdown(payload: dict[str, object]) -> str:
    query = str(payload.get("query", "")).strip()
    cache_status = payload.get("cache_status", "unknown")
    lines = [f'# Memory Search: "{query}"', "", f"Cache: {cache_status}"]
    cache_path = payload.get("cache_path")
    if cache_path:
        lines.append(f"Cache path: {cache_path}")
    age = payload.get("cache_age_seconds")
    if age is not None:
        lines.append(f"Cache age seconds: {age}")
    lines.append("")

    results = payload.get("results", {})
    if not isinstance(results, dict):
        results = {}
    for key in SECTION_TITLES:
        title = SECTION_TITLES[key]
        value = results.get(key, "— no matches")
        lines.append(f"## {title}")
        lines.append(str(value))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="+", help="Memory search query")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of markdown")
    parser.add_argument("--ttl-seconds", type=int, default=DEFAULT_TTL_SECONDS)
    parser.add_argument("--cache-dir", type=Path, default=CACHE_DIR)
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Delete the cached entry for this query before searching",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    query = " ".join(args.query)
    if args.clear_cache:
        cache_file_for(query, args.cache_dir).unlink(missing_ok=True)
    payload = run_memory_search(
        query,
        cache_dir=args.cache_dir,
        ttl_seconds=args.ttl_seconds,
    )
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(format_markdown(payload), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
