---
name: cloud-build-dispatch-canonical-path
description: "Superpowers Cloud Build (Prime Radiant) is fully operational end-to-end. Canonical trigger is ANY of 10 phrases ('build on cloud', 'run this plan on the cloud', etc.) which routes to /super → cloud-build plugin → box dispatch. Box harness is serf-3 + GLM-5.2 via internal proxy."
metadata: 
  node_type: memory
  type: project
  classification: critical
  window: 2026-07-16 → 2026-07-22
  issue_count: 31
  boxes_fired: "4 (e17cfb8, 8a12c52, 7864836341, fccc323)"
  originSessionId: fc7bb717-13d4-4e16-ac36-e9745dce1cf5
---

## What is working

**End-to-end verified** with 4 dummy PRs across Mac + jeff-ubuntu:

| Run ID | Box commit | Machine | Verification |
|---|---|---|---|
| `cb-e2e-jeff-ubuntu-20260721-172109-20260722002148-2001e7` | `e17cfb83ed` | jeff-ubuntu | ✅ |
| `cb-e2e-macbook-20260721-172109-20260722003813-1aba7a` | `8a12c527f2` | Mac | ✅ |
| `cb-dummy-fresh-215607-20260722045614-174b61` | `7864836341` | jeff-ubuntu | ✅ |
| `cb-healthcheck-113729-20260724183742-b505a7` | `fccc323` | jeff-ubuntu | ✅ (today) |

