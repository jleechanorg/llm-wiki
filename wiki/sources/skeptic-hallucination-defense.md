# Skeptic Hallucination Defense

**Ingested**: 2026-05-13
**Source**: feedback_2026-05-13_skeptic_hallucination_defense.md
**Bead**: bd-nmaj

## Summary

When the skeptic LLM repeatedly FAILs on a hallucinated claim about code behavior (inventing a function call or execution path that doesn't exist), defend by adding:

1. An **explicit code comment** at the hallucinated site stating the invariant
2. An **ordering test** that proves the invariant via `mock.invocationCallOrder`
3. A `--prompt` hint when re-running skeptic pointing to the test

## Case Study

PR #552 (`fork-reaction-agent-fallback.ts`): Skeptic claimed 3x that line 229 calls `updateSessionMetadataHelper()` after `sessionManager.spawn()`. This was false — line 229 is inside a spawn error catch block. The only metadata call is before kill (lines 156-164).

**Fix**: Added ghost session prevention comment + test "does NOT call updateSessionMetadataHelper after spawn — no ghost session recreation" proving: exactly 1 metadata call, ordering metadata→kill→spawn.

**Result**: Skeptic PASS on SHA 5dd12a26eb2add283ec9ad998e04aadedb11969e.

## Related Patterns

- [[skeptic-evidence-freshness]] — run skeptic only after all CI terminal
- [[skeptic-false-pass-codex-echo]] — Codex stdout echoes prompt template
- macOS `/private` prefix and symlink resolution for binary path matching (ao-health.sh 4-way match)
- Stale background monitors deliver old FAIL after subsequent PASS — check SHA match

## Does this affect [[jeffrey-oracle]]?

No — this is an AO skeptic workflow pattern, not a game engine or oracle concern.
