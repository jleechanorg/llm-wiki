# CFS leaf_cfs_rq Use-After-Free

**Type**: concept
**Created**: 2026-06-18

## Definition

A class of Linux kernel bug where a per-cgroup CFS scheduler structure (`task_group` / `cfs_rq`) is freed during cgroup teardown but a stale pointer remains on the `leaf_cfs_rq_list`. An idle CPU's periodic load balancer (`__update_blocked_fair` / `update_blocked_averages`) later walks that list and dereferences/executes the freed memory → use-after-free crash. First seen ~2016, resurfaced in the 6.16–6.17 scheduler rework.

## Signature (how to recognize)

| Indicator | Detail |
|---|---|
| Crash site | `__update_blocked_fair+0x...` via `do_idle → do_softirq → flush_smp_call_function_queue` |
| RIP/CR2 | non-canonical or freed address; `Code:` bytes nearly all-zero (freed page) |
| Trigger | heavy cgroup create/destroy churn (containers, ephemeral CI runners) |
| Timing | detonation decoupled from trigger → random uptime-to-crash; fires when "idle" |
| Version | independent within the affected series (e.g. crashed on 6.17.0-29 AND -35) |

## Mitigations (keep workloads running)

- `cgroup_disable=cpu` (kernel cmdline) — removes the CPU controller; buggy FAIR_GROUP_SCHED teardown path never runs. Containers keep running; lose per-cgroup CPU weights/limits. **Strongest; needs reboot.**
- `kernel.sched_autogroup_enabled=0`, `kernel.numa_balancing=0` (sysctl) — fewer transient sched groups → smaller race window. Partial; no reboot.
- Reduce cgroup churn (persistent vs ephemeral runners; fewer concurrent).
- Boot a pre-affected kernel.

## Connections

- [[Jeff-Ubuntu CFS leaf_cfs_rq UAF — root cause & mitigation|sources/jeff-ubuntu-cfs-uaf-2026-06-18]] — the incident where this was diagnosed
