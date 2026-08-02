---
name: separate-evidence-producer-from-verifier
description: "the agent that produces visual evidence must not be the one that certifies it — a recording lane's own PASS verdict on its own clip missed a wrong-transition and a contradicting finding"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bc3b0c3b-7695-40fc-916d-e83f512181b9
  modified: 2026-07-26T06:45:32.153Z
---

During PR #8602 (worldarchitect.ai) evidence work, a recording lane reported a send-button clip as PROVEN (claim: enabled→disabled transition on send). A separate verification lane opened the actual frames and found the clip showed a status pill transitioning to "Cancel" — not the claimed button-state transition — and rejected it rather than relabeling it as passing something adjacent.

The same verification lane also caught that an autoscroll clip, shot to support one claim, actually contained frames that were direct evidence autoscroll does NOT fire during streaming — a real, valuable finding, but not the claim it was shot to prove. It was held back rather than folded silently into the original claim.

Neither defect would have been caught by the shooter reviewing its own output — both required a reviewer with no stake in the recording's success re-opening the raw frames against the original claim text.

**Rule:** whoever produces a video/screenshot evidence artifact must not be the sole certifier of what it proves. A second pass — different agent/lane, or at minimum a deliberate "re-read the claim, then re-open the frames cold" step — is required before an artifact is marked PROVEN. This is a specific instance of the general evidence-review discipline in `~/.claude/skills/evidence-review/SKILL.md` (`/er`), applied at the individual-clip level, not just the PR-evidence-bundle level.

Related: [[feedback_2026-07-25_evidence_class_must_match_claim_class]], [[reference_2026-07-25_burned_in_numeric_hud_for_video_evidence]] (the fix that makes this kind of check faster and more reliable).
