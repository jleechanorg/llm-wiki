---
title: "Service Discrimination"
type: concept
tags: [infrastructure, port-management, service-detection, false-positive]
date: 2026-06-26
---

# Service Discrimination

**Definition**: When checking whether a specific service is running on a host, do NOT rely on `lsof -ti:PORT` or similar port-occupancy checks — they only confirm that *something* is listening, not that the *right* thing is. Always probe a service-specific endpoint and assert a known response shape (status code, JSON title, content type, etc.).

## Why it matters

Port 8000 is the most commonly conflicted port on developer machines (HTTP alternative, FastAPI defaults, OAuth proxies, memcached alternate, Jupyter, etc.). When multiple services are installed, a port check passes for the wrong service — silent false positives. Observed in `llm-inspector` 2026-06-26: `mem0_server.py` (FastAPI) and `ccproxy-api` both want port 8000; `lsof -ti:8000` returned non-empty for mem0, cli.ts auto-launcher concluded "ccproxy already running" without ever starting ccproxy.

## Pattern

```typescript
// ❌ Wrong: any listener passes
try { execSync("lsof -ti:8000"); running = true; } catch {}

// ✅ Right: probe a known endpoint and assert shape
const probe = async (): Promise<boolean> => {
  try {
    const res = await fetch("http://127.0.0.1:8000/openapi.json", {
      signal: AbortSignal.timeout(1500),
    });
    if (!res.ok) return false;
    const body = await res.json() as { info?: { title?: string } };
    return body?.info?.title === "CCProxy API Server";  // discriminator
  } catch { return false; }
};
```

## Discriminator catalog

| Service | Port | Discriminator endpoint | Assertion |
|---|---|---|---|
| ccproxy-api | 8000 | `GET /openapi.json` | `info.title === "CCProxy API Server"` |
| mem0_server | varies | `GET /health` | response contains `"status":"ok"` |
| FastAPI | varies | `GET /openapi.json` | `info.title` is custom (project-set) |
| Express | varies | `GET /` | typically HTML; check `X-Powered-By: Express` |

## Where else to apply

- `llm-inspector` `src/cli.ts:62-79, 320-353` — both `start` and `status` commands (now fixed)
- Any "is service X running?" check across any project
- launchd plist health-check scripts
- CI smoke tests that gate on "is upstream up?"

## Related concepts

- [[MacOSKeychainOAuthStorage]] — same class of false-positive: assuming file location is canonical when the OS migrated to a different storage
- [[LaunchdWorkerPIDRace]] — same class of false-positive: trusting PID file when launchd-managed processes bypass the writer
- [[SkillStaleness]] — same class of false-positive: trusting a helper's status string instead of running the mechanism