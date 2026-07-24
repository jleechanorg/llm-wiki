---
title: "Aside browser crash diagnosis: SIGABRT/mutex (not SIGTRAP/DCHECK) + hourly updater bootout fix (2026-06-27)"
type: source
tags: [feedback, crash-diagnosis, aside-browser, chromium, macos]
date: 2026-06-27
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-27_aside_browser_crash_diagnosis.md
bead: rev-np606
---

## Summary

Aside browser (Chromium-based AI agent) crashes are the same root cause family as Perplexity Comet — entitlements present, `NSXxxUsageDescription` missing in `Info.plist`, `com.apple.security.automation.apple-events` not granted. But the **secondary signature diverges**: Comet dies with `EXC_BREAKPOINT/SIGTRAP` from `ChromeMain` DCHECK; Aside dies with `EXC_CRASH/SIGABRT` from `std::__1::mutex::lock()` throwing `system_error` → uncaught C++ exception → `std::__terminate` → `abort()`. The mutex crash is triggered by the hourly `at.studio.AsideUpdater.wake` launchd job (`StartInterval: 3600`). User-side fix: `launchctl bootout gui/501/at.studio.AsideUpdater.wake` (applied 2026-06-27).

## Key Claims

- 5× AsideUpdater + 2× aside-daemon crashes in 24h before fix; 0 of those categories after `launchctl bootout`
- All crashes hit `std::__1::mutex::lock()` → `__throw_system_error` → `__cxa_throw` → `std::__terminate` → `abort()` — same exception unwinding chain, different trigger than Comet's SIGTRAP/DCHECK path
- TCC log confirms: `kTCCServiceAddressBook` and `kTCCServiceCalendar` fail with "requires entitlement ... but it is missing" — the same upstream defect class as Comet
- `~/Library/LaunchAgents/at.studio.AsideUpdater.wake.plist` has `StartInterval: 3600` and runs `AsideUpdater --wake-all --enable-logging` — this is the dominant crash trigger

## Key Quotes

> "Aside is a Y Combinator–backed AI-native Chromium browser launched June 2026" — [[AsideBrowser]]

> "service: kTCCServiceAddressBook requires entitlement com.apple.security.personal-information.addressbook but it is missing" — TCC log, 2026-06-27 16:39:20

> "Chromium-based AI browsers all hit the same entitlement/plist upstream defect, but the downstream crash mode depends on which code path the broken entitlement triggers" — lesson synthesized 2026-06-27

## Connections

- [[AsideBrowser]] — the entity this diagnostic applies to
- [[ChromiumAIBrowserCrashSignatures]] — the methodology concept this finding extends; adds SIGABRT/mutex as a sibling failure mode to SIGTRAP/DCHECK
- [[ReversibleFacadePattern]] — the bootout pattern (disable without removing) is a reversible facade; user can re-enable via `launchctl load ~/Library/LaunchAgents/at.studio.AsideUpdater.wake.plist`
- [[feedback-2026-06-25-chromium-ai-browser-crash-signatures]] — prior memory on the Comet SIGTRAP case
- [[feedback-2026-06-25-comet-ramdisk-profile]] — RAM-disk mitigation proven for Comet, not yet applied to Aside
- Bead `rev-np606` (closed 2026-06-27) — task record