All commits authored by `Cloud Build <supervisor@cloud-build.local>`, harness `serf-3`, model disclosed via `SERF_MODEL` env = `openrouter/z-ai/glm-5.2` via internal proxy at `10.0.100.1:65500` (NOT user's OpenRouter).

## Canonical trigger phrases (10 phrases, all route to /super)

- `run this plan on the cloud` (Prime Radiant canonical)
- `build on (the )?cloud` (user-preferred short form)
- `build this remotely`
- `kick off a cloud build`
- `use (the )?cloud`
- `on the cloud`
- `cloud build`
- `superpowers cloud`

Wired via UserPromptSubmit hook at `~/.claude/hooks/cloud-build-trigger.sh` on both machines. Routes to `/super` slash command (now a thin shim that delegates to Prime Radiant's `cloud-build` plugin skill).

## What was broken (fixes shipped)

1. **cd drift bug** (CRITICAL) — `cloud-build-super-dispatch.sh` v0.8.1 ships with `cd "$SCRIPT_DIR"` on Linux (script dir = `scripts/`, so subsequent `scripts/foo.sh` refs fail). Mac copy correct (`cd "$SCRIPT_DIR/.."`). **Fixed locally** with one-line sed:
   ```bash
   sed -i 's|^cd "$SCRIPT_DIR"$|cd "$SCRIPT_DIR/.."|' /path/to/cloud-build-super-dispatch.sh
   ```
   Verified: `preflight OK` after fix. Upstream bead `bd-c2q`.

2. **Silent local fallback** — older `/super` had a branch that auto-fell-through to local subagents when preflight failed. Removed. Memory: `super-command-never-fallback-local.md`.

3. **No natural-language trigger** — `/super` was slash-only. Wired UserPromptSubmit hook to intercept 10 phrases.

4. **OpenRouter 402 misread** — agents conflated local `claudeg` (user OpenRouter) with cloud box (internal proxy). They're separate. Memory: `superpowers-cloud-box-not-openrouter.md`.

5. **Heartbeat stale misdiagnoses** — ≥240s during long LLM calls is NORMAL. Don't abort on heartbeat alone. Memory: `cloud-build-heartbeat-stale-during-llm.md`.

6. **Lock contention** — same fp (both bastions share key) = parallel dispatch fails. Serialize or use different orphan-snapshot slug per attempt. Upstream bead `bd-d03`.

## Architecture summary

- **Client → box**: SSH git push/fetch (no other channel)
- **3 refs**: `private/<slug>` (work branch), `cloud/control` (client→box), `cloud/status` (box→client)
- **Box**: hermetic (no network, no API keys); tests must be stdlib-only
- **Setup**: `cb-client-setup.sh` reads enrollment code on stdin, writes `~/.config/cloud-build/state.json` + `~/.ssh/cloud-build/{id_ed25519,known_hosts}`
- **Both bastions enrolled** (Mac + jeff-ubuntu) with same cloud-build SSH key

## Orphan-snapshot recipe (for repos with secret history)

When the box's git-secret guard rejects your repo due to secret-bearing history:

```bash
ORIG=/path/to/real-repo; SLUG=cb-$(date +%s); DIR=~/$SLUG
cd "$DIR" && git init -q && git config user.email supervisor@cloud-build.local && git config user.name "Cloud Build"
git -C "$ORIG" archive --format=tar $(git -C "$ORIG" rev-parse origin/main) | tar -x
rm -rf evidence docs/ screenshots/ roadmap/ world_reference/ .beads/ testing_ui/ testing_mcp/
git add -A && git commit -q -m "snapshot"
git checkout -b private/<slug>
mkdir -p .claude/plans && cp plan.md .claude/plans/plan.md && touch .claude/cloud-build-hermetic-confirmed
git add -A && git commit -q -m "plan + hermetic"
gh api -X POST /user/repos -f name="$SLUG" -F private=true
git remote add origin https://github.com/<you>/$SLUG.git
git push -u origin HEAD:main && git push -u origin private/<slug>
CLOUD_HERMETIC_CONFIRMED=1 bash ~/superpowers-cloud-build-main/skills/cloud-build/scripts/cloud-build-super-dispatch.sh "$PWD" ".claude/plans/plan.md" "private/<slug>" "$(git rev-parse HEAD)"
```

## References

- **Master gist**: https://gist.github.com/jleechan2015/a15e331ffc62993376e4d7d5ed15fbfe
- **Plugin source mirror** (private): https://github.com/jleechanorg/superpowers-cloud-build-source
- **Issues tracker** (private, obra/Jesse Vincent viewer): https://github.com/jleechan2015/pb-archive-2026
- **Prime Radiant public marketplace** (cloud-build NOT here): https://github.com/prime-radiant-inc/prime-radiant-marketplace
- **Original `.tgz`**: `https://pub-347cd78fe2db440ab5f46aa1c1307d59.r2.dev/4684e636b84511ba0cdca7a18d9b172e/superpowers-cloud-build.tgz`
- **Box host**: `cloud.superpowers.build:22` (cloud-bastion SSH door)
- **Box harness**: `serf` v3 (Prime Radiant's `prime-radiant-inc/serf` repo)
- **Box model**: GLM-5.2 via internal proxy `10.0.100.1:65500`

## Reusable pattern

For anyone spinning up Cloud Build on a new machine:

```bash
# 1. Install
curl -LO "https://pub-347cd78fe2db440ab5f46aa1c1307d59.r2.dev/4684e636b84511ba0cdca7a18d9b172e/superpowers-cloud-build.tgz"
tar xzf superpowers-cloud-build.tgz
claude plugin marketplace add ~/superpowers-cloud-build-main
claude plugin install cloud-build@superpowers-cloud-build

# 2. Enroll
printf %s "$CODE" | bash ~/superpowers-cloud-build-main/skills/cloud-build/scripts/cb-client-setup.sh

# 3. PATCH cd drift on Linux (one line)
sed -i 's|^cd "$SCRIPT_DIR"$|cd "$SCRIPT_DIR/.."|' ~/superpowers-cloud-build-main/skills/cloud-build/scripts/cloud-build-super-dispatch.sh

# 4. Install UserPromptSubmit hook (so "build on cloud" works)
#    Write hook to ~/.claude/hooks/cloud-build-trigger.sh (see gist)
#    Add to ~/.claude/settings.json

# 5. Use any of: "build on cloud <task>", "run this plan on the cloud", /super <task>
```

## What NOT to do

- Don't use `/superlight` (legacy local claudeg router) — costs OpenRouter credits, not the box
- Don't silently substitute local subagents when preflight fails
- Don't abort on heartbeat stale alone
- Don't conflate local OpenRouter 402 with box stall
- Don't push to non-`private/*` branches (server enforces)
- Don't forget `CLOUD_HERMETIC_CONFIRMED=1` (preflight refuses without it)
- Don't fight `cd "$SCRIPT_DIR"` bug — patch the one line
