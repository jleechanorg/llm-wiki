---
title: "ChromiumAIBrowserCrashSignatures"
type: concept
tags: [crash-diagnosis, chromium, methodology, macos]
date: 2026-06-27
sources:
  - /Users/jleechan/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-27_aside_browser_crash_diagnosis.md
  - /Users/jleechan/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-25_chromium_ai_browser_crash_signatures.md
---

## Definition

Diagnostic methodology for crashes in Chromium-based AI browsers (Perplexity Comet, Arc Max, Brave Leo, Aside, etc.) on macOS. The upstream defect is the same family across vendors — entitlements present in `codesign -d --entitlements` but `NSXxxUsageDescription` missing from `Info.plist`, often combined with `com.apple.security.automation.apple-events` not granted under hardened runtime. The **downstream secondary signature depends on which code path the broken entitlement triggers**, so the exception type alone (SIGTRAP vs SIGABRT vs SIGSEGV) is a sibling failure mode, not a different root cause.

## Known secondary signatures (2026-06-27)

| Vendor | Exception | Origin frame | Trigger chain |
|---|---|---|---|
| Perplexity Comet | `EXC_BREAKPOINT/SIGTRAP` | `ChromeMain` (DCHECK hit) | Broken entitlement → Chromium DCHECK assert site |
| Aside | `EXC_CRASH/SIGABRT` | `std::__1::mutex::lock()` → `__throw_system_error` → uncaught C++ exception | Hourly `at.studio.AsideUpdater.wake` job cross-process lock with running browser |

Both crashes share the same root cause (entitlement ↔ Info.plist mismatch), but the secondary signature diverges based on which subsystem the broken entitlement reaches first.

## 5-probe order (apply before assuming user-code bug)

1. **Crash report exception type + stack origin frame** — tells you which subsystem the broken entitlement hit, not whether it's a different bug
2. **Entitlement ↔ Info.plist pairing** — `codesign -d --entitlements -` then `plutil -p Info.plist | grep -i Usage`. Any entitlement without matching `NSXxxUsageDescription` is a hard-abort trigger
3. **Hardened runtime + AppleEvents** — `com.apple.security.automation.apple-events` missing AND hardened runtime ON = structurally dead for AI agent mode
4. **Disk-write watchdog** — `log show --predicate 'subsystem == "com.apple.kernelescalation"' --last 30d` for `Event: disk writes`; > 25 KB/sec means kernel pressure
5. **Fanout mechanism** — Chromium-based AI browsers use MV3 extension service worker in `~/Library/Application Support/<Browser>/Default/Extensions/`; check `/Applications/<Browser>.app/Contents/MacOS/` for binary count

## User-side mitigations (vendor won't fix path)

- `launchctl bootout gui/$(id -u)/<browser>.updater.wake` — stop hourly updater (dominant crash contributor for both Comet and Aside)
- Grant `Screen Recording` to app's Helper (rarely helps but free)
- Avoid fanout tasks needing AppleEvents/camera/mic/photos/location until vendor ships entitlement+plist fixes
- Clear `~/Library/Application Support/<Browser>/Crashpad/completed/` (128 MB+ typical)
- Move browser data to RAM disk (12 GB HFS+) per [[feedback-2026-06-25-comet-ramdisk-profile]]

## Why this is a concept, not just a source

Two separate incidents (Comet 2026-06-25, Aside 2026-06-27) both resolved to the same upstream defect with different secondary signatures. The pattern generalizes: any future Chromium-based AI browser crash should be triaged through this 5-probe order regardless of vendor.

## Connections

- [[AsideBrowser]] — entity that hit the SIGABRT/mutex variant on 2026-06-27
- [[Chromium]] — base engine both vendors fork
- [[feedback-2026-06-25-chromium-ai-browser-crash-signatures]] — original Comet SIGTRAP methodology
- [[feedback-2026-06-27-aside-browser-crash-diagnosis]] — second incident, extends the methodology
- [[feedback-2026-06-25-comet-ramdisk-profile]] — RAM-disk mitigation proven for Comet
