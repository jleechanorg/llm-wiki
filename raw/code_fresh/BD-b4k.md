# BD-b4k

## GOAL
Add a step 08 screenshot to `test_llm_wizard_flow_e2e.py` to close the visual coverage gap between wizard steps 07 (step 3 complete) and 09 (game view loaded).

## MODIFICATION
- Identify where step 08 should be captured in `testing_ui/test_llm_wizard_flow_e2e.py` — likely the "Begin Adventure" button click or the loading/transitioning screen between wizard completion and game view.
- Add a `take_screenshot("08_wizard_launch")` (or equivalent) at that point.
- Ensure the VTT cue is also emitted so the video recording shows the transition frame.

## NECESSITY
The LLM wizard flow VTT jumps from cue 13 (`07_wizard_step4_preview`) to cue 16 (`09_game_view`) with cues 14–15 covering the launch click and wait. The absence of screenshot 08 leaves the campaign-creation handoff visually unverified — a reviewer cannot confirm the "Begin Adventure" button was actually clicked and the campaign ID was generated before the game view appeared.

## INTEGRATION PROOF
- Affected test: `testing_ui/test_llm_wizard_flow_e2e.py`
- VTT evidence: `run_1773554578: llm_wizard_flow_e2e/video/*.vtt` (cues 14-15 show the gap)
