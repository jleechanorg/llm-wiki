---
name: Robust Wiki Campaign Frontmatter Parsing and Aggregation Count Over Paginated gRPC Streams
description: Eliminate frontmatter parse failures causing noisy re-downloads and replace paginated doc streaming with server aggregation count() to prevent gRPC stream timeouts and _UnaryStreamMultiCallable _retry attribute crashes.
type: feedback
bead: rev-xq9iv
---

# Robust Wiki Campaign Frontmatter Parsing & Aggregation Count

## Context
During the daily campaign export ingest (`wiki-campaign-daily-ingest.sh`), campaigns from WorldArchitect.AI Firestore are synced to the `jleechanorg/llm-wiki` repository. Two critical failure modes were discovered on 2026-09-13:
1. **Blind Spot #3 (Brittle Frontmatter Parsing)**: `_stored_entry_count` in `download_campaign.py` used strict `text.startswith("---\n")` and `r"^entry_count:\s*(\d+)\s*$"`. Any quotes (`"2422"`), inline comments (`# scenes`), indentation, Windows CRLF line endings, UTF-8 BOM, or alternate legacy fields (`scene_total:`, `scene_count:`) returned `None`, classifying existing wiki pages as `Stale` and re-downloading them every daily run.
2. **The 10:09 Ingest Failure (`_UnaryStreamMultiCallable._retry`)**: An earlier attempt to bypass the 2,000-cap used `_paginated_count` (`story_ref.limit(2000).offset(offset).stream()`). Streaming hundreds of thousands of documents across 309 campaigns of `jleechan@gmail.com` dropped gRPC streaming connections. When Firestore attempted retry via `_retry_query_after_exception`, it crashed with `AttributeError: '_UnaryStreamMultiCallable' object has no attribute '_retry'`, aborting the entire scan for `jleechan@gmail.com`.

## Solution & Technical Rule
1. **Robust Frontmatter Parsing**:
   - Strip leading whitespace, BOM (`\ufeff`), and handle CRLF (`\r\n`) and UNIX (`\n`) delimiters cleanly.
   - Match `entry_count`, `scene_total`, and `scene_count` supporting optional quotes (`"..."`, `'...'`), indentation, and inline comments (`#...`).
   - Fall back to counting markdown scene headings (`## Scene <N>`) before declaring a stored count unparseable (`None`), preventing infinite re-download loops.
2. **Server-Side Aggregation Count Query**:
   - For counting collection size across large datasets, NEVER stream documents or use `.limit(N).offset(M).stream()`.
   - Use Firestore native server-side aggregation: `collection_ref.count().get()[0][0].value`. It executes on the server in milliseconds, costs 1 read per 1,000 documents (not 1 read per document), and never triggers streaming socket timeouts or gRPC stream retry bugs.
   - Provide fallback to `_paginated_count` only for unit-test mock objects lacking `.count()`.

## Verification & Impact
- TDD suite in `skills/download-campaign/tests/test_download_campaign.py` established 7 RED failures on the brittle baseline and passed 23/23 GREEN after the fix.
- Shipped to `origin/main` of `jleechanorg/jleechanclaw` in commit `fab82fbcd3012c32b5781d5fad688845717a50f2`.
- Subsequent ingest run scanned 218 users with 0 errors (`Downloaded=7 Skipped=329 Errors=0 Users=218`), refreshing `Aizen merc nation` (`fazA3KUUdfZYky18TMyq`) from 2,000 to 2,422 entries (+422 scenes), refreshing 4 other 2,000+ scene campaigns, and adding 2 new campaigns to `llm-wiki` in commit `69c8597f85b840c021bff6a15da28aca89151959`.
