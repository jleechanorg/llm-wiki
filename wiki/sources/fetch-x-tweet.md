---
title: "Fetch X (Twitter) Tweet"
type: source
tags: [twitter, scraping, alternative-frontend, x-com]
date: 2026-05-01
source_file: raw/fetch-x-tweet.md
---

## Summary
Fetch tweets that require authentication by using alternative Twitter frontends. fxtwitter.com is the primary option; nitter.net and vxtwitter.com are fallbacks. Extract tweet text, media URLs, and video streams from the HTML response.

## Key Claims
- Direct curl to x.com/twitter.com returns 401/402 auth errors
- fxtwitter.com is the best option — embeds video directly in OG tags
- Extract tweet text via `og:description` meta tag
- Extract playable MP4 URL from `twitter:player:stream` meta tag
- nitter.net may be rate-limited or down
- Adding `-H "User-Agent: Mozilla/5.0"` header may help

## Key Quotes
> "fxtwitter embeds video directly in OG tags - can extract playable MP4 URL" — fetch-x-tweet

## Connections
- [[fxtwitter]] — primary Twitter alternative frontend
- [[nitter]] — fallback Twitter alternative frontend (RSS-style)
- [[vxtwitter]] — alternative Twitter alternative frontend
- [[WebScraping]] — broader web scraping concepts