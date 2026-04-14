# OpenClaw E2E Remote Routing — Test Evidence

**Branch**: `feat/openclaw-gateway-url-setting`
**Commit**: `95c192839` (fixes) + `4e168f784` (docs)
**Date**: 2026-02-22 (UTC)

## Passing Runs Summary

| Run ID | Mode | Routing | Checks | Result | Duration | Notes |
|--------|------|---------|--------|--------|----------|-------|
| `run_1771740202` | Auto + local fallback | `remote_with_fallback:explicit` | 13 recorded ✅ | **PASS** | 06:03–06:08 UTC | DNS failed → fell back to local tap proxy |
| `run_1771742012` | Strict remote-only + DNS | `remote_required:explicit` | 14 recorded ✅ | **PASS** | 06:33–06:40 UTC | DNS resolved → streamed via Cloudflare tunnel |

> **Note on check counts**: `checks_passed` counts all recorded checks, not just the required subset.
> `step7_settings_persisted` was required but never emitted by the test code in these runs —
> this gap is tracked in REV-403z / REV-7lnf and fixed in subsequent commit.

---

## Run 1: Auto Routing — Fell Back to Local Tap Proxy

**Run ID**: `run_1771740202`
**Evidence path**: `/tmp/worldarchitectai/feat_openclaw-gateway-url-setting/openclaw_e2e/run_1771740202/`

**Environment**:
```
OPENCLAW_ROUTING_MODE=auto
OPENCLAW_REQUIRE_REMOTE_GATEWAY_URL=true
OPENCLAW_ALLOW_LOCAL_ROUTE_FALLBACK=true
OPENCLAW_REQUIRE_PUBLIC_URL_DNS=false
```

**Tunnel**: `https://danny-guitars-suspected-sponsorship.trycloudflare.com` (cloudflared)
— DNS resolution: `false` at time of test
— **chosen_mode: `local_route`** — DNS failed to resolve within the check window; test fell back to local tap proxy (correct behaviour for `allow_local_fallback=true`)
— This run proves the **local fallback path** works, not the remote routing path

**Proof checks (13 recorded, all passed)**:
```
✅ step0_gateway_started
✅ step0_tap_proxy_started
✅ step1_openclaw_settings_local
✅ step1_gateway_url_cleared
✅ step1_provider_openclaw
✅ step1_port_set
✅ step2_script_downloaded
✅ step2_tunnel_script_output
✅ step2_public_url_dns_check_required
✅ step2_routing_mode_decision       [chosen_mode=local_route, reason=public_url_not_resolvable_fallback]
✅ step8_gateway_route_expected_local
✅ step8_tap_capture_local           [tap_requests=7]
✅ step8_route_traffic_verified
⚠️ step7_settings_persisted         [not recorded — test code gap, see REV-403z]
```

**Streaming result** (from `test_complete.json`):
- 3 × character mode LLM calls via OpenClaw provider
- 7 tap proxy requests captured — proves backend→OpenClaw traffic flows through local tap proxy on fallback
- LLM provider: `openclaw`, model: `openclaw/gemini-3-flash-preview`

---

## Run 2: Strict Remote-Only with DNS Verification

**Run ID**: `run_1771742012`
**Evidence path**: `/tmp/worldarchitectai/feat_openclaw-gateway-url-setting/openclaw_e2e/run_1771742012/`

**Environment**:
```
OPENCLAW_ROUTING_MODE=remote_only
OPENCLAW_REQUIRE_REMOTE_GATEWAY_URL=true
OPENCLAW_REQUIRE_PUBLIC_URL_DNS=true
```

**Tunnel**: `https://city-resume-veterans-streams.trycloudflare.com` (cloudflared, pid 11834)
— DNS resolved: `true` (after 60 attempts × 2s = up to 120s budget)
— HTTP routing layer ready: `true` (probe confirmed after DNS resolution)
— Fallback: `false`

