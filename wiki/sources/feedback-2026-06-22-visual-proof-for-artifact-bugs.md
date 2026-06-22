---
title: "Visual Proof Required for Email/UI Artifact Bugs"
type: source
tags: [feedback, verification, email, ui, playwright, workflow-yaml-test]
date: 2026-06-22
source_file: feedback_2026-06-22_visual_proof_for_artifact_bugs.md
bead: rev-g0j11
---

## Summary
For bugs where the user sees a rendered artifact (email body, web UI, exported PDF), the verification must be the artifact itself — not the code that produced it. PR #7798 cost-report fix took 3 cycles because the model trusted `cost_report_lib.send_email()` returning `sent=True` instead of opening the actual INBOX message. The root cause was a duplicate plain-text email sender (`dawidd6/action-send-mail`) in the workflow YAML, not the python side.

## Key Claims
- `sent=True` / build green / unit test pass are code-side signals, NOT user-side observations. For artifact bugs, the user-facing artifact is the only valid proof.
- "Make the broken step WORK by populating its inputs" is the wrong fix when the step is itself the unwanted behavior. The question is "what do I want the system to NOT do?" — answer is delete, not populate.
- Workflow-YAML regression tests catch duplicate-send bugs that python-side unit tests cannot. Pattern: read the YAML, assert no `*action-send-mail*` step exists, no step is named `Send report email`, no step references the body file:// path as its body.
- When you can't read the user's INBOX programmatically (IMAP/OAuth failure), render the artifact locally via Playwright headless + `python3 -m http.server` and screenshot. This is the offline substitute for direct feedback.
- IMAP app passwords failed (`Invalid credentials`), OAuth scope didn't include Gmail. Without those, the model kept reasoning from code-side return values instead of artifacts.

## Key Quotes
> "I trusted `sent=True` as proof of fix. `cost_report_lib.send_email()` returned `sent=True` after the multipart/alternative change. I read that as 'email is sent, fix is good' — but the user was seeing a DIFFERENT email in their INBOX."

> "My 'fixes' were working around the wrong layer. The first 'fix' (commit ac1d91422b) populated `$GITHUB_OUTPUT` so the dawidd6 step's `subject` was no longer empty. That made the dawidd6 step stop FAILING. But the step was still SENDING a duplicate plain-text email."

## Connections
- [[Playwright]] — used to render the email HTML locally when IMAP/OAuth failed
- [[DefaultTestEmailFallback]] — related concept; the default-test-email pattern is itself a "trust the artifact, not the code" pattern
- [[Body-Diff-Verification]] — Step 0 of the Jeffrey Oracle is the same principle for PRs: read the actual diff, not the description
- [[7-Green-Proof-Artifact]] — visual artifact proof is a generalization of the "7-green proof must be a real artifact" rule
- [[7-Green-Verification]] — see related verification framework
- [[RAGScorerArtifactsEyesOnOutput]] — same pattern in eval metrics: read the raw output before trusting aggregate scores
