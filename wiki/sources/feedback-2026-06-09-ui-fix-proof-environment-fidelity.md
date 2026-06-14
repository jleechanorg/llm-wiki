---
title: "UI fix proof: environment fidelity required (2026-06-09)"
type: source
tags: [feedback, ui, ui-bug, environment-fidelity, playwright, headless, evidence, red-green, bootstrap]
date: 2026-06-09
source_file: raw/feedback_2026-06-09_ui_fix_proof_environment_fidelity.md
---

## Summary
Headless Playwright passing does NOT prove a UI/CSS fix works in the user's real browser. The test must first **reproduce the reported bug (RED phase)** in matching conditions before claiming a fix. Two distinct failure modes from PR #7328 (duplicate campaign modal) showed this in one session: headless computed style on `.modal-content` looked correct, but Bootstrap's `--bs-heading-color` was overriding `.modal-title` in Chrome's full CSS cascade (wrong element checked); and a fresh headless env had no stale localStorage cache or auth timing issues, so the `renderCampaignList()` silent catch-block fallback never fired — but in the real browser it did.

## Key Claims
- "Using Playwright headless" satisfies the tool-selection rule. It does **NOT** satisfy environment fidelity.
- When the user reports a specific visual bug, first verify the test CAN reproduce the bug (RED phase). If the bug doesn't show up headlessly, say so explicitly — do not skip to "fix looks correct."
- Always check the computed style on the **exact element** the user described as broken, not just a parent container.
- When the bug involves network/auth/cache state: either reproduce those conditions in the test, or explicitly state "this path is not exercised in the test environment."

## Two Failure Modes from PR #7328
1. **CSS override not seen by headless**: `.modal-content` had correct computed style, but Bootstrap's `--bs-heading-color` cascade overrode `.modal-title` in real Chrome. Test checked the wrong element.
2. **Stale-state fallback never fires headlessly**: Fresh headless env had no stale localStorage cache and no auth timing issues, so the `renderCampaignList()` silent catch-block fallback never fired. In real browser it did.

## Key Quotes
> "Using Playwright headless" satisfies the tool-selection rule only. It does NOT satisfy environment fidelity.

> When the user reports a specific visual bug: first verify the test CAN reproduce the bug (RED phase). If the bug doesn't show up headlessly, say so explicitly — do not skip to "fix looks correct."

## Connections
- [[UI-Bug-Fix-Proof]] — RED before GREEN; environment fidelity checklist
- [[EvidenceStandards]] — `ui-bug-fix-proof--environment-fidelity` checklist
- [[PlaywrightHeadless]] — tool selection vs environment fidelity
- [[BootstrapCascade]] — `--bs-heading-color` CSS variable override on `.modal-title`
- [[StaleStateFallback]] — silent catch-block fallbacks that don't fire in fresh envs
- [[harness-guardrails]] — UI bug repro rules
