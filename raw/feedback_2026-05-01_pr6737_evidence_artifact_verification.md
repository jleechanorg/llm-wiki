---
name: PR 6737 evidence artifact verification
description: Evidence work is not complete until the PR-published artifacts, not just local output, prove the current HEAD with real server/service mode and required media.
type: feedback
bead: rev-6737learn
---

Context: On May 1, 2026, PR https://github.com/jleechanorg/worldarchitect.ai/pull/6737 was blocked because its PR body and evidence artifacts were stale and incomplete. The PR HEAD had moved to 6097bdaa8d38f78c06aaa14f110ddb1451b92a08 while the description still cited 1b8327b42635a4a2f96c6ca45ebfd179ae26be90, and the provided evidence was pasted unit-test output plus mock smoke checks.

Technical detail: For non-test `mvp_site/**` changes, unit tests and mock CI smoke output are supporting checks only. They do not prove production behavior. If the changed path can affect modal routing, game state, LLM behavior, persistence, streaming, APIs, or visible browser state, the `/es` bundle must include current PR HEAD provenance, a real local server, real service mode including real LLM calls when applicable, raw logs/traces, checksums, and captioned UI video when behavior is user-visible.

Solution applied: Regenerated evidence on branch `pr6737-evidence-fix` at commit 7f75e829248787ff8060034e4b24e6d793eb4f00 using local server `http://127.0.0.1:8072`, `TEST_MODE=real`, `MCP_TEST_MODE=real`, and `MOCK_SERVICES_MODE=false`. Uploaded self-contained terminal and browser artifacts to the GitHub release `evidence-pr-6737`, including distinct MP4/GIF/WebM UI captures, screenshots, raw result JSON, checksums, and captions. Updated the PR body and posted https://github.com/jleechanorg/worldarchitect.ai/pull/6737#issuecomment-4357635323.

Verification: A real browser flow against campaign `a4dq0uD9zVZ23KA0iQbh` showed `modal_count=0`, enabled input/submit before and after the story action, and story count changing from 8 to 10. The fallback Skeptic Self-Verify workflow posted `VERDICT: PASS`, and Green Gate run https://github.com/jleechanorg/worldarchitect.ai/actions/runs/25200839982 completed successfully with latest Skeptic Gate success for the current evidence.

Reusable pattern: Before reporting evidence fixed, verify the exact public PR/release/gist artifacts reviewers will inspect. Confirm the PR body names the current GitHub HEAD SHA, links the evidence bundle, and includes raw logs/checksums/media. Rerun skeptic/green gates after artifact publication so the latest comments and workflow runs correspond to the evidence that is actually linked.
