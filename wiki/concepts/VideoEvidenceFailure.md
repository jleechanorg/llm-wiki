---
title: "VideoEvidenceFailure"
type: concept
tags: [evidence, testing, playwright, overlay, verification]
sources: []
last_updated: 2026-04-11
---

# Video Evidence Failure — Analysis & Patterns

Video evidence capture for UI/agent verification has been attempted extensively across the worldai-claw, worldarchitect.ai, and agent-orchestrator repos. Every attempt has either produced misleading evidence, failed to produce evidence at all, or required significant workarounds.

Related: [[Harness5LayerModel]] — this failure spans L3 (execution: recording infrastructure) and L4 (verification: what the evidence actually proves).

## What Was Tried

### 1. Playwright Video Recording (worldai_claw)

**Infrastructure built:**
- `testing_ui/video_utils.py` — `video_context_kwargs()` returns `record_video_dir` + `record_video_size` for Playwright contexts
- `testing_ui/conftest.py` — injects `TEST_RECORD_VIDEO` env var, sets up per-test video directories
- `testing_ui/test_full_lifecycle_video.py` — 600+ line test that runs 3-turn gameplay lifecycle with video capture
- `testing_ui/test_rpg_engine_video.py` — standalone Phaser game recording with mock data injection
- ~40+ video test files copied across worktrees (worktree_feat, worktree_pr26-rebase, worktree_ios, worktree_blockchain-companion-design, worktree_warplike-terminal-design, etc.)
- `scripts/ralph/CLAUDE-video.md` — explicit instruction for Ralph agent: record video, validate with ffprobe, commit evidence
- `PROMPT.md` — soft validation: "warning is printed (not a hard failure — Playwright flushes late)"

**Why it fails:**

**L3 failure — Overlay canvas blocks game content in recorded video.**
`AmbientBackground.web.tsx` renders a `<canvas>` inside a `position: fixed; z-index: 0` container. This permanently overlays all game content because:
- The canvas is not `pointer-events: none` on its own — but more critically, it covers the full viewport
- Playwright captures what's rendered in the DOM, including the canvas layer
- The `_screenshot_without_overlay()` function in `test_full_lifecycle_video.py` (lines 169–203) was built specifically to workaround this for screenshots: it hides all `<canvas>` elements before screenshot, restores after. But this workaround does NOT apply to video recording — Playwright captures the live DOM state, and the canvas is always visible during recording.

The `zIndex: 0` on the overlay container means the canvas sits behind content by default, but the canvas itself is animated and visually dominant (stars/embers/aurora render at full opacity). In recorded video, the starfield/particle overlay visibly covers game text and chat bubbles.

**L4 failure — ffprobe metadata validation ≠ content validation.**
`test_full_lifecycle_video.py` reports PASS when:
- ffprobe confirms a valid `.webm` file exists
- file has valid duration metadata
- no assertion errors during test execution

Critically documented failure (from `video-frame-review.md`):
> *"The `test_full_lifecycle_video` (101.76s) was reported 'pass' because ffprobe confirmed a valid .webm file. Frame review revealed every GM response was `[CHARACTER CREATION - No Character Built]` — the game never actually worked."*

The test produced 101.76 seconds of misleading video evidence. The video artifact was real and valid — the game was broken.

**L3 failure — Video write timing uncertainty.**
`PROMPT.md` notes that video files may not be written yet by Playwright teardown, so mtime validation uses a 30-second tolerance window. Tests use a soft warning, not a hard failure, when no video is found. This means tests can report PASS with no video evidence.

**L4 failure — Video duration ≠ real interaction time.**
Line 673 in `test_full_lifecycle_video.py` asserts `video_frame_count >= 20` (frames at 1fps). This checks 20+ seconds of video exists — but 20 seconds of a loading spinner or error state satisfies this assertion. The ffprobe duration check (lines 679–688) confirms a valid file with duration, but `ffprobe -v error -show_entries format=duration` tells you how long the file is, not whether the content is meaningful.

### 2. iOS Simulator Recording (simctl)

**What was tried:**
- `scripts/claude_mcp.sh` (lines 941–1040+) — `install_ios_simulator_mcp()` function installs `ios-simulator-mcp` from GitHub, checks for macOS + Xcode, guards with `IOS_SIMULATOR_ENABLED` env var
- `mcp__ios-simulator-mcp__record_video` tool — available in Claude Code when MCP is configured
- `mcp__ios-simulator-mcp__screenshot` tool — screenshot via simctl

**Why it fails:**

- Requires macOS + Xcode CLI tools (conditional guard at line 969–980, but not enforced in automation)
- The ios-simulator-mcp server must be explicitly enabled via `IOS_SIMULATOR_ENABLED=true`
- No test files or worktrees actually use the ios-simulator-mcp for video evidence — the infrastructure was set up but never integrated into CI or test suites
- The `testing_mcp/test_*.py` files use Playwright, not the iOS simulator MCP
- iOS testing in worktree_ios/ uses Playwright for the web frontend, not simctl for the native app

### 3. Chrome Superpowers Screenshot (worldarchitect.ai)

**What was tried:**
- Chrome Superpowers MCP for `screenshot`, `navigate`, `click`, `get_dom` actions
- `worldarchitect-chrome.sh` script with `screenshots` command
- Screenshots saved to session dirs, validated with OCR

**Why it partially works:**
- Screenshots are used successfully in worldarchitect.ai for browser test evidence
- `chrome-localhost3000-usage.md` skill documents proper screenshot patterns
- Screenshot → OCR validation (via `browser-testing-ocr-validation.md`) confirms text visibility
- BUT: screenshots are point-in-time. For flows, multiple screenshots are needed and sequencing is manual. No systematic video recording.

