---
name: verify-secret-backend-before-declining-rotation
description: Grep the actual storage backend of a leaked credential before declaring its rotation outside agent authority
metadata: 
  node_type: memory
  type: feedback
  bead: rev-learning-verify-secret-backend-before-declining-f90ur
  originSessionId: 4f8afbc1-abc9-41f4-a3bf-f79cbc7e2177
  modified: 2026-09-13T16:18:06.006Z
---

Told the user rotating a leaked `SMOKE_TOKEN` (found live in PR #9842's Cloud
Logging evidence captures) was "outside agent authority, no access to rotate
production secrets" — an assumption that it was a GCP Secret Manager secret,
never actually checked. Grepping `.github/workflows/*.yml` showed it is a
**GitHub Actions repo secret** (`secrets.SMOKE_TOKEN`), injected as a plain
Cloud Run env var at deploy time. `gh secret set SMOKE_TOKEN` rotated it
directly, using `gh` access already established earlier in the same session
for PR operations.

**Why:** "production secret" is not one storage backend — GitHub Actions
secrets, GCP Secret Manager, and plain env/dotfiles have completely different
access models, and only some are genuinely outside a session's existing
write access. Declining an action on an unverified assumption about *where*
a credential lives wastes the user's time reopening something the agent could
already do, and forces the user to either do it manually or push back (as
happened here: "why can't you rotate it?").

**How to apply:** before declaring any credential rotation/action out of
scope, grep the credential's actual usage site (`grep -rn <NAME>
.github/workflows/ scripts/ mvp_site/`) to identify the real backend — GitHub
Actions secret (`secrets.X`, rotatable via `gh secret set`), GCP Secret
Manager (`secretKeyRef`, needs IAM/console access this session may genuinely
lack), or a plain env/dotfile (needs the user's shell) — rather than assuming
from the credential's general "production secret" label. Only decline once
the actual backend is confirmed to require access the session doesn't have.

Related: [[br-discovery-is-not-cwd-confined]] (same session, same root-cause
discipline: verify the actual resolved target before acting or declining).
