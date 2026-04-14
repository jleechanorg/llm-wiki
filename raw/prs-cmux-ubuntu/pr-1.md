# PR #1: feat: GTK4 Linux port phases 1-7 complete — split panes, notifications, session restore

**Repo:** jleechanorg/cmux_ubuntu
**Merged:** 2026-03-09
**Author:** jleechan2015
**Stats:** +10284/-0 in 54 files

## Summary
Complete GTK4 Linux port of cmux through all 7 phases, with real UI evidence (Docker + Xvfb + scrot screenshots) reviewed by both supervisor and cmux_coder before each phase gate.

### Phase Evidence (all screenshots at 1280×800 RGB, Ubuntu 24.04 + Xvfb)

| Phase | Feature | Evidence | Tests |
|-------|---------|---------|-------|
| 1 | TDD setup + cmux-core data model | Baseline | 94 passing |
| 2 | Session persistence (XDG atomic save/load) | macOS PR screenshot | 94 passing |
| 3 | GTK4 sideb

## Test Plan
- [x] `cargo test -p cmux-core` → 101 passed, 0 failed
- [x] `docker build -t cmux-gtk .` → clean build on Ubuntu 24.04
- [x] Xvfb + scrot screenshots for phases 3, 4, 5, 6, 7 — all reviewed
- [x] Split pane UI: two VTE terminals visible side-by-side
- [x] Notification dot: red CSS dot on Tab 2
- [x] Session save/load wired end-to-end

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->

## Raw Body
## Summary

Complete GTK4 Linux port of cmux through all 7 phases, with real UI evidence (Docker + Xvfb + scrot screenshots) reviewed by both supervisor and cmux_coder before each phase gate.

### Phase Evidence (all screenshots at 1280×800 RGB, Ubuntu 24.04 + Xvfb)

| Phase | Feature | Evidence | Tests |
|-------|---------|---------|-------|
| 1 | TDD setup + cmux-core data model | Baseline | 94 passing |
| 2 | Session persistence (XDG atomic save/load) | macOS PR screenshot | 94 passing |
| 3 | GTK4 sidebar — ListBox with workspace tabs | 1280×800 GTK4 window, sidebar + tab bar + placeholder terminal area | 94 passing |
| 4 | VTE terminal — real `vte4::Terminal` widget | 1280×800: "cmux terminal ready / $ " in live VTE | 94 passing |
| 5 | Split panes — `gtk4::Paned` mirroring `SplitNode` tree | **Two VTE terminals side-by-side** (pane 1 / pane 2) | 94 passing |
| 6 | Notification rings — CSS red dot on tabs | **Red dot visible on Tab 2 in sidebar** | 99 passing |
| 7 | Session restore — save on close, load on startup | Full UI + session wired, 2 new integration tests | **101 passing** |

### Phase 3 — GTK4 Sidebar
- Workspaces header + Tab 1 (blue active) in ListBox sidebar
- Tab bar with Tab 1 button
- Terminal area placeholder with "Split panes will appear here"

### Phase 4 — VTE Terminal
- Same layout with real `vte4::Terminal` widget
- Shows `cmux terminal ready` and `$ ` prompt fed via `terminal.feed()`

### Phase 5 — Split Panes
- `build_split_widget()` recursively maps `SplitNode` → `gtk4::Paned`
- **Two live VTE terminals side-by-side**: "pane 1 / $ " and "pane 2 / $ "
- Horizontal `Paned` with `vexpand`/`hexpand` on each leaf

### Phase 6 — Notification Rings
- CSS provider: `#notification-dot { background-color: #ff0000; border-radius: 4px; }`
- Applied via `style_context_add_provider_for_display`
- **Red dot clearly visible** to left of "Tab 2" in sidebar
- 5 new notification state unit tests

### Phase 7 — Session Restore
- `connect_close_request` sa
