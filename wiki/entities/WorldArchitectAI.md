---
title: "WorldArchitect.AI"
type: entity
tags: [platform, ai-agent, worldbuilding]
sources: [waitlist-gating-account-switching-flow]
last_updated: 2026-06-20
---

## Overview

WorldArchitect.AI is an AI-powered collaborative worldbuilding platform that enables users to create and share interactive fictional worlds with AI-generated narratives and characters.

## Key Systems

- **Waitlist Gating** — restricts access to authorized users when `WAITLIST_MODE_ENABLED` is true
- **Firebase Auth** — primary authentication backend
- **SPA Routing** — client-side route handling with auth state listeners

## References
- [[WaitlistGatingMode]] — access control mechanism
- [[FirebaseAuth]] — authentication system
- [[PR7705]] — waitlist/auth fix PR
