---
title: "Headless Mode"
type: concept
tags: [browser, automation, testing]
sources: []
last_updated: 2026-04-08
---

## Definition
Browser execution mode where the browser runs without a visible UI window, enabling automated testing and screenshot capture in background processes.

## Key Features
- No visible browser window
- Faster execution than headed mode
- Ideal for CI/CD pipelines
- Supported by Chrome, Firefox, Edge

## Chrome Options for Headless
```python
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
```

## Related Concepts
- [[Selenium]]
- [[Browser Automation]]
- [[Screenshot Capture]]
