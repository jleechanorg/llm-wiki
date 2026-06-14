# Green Gate GATE-6 is a hard evidence-link regex with NO docs-only/N-A escape (2026-06-04)

`.github/workflows/green-gate.yml` lines 458-469: GATE-6 sets EVIDENCE_REQUIRED=true
whenever changed files match `^(testing_(mcp|ui)/|mvp_site/|deploy\.sh$|\.github/workflows/evidence-gate\.yml$)`.
HAS_EVIDENCE is true only if PR body+comments match the regex
`https?://[^ ]*\.(mp4|gif|cast)|gist\.github\.com/|asciinema\.org/a/|loom\.com/share/|user-attachments\.githubusercontent\.com/`.
There is NO label, "N/A", or docs-only bypass. So ANY PR touching `mvp_site/**`
— even a string-only tool-description doc change (#7246) or a pure unit-testable
detector field-source change (#7247) — cannot make the Green Gate check go green
without a real media/gist evidence link in the body/comments.

Consequence: PRs #7246 and #7247 both reach Gates 1-5 PASS (CI success, no conflict,
CR APPROVED, Bugbot clean, comments resolved) and fail ONLY GATE-6. When the change
has no LLM/streaming/state-persistence behavior, fabricating a real-LLM /es run is
forbidden — report GATE-6 as a hard meta-gate blocker, do not fake evidence.

reviewDecision stays "" even with CodeRabbit APPROVED because CodeRabbit is not a
CODEOWNERS-required reviewer; GATE-3 reads the CR review state directly and passes.
