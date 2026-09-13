---
name: aside-repl-session-sandbox-and-tab-lifetime
description: "aside repl rejects file paths outside its per-invocation session dir, and tabs close when the invocation exits — killing in-flight LLM web chats"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b92d14f8-3b7c-4f7e-a9e1-898592165bbf
  modified: 2026-09-13T02:42:10.772Z
---

Two `/wa` lanes (2026-09-01, PR #9493 and #8988 reviews) independently rediscovered the same two `aside repl` transport traps:

1. **Session-dir sandbox**: any file path outside the invocation's own ephemeral session directory (`~/.aside/u/0/sessions/<random>`) fails with "escapes the session directory." Attachment/packet files must be written via the exposed `fs` global *from inside the same script* that opens the tab — pre-staged host paths cannot be copied in.
2. **Tab lifetime = invocation lifetime**: the browser tab closes when the `aside repl` process exits (~120s cap), and an in-flight web-chat generation vanishes from the vendor's history when that happens (confirmed on both Gemini and ChatGPT). The entire attach→prompt→submit→poll-to-completion sequence must run in ONE invocation; slow "thinking" models (ChatGPT extended mode) cannot finish in budget — select instant/fast modes up front.

**Why:** each lane burned significant time rediscovering this; the second lane succeeded 3-of-3 only after applying both workarounds.

**How to apply:** when briefing any `/wa` or [[aside-browser-default]] browser-automation task, include both constraints in the prompt: single-invocation end-to-end scripts, `fs`-global file staging, instant-mode model selection. If a review needs >120s generation, expect partial coverage and disclose it rather than retrying blind.

## 2026-09-12 addendum (PR #9835/#9846 `/wa` review, `aside` CLI not MCP tool)

Using the `aside` CLI (`aside --account u0 repl "..."`) instead of the `mcp__aside-mcp__repl` tool (which was pinned to a signed-out account, `aside account use u0` does not affect it):

- **Correction to point 1 above**: pre-staged host paths DO work, contradicting the blanket claim — but only under `~/.aside/uploads/<subdir>/`, not arbitrary paths. Plain `cp file ~/.aside/uploads/myrun/` then `setInputFiles(["myrun/file.txt"])` (relative to that root) succeeded. `~/.aside/u/0/sessions/<random>` may be a separate, stricter sandbox for a different code path.
- **`attachBrowserTab(targetId)` times out ~33s ("CDP command timeout: Page.enable") for tabs opened in a *prior* `aside repl` invocation**, essentially always, in this environment. `openTab(url)` fresh in the *same* invocation is reliable; treat cross-invocation tab reuse as broken, not flaky.
- **Vendor composer behavior diverges sharply on large pasted/injected text**, confirmed same session, same packets:
  - Gemini: `keyboard.press("Meta+V")` after copying to the macOS clipboard (`pbcopy`) reliably lands 50-70KB of text in the composer and produces a real, complete response (`page.evaluate(() => document.querySelectorAll('[data-message-author-role]')...)`  — NOT the accessibility `snapshot()` tree, which truncates long text nodes to a short summary — gives the true full response text).
  - ChatGPT (`#prompt-textarea`): clipboard paste silently no-ops (composer length stays ~= prompt-only length, no error). `page.evaluate(el => el.innerText = text; el.dispatchEvent(new InputEvent('input',...)))` DOM injection *does* land the text (readback confirms full length) and does NOT disable the send button, but clicking send afterward produced no navigation and no assistant response — likely a client-side length/validation limit on a single ~60KB message, still unconfirmed.
  - Perplexity (`[role="textbox"]`): same clipboard-paste no-op; the DOM-injection technique failed outright (`inserted length: 1`).
  - `keyboard.type()` of the full packet text (not paste/injection) is not a safe fallback: typing ~58K chars via synthesized keystrokes crashed the Aside daemon entirely (`fetch failed: other side closed`), requiring `open -a Aside` to recover.
- **Net effect**: budget one working seat (Gemini) as the realistic default for large-packet `/wa` reviews in this environment; treat ChatGPT/Perplexity as a bonus if their much smaller prompts (no huge attachment) work, and disclose the coverage gap rather than burning more retries once one DOM-injection + one paste attempt both fail for a given vendor.
