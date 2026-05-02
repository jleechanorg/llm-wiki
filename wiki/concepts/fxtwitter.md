---
title: fxtwitter
type: concept
tags: [twitter, scraping, alternative-frontend]
last_updated: 2026-05-01
---

# fxtwitter (fxtwitter.com)

Alternative Twitter frontend that bypasses authentication. Best option for fetching tweet content programmatically.

## Usage
```bash
curl -sL "https://fxtwitter.com/USERNAME/status/TWEET_ID"
```

## Capabilities
- Extract tweet text via `og:description` meta tag
- Extract playable MP4 URL from `twitter:player:stream`
- No API key required

## Related
- [[nitter]] — fallback RSS-style alternative
- [[vxtwitter]] — another Twitter alternative
- [[Fetch X Tweet]] — detailed usage guide