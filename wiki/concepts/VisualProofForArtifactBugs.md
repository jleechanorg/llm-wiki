---
title: "Visual Proof for Artifact Bugs (email, UI, PDF)"
type: concept
tags: [verification, email, ui, playwright, workflow-yaml-test, anti-pattern]
sources: [feedback-2026-06-22-visual-proof-for-artifact-bugs]
last_updated: 2026-06-22
---

## Definition
For bugs where the user sees a rendered artifact (email body in their INBOX, a web UI in their browser, a PDF in their downloads), the verification must be the artifact itself — not the code that produced it, not the build status, not the return value of the send function. The artifact IS the proof.

## The Wrong Mental Model (Anti-Pattern)
"I changed the code, the build is green, the unit tests pass, the function returns success — therefore the user sees the fix." This treats the user as if they read your code's return values instead of looking at their own screen. They don't. The user sees the artifact that was rendered for them, which may have been produced by:
- a different code path than the one you "fixed"
- a parallel/duplicate sender you didn't notice
- a stale cache, a wrong config, or a layer-2 system you didn't think to check
- a preprocessor/markdown renderer that doesn't render what you wrote

## The Right Mental Model
The verification is the artifact. Open it. Look at it. If the bug is "the email is unformatted", open the email in Gmail (or a Gmail-like renderer). If the bug is "the button doesn't work", open the page in a real browser and click it. If you can't open the user's actual artifact, render the same code path locally and screenshot.

## When You Can't Reach the User's Artifact
Common in this environment: IMAP fails with `Invalid credentials` on app passwords; OAuth scope doesn't include Gmail. Workaround:

```bash
# 1. Render the artifact locally via the same code path the production uses
python3 - <<'PY'
import sys
sys.path.insert(0, "/path/to/repo")
from scripts import cost_report_lib as crl
# ... build the actual payload the workflow would produce
body = crl.format_gcp_report_body(summary, "complete")
html = crl._markdown_to_html(body)
open("/tmp/email_actual.html", "w").write(html)
PY

# 2. Serve it via plain HTTP (file:// is blocked by Playwright)
python3 -m http.server 8765 > /tmp/http_server.log 2>&1 &

# 3. Use Playwright headless to navigate and screenshot
# mcp__playwright-mcp__browser_navigate(url="http://localhost:8765/email_actual.html")
# mcp__playwright-mcp__browser_take_screenshot(type="png", fullPage=true, filename="proof.png")
```

The screenshot is now the proof. Show it to the user. They can confirm "yes, that's what I see" or "no, mine looks different" — and the difference tells you which layer is wrong.

## The Duplicate-Sender Bug Class
A common pattern that defeats code-side verification:

1. The python script calls `send_email()` — this is the "real" sender
2. A workflow step (or a second SMTP action) also sends the same content — this is the "duplicate" sender
3. The user sees the duplicate's output (often plain text or unformatted)
4. The model "fixes" the python sender and verifies `sent=True`
5. The user's INBOX still has the unformatted duplicate

**The fix is delete-the-duplicate, not improve-the-real-one.** The question to ask is "what do I want the system to NOT do?" — the answer is the duplicate, not the working one. "Make the broken step WORK by populating its inputs" is the wrong fix when the step is itself the unwanted behavior.

## Workflow-YAML Test Pattern
Add a regression test that reads the workflow YAML and asserts structural invariants:

```python
def test_workflow_does_not_use_dawidd6_action_send_mail(self):
    for step in self._steps():
        uses = step.get("uses") or ""
        self.assertNotIn("action-send-mail", uses)
        self.assertNotIn("dawidd6", uses)

def test_workflow_has_no_step_named_send_report_email(self):
    for step in self._steps():
        self.assertNotEqual(
            (step.get("name") or "").strip(),
            "Send report email",
        )

def test_python_smtp_send_step_does_not_attach_plain_text_body(self):
    for step in self._steps():
        if "action-send-mail" in (step.get("uses") or ""):
            body = (step.get("with") or {}).get("body", "")
            self.assertNotIn("file:///tmp/body.txt", str(body))
```

The python `send_email()` becomes the single source of truth for the email body and the SMTP send. Re-introducing a duplicate fails CI.

## When to Apply
- Any bug reported with "I see X" / "the screen shows Y" / "the email says Z" — these are artifact reports, treat the artifact as ground truth
- Any bug where your "fix" is in layer A but the symptom is in layer B (e.g., fix in python, symptom in Gmail) — render layer B's artifact and compare
- Any bug where the verification loop is "I sent it" / "I built it" / "I tested it" — none of those verify the user-facing artifact
- Any time the user explicitly says "are you blind?" or "look at the actual output" — they're telling you the verification is missing

## Related Concepts
- [[Playwright]] — primary tool for rendering artifacts locally
- [[DefaultTestEmailFallback]] — the default-test-email pattern is itself a "trust the artifact, not the code" pattern (default to sending to a real address, not a mock)
- [[Body-Diff-Verification]] — Step 0 of the Jeffrey Oracle: read the actual diff, not the PR description. Same principle for PRs.
- [[7-Green-Proof-Artifact]] — visual artifact proof is a generalization: 7-green requires a real artifact, not "CI is green"
- [[RAGScorerArtifactsEyesOnOutput]] — eval metrics: read raw output before trusting aggregate numbers

## Reference
- Source: [feedback-2026-06-22-visual-proof-for-artifact-bugs](../sources/feedback-2026-06-22-visual-proof-for-artifact-bugs.md)
- Bead: rev-g0j11
- PR: [#7798](https://github.com/jleechanorg/worldarchitect.ai/pull/7798) (head `9962b7d9c1`, merge `62878a06`)
