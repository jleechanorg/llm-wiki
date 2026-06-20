---
title: "WebKit IndexedDB Hang Deadlock"
type: concept
tags: [webkit, ios, indexeddb, persistence, deadlock, firebase-js-sdk-8019]
sources: [pr7720-ios-webkit-indexeddb-persistence-deadlock]
last_updated: 2026-06-20
---

# WebKit IndexedDB Hang Deadlock

## Phenomenon

On iOS Safari/WebKit, after the OS suspends the browser process, IndexedDB `open()` / read transactions never settle (callback never fires). The page appears stuck. A normal reload reuses the same hung WebKit process + stuck IndexedDB, so the broken state persists. Only killing the process (cold restart) clears it.

## Reproduction discipline

- **Reproducing organically** (no stub) from page JS off a real device is **unreachable** — the hang is a device-level OS-process-suspension property.
- **Correct model:** deterministic stub that simulates the hang shape (e.g. `IndexedDB.open` patched to never resolve). All RED/GREEN tests stub this way.
- **Strongest evidence:** real-device reproduction on iOS Simulator (MobileSafari) with the deployed bundle, confirmed by raw HTTP capture of the served JS containing the neutralization block.

## Mechanism (firebase-js-sdk 9.6.1)

firebase-js-sdk issue #8019's title references "Web-Locks", but on the 9.6.1 compat bundle prod ships, there are zero `navigator.locks` references (verified via `curl -sL --compressed -A "Mozilla/5.0"`; a bare curl returns a 598 B stub and gives a false 0-count). The wedge on 9.6.1 is the IndexedDB open/read never settling, not Web-Locks coordination (that path is in newer SDK lines).

## Diagnosis checklist

1. Symptom: page blank/hung on iOS only; Chrome/Firefox desktop fine.
2. Reload does NOT fix it; cold restart DOES.
3. `firebase.auth().onAuthStateChanged(cb)` — `cb` never fires.
4. Network tab shows the auth/data fetch failing with "User not authenticated".
5. SDK version uses `Persistence.LOCAL` → resolves to `indexedDBLocalPersistence` on iOS.

If all five hold, this is the deadlock. Apply the [[IndexedDBNeutralizationPattern]] fix.

## Related

- [[FirebaseJSSDK]]
- [[IndexedDBNeutralizationPattern]]
- [[FirebaseAuthPersistenceFallback]]
- [[PR7720]]
- [[MobileAuthReproFidelity]]
