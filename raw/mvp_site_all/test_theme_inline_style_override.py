#!/usr/bin/env python3
"""TDD test: theme CSS overrides must not be blocked by inline styles in app.js.

HIGH SEVERITY: fantasy.css defines [data-theme='fantasy'] .dice-rolls and .resources
overrides, but inline style="background-color: ..." in app.js HTML templates
always beat selector-based CSS. This makes the fantasy theme overrides dead code.

Regression guard: these classes must NOT carry inline background-color.
"""

import re
import unittest
from pathlib import Path

APP_JS = Path(__file__).parent.parent.parent / "mvp_site" / "frontend_v1" / "app.js"

# Elements with CSS class-based theme overrides in fantasy.css.
# These must NOT have inline background-color (which would block the theme override).
THEMED_CLASSES = ["resources", "dice-rolls", "system-warnings", "planning-block"]


def _load_app_js() -> str:
    return APP_JS.read_text(encoding="utf-8")


class TestNoInlineBackgroundColorOnThemedElements(unittest.TestCase):
    """Inline background-color on themed classes blocks fantasy.css overrides."""

    def setUp(self):
        self.content = _load_app_js()

    def test_resources_class_has_no_inline_background_color(self):
        """'.resources' elements must not carry inline background-color."""
        # Match: class="resources" ... style="... background-color: ...
        # or: style="...background-color..." ... class="resources"
        hits = re.findall(
            r'class=["\']resources["\'][^>]*style=["\'][^"\']*background-color',
            self.content,
        ) + re.findall(
            r'style=["\'][^"\']*background-color[^"\']*["\'][^>]*class=["\']resources["\']',
            self.content,
        )
        self.assertEqual(
            hits,
            [],
            f".resources has inline background-color that blocks fantasy.css override: {hits}",
        )

    def test_dice_rolls_class_has_no_inline_background_color(self):
        """'.dice-rolls' elements must not carry inline background-color."""
        # Also check .style.cssText assignments on elements with class dice-rolls
        # Regex: 'dice-rolls' ... style.cssText ... background-color (within ~5 lines)
        hits = re.findall(
            r'class=["\']dice-rolls["\'][^>]*style=["\'][^"\']*background-color',
            self.content,
        ) + re.findall(
            r'style=["\'][^"\']*background-color[^"\']*["\'][^>]*class=["\']dice-rolls["\']',
            self.content,
        )
        self.assertEqual(
            hits,
            [],
            f".dice-rolls has inline background-color that blocks fantasy.css override: {hits}",
        )

    def test_dice_rolls_style_css_text_has_no_background_color(self):
        """rollDiv.style.cssText for '.dice-rolls' must not include background-color."""
        # Find className = 'dice-rolls' then style.cssText = '...' within 5 lines
        matches = re.findall(
            r"className\s*=\s*['\"]dice-rolls['\"].*?style\.cssText\s*=\s*['\"]([^'\"]+)['\"]",
            self.content,
            re.DOTALL,
        )
        for m in matches:
            self.assertNotIn(
                "background-color",
                m,
                f"dice-rolls style.cssText must not set background-color: {m!r}",
            )

    def test_system_warnings_class_has_no_inline_background_color(self):
        """'.system-warnings' elements must not carry inline background-color."""
        hits = re.findall(
            r'class=["\']system-warnings["\'][^>]*style=["\'][^"\']*background-color',
            self.content,
        ) + re.findall(
            r'style=["\'][^"\']*background-color[^"\']*["\'][^>]*class=["\']system-warnings["\']',
            self.content,
        )
        self.assertEqual(
            hits,
            [],
            f".system-warnings has inline background-color that blocks fantasy.css override: {hits}",
        )


if __name__ == "__main__":
    unittest.main()
