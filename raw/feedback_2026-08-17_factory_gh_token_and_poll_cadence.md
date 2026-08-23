---
name: factory-gh-token-and-poll-cadence
description: "Linux auto-factory daemon (jeff-ubuntu) gets 403 rate-limit on /linux gh probes — root cause is poll cadence vs GitHub's 5000/hr budget, NOT auth. Fix = explicit GH_TOKEN drop-in + bump fast_tick_secs."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f1badbe5-24ec-4e06-839c-c4267fe4d0bc
  modified: 2026-08-17T06:31:41.154Z
---

Linux auto-factory daemon on `jeff-ubuntu` (under `ai.dark-factory.daemon.service`) was hitting GitHub API 403s on `gh pr view` probes. Looked like a broken token, was actually rate-limit exhaustion.

**Why:** Daemon polls ~70 PRs at `fast_tick_secs=10` → ~31 INTAKE events/min = ~1860/hr just from intake, plus worker-side `gh` calls under `max_workers=80`. GraphQL budget (5000/hr) blows past 70% in ~30 min. All `jleechan2015` tokens (`~/.bashrc GH_TOKEN/GITHUB_TOKEN/ACCESS_TOKEN`, `~/.config/gh/hosts.yml`) share the SAME rate-limit pool — a new jleechan2015 PAT won't help.

**How to apply:** When "factory can't read PRs" surfaces:
1. **Token check first (cheap):** `ssh jeff-ubuntu 'gh api user --jq .login'` — confirms any of the 4 token sources works. Do NOT recommend a new PAT until you've ruled out rate limit.
2. **Rate-limit check:** `ssh jeff-ubuntu 'gh api rate_limit --jq "{core: .resources.core, graphql: .resources.graphql}"'` — if graphql.used > 3500 or core.used > 4500, you have your answer.
3. **Fix = belt-and-suspenders:** (a) add explicit `Environment=GH_TOKEN=...` drop-in at `~/.config/systemd/user/ai.dark-factory.daemon.service.d/github-token.conf` so `gh` doesn't depend on bashrc inheritance; (b) bump `fast_tick_secs=10 → 60` and `slow_tick_secs=30 → 300` in `<release-dir>/config/daemon.toml`. Then `systemctl --user daemon-reload && systemctl --user restart ai.dark-factory.daemon.service`.
4. **PR #8958 was collateral damage, not the cause** — once budget is healthy, the daemon picked it up automatically (EXISTING_PR_ADOPTED events within 90s of restart).

The daemon's systemd unit (`ai.dark-factory.daemon.service`) has `UnsetEnvironment=GITHUB_TOKEN` but no `Environment=GH_TOKEN=` — so `gh` auth depends on user-manager inheritance from bashrc. If bashrc breaks, factory breaks silently.

Related: [[feedback_2026-08-03_af_daemon_blocked_for_dark_factory]], [[project_2026-08-04_af_idle_12h_loop]].