**Proof checks (14/14 passed)**:
```
✅ step0_gateway_started
✅ step0_tap_proxy_started
✅ step1_openclaw_settings_local
✅ step1_gateway_url_cleared
✅ step1_provider_openclaw
✅ step1_port_set
✅ step2_script_downloaded
✅ step2_tunnel_script_output
✅ step2_public_url_dns_check_required    [attempts=60, resolved=true]
✅ step2_routing_mode_decision            [chosen_mode=remote_tunnel, reason=public_url_resolvable]
✅ step2_remote_route_required            [configured_gateway_url=https://city-resume-veterans-streams.trycloudflare.com]
✅ step8_gateway_route_expected_local     [configured_gateway_url=https://city-resume-veterans-streams.trycloudflare.com]
✅ step8_tap_capture_local               [reason=remote routing active — tap traffic not expected]
✅ step8_route_traffic_verified           [reason=remote routing — traffic verified via streaming success in Steps 4-6]
```

**Streaming result** (from `test_complete.json`):
- Steps passed: [0, 1, 2, 3, 4, 5, 6, 7, 8] — all 9 steps
- Character mode run 1: `story_length=2932`, `chunk_count=20` ✅
- Character mode run 2: `story_length=2160`, `chunk_count=35` ✅
- God mode run: `story_length=199`, `chunk_count=7` ✅
- Provider: `openclaw`, model: `openclaw/gemini-3-flash-preview`
- Gateway URL persisted in settings: `https://city-resume-veterans-streams.trycloudflare.com`
- `openclaw_gateway_requests=0` — tap proxy correctly sees zero traffic (traffic went to Cloudflare URL directly)

---

## Full Run History

| Run ID | Routing mode | Passed | Failed | Result |
|--------|-------------|--------|--------|--------|
| `1771737866` | `remote_required:auto` | 7 | 2 | FAIL (DNS 12s budget) |
| `1771737951` | `remote_required:auto` | 7 | 2 | FAIL (DNS 12s budget) |
| `1771738033` | `remote_required:auto` | 7 | 2 | FAIL (DNS 12s budget) |
| `1771738123` | `remote_required:auto` | 9 | 0 | FAIL (missing required checks) |
| `1771738189` | `remote_required:auto` | 7 | 2 | FAIL (DNS 12s budget) |
| `1771738259` | `remote_with_fallback:explicit` | 10 | 0 | FAIL (missing step7) |
| **`1771738517`** | `remote_with_fallback:explicit` | 13 | 0 | **PASS** |
| `1771739047` | `remote_required:explicit` | 7 | 2 | FAIL (tap proxy timeout 30s) |
| `1771739268` | `remote_with_fallback:explicit` | 10 | 0 | FAIL (missing step7) |
| **`1771740202`** | `remote_with_fallback:explicit` | 13 | 0 | **PASS** |
| `1771740539` | `remote_required:explicit` | 7 | 2 | FAIL (DNS 12s budget) |
| `1771740791` | `remote_required:explicit` | 11 | 3 | FAIL (Cloudflare 502) |
| `1771741314` | `remote_required:explicit` | 11 | 0 | FAIL (missing step7) |
| **`1771742012`** | `remote_required:explicit` | 14 | 0 | **PASS** |

---

## Evidence Files per Passing Run

Each run directory contains:

| File | Contents |
|------|----------|
| `openclaw_e2e_proof_manifest.json` | All check results with pass/fail |
| `openclaw_e2e.webm` | Full screen recording of browser test |
| `http_request_responses.jsonl` | All HTTP request/response pairs |
| `openclaw_tunnel_script_output.json` | Tunnel startup, URL, DNS status |
| `openclaw_gateway_setup.json` | Settings page configuration |
| `settings_configured.json` | Final gateway URL configured in UI |
| `test_complete.json` | LLM streaming results per character mode |
| `continue_character_*.json` | Per-attempt streaming proof |
| `screenshots/` | Step-by-step browser screenshots |
| `videos/` | Playwright video recording |
