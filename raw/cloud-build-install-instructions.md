# Superpowers Cloud Build — install instructions (canonical)

> Vendor: **Prime Radiant, Inc.**
> Tester: Jeffrey Lee Chan (jleechan2015)
> Service host: `cloud.superpowers.build`
> Source: enrollment email — single-use code, expires 24h after issue

## When to use this

Jeffrey is testing **Superpowers Cloud Build** as a bastion host. The service runs code remotely in hermetic boxes (`serf` CLI + GLM-5.2 via box's internal proxy `10.0.100.1:65500`, NOT OpenRouter). To onboard a new machine (Mac or Linux), follow these steps verbatim.

## Prerequisites

- **Superpowers installed first** — see `~/.claude/skills/superpowers-using-superpowers` or the Codex equivalent. Cloud Build sits on top of Superpowers.
- For Linux: a passwordless SSH alias to the existing bastion (MacBook) so you can copy keypair + state.json + scripts from an already-enrolled sibling. See `cloud-build-bastion-host-both-machines` memory.
- For Codex on the Mac: a fresh Codex process, app restart, or new task after install so the plugin loads.

## Step 1 — Save the enrollment code

The enrollment code arrives in an email titled like *"Cloud Build invite for <name>"*. Format:

```
Enrollment code: <40-hex-chars>
Expires: <ISO-8601 UTC>
This code is single-use.
```

Codes expire ~24h. Single-use. Save it BEFORE running setup — you'll be prompted on first handoff. Store pattern: `~/.config/cloud-build/enrollment_code.txt` with `chmod 600`.

## Step 2 — Download and extract

```bash
cd ~
curl -LO "https://pub-347cd78fe2db440ab5f46aa1c1307d59.r2.dev/4684e636b84511ba0cdca7a18d9b172e/superpowers-cloud-build.tgz"
tar xzf superpowers-cloud-build.tgz
```

This extracts to `~/superpowers-cloud-build-main/` containing:
- `assets/cloud-build-client-config-v0.json` — bundled trust anchor
- `skills/cloud-build/SKILL.md` — usage docs
- `skills/cloud-build/scripts/{lib-client.sh, preflight-local.sh, cloud-build-super-dispatch.sh, cb-client-setup.sh, lib-client-test.sh, validate-package.sh}`

## Step 3a — Claude Code install

```bash
/plugin marketplace add ~/superpowers-cloud-build-main
/plugin install cloud-build@superpowers-cloud-build
```

## Step 3b — Codex install

```bash
codex plugin marketplace add ~/superpowers-cloud-build-main
codex plugin add cloud-build@superpowers-cloud-build
```

**Codex note:** start a fresh Codex process, restart the desktop app, or open a new task so the plugin loads. Existing sessions won't see the new plugin.

## Step 4 — First enrollment

Run the setup script with the enrollment code (single-use, 24h expiry):

```bash
printf %s "$CODE" | bash ~/superpowers-cloud-build-main/skills/cloud-build/scripts/cb-client-setup.sh
```

This writes:
- `~/.config/cloud-build/state.json` (enrolled_fp_hash, host, identity_file paths)
- `~/.ssh/cloud-build/id_ed25519` + `.pub` (the box authenticates THIS key, not the machine)
- `~/.ssh/cloud-build/known_hosts` (pinned from `assets/cloud-build-client-config-v0.json`)

**Sanity check:** `ssh -i ~/.ssh/cloud-build/id_ed25519 cloud-bastion@cloud.superpowers.build` → `cloud-bastion: interactive shell is not permitted` (exit 0). Key accepted; box refuses interactive shells; the real channel is `git push` + control frame via `cloud_build_handoff`.

## Step 5 — Prepare your first build

1. Open your repository in Claude Code or Codex.
2. Use **Superpowers** to design the work (brainstorming → writing-plans).
3. Commit the plan (`docs/superpowers/plans/YYYY-MM-DD-<feature>.md` or `plans/<feature>.md`).
4. Make sure the work branch is `private/<slug>` (server enforces this).

## Step 6 — Trigger the box

When the plan is committed and ready, **say to Claude Code or Codex**:

```
run this plan on the cloud
```

Cloud Build will:
1. Check the repository (preflight: clean tree, no `.gitmodules`, no desktop markers, plan committed on HEAD, `CLOUD_HERMETIC_CONFIRMED=1`, branch under `private/`).
2. Guide the handoff — ask for the enrollment code on your first run (single-use).
3. Execute the plan remotely in a hermetic box.
4. Land the completed work back in your repository (orphan-snapshot handoff if the box's git-secret guard rejects the real repo due to secret-bearing ancestry).

## Orphan-snapshot handoff (when main has secret-bearing history)

The box's server-side **git secret guard scans the full ancestry** of the pushed `private/*` branch. worldarchitect.ai main's history has secrets, so direct handoffs fail. Workaround:

```bash
mkdir -p ~/cb-<slug> && cd ~/cb-<slug>
git -C "$ORIGINAL_REPO" archive --format=tar <work-sha> | tar -x
rm -rf evidence docs/ screenshots/ roadmap/ world_reference/ .beads/ testing_ui/ testing_mcp/
git init -q && git config user.email supervisor@cloud-build.local && git config user.name "Cloud Build"
git add -A && git commit -q -m "snapshot"
git checkout -b private/<slug>
mkdir -p .claude/plans && cp <plan.md> .claude/plans/ && touch .claude/cloud-build-hermetic-confirmed
git add -A && git commit -q -m "<slug>: plan + hermetic confirmation"
gh api -X POST /user/repos -f name=cb-<slug> -F private=true
git remote add origin https://github.com/jleechan2015/cb-<slug>.git
git push -u origin private/<slug>
```

Then dispatch:

```bash
CLOUD_HERMETIC_CONFIRMED=1 bash ~/superpowers-cloud-build-main/skills/cloud-build/scripts/cloud-build-super-dispatch.sh \
    "$PWD" ".claude/plans/<plan>.md" "private/<slug>" "$(git rev-parse HEAD)"
```

## Known bug in v0.8.1 (Linux only)

`cloud-build-super-dispatch.sh` shipped with `cd "$SCRIPT_DIR"` — wrong. Should be `cd "$SCRIPT_DIR/.."` (skill root, not `scripts/`). Mac copy is correct; Linux copy is broken. **Apply one-line fix on every Linux bastion**:

```diff
-cd "$SCRIPT_DIR"
+# SCRIPT_DIR is scripts/ itself; the scripts/... references below expect the skill root.
+cd "$SCRIPT_DIR/.."
```

After fix: `preflight OK` and dispatch proceeds.

## Polling after dispatch

```bash
bash ~/superpowers-cloud-build-main/skills/cloud-build/scripts/lib-client.sh cloud_build_fetch_status "$PROJECT"
```

When `head_sha` advances, land the result:

```bash
bash ~/superpowers-cloud-build-main/skills/cloud-build/scripts/lib-client.sh cloud_build_land_result \
    "$PROJECT" "$WORK_BRANCH" "$HEAD_SHA" "$RUN_ID"
```

**Heartbeat-stale during long LLM is NORMAL** (≥240s on `cloud_build_check_heartbeat` does NOT mean wedged — the box keeps working). Use `cloud_build_land_result` when `head_sha` advances; only abort if `cloud_build_fetch_status` shows `state=failed`.

## Box identity disclosure

Box author is always `Cloud Build <supervisor@cloud-build.local>`. Box model is undisclosed in `cloud/status` JSON (`model:""`), but can be probed via an in-plan `AGENT_IDENTITY.md` task that reads `SERF_MODEL` env + process table. Confirmed 5/5: `serf` CLI + `openrouter/z-ai/glm-5.2` via box internal proxy `10.0.100.1:65500` (NOT OpenRouter — `claudeg`/OpenRouter 402 does NOT affect the box).

## Cross-references

- `~/roadmap/nextsteps-2026-07-19-superpowers-cloud-build.md` — orphan-snapshot recipe, ground truth on cloud-build (first proven coding run)
- `~/roadmap/nextsteps-2026-07-20-superpowers-cloud-coding-resume.md` — re-dispatch recipe after session death
- `~/roadmap/learnings-2026-07.md` — entry 2026-07-19 superpowers cloud build unblocked
- `~/.claude/projects/-home-jleechan-projects/memory/superpowers-cloud-build-orphan-snapshot.md` — orphan-snapshot handoff distilled memory
- `~/.claude/projects/-home-jleechan-projects-worldarchitect-ai/memory/super-command-never-fallback-local.md` — `/super` must always dispatch to real box, never local subagents/claudeg
- `~/.claude/projects/-home-jleechan-projects-worldarchitect-ai/memory/cloud-build-bastion-host-both-machines.md` — both machines enrolled as bastions
- `~/.claude/projects/-home-jleechan-projects-worldarchitect-ai/memory/superpowers-cloud-box-not-openrouter.md` — box uses internal proxy, not OpenRouter
- `~/.claude/projects/-home-jleechan-projects-worldarchitect-ai/memory/cloud-build-heartbeat-stale-during-llm.md` — heartbeat-stale during LLM is normal
- `~/.claude/projects/-home-jleechan-projects-worldarchitect-ai/memory/superpowers-cloud-vs-dark-factory.md` — cloud-build ≠ dark-factory ≠ ao

## Gist (this file)

https://gist.github.com/jleechan2015/<this-gist-id>

Bug-report gist (cd drift, repro + fix):
https://gist.github.com/jleechan2015/286f0b03b75d5036ae490ccd6073abd8
