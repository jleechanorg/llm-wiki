# Claude Code Auto-Compaction Research — 2026-04-05

## Root Cause

The compaction threshold (~150K tokens) was designed for 200K context windows. On 1M, it fires at ~15% usage. This is a known, widely-reported bug with no reliable workaround.

## Your Specific Situation (3 compounding factors)

1. **`CLAUDE_CODE_DISABLE_1M_CONTEXT=true`** in ~/.bashrc:937 forced 200K — **FIXED** (removed)
2. **`--continue` from old 200K session** inherited old context config — confirmed regression in v2.1.90 (#42376)
3. **Even on true 1M, compaction fires at ~15%** because threshold is hardcoded at ~150K

## Key GitHub Issues

| Issue | Summary |
|-------|---------|
| #34202 | Threshold (150K) doesn't scale with 1M — fires at 15% |
| #42375 | Compaction at ~6% (63K/1M) even with AUTOCOMPACT_PCT_OVERRIDE=95 |
| #42817 | ALL disable methods fail — Math.min() caps override |
| #42590 | Strips ~90% of information during multi-step tasks |
| #42394 | DISABLE_AUTO_COMPACT=1 ignored |
| #6689 | Feature request for --no-auto-compact (open since Aug 2025) |
| #40352 | CRITICAL: Race condition destroys entire transcript on compaction failure |
| #36649 | 1M regresses to 200K (v2.1.78) |
| #41082 | 1M regressed to 200K on Max plan (v2.1.87) |
| #34363 | Buffer mismatch: 232.9K buffer on 200K window = instant loop |
| #42376 | --continue silently drops context (v2.1.90 regression) |
| #40547 | Intelligence regression since 1M upgrade |

## Version Analysis

| Version | Key Changes |
|---------|------------|
| v2.1.77 | Fixed --resume truncation, fixed memory growth from progress msgs |
| v2.1.89 | Fixed autocompact thrash loop (3x detection), PostCompact hook |
| v2.1.90 | REGRESSION: --continue silently drops context |
| v2.1.91 | Fixed transcript chain breaks on --resume |

## MCP Overhead (from prior analysis)

- 186 MCP tools = 99.8K tokens (49.9% of 200K window)
- Removable: Notion (8K), Playwright (12K), Puppeteer (3K), React (4K) = ~27K savings
- Duplicate CLAUDE.md loading = 23.8K waste
- Per-turn system-reminder injection: ~19K (skills, deferred tools, hooks, MCP)
- Total per API call minimum: ~45K before any conversation

## Local Telemetry (bd-tl9t)

- Apr 4-5: 147 compact_boundary events vs Mar 21-22: 38 (3.9x increase)
- Normalized: 0.29 per 100 user msgs (Apr) vs 0.10 (Mar)
- preTokens at compaction: 167K-186K (confirms 200K window, not 1M)

## Community Resources

- ArkNill/claude-code-cache-analysis: proxy analysis showing 200K tool result cap, 327 silent microcompacts
- Lydia Hallie (Anthropic) acknowledged peak-hour tightening
- Community PreCompact hook workaround: exit code 2 blocks compaction

## Actionable Next Steps

1. Stay on v2.1.77 or upgrade to v2.1.91+ (skip v2.1.90)
2. Trim MCP servers (~27K savings)
3. Fresh sessions only — avoid --continue/--resume
4. Implement PreCompact hook (exit code 2 to block)
5. File consolidated bug with bd-tl9t telemetry data
