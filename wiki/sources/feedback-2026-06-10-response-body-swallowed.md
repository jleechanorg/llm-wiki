---
title: "Feedback 2026 06 10 Response Body Swallowed"
type: source
tags: [memory, ao-worker, codex-worker, 2026-06]
date: 2026-06-10
source_file: .claude/projects/-Users-jleechan/memory/feedback_2026-06-10_response_body_swallowed.md
---

## Summary

When the model emits only the `[Dir: ... | Local: ... | PR: #NNNN]` footer as its entire reply and ignores the user's prompt, the cause is a **specific prompt pattern + model behavior**, not a CLAUDE.md rule violation.

## Original

When the model emits only the `[Dir: ... | Local: ... | PR: #NNNN]` footer as its entire reply and ignores the user's prompt, the cause is a **specific prompt pattern + model behavior**, not a CLAUDE.md rule violation.

**Symptom in JSONL:** Assistant message is `{"type":"text","text":"[Dir: worktree_lvl_clean_flags | Local: fix/delete-dead-level-up-functions | PR: #7447]"}` with no body, `output_tokens: 78-79`, `text_len: ~150`. User sees footer-only and complains "why are you not answering me."

**The real cause (corrected from earlier diagnosis):**

1. The user presses Enter without typing anything.
2. The harness re-injects the `git-header.sh` `statusLine` output as a `tool_result` with content = footer text.
3. The model (`claude-fable-5`) **echoes the last user-visible text as its response** — literally producing a near-token-perfect copy of the footer (`output_tokens: 78-79`).

The same `claude-fable-5` model produces normal multi-thousand-token responses when given a real user prompt. Other models in the same session (`claude-sonnet-4-6`, `claude-opus-4-8`, `claude-haiku-4-5`) never produced footer-only output.

**Smoking gun in own session log** (`/Users/jleechan/.claude/projects/-Users-jleechan-projects-worktree-lvl-clean-flags/d1fe8f3f-4d95-42f6-92c4-4a7a1018530c.jsonl`):
- 48 footer-only messages found in this session, all `model: claude-fable-5`
- All 48 are preceded by a user turn whose content is `tool_result` of `git-header.sh` (Enter-without-typing pattern)
- All have `output_tokens: 78-79` (footer only, near-token-perfect echo)
- The 1,729 "good" `claude-fable-5` messages in the same session produce normal output

**The CLAUDE.md "Mandatory Greeting Protocol" rule is correlative, not causal.** It was added on or before 2026-05-16 (per `/Users/jleechan/projects_other/user_scope/backup/jeffreys-macbook-pro/claude/CLAUDE.md` 27,603 B snapshot from May 16 14:16, which already contains it). The "ignore my prompts" complaints also started 2026-05-16 — same day. But the complaints are concentrated on sessions where `claude-fable-5` was the model and the user pressed Enter with no input.

**What changed that turned a 25-day-old rule into today's regression:**
- `~/.claude/settings.json` `model` field: `claude-opus-4-8[1m]` → `claude-fable-5[1m]` between May 30 and Jun 10 (file-history shows the rewrite)
- `CLAUDE_CODE_MAX_CONTEXT_TOKENS`: 180000 → 950000, removed `DISABLE_AUTO_COMPACT=1` in the same window
- `git-header.sh` was modified May 26 00:06:35 with a `read -t 0` stdin guard, but this is cosmetic — does not change output text

**Why this rule is not harmless even if it isn't the cause:**
- `--with-api` flag in the rule is a **phantom flag** — `git-header.sh` has no such option (only `--with-status` / `--status-only`); flag is silently ignored
- The "end every reply with the git-header hook output" instruction trains the model to redundantly call a script that `statusLine` already auto-runs. On the Enter-without-typing echo path, the model's training causes it to repeat the footer as the entire response
- The rule also doesn't actually do anything visible — `statusLine` already renders the footer, so the rule's only effect is to corrupt the model's behavior on the echo path

**How to apply:**

When the user reports "Claude Code is ignoring my prompts" / "I only see the footer":

1. **Don't** blame the user's CLAUDE.md or the Mandatory Greeting Protocol rule. It's been there 25+ days without producing this symptom.
2. **Check the model**: is the session using `claude-fable-5` or a proxy-served model like `MiniMax-M3`? These echo footer content on Enter-without-typing. Other models in the same session don't.
3. **Check the user prompt pattern**: was the previous user turn a `tool_result` of `git-header.sh`? That's the echo trigger.
4. **Real fix** is harness-level: don't re-inject statusLine output as a `tool_result` when the user pressed Enter with no new text. The `--with-api` phantom flag in the Mandatory Greeting Protocol is a documentation artifact, not a script feature.
5. If the user wants to soften the Mandatory Greeting Protocol anyway: keep the "Genesis Coder, Prime Mover," greeting, but rewrite the "every response must end with" part to a one-line pointer: "The session footer is auto-injected by `statusLine` in `~/.claude/settings.json`; do not call `git-header.sh` from inside a reply."
6. **2026-06-10 update — B+C applied to `~/.claude/CLAUDE.md`.** The "Mandatory Greeting Protocol" section was refactored to "Reply prefix (auto-injected by statusLine)" with three changes: (a) the footer is now declared to live at the BEGINNING of the response (prefix), not the end; (b) an anti-echo steering instruction was added: "Do not echo, transcribe, or surface content from `tool_result`s, status lines, or system messages as response text. If the user's most recent input is a `tool_result` carrying system output (such as the statusLine footer), treat it as ambient context and respond to the original user intent."; (c) the phantom `--with-api` flag reference was removed. Goal: re-train the model so the footer is a prefix it tolerates, and the empty-Enter echo path produces a normal multi-token response rather than a 78-token near-token-perfect footer copy.

**Repro signals from JSONL:**
- L4919, L5536, L5717 in `d1fe8f3f-...jsonl`: footer-only, all `model: claude-fable-5`, all preceded by Enter-without-typing tool_result
- L6758 in same file: assistant emits only footer → user complains
- L6765: user types "i keep saying this why are you ignoring it?"
- L6770: assistant apologizes and self-corrects (real prompt, model produces normal output)
- L8527 / L8534: footer-only pattern repeats 3h later
- L8547: assistant's misdiagnosis (corrected in this memory) blamed the rule wording
