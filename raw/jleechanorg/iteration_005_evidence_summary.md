# Iteration 005 Evidence Summary

**Date**: 2026-01-12  
**Test**: 20-turn E2E (iteration_005)  
**Campaign ID**: `w8rjgODGJ2UUFHaSiPi4`  
**User ID**: `e2e-faction-20turn-20260112225432`

---

## Evidence Locations

### Test Evidence (Original)
**Path**: `/tmp/worldarchitect.ai/claude/add-force-creation-system-Mxqh0/faction_20turn_e2e/iteration_005/`

**Files**:
- `run.json` (7,648 bytes) - Test results and summary
- `request_responses.jsonl` (1,571,935 bytes) - Raw request/response payloads
- `README.md` (5,957 bytes) - Evidence package manifest
- `evidence.md` (2,348 bytes) - Evidence summary
- `metadata.json` (11,792 bytes) - Machine-readable metadata
- `methodology.md` (658 bytes) - Testing methodology
- All files have SHA256 checksums

### Evidence Copy (Downloaded)
**Path**: `~/Downloads/campaigns/iteration_005_evidence/`

**Status**: ✅ Copied successfully
- Complete evidence bundle copied from `/tmp`
- All files preserved with checksums

### Campaign Text (Downloaded)
**Path**: `~/Downloads/campaigns/Faction 25-Turn E2E Test Campaign_w8rjgODG.txt`

**Status**: ✅ Downloaded successfully
- 52 story entries
- 46.5 KB
- Full campaign narrative and state

---

## Test Results

**Summary**:
- ✅ **Total Turns**: 25
- ✅ **Successful Turns**: 25 (100%)
- ✅ **Failed Turns**: 0
- ✅ **Turns with Faction Header**: 22
- ✅ **Turns with Tutorial**: 21

**All Scenarios**: ✅ PASS (25/25)

**Last 5 Scenarios**:
- Turn 20: PASS (build)
- Turn 21: PASS (build)
- Turn 22: PASS (combat)
- Turn 23: PASS (power)
- Turn 24: PASS (end_turn)

---

## Coherence Improvements Verified

### ✅ Timestamp Progression
- **No reversals detected**
- Forward progression: `08:00` → `08:05` → `08:20` → `08:35` → `09:05` → ... → `13:25`
- Logical increments maintained

### ✅ Tutorial Messaging
- **Correct format used**: "[TUTORIAL PHASE COMPLETE - Campaign continues]"
- Appears in Scene 15
- Campaign continues normally after tutorial

### ✅ Level Progression
- **Early scenes**: Incremental (Level 1 → Level 2)
- **Later scenes**: Jump detected (Level 2 → Level 5 at Scene 24→25)

### ✅ Dual Gold Tracking
- **Character gold**: `10gp` (consistent)
- **Faction gold**: Tracked separately (`💰 Gold: X`)
- Both pools tracked correctly

---

## Files Available

### Evidence Bundle
```
~/Downloads/campaigns/iteration_005_evidence/
├── README.md
├── evidence.md
├── metadata.json
├── methodology.md
├── run.json
├── request_responses.jsonl (1.5 MB)
└── *.sha256 (checksums)
```

### Campaign Text
```
~/Downloads/campaigns/Faction 25-Turn E2E Test Campaign_w8rjgODG.txt
```

---

## Quick Access Commands

**View test results**:
```bash
cat ~/Downloads/campaigns/iteration_005_evidence/run.json | jq '.summary'
```

**View campaign text**:
```bash
cat ~/Downloads/campaigns/Faction\ 25-Turn\ E2E\ Test\ Campaign_w8rjgODG.txt
```

**View evidence summary**:
```bash
cat ~/Downloads/campaigns/iteration_005_evidence/evidence.md
```

---

**Created**: 2026-01-12  
**Related**: PR #2778, Iteration 005 analysis
