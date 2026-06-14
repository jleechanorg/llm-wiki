---
name: ui-fix-proof-environment-fidelity
description: "Headless Playwright passing ≠ UI bug fixed in user's real browser — test must reproduce the bug first (RED) in matching conditions"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: cad2d26e-a47b-412d-a7c9-70d58bddd0b7
---

Do NOT claim a UI/CSS fix is proven based on headless Playwright screenshots unless the test first reproduced the reported bug.

**Why:** PR #7328 duplicate campaign modal — I ran Playwright headless, saw "correct" colors and list updating, reported success. User's real Chrome browser still showed teal title text and list not updating. Two failure modes:
1. CSS: headless computed style on `.modal-content` looked correct, but Bootstrap's `--bs-heading-color` was overriding `.modal-title` in Chrome's full CSS cascade. Test checked the wrong element.
2. List update: Fresh headless env had no stale localStorage cache and no auth timing issues. The `renderCampaignList()` silent catch-block fallback never fired. In real browser it did.

**How to apply:**
- When user reports a specific visual bug: first verify the test CAN reproduce the bug (RED phase). If the bug doesn't show up headlessly, say so explicitly — do not skip to "fix looks correct."
- Always check the computed style on the EXACT element the user described as broken, not just a parent container.
- When the bug involves network/auth/cache state: either reproduce those conditions in the test, or explicitly state "this path is not exercised in the test environment."
- "Using Playwright headless" satisfies the tool-selection rule only. It does NOT satisfy environment fidelity.

See [[harness-guardrails]] and [[evidence-standards]].
