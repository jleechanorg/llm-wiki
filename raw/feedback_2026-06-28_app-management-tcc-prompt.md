---
name: macos-app-management-tcc-prompt-fires-from-cmux-dev-launch-enumeration-root-cause
description: "Why cmux DEV builds trigger \"X would like to access data from other apps\" and the two enumeration sites that cause it, plus the three-step fix"
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: c5b1d462-2cbc-435d-88ea-20932a77e93b
---

# macOS App Management TCC prompt fires from cmux DEV launch

## Context

The user reported always seeing the dialog `"cmux DEV may-18" would like to access data from other apps. Keeping app data separate makes it easier to manage your privacy and security.` (with [Don't Allow] [Allow]) on every tagged build. They thought it was the screensaver code path. It was actually **two** enumeration sites.

## Root cause

macOS keys the **App Management** TCC category to **bundle ID**. `scripts/reload.sh:519` derives a unique bundle ID per `--tag` value:

```bash
BUNDLE_ID="com.cmuxterm.app.debug.${TAG_ID}"   # TAG_ID = lowercased, dot-separated tag
```

That means every fresh `cmux DEV <tag>.app` is treated as a new app by TCC. macOS prompts once per new bundle, so each new tag re-prompts the user.

The two enumeration sites that triggered the prompt:

1. **`Sources/MacPresenceMonitor.swift:152`** — `liveScreensaverRunning()` called `NSWorkspace.shared.runningApplications.contains { $0.bundleIdentifier == "com.apple.ScreenSaver.Engine" }`. Hit on first phone-forwarding notification per launch.

2. **`Sources/AppDelegate.swift:15433`** — `enforceSingleInstance()` called `NSRunningApplication.runningApplications(withBundleIdentifier: bundleId)` from `applicationDidFinishLaunching`. Hit on every launch.

`NSWorkspace.shared.open(...)`, `NSWorkspace.shared.activateFileViewerSelecting(...)`, `NSWorkspace.shared.icon(...)`, `NSRunningApplication.current.activate(...)`, and `NSWorkspace.shared.selectFile(...)` (FilePreviewPanel, BrowserPanel, SettingsWindowPresenter) are **gated behind user action** — they did NOT trigger the prompt.

## Fix

Three commits on `fix/screensaver-notification-tracking` (pushed, merged via PR #9 chain):

1. **Replace `NSWorkspace.shared.runningApplications` enumeration with `DistributedNotificationCenter`** subscribing to the screensaver daemon's Darwin notifications (`com.apple.screensaver.didstart` / `com.apple.screensaver.didstop`). The subscription is passive — never enumerates apps, never triggers App Management TCC. **Trade-off**: defaults to false at launch; if the screensaver was already running when cmux launched, we won't see it until the screen wakes and a stop notification fires (one missed push, acceptable).

2. **Remove `enforceSingleInstance()` entirely** — the existing `observeDuplicateLaunches()` observer (passive `NSWorkspace.didLaunchApplicationNotification` subscription) handles new-duplicate launches. Instances already running when this one starts are no longer terminated (acceptable trade-off for a terminal app where users typically run one cmux).

3. **Install tagged builds to `/Applications/cmux DEV <tag>.app/`** in `scripts/reload.sh`, and point `/tmp/cmux-last-cli-path` at that durable install path instead of the evictable `~/Library/Developer/Xcode/DerivedData/cmux-<tag>/` path. Survives Xcode's automatic DerivedData cleanup, `Xcode → Delete Derived Data`, disk pressure, and `cleanup-dev-builds.sh --apply`.

`scripts/cleanup-dev-builds.sh` updated to:
- Add `/Applications/cmux DEV ${tag}.app` to `artifact_paths_for_tag()` so cleanup actually removes the install.
- Match the active-tag regex against both `DerivedData/cmux-<tag>/` and `/Applications/cmux DEV <tag>.app/` paths.

## Verification

- 5/5 logic tests passed (script exercises install + cleanup paths against a fake `.app`).
- Real `./scripts/reload.sh --tag shim-resilience-verify` produced `/Applications/cmux DEV shim-resilience-verify.app/` (43 MB binary) and updated the marker to that durable path. `cmux --version` returned `cmux 0.64.16 (96) [0ff2dd9df]`.
- `agy --print --dangerously-skip-permissions "..."` ran headless, exit 0, **0 matches** for `Tool call denied | jsonhook__cmux_PreToolUse_0_0 | by pre-tool hook | Trajectory ID` in fresh transcripts (`/tmp/cmux-investigation-agy-headless-2026-06-28/`).
- PR #9 merged 2026-06-28T19:17:55Z.

## Reusable pattern

When fixing macOS TCC prompts in any app:

1. **Identify** each gate in `enabled()` / `is_ready()` / activation check by reading the source — list every API call that triggers the TCC category. For App Management: `NSWorkspace.shared.runningApplications`, `NSWorkspace.shared.urlForApplication(...)`, `NSRunningApplication`, `Bundle(url:)` for foreign apps.
2. **State the gate-by-gate env** — for each enumeration site, what input triggered it on the user's machine? (CMUX_TAG, default forwarding config, app delegate init path.)
3. **Cite the tool call + output** that proves `enabled() == True` in the standard harness startup path, **not** a launchd/cron env that explicitly sets the activation var. Banned: "cache works" based on launchd test logs that set the cache var.
4. **Replace, don't suppress** — `DistributedNotificationCenter` (passive) instead of `NSWorkspace.shared.runningApplications` (enumeration). `NSWorkspace.didLaunchApplicationNotification` observer (passive) instead of `NSRunningApplication.runningApplications` polling.

## Files changed

- `Sources/MacPresenceMonitor.swift:152-167` — `liveScreensaverRunning()` now reads `ScreensaverStateTracker.shared.isRunning`.
- `Sources/ScreensaverStateTracker.swift` (new) — `@MainActor` singleton subscribing to `DistributedNotificationCenter.default().addObserver(forName: NSNotification.Name("com.apple.screensaver.didstart")...)`.
- `Sources/AppDelegate.swift:1425-1432` and `15425-15449` — `enforceSingleInstance()` call and body removed; `observeDuplicateLaunches()` retained.
- `scripts/reload.sh:1010-1044` — install tagged builds to `/Applications/cmux DEV ${TAG_SLUG}.app/`, point marker there.
- `scripts/cleanup-dev-builds.sh:91` and `127-135` — `/Applications/` in artifact list; updated active-tag regex.
- `tests/test_cli_dev_cli_shim_resilience.py` (new, dark-factory–written) — passes both regex branches.

## References

- cmux commit `84f5eee01 fix(antigravity): prevent cmux feed bridge from denying agy tool calls` — prior cmux-side fix for a related but different TCC category (cmux feed bridge hooks in Antigravity sessions).
- cmux PR #9 — merge commit `d2050bfc38ff1eb660208d584bd5c80097e5871e`, merged 2026-06-28T19:17:55Z.
- Hermes MEMORY entry `feedback_2026-06-27_dir_inheritance_works_on_june27_not_release.md` — related: Release vs DEV cmux builds behave differently due to libghostty fix presence.