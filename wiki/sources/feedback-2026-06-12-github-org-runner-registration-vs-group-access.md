---
title: "GitHub org runner registration vs group access (2026-06-12)"
type: source
tags: [feedback, github-actions, self-hosted-runner, runner-groups, jleechanorg, worldarchitect-ai]
date: 2026-06-12
source_file: raw/feedback_2026-06-12_github_org_runner_registration_vs_group_access.md
---

## Summary
`jleechanorg` self-hosted runners dispatch via runner-group access + label matching, NOT per-repo `config.sh` re-registration. Re-registering per-repo would actually be harmful (removes runners from org-wide availability). When a runner pool looks under-used, the diagnostic is label matching + busy state on other repos, not re-registration. `busy=true` is unprovable from the run-level API alone — need per-job `runner_name` from `.../runs/{id}/jobs`.

## Key Claims
- `jleechanorg` has ONE runner group ("Default", `visibility:all`, `default:true`, `selected_repositories:0`). Every repo in the org can dispatch to every runner in this group; no per-repo registration needed.
- 11 org runners as of 2026-06-13: 5× `bare-org-runner-N` (Linux X64, offline), 6× `org-runner-mac-N` (Linux ARM64, online+busy — name is a misnomer, they are Linux VMs/emulators with ARM64 cores, NOT actual Mac hardware), 1× `wa-oss-runner-local` (macOS ARM64, online+busy, the legacy Mac dev box).
- The 6 `org-runner-mac-N` carry labels `[self-hosted, Linux, self-hosted-mikey, ARM64]`; `wa-oss-runner-local` carries `[self-hosted, macOS, ARM64, self-hosted-mikey]`. No worldarchitect.ai workflow pins `runs-on: macOS`, so the effective self-hosted pool is **7 runners**, not 1.
- Direct proof: in-progress run 27457500331 had 4 self-hosted jobs all assigned to `org-runner-mac-2/3/4` (no `wa-oss-runner-local` in sight).
- The wrong proposal (per-repo `config.sh --url .../jleechanorg/worldarchitect.ai --token <token>` re-registration) would (1) not fix the perceived gap and (2) be actively harmful — it removes the runner from org-wide availability and pins it to a single repo.
- `gh api .../actions/runs` returns `runner_name` as a workflow-level field that is often empty for self-hosted jobs. The actual per-job assignment is at `.../runs/{run_id}/jobs` with `runner_name` + `runner_id` per job.

## Key Quotes
> "The right diagnostic question when a runner pool seems under-used is NOT 'how do I re-register them?' but: (a) Does the workflow's `runs-on:` selector match the runner's labels? (b) Is the runner saturated by OTHER repos?"

## Connections
- [[feedback-self-hosted-mikey-label-routing-2026-06-13]] — same shared-selector / label-routing framing
- [[github-org-runner-inventory-2026-06-12]] — current inventory snapshot referenced from this memory
- [[SelfHostedRunnerNaming]] — covers the `org-runner-mac-N` misnomer (Linux ARM64, not Mac hardware)
- [[feedback-2026-06-09-runner-supervisor-and-ops]] — operates on the same 6+1 runner pool
- [[feedback-2026-06-03-self-hosted-race-fix]] — the underlying Docker cleanup primitive that this runner pool's heal-runners.sh depends on

## Bead / PR / Roadmap

- Bead: not yet filed
- Verified via: `gh api orgs/jleechanorg/actions/runner-groups` + `gh api .../actions/runs/27457500331/jobs`
- Origin session: `73be4e82-d635-4fd2-96b7-639072ec7448`
- Correction date: 2026-06-13 (user=jleechan2015)

## [[jeffrey-oracle]]

Not affected. This is a self-hosted runner org-level configuration / diagnostic question specific to jleechanorg.
