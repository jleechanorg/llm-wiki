# OpenClaw E2E Remote Routing Fix

**Branch**: `feat/openclaw-gateway-url-setting`
**Commit**: `95c192839`
**Date**: 2026-02-21

## Problem

The OpenClaw E2E test was failing in strict remote-only routing mode. The Cloudflare Quick Tunnel URL was registered but DNS resolution was failing within the test's 12-second polling window. Even after extending the DNS window, the tunnel returned 502 Bad Gateway because the routing layer wasn't ready when HTTP requests arrived.

In fallback mode (`auto + local fallback`), streaming failed at exactly 31 seconds due to a tap proxy timeout hardcoded at 30s.

## Root Causes and Fixes

### Fix 1 — Tap proxy timeout (30s → 120s)

**File**: `testing_ui/test_openclaw_e2e.py`
**Location**: HTTPConnection tap proxy constructor

LLM streaming responses routinely exceed 30 seconds. The tap proxy's `HTTPConnection` timeout cut live streams.

```python
# Before:
conn = http_client.HTTPConnection(gateway_host, gateway_port, timeout=30)
# After:
conn = http_client.HTTPConnection(gateway_host, gateway_port, timeout=120)
```

### Fix 2 — DNS check window (12×1s → 60×2s)

**File**: `testing_ui/test_openclaw_e2e.py`
**Location**: `__init__` DNS check defaults

`trycloudflare.com` subdomains are **not wildcards**. Each tunnel registers an individual DNS record that takes 60–120 seconds to propagate. The original 12-second budget was far too short.

```python
# Before: 12 attempts × 1.0s = 12s budget
# After:  60 attempts × 2.0s = 120s budget
self._public_url_dns_check_attempts = max(1, int(os.getenv("OPENCLAW_PUBLIC_URL_DNS_CHECK_ATTEMPTS", "60")))
self._public_url_dns_check_interval_s = max(0.25, float(os.getenv("OPENCLAW_PUBLIC_URL_DNS_CHECK_INTERVAL_SECONDS", "2.0")))
```

### Fix 3 — Step 8 remote routing check (false failure)

**File**: `testing_ui/test_openclaw_e2e.py`
**Location**: Step 8 gateway route verification

In `remote_only` mode, traffic goes directly to the Cloudflare URL — the local tap proxy sees **zero traffic** by design. The old Step 8 logic treated `has_tap_traffic=False` as a failure.

Added `is_remote_route` branch: when `gateway_url_mode == "remote_tunnel"`, accept zero tap traffic and use streaming success from Steps 4–6 as the routing proof.

### Fix 4 — Tunnel HTTP connectivity probe (after DNS resolution)

**File**: `testing_ui/test_openclaw_e2e.py`
**Location**: After `_is_public_url_resolvable()` succeeds

DNS propagation completes before Cloudflare's routing layer is ready. The tunnel returns 502/503/504 during a brief stabilization window after DNS resolves.

Added a 15-attempt × 2s HTTP probe loop against `/health` that waits for the routing layer to accept traffic before proceeding with streaming tests.

## Test Results

### Mode 1 — Auto routing with local fallback

```
OPENCLAW_ROUTING_MODE=auto
OPENCLAW_REQUIRE_REMOTE_GATEWAY_URL=true
OPENCLAW_ALLOW_LOCAL_ROUTE_FALLBACK=true
OPENCLAW_REQUIRE_PUBLIC_URL_DNS=false
```

Result: **PASSED** — 7 tap proxy calls captured, all 8 steps green.

Evidence: `/tmp/worldarchitectai/feat_openclaw-gateway-url-setting/openclaw_e2e/run_1771739268/`

### Mode 2 — Strict remote-only with DNS verification

```
OPENCLAW_ROUTING_MODE=remote_only
OPENCLAW_REQUIRE_REMOTE_GATEWAY_URL=true
OPENCLAW_REQUIRE_PUBLIC_URL_DNS=true
```

Result: **PASSED** — streaming via Cloudflare tunnel confirmed, all 8 steps green.

Evidence: `/tmp/worldarchitectai/feat_openclaw-gateway-url-setting/openclaw_e2e/run_1771741866/`

## Files Changed

| File | Change |
|------|--------|
| `testing_ui/test_openclaw_e2e.py` | Tap proxy timeout, DNS window, HTTP probe, Step 8 remote routing branch |
| `testing_ui/lib/browser_test_base.py` | Pre-existing branch changes (settings navigation, OpenClaw setup helpers) |
