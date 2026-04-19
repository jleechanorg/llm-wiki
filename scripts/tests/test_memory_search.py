from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import memory_search  # noqa: E402


class FakeSource:
    def __init__(self, name: str, response: str) -> None:
        self.name = name
        self.response = response
        self.calls = 0

    def __call__(self, query: str) -> str:
        self.calls += 1
        return f"{self.response}::{query}"


def test_run_memory_search_writes_cache_and_reuses_fresh_entry(tmp_path: Path) -> None:
    now = dt.datetime(2026, 4, 18, 20, 30, tzinfo=dt.timezone.utc)
    roadmap = FakeSource("roadmap", "roadmap-hit")
    wiki = FakeSource("wiki", "wiki-hit")
    sources = {"roadmap": roadmap, "wiki": wiki}

    first = memory_search.run_memory_search(
        "  Memory Search  ",
        cache_dir=tmp_path,
        ttl_seconds=3600,
        now=now,
        search_sources=sources,
    )

    assert first["cache_status"] == "miss"
    assert roadmap.calls == 1
    assert wiki.calls == 1
    assert first["results"]["roadmap"] == "roadmap-hit::memory search"
    cache_file = tmp_path / f"{memory_search.query_hash('memory search')}.json"
    assert cache_file.exists()

    second = memory_search.run_memory_search(
        "memory search",
        cache_dir=tmp_path,
        ttl_seconds=3600,
        now=now + dt.timedelta(minutes=30),
        search_sources=sources,
    )

    assert second["cache_status"] == "hit"
    assert roadmap.calls == 1
    assert wiki.calls == 1
    assert second["results"] == first["results"]


def test_run_memory_search_ignores_expired_cache(tmp_path: Path) -> None:
    now = dt.datetime(2026, 4, 18, 20, 30, tzinfo=dt.timezone.utc)
    roadmap = FakeSource("roadmap", "fresh-roadmap")
    sources = {"roadmap": roadmap}

    memory_search.run_memory_search(
        "cache ttl",
        cache_dir=tmp_path,
        ttl_seconds=3600,
        now=now,
        search_sources=sources,
    )
    assert roadmap.calls == 1

    result = memory_search.run_memory_search(
        "cache ttl",
        cache_dir=tmp_path,
        ttl_seconds=3600,
        now=now + dt.timedelta(hours=2),
        search_sources=sources,
    )

    assert result["cache_status"] == "miss"
    assert roadmap.calls == 2


def test_load_cached_result_rejects_mismatched_query_hash(tmp_path: Path) -> None:
    now = dt.datetime(2026, 4, 18, 20, 30, tzinfo=dt.timezone.utc)
    cache_file = tmp_path / f"{memory_search.query_hash('hello')}.json"
    cache_file.write_text(
        '{"canonical_query": "wrong", "created_at": "2026-04-18T20:00:00+00:00", "results": {"roadmap": "bad"}}'
    )

    cached = memory_search.load_cached_result(
        "hello",
        cache_dir=tmp_path,
        ttl_seconds=3600,
        now=now,
    )

    assert cached is None


def test_format_markdown_includes_cache_status_and_sections() -> None:
    payload = {
        "query": "memory search",
        "cache_status": "hit",
        "results": {"roadmap": "line 1", "wiki": "line 2"},
    }

    formatted = memory_search.format_markdown(payload)

    assert '# Memory Search: "memory search"' in formatted
    assert "Cache: hit" in formatted
    assert "## Roadmap" in formatted
    assert "## Wiki" in formatted
