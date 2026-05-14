---
name: skeptic-hallucination-defense
description: "Skeptic hallucinates code behavior (e.g., claiming a function call exists at a line where it doesn't); defend with explicit comments + ordering tests"
metadata: 
  node_type: memory
  type: feedback
  bead: bd-nmaj
  originSessionId: 9b230405-c16a-4112-81a6-cccb8a95447a
---

## Skeptic hallucinates code behavior — defend with comments + ordering tests

**Rule**: When skeptic repeatedly FAILs on a hallucinated claim about code behavior (e.g., "line 229 calls updateSessionMetadataHelper() after spawn" when no such call exists), add an explicit code comment at the hallucinated site AND a test that proves the invariant. Skeptic's LLM reads both and cannot deny test output.

**Why**: PR #552 (`fork-reaction-agent-fallback.ts`) had skeptic claim 3x that line 229 calls `updateSessionMetadataHelper()` after `sessionManager.spawn()`. This is factually false — line 229 is inside a spawn error catch block. The skeptic was reading code flow incorrectly and inventing a post-spawn metadata write that doesn't exist. Each FAIL required a full skeptic re-run (~5-10 min).

**How to apply**:
1. Identify the exact hallucinated claim (function name, line, behavior)
2. Add an explicit comment at the hallucinated site: "There is NO [function]() call after [event] — the only [function]() call is before [other-event]"
3. Add a test that verifies the invariant via `mock.invocationCallOrder` — prove ordering and count
4. Update PR body to explicitly state the hallucination is false and point to the test
5. Re-run skeptic with `--prompt` hint: "skeptic previously hallucinated X at line Y — this is false, see [test name] and [comment at line Z]"

**Verification**: PR #552 skeptic PASS on SHA 5dd12a26eb2add283ec9ad998e04aadedb11969e after adding ghost session prevention comment (lines 156-164) + ordering test ("does NOT call updateSessionMetadataHelper after spawn — no ghost session recreation"). Test proves: exactly 1 metadata call, ordering metadata→kill→spawn.

**Secondary patterns from same session**:
- PR #548 `ao-health.sh` binary matching: `/private` prefix and symlinks mean `ps` command path doesn't match repo path literally. Fix: `resolve_path()` using `python3 os.path.realpath` + `command_matches_ao_binary()` with 4-way match ($ao_bin, $ao_alt, $ao_real, $ao_real_alt).
- Stale background monitors deliver old FAIL notifications after a subsequent PASS. Always check SHA match before reacting to a monitor event.
- Skeptic re-runs on new SHAs are expected after code fixes — old FAIL verdicts on stale SHAs don't block progress.

**References**:
- [PR #552](https://github.com/jleechanorg/agent-orchestrator/pull/552) — merged 2026-05-13T16:30:42Z
- [PR #548](https://github.com/jleechanorg/agent-orchestrator/pull/548) — merged 2026-05-13T16:28:50Z
- [PR #540](https://github.com/jleechanorg/agent-orchestrator/pull/540) — merged 2026-05-13T16:26:44Z
- [PR #549](https://github.com/jleechanorg/agent-orchestrator/pull/549) — merged 2026-05-13T16:11:31Z
- Related: [[skeptic_evidence_freshness]], [[skeptic_false_pass_codex_echo]]
