---
name: dk2d-chrono-operational-lessons
description: "Generalizable lessons from the CHRONO mission — silently-ignored CLI flags, janitor mid-run destruction, provider-window scheduling, gate-null vs gate-fail, stop-hook vs time-box dispute protocol"
metadata: 
  node_type: memory
  type: feedback
  bead: wc-quvu
  originSessionId: 027a6a99-2f6b-4631-90e4-7c1dfb585883
---

## CHRONO mission operational lessons (2026-07-14) — the generalizable failure classes

Companion to `project_2026-07-14_dk2d_chrono_lpc_unification.md` (mission record). These five lessons apply beyond DK2D.

### 1. A CLI flag that "worked" may be silently ignored — verify consumption, not acceptance

`run_dk2d_evidence.py --out <dir>` ran without error for THREE runs while writing evidence to the /tmp default: argv was only scanned for `--partial`, so any other flag was accepted and ignored. The tell was in the log all along: `EVIDENCE: /tmp/...` vs my `out=` echo. **Rule: after passing a flag, verify the tool's own output reflects it (header line, output path, behavior delta). "Ran without erroring" proves nothing — most hand-rolled arg scanners ignore unknown flags.** Same class as the CLAUDE.md negative-claims rule (CLIs silently accept unknown flags).
**FIX**: commit on dragonknight-2d-clean 2026-07-14 — `--out` wired as DK_EVID alias + unknown flags now FATAL (testing_ui/run_dk2d_evidence.py `_cli_out_dir()`).

### 2. The /tmp janitor destroys evidence MID-RUN, not just between runs

Known rule was "run evidence OUTSIDE /tmp (janitor deletes long-run artifacts)". New sharper fact: the janitor deleted `static_frames/f0143.png` WHILE the harness was reading the sequence (gate 4.1 false-FAIL with `static_ok: 3` — one playthrough's report missing, error `[Errno 2] No such file` mid-imagehash-pass). A run that both writes and reads /tmp within ~15 minutes is still vulnerable. **Rule: evidence pipelines must write primary output to a janitor-safe location from the first byte (DK_EVID / --out to ~/dk2d_evidence), not copy-after.**

### 3. Provider health is a scheduling axis; distinguish gate-null from gate-fail

MiniMax long-generation (2-6k char) streams hang >120s overnight PT while short turns stay at 2.05s first-token — run trend 15/15 → 13 → 13 → 14 → 10 (22:59 PT → 00:51 PT), then morning 14 → 14 → 15 (15:30Z+). Schedule real-LLM evidence runs morning/midday PT. Also: a STRICT harness fails runs on `pass: null` gates — the 15:30Z run "failed" only because the GM sampled zero dice turns (5.1 unmeasurable, not broken). **Read the manifest's measured detail before classifying a failed run: null-sampled ≠ regression.**

### 4. Adversarial pipeline art defects: generators fake alpha; quantizers resurrect keyed colors

Grok bakes "translucency" as RGB blends WITH its own magenta background (sampled smoke at (187,80,186)) — no fixed-radius chroma tolerance can separate it. And PIL median-cut quantization AFTER keying remapped edge pixels back onto magenta palette entries. Fix pattern: hue-FAMILY channel test (G clearly below both R and B, R≈B) applied at every pipeline stage, key BEFORE quantize, and re-verify the FINAL shipped bytes at zoom (a numeric pre-quantize check passed while shipped pixels were still magenta).

### 5. Stop-hook vs time-box disputes: record both readings, act under your own authority, hand the user a kill switch

When the session Stop-hook goal (harness-enforced, "treat the condition as your directive") collided with the expired 12h autonomy box, the sidekick refused continuation (only a fresh user message authorizes) while the team-lead continued narrow evidence-capture under hook-as-user-feedback. Both were defensible. The protocol that worked: never route the disputed action through the refusing agent (permission laundering), own it explicitly from the seat that has the authority claim, record BOTH positions verbatim-in-substance in the mission file (ironclad r12), and give the user a concrete kill switch + adjudication request. Outcome resolved it (15/15 seal) without either agent capitulating.

**Verification**: all five lessons carry receipts in `roadmap/dragonknight-2d-chrono-ironclad-2026-07-13.md` r1-r15 (pushed) and the bundles under `~/dk2d_evidence/`.
