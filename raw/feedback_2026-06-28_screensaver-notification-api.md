---
name: macos-screensaver-detection-api-gotchas-nsworkspace-vs-darwin-distributed-notifications-class-rename
description: NSWorkspace has NO screensaverDidStart/DidStop members; screensaver events come via Darwin distributed notifications on com.apple.screensaver.didstart/stop; NSDistributedNotificationCenter was renamed to DistributedNotificationCenter
metadata: 
  node_type: memory
  type: reference
  bead: none
  originSessionId: c5b1d462-2cbc-435d-88ea-20932a77e93b
---

# macOS screensaver detection — API gotchas

Three landmines hit while implementing `ScreensaverStateTracker` to replace `NSWorkspace.shared.runningApplications` enumeration. All three wasted commits.

## 1. `NSWorkspace` does NOT have `screensaverDidStart/DidStop` notifications

The intuitive API does not exist:

```swift
// COMPILE ERROR: Type 'NSWorkspace' has no member 'screensaverDidStartNotification'
NSWorkspace.shared.notificationCenter.addObserver(
    forName: NSWorkspace.screensaverDidStartNotification, ...
)
```

The screensaver daemon posts **Darwin distributed notifications**, not NSWorkspace notifications. The right subscription is:

```swift
let center = DistributedNotificationCenter.default()
center.addObserver(
    forName: NSNotification.Name("com.apple.screensaver.didstart"),
    object: nil,
    queue: .main
) { _ in /* screensaver started */ }

center.addObserver(
    forName: NSNotification.Name("com.apple.screensaver.didstop"),
    object: nil,
    queue: .main
) { _ in /* screensaver stopped */ }
```

Names are stable across all macOS versions that ship a screensaver daemon.

## 2. `NSDistributedNotificationCenter` was renamed to `DistributedNotificationCenter`

In the macOS SDK the cmux repo targets, `NSDistributedNotificationCenter` produces:

```
'NSDistributedNotificationCenter' has been renamed to 'DistributedNotificationCenter'
```

The `NS` prefix was dropped. `DistributedNotificationCenter.default()` is the replacement. **The renamed class still exists** as a deprecation alias for one or two SDK versions before removal.

## 3. Default to `false` on cold start

If the screensaver is already running when the app launches, the subscription fires only after the user wakes the screen and a `com.apple.screensaver.didstop` notification posts. For an "only when away" phone-forwarding heuristic, this means one push may leak through to the phone before the state updates. Acceptable trade-off — better than enumerating apps at launch and triggering App Management TCC.

## Reusable pattern

For any "X state was already true at launch" question on macOS:

| Question | Enumeration API (triggers TCC) | Passive alternative |
|---|---|---|
| Is screensaver running? | `NSWorkspace.shared.runningApplications.contains { $0.bundleIdentifier == "com.apple.ScreenSaver.Engine" }` | Subscribe to `com.apple.screensaver.didstart/stop` via `DistributedNotificationCenter`; default `false` at launch |
| Is app X launched? | `NSRunningApplication.runningApplications(withBundleIdentifier: "X")` | `NSWorkspace.shared.notificationCenter.addObserver(forName: NSWorkspace.didLaunchApplicationNotification, ...)`; observer fires for the next launch only |
| What URL handles scheme X? | `NSWorkspace.shared.urlForApplication(toOpen:)` | Read `~/Library/Preferences/com.apple.LaunchServices/com.apple.launchservices.secure.plist` (private API; not recommended) |
| Is the screen locked? | `CGSessionCopyCurrentDictionary()` `kCGSSessionOnConsoleKey` | Subscribe to `com.apple.screenIsLocked` / `com.apple.screenIsUnlocked` Darwin notifications |

When in doubt, prefer passive notification subscription over polling/enumeration. App Management and Accessibility TCC categories both gate on the same enumeration primitives.

## References

- cmux commit `c543957d8 fix(presence): source screensaver signal from passive notifications` — initial fix using nonexistent `NSWorkspace.screensaverDidStartNotification`.
- cmux commit `1c8605cdb fix(presence): use NSDistributedNotificationCenter for screensaver events` — correction #1.
- cmux commit `491b357af fix(presence): use renamed DistributedNotificationCenter API` — correction #2.
- Apple Developer Forums: "What's the right way to detect screen lock / unlock / screensaver state?" — answer is `com.apple.screenIsLocked/IsUnlocked` and `com.apple.screensaver.didstart/stop` via Darwin notifications.