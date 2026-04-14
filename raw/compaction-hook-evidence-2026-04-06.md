# PreCompact Hook Evidence — 2026-04-06

## Key Finding
PreCompact hook DOES fire on v2.1.77 but only blocks SOME compaction attempts.

## Evidence

### Hook log (4 entries)
```
2026-04-06T03:08:36Z ALLOWED compaction (AO worker / headless)
2026-04-06T03:10:30Z ALLOWED compaction (AO worker / headless)
2026-04-06T03:12:06Z BLOCKED auto-compaction (interactive guard)
2026-04-06T03:14:10Z ALLOWED compaction (AO worker / headless)
```

### Main session: 52 compactions, 1 block
- Session b5c3fe16: 52 compact_boundary events, 2872 lines
- Hook fired 4 times total (3 ALLOWED for AO workers, 1 BLOCKED for interactive)
- Ratio: 1 block out of 52 compactions = hook only intercepts ~2% of compactions

### Test sessions: 0 compactions
- v2.1.77 test session (4478dd7c): 0 compactions, 347 lines — never hit threshold
- v2.1.92 test session (1478316a): 0 compactions, 616 lines — never hit threshold
- Could not reproduce compaction in test sessions despite 50+ prompts

## Interpretation
1. PreCompact hook exists and fires on v2.1.77 (contradicts earlier finding)
2. But it only intercepts a fraction of compaction events (~2%)
3. Most compactions bypass the hook entirely
4. v2.1.92 may have better hook coverage but we couldn't force compaction in test sessions
5. The test sessions didn't compact because they lack the massive per-turn overhead
   (300 skill descriptions, hook outputs, system-reminders) that the main session has

## Still unknown
- Does v2.1.92 have better PreCompact hook coverage?
- Can exit code 2 actually block ALL compactions on any version?
- Are there multiple compaction code paths, only some of which check hooks?
