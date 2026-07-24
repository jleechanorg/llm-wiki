---
name: ezgha-memory-detection-needs-explicit-vm-total-mb-override
description: "ezgha's `docker info --format {{.MemTotal}}` returns the docker daemon's view (15957MB on a 24GB Colima VM), NOT the VM ceiling. ezgha silently clamps per-runner memory to (daemon_mem - reserve) / count. Fix: set explicit `vm_total_mb` config so the clamp uses the real VM ceiling. PR #77 in jleechanorg/ez-gh-actions."
metadata: 
  node_type: memory
  type: feedback
  bead: ez-gh-actions-yz6b
  originSessionId: 6d6509e7-ea7b-44a2-8aa5-e0699e99ba2c
---

# ezgha memory detection needs explicit vm_total_mb override

## Context
- 2026-07-13 round 2: User expected 6 mac runners but only 3 online. ezgha config had `count = 3` with comment "TEMP 2026-07-12: yz6b fail-loud guard — VM 16GiB cannot fund 6x3072MB floor + 4096 reserve; restore to 6 after Colima resize to 24GiB"
- Resized Colima to 24GiB. Set count=6, memory_mb=3072, added `vm_total_mb = 24576`
- ezgha STILL clamped each runner to 2318MB (-25% from configured 3072) and started logging "clamping memory 3072 -> 2318 MB (fleet_budget 13909 MB [daemon 15957 MB - guest_reserve 2048 MB] / 6 runners)"
- Root cause: ezgha's `daemon_capacity()` reads `docker info --format "{{.MemTotal}}"`. On Colima, docker daemon reports the daemon's view (15957MB), NOT the actual VM ceiling (24GiB). The `vm_total_mb` config override existed but `effective_limits()` didn't use it.

## The fix (PR #77 in jleechanorg/ez-gh-actions)
```rust
// Before:
pub fn effective_limits(cfg: &Config) -> (f64, u64) {
    effective_limits_with_capacity(cfg, daemon_capacity())
}

// After:
pub fn effective_limits(cfg: &Config) -> (f64, u64) {
    let (ncpu, daemon_mem) = match daemon_capacity() {
        Some(c) => c,
        None => return (cfg.limits.cpus, cfg.limits.memory_mb),
    };
    let fleet_mem_base = cfg.runner.vm_total_mb.unwrap_or(daemon_mem);
    effective_limits_with_capacity(cfg, Some((ncpu, fleet_mem_base)))
}
```

## Math (post-fix)
- `vm_total_mb = 24576` (24GiB)
- `guest_reserve_mb = 2048`
- `fleet_budget = 24576 - 2048 = 22528`
- `count = 6`
- `per_runner = 22528 / 6 = 3754MB` (respects 3072MB floor + headroom, no clamping)

## Rule for future ezgha configuration
- **Always set `vm_total_mb` explicitly** when running ezgha inside a VM (Colima, Lima, Docker Desktop) — the daemon's `MemTotal` will be less than the VM ceiling.
- **Memory budget formula**: `per_runner_mb = (vm_total_mb - guest_reserve_mb) / count` — must be ≥ `memory_mb` (the configured per-runner memory) or ezgha will clamp and log.
- **6-runner floor at 3GB each + 2GB reserve = 20GB VM** minimum (with `memory_mb=3072`, `count=6`).
- **The startup fail-loud guard** (`derive_memory_budget()` in `docker_backend.rs`) already uses `vm_total_mb`; PR #77 makes the runtime `effective_limits()` consistent with it.

## References
- PR: https://github.com/jleechanorg/ez-gh-actions/pull/77 (merged as commit 85c9ded)
- Bead: `ez-gh-actions-yz6b` (in ez-gh-actions repo) — original fail-loud guard; PR #77 makes guard + runtime clamp consistent
- File: `src/docker_backend.rs` — `daemon_capacity()`, `effective_limits()`, `derive_memory_budget()`
- Mac runner restore: Colima VM 4GiB → 24GiB; ezgha count 3 → 6; memory_mb 8192 → 3072
- 68 existing docker_backend unit tests pass; new behavior exercised by existing fixtures

## Verification
- Manual test: 24GiB Colima, count=6, memory_mb=3072, vm_total_mb=24576, guest_reserve_mb=2048
- Per-runner memory after fix: 3754MB (configured 3072 + headroom, no clamping)
- GitHub-side runner count: 6 (all online, no clamping warnings)
