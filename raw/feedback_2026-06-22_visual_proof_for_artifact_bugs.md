---
name: visual-proof-for-artifact-bugs
description: "For email/UI bugs, the user's INBOX/screen is the source of truth — `sent=True` / build green / unit test pass are NOT. Render the actual artifact visually before claiming fixed."
metadata:
  node_type: memory
  type: feedback
  bead: rev-g0j11
  originSessionId: 8449a0a7-5867-4d22-b649-177a04c57b1a
---

For any bug where the user sees a rendered artifact (email body, web UI, exported PDF, etc.), the verification must be the artifact itself — not the code that produced it. PR #7798 cost report fix took 3 cycles because I kept reasoning from `cost_report_lib.send_email()` returning `sent=True` instead of from the message in the operator's Gmail INBOX.

**Why it bit me (2026-06-22 incident):**

The duplicate-email bug had two send paths in the daily-gcp-cost-report workflow:
1. `cost_report_lib.send_email()` — multipart/alternative, working correctly since 2026-06-22.3
2. `dawidd6/action-send-mail` step in `.github/workflows/daily-gcp-cost-report.yml` — re-sent the same body as plain text

When the user said "the email is not formatted at all" (literal `**bold**` and `| table |` in their INBOX), I "fixed" it by populating the dawidd6 step's `subject` from `$GITHUB_OUTPUT` (commit `ac1d91422b`). That made the dawidd6 step stop FAILING — but it was still SENDING a duplicate plain-text email. I treated "step succeeds" as "no more duplicate", which was wrong on two counts:

- The duplicate was happening at the **action** level (a separate workflow step), not the python level. The python `send_email()` was already correct.
- "Succeeds" ≠ "doesn't send an unwanted email". An action that runs and produces a real email in INBOX is "successful" in CI's eyes but a duplicate in the user's eyes.

**The actual fix:** A RED workflow-YAML test (read the YAML, assert no dawidd6 step) + delete the dawidd6 step from the workflow. Took 1 commit. Should have been the first commit.

**Why I didn't catch it day 1:** No programmatic feedback loop to read the user's actual INBOX. IMAP failed (`Invalid credentials` on app password), OAuth scope didn't include Gmail. Without that, I kept reasoning from the code (which said "we sent multipart/alternative") instead of the artifact (which the user could see). The user had to keep screenshotting unformatted text and asking "are you blind?" before the lightbulb went off.

**The pivot that worked:** When the user finally asked "are your visual tools working or no?" I rendered the actual HTML via Playwright headless (`mcp__playwright-mcp__browser_navigate` to `http://localhost:8765/email_actual.html` after serving the python-generated HTML via `python3 -m http.server`), took a `browser_take_screenshot` with `fullPage: true`, and showed the actual rendered output. The user could see what I'd see in Gmail.

**How to apply:**

- For email/UI/PDF bugs, the artifact IS the proof. `sent=True` is a code-side return value, not a user-side observation.
- When you can't read the artifact directly (no IMAP/OAuth), render it locally via Playwright and screenshot. `python3 -m http.server` + `browser_navigate('http://localhost:8765/...')` + `browser_take_screenshot` is the offline substitute.
- "Fix makes the build green" and "fix makes the user's experience correct" are DIFFERENT claims. Treat the latter as the actual goal.
- When a user complaint contains a screenshot, parse it carefully. "Unformatted email with literal `**`" → the email IS the source of truth → find every code path that produces that email body, not just the one I think is responsible.
- Two-step bug class: prior "fix" made the broken duplicate WORK (populated its inputs so it ran successfully) instead of removing the duplicate. Ask: "what was the buggy code path doing that I want to NOT do?" — if the fix is "make the buggy path run successfully", the fix is wrong.

**Related:** [[rag-scorer-artifacts-eyes-on-output]] — same pattern in eval metrics. Read the raw output before trusting the aggregate number.