**Why it fails for systematic video evidence:**
- Screenshot-based evidence requires manual orchestration per test
- No automatic video recording from browser interactions
- The `run_browser_tests.sh` script calls Playwright Python tests but only saves screenshots on failure (line 77: `"📸 Screenshots saved to /tmp/worldarchitect_browser_screenshots/"` only on failure)
- No GIF/video generation from screenshot sequences

### 4. ffmpeg (auxiliary, not primary)

**What was tried:**
- `ffprobe` for video duration validation
- `ffmpeg` for frame extraction (1fps sampling)
- `ffmpeg` for `.cast` → `.gif` conversion (asciinema workflow)
- `video-frame-review.md` skill — explicit documentation that Claude Code can `Read` JPEG frames

**Why it fails:**
- ffmpeg is only used for validation, not recording. It doesn't solve the "what to record" problem.
- Frame extraction from Playwright `.webm` files revealed the 101-second failure, but this was discovered post-hoc via manual review, not automated validation.

### 5. asciinema (tmux evidence)

**What was tried:**
- `tmux-video-evidence.md` skill — detailed instructions for recording terminal evidence with asciinema + agg
- Requires `brew install asciinema` and `brew install agg`

**Why it fails:**
- Requires human setup (brew install, manual recording)
- Used for terminal evidence, not browser/UI evidence
- No CI integration or automated invocation
- Terminal evidence alone doesn't prove UI behavior

### 6. Claude-in-Chrome GIF Creator

**What was tried:**
- `mcp__claude-in-chrome__gif_creator` mentioned in `ui-video-evidence.md`
- Described as "preferred for agent sessions"

**Why it fails:**
- Never integrated into any testing infrastructure
- No test files using this MCP tool
- No evidence of successful runs across any repos

## Common Failure Pattern

The failures share a common root cause across [[Harness5LayerModel]]:

**L3 (Execution) failures:**
- Playwright video captures the DOM as rendered — includes the overlay canvas
- iOS simulator MCP has infrastructure but no CI integration
- No automated browser → video pipeline that survives the full test lifecycle

**L4 (Verification) failures:**
- Test passes when ffprobe finds a valid `.webm` file — regardless of content
- Duration metadata used as proxy for meaningful interaction
- No automated frame-level review of video content
- Screenshot-only on failure (`run_browser_tests.sh` line 77) means video is never produced for passing runs

**The meta-failure:**
The `_screenshot_without_overlay()` workaround in `test_full_lifecycle_video.py` is a code smell — it proves the overlay was a known problem during test development, but instead of fixing the root cause (z-index 0 overlay in AmbientBackground.web.tsx), a screenshot-level workaround was added. The video still records the overlay. The workaround is incomplete.

## What Would Need to Be True for Video Evidence to Work

### L3 Prerequisites

1. **Fix the overlay.** Either:
   - Change `AmbientBackground.web.tsx` to use `z-index: -1` or `pointer-events: none` with proper transparent capture, OR
   - Conditionally disable the canvas during headless browser recording, OR
   - Use a Playwright context option that captures beneath overlay layers

2. **iOS simulator MCP integration.** Either:
   - Add `ios-simulator-mcp` to the standard MCP config, enabled via `IOS_SIMULATOR_ENABLED=true` gate, OR
   - Integrate `mcp__ios-simulator-mcp__record_video` into the testing_mcp/ test suite as an alternative to Playwright for native app verification

3. **Automated recording pipeline.** Either:
   - `TEST_RECORD_VIDEO=true` in CI for key e2e tests, not just local runs, OR
   - Record only on failure (current approach is screenshot-only on failure, but video could be added)

### L4 Prerequisites

1. **Frame-level validation, not metadata validation.** Replace ffprobe duration checks with:
   - Automated 1fps frame extraction + OCR/text extraction from key frames (25%, 50%, 75%, final)
   - Assertion that extracted text contains expected scene content (not error states like `[CHARACTER CREATION - No Character Built]`)
   - The `video-frame-review.md` skill provides the methodology — it needs to be automated into the test teardown

2. **Video must be a hard requirement, not a soft warning.** If no video file is produced, the test should fail. Currently `PROMPT.md` explicitly says "warning is printed (not a hard failure)" — this must change.

3. **Final frame validation.** Assert that the final frame contains expected end state text. A 101-second video of failure with valid metadata passes every current check.

## Key Source References

- `project_worldaiclaw/worldai_claw/testing_ui/test_full_lifecycle_video.py` — primary test with overlay workaround (lines 169–203)
- `project_worldaiclaw/worldai_claw/packages/web/src/components/AmbientBackground.web.tsx` — the overlay source (line 345: `position: 'fixed'`, line 351: `zIndex: 0`)
- `project_worldaiclaw/worldai_claw/.claude/skills/video-frame-review.md` — critical post-mortem on 101s misleading video
- `project_worldaiclaw/worldai_claw/testing_ui/video_utils.py` — video context helper
- `project_worldaiclaw/worldai_claw/scripts/ralph/CLAUDE-video.md` — ralph agent instructions
- `worldarchitect.ai/run_browser_tests.sh` — screenshot-on-failure pattern
- `worldarchitect.ai/.claude/skills/chrome-localhost3000-usage.md` — chrome screenshot skill
- `worldarchitect.ai/.claude/skills/browser-testing-ocr-validation.md` — screenshot OCR validation
- `~/.claude/skills/tmux-video-evidence.md` — asciinema workflow
- `~/.claude/skills/ui-video-evidence.md` — UI GIF evidence standards
- `worldarchitect.ai/.cursor/rules/evidence-canonical.mdc` — canonical evidence path references
