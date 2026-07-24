---
name: feedback-2026-06-27-aside-browser-crash-diagnosis
description: "Aside browser (Chromium-based, AI agent) crashes are same root cause family as Perplexity Comet (entitlement ↔ Info.plist mismatch + missing automation.apple-events) but secondary signature is SIGABRT/mutex-deadlock, NOT SIGTRAP/DCHECK. Hourly AsideUpdater.wake launchd job is the biggest contributor; bootout is the user-side fix."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e7388df9-30a0-4b2d-a4d0-c5db1bc5c380
  bead: rev-np606
---

On 2026-06-27 the user reported Aside browser "crashed randomly." Investigation showed 5× AsideUpdater + 2× aside-daemon crashes in 24h, all with `EXC_CRASH/SIGABRT` ("Abort trap: 6"). Root cause is the same family documented in [[feedback-2026-06-25-chromium-ai-browser-crash-signatures]]: entitlements present, `NSXxxUsageDescription` missing in `Info.plist`, `com.apple.security.automation.apple-events` not granted.

**Secondary signature divergence** (the new lesson):
- Comet → `EXC_BREAKPOINT/SIGTRAP` from `ChromeMain` DCHECK hit
- Aside → `EXC_CRASH/SIGABRT` from `std::__1::mutex::lock()` throwing `system_error` → uncaught C++ exception → `std::__terminate` → `abort()`

The mutex crash is triggered by the **hourly `at.studio.AsideUpdater.wake` launchd job** (`StartInterval: 3600`, `LimitLoadToSessionType: Aqua`, runs `AsideUpdater --wake-all`). Each wake acquires cross-process locks with the running browser; when the running browser holds a lock the updater needs (or vice versa), `pthread_mutex_lock()` throws and Aside's daemon has no `catch (...)` upstream.

**TCC log evidence** (same family as Comet):
> `service: kTCCServiceAddressBook requires entitlement com.apple.security.personal-information.addressbook but it is missing`
> `service: kTCCServiceCalendar requires entitlement com.apple.security.personal-information.calendars but it is missing`

**User-side mitigations applied 2026-06-27:**
1. `launchctl bootout gui/$(id -u)/at.studio.AsideUpdater.wake` — **unregistered the hourly updater**. Verified: `launchctl print gui/$(id -u)/at.studio.AsideUpdater.wake` now returns "Could not find service." Aside GUI + CLI still work (CLI version 1.26.626.1517 alive).
2. `rm -rf ~/Library/Application\ Support/Aside/Crashpad/completed` — cleared the empty completed dir (4.3 MB total Crashpad retained). Reversible: Crashpad recreates `completed/` automatically.

**Why:** Chromium-based AI browsers all hit the same entitlement/plist upstream defect, but the downstream crash mode depends on which code path the broken entitlement triggers. For Aside, the buggy entitlement chain reaches the C++ mutex layer (not the DCHECK layer that catches Comet), so the secondary signature is SIGABRT not SIGTRAP. Diagnose via 5-probe order (entitlement ↔ Info.plist pair → hardened runtime + AppleEvents → disk-write watchdog → fanout mechanism → process count), not by exception type alone.

**How to apply:**
- Same 5-probe order from [[feedback-2026-06-25-chromium-ai-browser-crash-signatures]] applies to Aside. Don't stop at "exception is SIGABRT, not SIGTRAP — must be different bug."
- Add a 6th probe: `cat ~/Library/LaunchAgents/at.studio.AsideUpdater.wake.plist` and `launchctl list | grep -i aside` — if the updater job is loaded, bootout is the single biggest user-side win.
- After bootout, the 24 running Aside processes is still high but acceptable (Chromium helpers + extensions). Extension audit is a follow-up not a fix.
- For Aside-specific: `~/Library/Application Support/Aside` is 1.6 GB, `~/Library/Caches/Aside` is 823 MB — both candidates for RAM-disk migration per [[feedback-2026-06-25-comet-ramdisk-profile]]. Not yet applied.

**Verification probe order (Aside-specific, extend the global 5-probe order):**
```bash
ps aux | grep -iE "aside" | grep -v grep | wc -l                          # 24 = high (helpers + extensions)
codesign -d --entitlements - /Applications/Aside.app/Contents/MacOS/Aside  # confirm missing automation.apple-events
plutil -p /Applications/Aside.app/Contents/Info.plist | grep -i "Usage"   # will return empty (no NSXxxUsageDescription)
ls ~/Library/LaunchAgents/ | grep -i aside                                # 3 plists: asidekeystone.agent, asidekeystone.xpcservice, AsideUpdater.wake
launchctl list | grep -i aside                                            # should NOT show AsideUpdater.wake after bootout
ls -lat ~/Library/Logs/DiagnosticReports/ | grep -i aside                 # crash report count
```

**Provenance:**
- Crash report evidence: `/Users/jleechan/Library/Logs/DiagnosticReports/aside-daemon-2026-06-27-172743.ips` (latest daemon crash)
- 5 AsideUpdater crashes: `AsideUpdater-2026-06-27-{172012,172013,172014}.ips` + 2 retired
- Updater plist: `~/Library/LaunchAgents/at.studio.AsideUpdater.wake.plist`
- TCC log: `log show --predicate 'subsystem == "com.apple.TCC"' --last 1h --style compact | grep -i aside`
- Date: 2026-06-27 17:27-17:30 PDT (crashes); 17:35 (fix applied)
- Cross-reference: [[feedback-2026-06-25-chromium-ai-browser-crash-signatures]] (methodology), [[feedback-2026-06-25-comet-ramdisk-profile]] (RAM-disk profile)
