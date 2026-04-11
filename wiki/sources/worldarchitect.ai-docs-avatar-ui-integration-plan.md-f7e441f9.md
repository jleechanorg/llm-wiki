---
title: "Engineering Plan: User Avatar UI Integration"
type: source
tags: [worldarchitect-ai, engineering-plan, ui-integration, avatar, firebase, frontend]
sources: []
date: 2026-01-15
source_file: raw/worldarchitect.ai-docs-avatar-ui_integration_plan.md
last_updated: 2026-04-07
---

## Summary
Engineering plan for integrating user avatars into the campaign play UI. Allows users to upload custom avatars via a button in the top-right header area during gameplay, display their avatar in the bottom-left corner during campaign gameplay, and optionally upload an avatar during campaign creation as part of the 3-step creation wizard.

## Key Claims
- **Avatar Upload During Gameplay**: Users can upload via button in top-right header area (left of existing Download button)
- **Avatar Display**: Shown in bottom-left corner during campaign gameplay
- **Avatar in Campaign Creation**: Optional upload in Step 1 of wizard (after character name field)
- **Existing Component**: Uses Radix UI `@radix-ui/react-avatar` component already present in codebase
- **Backend Storage**: Avatar URL stored in Firestore at `users/{user_id}/settings` alongside existing settings (theme, debug_mode, etc.)
- **Image Storage**: Firebase Storage bucket configured via `FIREBASE_STORAGE_BUCKET` env var
- **3-Step Wizard**: Step 1 (Campaign Basics), Step 2 (AI Personalities), Step 3 (Review & Launch)

## Key Quotes
> "This document outlines the engineering plan for integrating user avatars into the campaign play UI." — Executive Summary

> "Avatar upload is optional (not blocking campaign creation)" — Design Specifications

## Connections
- [[WorldArchitect.AI]] — source project
- [[React V2 Current Status]] — related frontend work
- [[Firebase Setup]] — related backend doc for storage configuration
- [[API Reference]] — related backend API documentation

## Contradictions
- None identified yet
