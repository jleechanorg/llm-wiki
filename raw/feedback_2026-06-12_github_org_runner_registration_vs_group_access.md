---
name: github-org-runner-registration-vs-group-access
description: "GitHub Actions self-hosted runners in jleechanorg use a single \"Default\" runner group with visibility:all; dispatch is via runner-group access + label matching, NOT per-repo config.sh re-registration. Re-registering per-repo REMOVES from org-wide availability and pins each runner to a single repo (harmful)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 73be4e82-d635-4fd2-96b7-639072ec7448
---

## The mechanism (correct)

GitHub Actions self-hosted runners in the jleechanorg org work via:

- **One runner group** "Default", `visibility: all`, `default: true`, `selected_repositories: 0`
- **Dispatch mechanism:** runner-group access (granted org-wide) + label matching
- Every repo in `jleechanorg` can dispatch to every runner in this group; **no per-repo registration needed**
- 11 org runners total as of 2026-06-13:
  - 5× `bare-org-runner-N` (Linux X64, **offline**)
  - 6× `org-runner-mac-N` (Linux ARM64, **online+busy** — note: name "mac" is a misnomer; they are Linux VMs/emulators with ARM64 cores, NOT actual Mac hardware)
  - 1× `wa-oss-runner-local` (macOS ARM64, online+busy) — only this one is the legacy Mac dev box

## Label matching determines pool eligibility, not registration

- worldarchitect.ai's shared selector is `["self-hosted", "self-hosted-mikey"]` (per CLAUDE.md)
- The 6 `org-runner-mac-N` carry both labels `[self-hosted, Linux, self-hosted-mikey, ARM64]` → they qualify
- `wa-oss-runner-local` carries `[self-hosted, macOS, ARM64, self-hosted-mikey]` → also qualifies
- **No workflows pin `runs-on: macOS`** (verified by grep on 2026-06-13), so the effective self-hosted pool for worldarchitect.ai is **7 runners**, not 1
- Direct proof: in-progress run 27457500331 had 4 self-hosted jobs all assigned to `org-runner-mac-2/3/4` (no `wa-oss-runner-local` in sight)

## What I got wrong (so future agents don't repeat it)

I claimed "the 6 org runners aren't registered for this repo — that's the registration gap. To use them, each would need `./config.sh --url .../jleechanorg/worldarchitect.ai --token <token>` to re-register against this repo."

This is wrong on both counts:
1. **There is no registration gap.** Runner-group access is already granted org-wide. The runners CAN already serve worldarchitect.ai jobs (proven by the in-flight run above).
2. **Re-registering per-repo would be actively harmful.** It would remove each runner from org-wide availability (`visibility: all` would no longer apply to that runner) and pin it to a single repo. The org-wide mechanism is the whole point.

The right diagnostic question when a runner pool seems under-used is NOT "how do I re-register them?" but:
- (a) Does the workflow's `runs-on:` selector match the runner's labels? (label matching, not registration)
- (b) Is the runner saturated by OTHER repos? (`busy=true` doesn't prove which repo; need to check job-level `runner_name` on a recent run to see actual assignments)

## API gotcha: runner assignments are per-job, not per-run

`gh api .../actions/runs` returns `runner_name` as a workflow-level field that is often empty for self-hosted jobs. The actual per-job runner assignment is at `.../runs/{run_id}/jobs` and shows `runner_name` + `runner_id` per job. To prove "is runner X serving repo Y?", look at a specific job in a specific run, not the run-level field.

## How to apply

- When asked "why aren't X runners being used by repo Y?" → do NOT propose per-repo `config.sh` re-registration
- First check: does the workflow's `runs-on:` selector match the runner's labels? (`gh api .../actions/runs/<id>/jobs | jq '.jobs[].runner_name'`)
- Second check: is the runner saturated by other repos or genuinely idle? (`gh api orgs/jleechanorg/actions/runners --jq '.runners[] | {id, name, busy}'`)
- For org-wide pool sizing: count runners in the "Default" group with `visibility: all`, not runners in the repo's runner-list (which is per-repo, not org-wide)
- **`busy=true` is unprovable from API alone** — could be serving any repo; need job-level inspection to attribute

## Reference

- Correction date: 2026-06-13, user=jleechan2015
- Project: jleechanorg (org-wide) / worldarchitect.ai (one consumer repo)
- Verified via: `gh api orgs/jleechanorg/actions/runner-groups` + `gh api .../actions/runs/27457500331/jobs`
- Related: see also `[[github-org-runner-inventory-2026-06-12]]` (current inventory snapshot)
