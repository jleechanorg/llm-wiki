---
title: "Jeff-Ubuntu CFS leaf_cfs_rq UAF — root cause & mitigation"
type: source
tags: [linux-kernel, scheduler, cgroups, use-after-free, self-hosted-runners, 6.17-hwe, jeff-ubuntu]
date: 2026-06-18
source_file: ~/.claude/projects/-home-jleechan-projects-other-user-scope/memory/project_2026-06-18_cfs_uaf_root_cause_and_mitigation.md
---

## Summary
Jeff-Ubuntu's repeated silent hard freezes (Apr–Jun 2026) are a use-after-free in the CFS scheduler's per-cgroup accounting on Ubuntu 6.17.x HWE kernels. A `task_group`/`cfs_rq` is freed during cgroup teardown but a stale pointer is left on `leaf_cfs_rq_list`; an idle CPU's load balancer (`__update_blocked_fair+0x3fa`, via `do_idle → do_softirq → flush_smp_call_function_queue`) later walks the freed structure and executes a freed (all-zero `Code:`) page → instant reset. Confirmed via pstore panic dump + multi-engine /research.

## Key Claims
- Bug **class** = the 2016 `leaf_cfs_rq_list` UAF, resurfaced in the 6.16–6.17 scheduler rework. No single pinned CVE; Ubuntu/Fedora/openSUSE all report 6.17 panics.
- **Version-independent within 6.17.x** — crashed identically on `6.17.0-29` AND `-35`, so rolling HWE point releases cannot fix it.
- **nvidia exonerated** — stack is pure scheduler/softirq/idle; zero Xid/NVRM/GPU frames in any boot.
- **Runners are the TRIGGER, not the detonator** — their cgroup create/destroy churn plants the dangling pointer; the idle balancer detonates it hours later. Explains random 1h–30h uptime-to-crash and crashes occurring while "idle".
- Crash history (uptime-to-crash, all abrupt resets): 18h, 14h, 1h24m, 30h, 5h16m.

## Mitigation
- IN EFFECT (no reboot): `/etc/sysctl.d/99-cfs-uaf-mitigation.conf` → `kernel.sched_autogroup_enabled=0`, `kernel.numa_balancing=0` (fewer transient sched groups → smaller race window). Correlated with a 2d11h stable streak (longest in the saga, runners running) — encouraging but ~2× prior best, not yet conclusive.
- STAGED, needs reboot: `cgroup_disable=cpu` on the kernel cmdline — removes the CPU controller so the buggy FAIR_GROUP_SCHED teardown path is never exercised; containers keep running, only per-cgroup CPU weights/limits lost. Named #1 mitigation by Perplexity + Grok in /research. As of 2026-06-18 NOT yet applied (no reboot).

## Connections
- [[CFS leaf_cfs_rq Use-After-Free|concepts/cfs-leaf-cfs-rq-uaf]] — the reusable bug class + signature + mitigations
- Process lesson: verify a fix is LIVE (`/proc/cmdline`, `/sys/fs/cgroup/cgroup.controllers`), not merely staged, before declaring victory.
