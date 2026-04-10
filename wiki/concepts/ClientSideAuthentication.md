---
title: "Client-Side Authentication"
type: concept
tags: [authentication, client-side, firebase, javascript, security]
sources: []
last_updated: 2026-04-08
---

## Description
Authentication handled in the browser using JavaScript SDKs rather than server-side session management.


## WorldArchitect.AI Implementation
Firebase Auth SDK loaded in browser:
```html
<script src="https://www.gstatic.com/firebasejs/9.6.1/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.6.1/firebase-auth-compat.js"></script>
```

## Security Considerations
- Tokens stored in browser storage
- Session handled via Firebase auth state
- Server validates Firebase ID tokens
