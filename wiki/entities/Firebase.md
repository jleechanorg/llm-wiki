---
title: "Firebase"
type: entity
tags: [backend, auth, database]
sources: [waitlist-gating-account-switching-flow]
last_updated: 2026-06-20
---

## Overview

Firebase is Google's mobile and web application development platform. WorldArchitect.AI uses Firebase Authentication for user identity management and Firestore for data persistence.

## Usage in WorldArchitect.AI

- **Firebase Auth** — `onAuthStateChanged` listener for auth state changes
- **Google Auth Provider** — `setCustomParameters({ prompt: 'select_account' })` for forced account chooser
- **Firestore** — `is_waitlist_mode_enabled()` and `get_waitlist_access_status()` for waitlist checks

## References
- [[WaitlistGatingMode]] — access control mechanism
- [[OAuthGoogleFlow]] — Google OAuth integration
