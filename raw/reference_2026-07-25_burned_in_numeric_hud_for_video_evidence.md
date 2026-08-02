---
name: burned-in-numeric-hud-for-video-evidence
description: "rendering state values (scrollTop, scrollHeight, streamingTextLen) directly into evidence video frames turns a visual-inference judgment call into a readable number, settling motion/state claims a reviewer would otherwise have to eyeball"
metadata: 
  node_type: memory
  type: reference
  originSessionId: bc3b0c3b-7695-40fc-916d-e83f512181b9
  modified: 2026-07-26T06:45:42.206Z
---

The strongest video evidence produced during the PR #8602 / worldarchitect.ai UI-behavior push burns numeric state directly into the recorded frames — e.g. `scrollTop=49966 scrollHeight=51081 atBottom=false streamingTextLen=...` — so a reviewer reads a number off the pixels instead of judging whether something "looks like it moved."

This settled a long-open question: whether scroll position is preserved during streaming. The HUD showed `scrollTop` pinned at exactly 49966 for 21 seconds while `scrollHeight` grew by 325px — an unambiguous, numeric confirmation that would have been a subjective call from pixels alone. Artifact: `docs/user-stories-ui/videos/scroll-position-preserved-during-streaming.mp4` on branch `docs/user-stories-ui-visual-spec` (worldarchitect.ai repo; file confirmed present via `git ls-tree`).

**Technique, reusable for any UI-motion or UI-state claim:** when building a capture harness for a "does X change/stay the same over time" claim, instrument the page to render the relevant state variable(s) into an on-screen overlay (or console-log timestamped alongside frame numbers) so the resulting video is self-proving. This directly counters the failure mode in [[feedback_2026-07-14_static_gameplay_certification_miss]] and [[feedback_2026-06-28_video_evidence_static_frame]] — where idle-bob/pixel-jitter made visual-only motion checks unreliable — by giving the reviewer a number instead of a vibe.
