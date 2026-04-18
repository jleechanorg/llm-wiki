---
name: memory-search
description: "Search across all memory systems — ~/roadmap, beads, claude memories, hermes sqlite (audit log), hermes briefings, hermes index, openclaw memories, wiki, and conversation history. Use whenever the user asks to search memories, find something in memories, or looks for anything that might have been captured in any memory store. Trigger on: 'search memories', 'find in my memories', '/ms', '/memory_search', 'search across all memories', 'look up in memory', 'did I save this somewhere', 'do I have anything about X in memory'."
---

# Memory Search

Lightweight parallel search across all memory sources. No internal subagents — just direct `/e` subagents dispatched by the executing agent.

## Cache

Cache dir: `~/llm_wiki/.cache/memory-search/`

- **Lookup**: Check `cache/<query-hash>.json` — if TTL not expired, return cached results
- **Write**: After all sources return, write merged results to cache
- **TTL**: 1 hour default
- **Key**: SHA-256 of canonicalized query (lowercased, stripped)

## Memory Sources

1. **~/roadmap** — Project roadmaps and planning docs
2. **beads** — Issue/bead tracking (`~/.claude/projects/*/memory/*.md` or `.beads/issues.jsonl`)
3. **claude memories** — Session memories (`~/.claude/projects/*/memory/`)
4. **hermes sqlite** — `~/.hermes/memory.db` — table is `memory_history` (audit log, not primary content)
5. **hermes memory/** — `~/.hermes/memory/briefing-*.md` and `mcp-mail-ack-log.md`
6. **hermes MEMORY.md** — `~/.hermes/MEMORY.md`
7. **openclaw** — `~/openclaw-repo/MEMORY.md`
8. **wiki** — `~/llm_wiki/` (via /wiki-search)
9. **history** — `~/.claude/projects/*/*.jsonl`

Note: Mem0 (Qdrant at localhost:6333) not filesystem-accessible — skip.

## Execution

Run all searches in parallel via `/e` subagents:

```
/e Search ~/roadmap for "$QUERY". List files with matching snippets.

/e Search beads for "$QUERY". Check ~/.claude/projects/*/memory/*.md and .beads/issues.jsonl. Show matching bead IDs and titles.

/e Search ~/.claude/projects/*/memory/ for "$QUERY". Search MEMORY.md indexes and individual .md files. Show snippets.

/e Search ~/.hermes/memory.db: sqlite3 ~/.hermes/memory.db "SELECT memory_id, action, created_at, new_value FROM memory_history WHERE new_value LIKE '%$QUERY%' LIMIT 20;"

/e Search ~/.hermes/memory/briefing-*.md and ~/.hermes/memory/mcp-mail-ack-log.md for "$QUERY". Show file:line matches with snippets.

/e Search ~/.hermes/MEMORY.md for "$QUERY". Show matching entries.

/e Search ~/openclaw-repo/MEMORY.md for "$QUERY". Show snippets.

/wiki-search $QUERY

/e Search ~/.claude/projects/*/*.jsonl for "$QUERY": grep -l "$QUERY" ~/.claude/projects/*/*.jsonl 2>/dev/null | head -5; grep -H "$QUERY" ~/.claude/projects/*/*.jsonl 2>/dev/null | head -20
```

## Aggregation

Wait for all 9 subagents. Merge results:

```
# Memory Search: "$QUERY"

## ~/roadmap
[results]

## Beads
[results]

## Claude Memories
[results]

## Hermes SQLite (audit log)
[results]

## Hermes Briefings
[results]

## Hermes Index
[results]

## OpenClaw
[results]

## Wiki
[results]

## History
[results]
```

No matches → mark as "— no matches". Sort by relevance within sections.
