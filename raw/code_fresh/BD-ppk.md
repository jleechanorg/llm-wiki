# BD-ppk

## GOAL
Fix the misleading screenshot name `wizard_08_guided_mode_hidden_fields.png` in `test_wizard_character_setting.py` so the screenshot accurately reflects what is being captured, and add a clarifying comment in the test source.

## MODIFICATION
- Rename the `take_screenshot` call at `testing_ui/core_tests/test_wizard_character_setting.py:248` from `"wizard_08_guided_mode_hidden_fields"` to `"wizard_08_guided_mode_dom_check"` (or similar) to reflect that this is a DOM-state assertion, not a visual hidden-state confirmation.
- Add a code comment before the screenshot explaining: the DOM eval at line 235 already captured the hidden/visible state; the screenshot shows the page at time-of-assertion, not after a user action that triggers hiding.
- Optionally add a second screenshot taken after programmatically clicking the Guided Wizard radio to produce a genuine "fields hidden" visual.

## NECESSITY
The current screenshot name implies it proves fields are hidden, but the image shows them visible. This misleads future reviewers (as flagged in the evidence review) and weakens the test's documentary value as regression evidence.

## INTEGRATION PROOF
- Affected file: `testing_ui/core_tests/test_wizard_character_setting.py:248`
- Evidence screenshot: `testing_ui/core_tests/test_wizard_character_setting.py:248` (screenshot name: `wizard_08_guided_mode_dom_check`)
