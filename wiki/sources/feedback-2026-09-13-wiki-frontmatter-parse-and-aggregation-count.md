---
title: "Robust Wiki Campaign Frontmatter Parsing and Aggregation Count Over Paginated gRPC Streams"
type: source
tags: [campaign-export, firestore, grpc, frontmatter, tdd, llm-wiki, hermes]
date: 2026-09-13
source_file: "raw/feedback_2026-09-13_wiki_frontmatter_parse_and_aggregation_count.md"
last_updated: 2026-09-13
---

## Summary
During the daily WorldArchitect.AI campaign export ingest (`wiki-campaign-daily-ingest.sh`), two critical failure modes caused silent skips and repeated downloads: brittle frontmatter parsing in `_stored_entry_count` (which rejected quoted numbers, comments, indentation, CRLF, and BOM), and unbounded paginated streaming in `_paginated_count` across 309 collections that dropped gRPC connections and crashed on `_UnaryStreamMultiCallable._retry`. Both were resolved via TDD by adding robust regex/scene fallbacks and native Firestore server aggregation `count()`.

## Key Claims
- **Brittle frontmatter parsing causes noisy infinite re-downloads**: When `_stored_entry_count` returns `None`, existing campaigns are marked `Stale` and re-downloaded every run.
- **Support formatting variants & body fallbacks**: Frontmatter parsers must handle quotes, comments, BOM, CRLF, and fallback to counting `## Scene <N>` headings before failing.
- **Never stream collections solely to count documents**: Unbounded `.limit(N).offset(M).stream()` across hundreds of collections causes gRPC stream timeouts. When Firestore attempts `_retry_query_after_exception`, it crashes with `AttributeError: '_UnaryStreamMultiCallable' object has no attribute '_retry'`.
- **Use native Firestore server aggregation**: `collection_ref.count().get()[0][0].value` executes on the server in milliseconds, consumes 1 read per 1,000 docs, and avoids socket drops.

## Connections
- [[FirestoreService]] — backend data store for player campaign story entries
- [[CampaignExportIngest]] — daily ingest pipeline to LLM wiki
- [[HermesAgent]] — automation runner managing cron exports
