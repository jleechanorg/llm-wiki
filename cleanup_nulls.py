#!/usr/bin/env python3
"""Clean up null entries in bandit state rubric_scores."""
import json
from pathlib import Path

BANDIT_STATE_PATH = Path(__file__).parent / "technique_bandit" / "bandit_state.json"

with open(BANDIT_STATE_PATH) as f:
    state = json.load(f)

# Clean up null entries
for pr_num, entries in list(state.get("rubric_scores", {}).items()):
    if isinstance(entries, dict):
        for tech, rows in list(entries.items()):
            if isinstance(rows, list):
                # Filter out null entries
                cleaned = [r for r in rows if r.get("total") is not None]
                if cleaned:
                    entries[tech] = cleaned
                else:
                    del entries[tech]
        # Remove PR if no techniques left
        if not entries:
            del state["rubric_scores"][pr_num]

# Update ET stats
et_scores = []
for pr, entries in state.get("rubric_scores", {}).items():
    if isinstance(entries, dict) and "ET" in entries:
        for e in entries["ET"]:
            if e.get("total"):
                et_scores.append(e["total"])

state["techniques"]["ET"]["n"] = len(et_scores)
state["techniques"]["ET"]["scores"] = et_scores
state["techniques"]["ET"]["mean"] = sum(et_scores) / len(et_scores) if et_scores else 0

with open(BANDIT_STATE_PATH, "w") as f:
    json.dump(state, f, indent=2)

print(f"Cleaned up. ET n={len(et_scores)}, mean={sum(et_scores)/len(et_scores) if et_scores else 0:.1f}")
