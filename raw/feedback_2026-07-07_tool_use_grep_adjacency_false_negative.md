---
name: tool-use-grep-adjacency-false-negative
description: "grepping JSONL transcripts for '\"type\":\"tool_use\",\"name\":\"mcp__X__' to check real usage silently misses matches because a \"id\" field commonly sits between type and name"
metadata: 
  node_type: memory
  type: feedback
  bead: rev-crlxj (closed)
  originSessionId: ed376cb6-f347-4237-a510-b404c88d46f0
---

**The bug:** to check whether an MCP server/tool was ever actually invoked (not just listed as available), the natural grep is `"type":"tool_use","name":"mcp__<server>__"` — assuming the JSON keys appear adjacent in that order in the serialized line. They usually don't: real transcript objects commonly serialize as `"type":"tool_use","id":"toolu_...","name":"mcp__<server>__<tool>"`, with an `id` field in between. The adjacency-assuming grep silently returns 0 matches even when real usage exists — no error, just a false "unused" signal.

**Real impact (2026-07-07 MCP cleanup session):** this exact grep was used to justify removing several MCP servers as "confirmed 0 usage." An adversarial codex CLI review caught it by writing its own JSON-parsing script instead of trusting the grep, and found real, substantial usage the grep had missed entirely:

| Server | Grep said | Real usage (corrected) |
|---|---|---|
| ios-simulator-mcp (Mac) | 0 | **279** |
| playwright-mcp (Mac) | 0 | **221** |
| sequential-thinking (Mac) | 0 | **44** |
| memory-mcp (Mac) | 0 | 6 |
| filesystem-mcp (Mac) | 0 | 2 |
| context7 (Mac) | 0 | 0 (genuinely correct) |

Only `context7` turned out to be a true negative — every other "0 usage" claim was wrong. This directly led to removing two heavily-used tools (ios-simulator-mcp, playwright-mcp) from the user's Claude Code config based on false data.

**The fix:** use a non-adjacency-assuming pattern. Either:
1. A regex that allows any characters between the two keys within the same JSON object: `"type":"tool_use"[^}]*?"name":"mcp__<server>__<tool>"` (works line-by-line since each JSONL line is one JSON object — `[^}]*?` won't cross into a different top-level object as long as there's no unescaped `}` before it, which holds for `tool_use` blocks since `id`/`input` don't typically contain bare `}` at the top nesting level for simple values, though nested objects in `input` could theoretically produce false negatives too — a full JSON parser is safer for anything consequential).
2. Or, better: actually `json.loads()` each line and walk the structure looking for `content` blocks with `type == "tool_use"`, matching `name` exactly. This is what the adversarial review's corrected script effectively did and is the only fully-reliable method.

**How to apply:** never trust a "0 usage" / "confirmed unused" claim about a tool or server based on a hand-written grep pattern without first verifying the pattern actually finds a KNOWN-true-positive case (e.g. grep for a tool you know was used in the current session, confirm it matches, THEN trust negative results for others). Prefer a real JSON parser over regex/grep whenever the claim will drive a removal/deletion decision — the cost of a false negative here was deleting working tools, not just a wrong report.

See also [[mcp-tool-search-default-and-config-dir-trap]] and [[sidekick-same-name-respawn-race]] from the same session's broader MCP cleanup work.
