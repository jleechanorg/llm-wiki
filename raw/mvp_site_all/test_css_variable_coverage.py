"""Unit tests: every CSS var() usage must have a corresponding definition.

Catches the class of bug where enhanced-components.css (or any other file)
references --glass-background, --shadow-elevated, etc. but no CSS file
actually defines them — causing `background: var(--undefined)` to resolve
to `transparent` and silently breaking dropdown menus, cards, etc.
"""

from __future__ import annotations

import re
from pathlib import Path

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend_v1"

# Pattern to extract variable USAGES: var(--foo) or var(--foo, fallback)
VAR_USAGE_RE = re.compile(r"var\(\s*(--[\w-]+)")

# Pattern to extract variable DEFINITIONS: --foo: value
VAR_DEFINITION_RE = re.compile(r"(--[\w-]+)\s*:")


def _collect_css_files() -> list[Path]:
    """Collect all CSS files in the frontend directory tree."""
    return sorted(FRONTEND_DIR.rglob("*.css"))


def _extract_var_usages(css_files: list[Path]) -> dict[str, list[str]]:
    """Return {variable_name: [file:line, ...]} for every var() usage."""
    usages: dict[str, list[str]] = {}
    for path in css_files:
        text = path.read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines(), 1):
            for match in VAR_USAGE_RE.finditer(line):
                var_name = match.group(1)
                usages.setdefault(var_name, []).append(f"{path.name}:{i}")
    return usages


def _extract_var_definitions(css_files: list[Path]) -> set[str]:
    """Return set of all CSS variable names that are defined somewhere."""
    definitions: set[str] = set()
    for path in css_files:
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            for match in VAR_DEFINITION_RE.finditer(line):
                definitions.add(match.group(1))
    return definitions


# Bootstrap defines --bs-* vars at runtime via its own CSS; they won't appear
# in our source .css files but are always available when Bootstrap loads.
CSS_BUILTINS = frozenset(
    var for var in [] if False  # placeholder — built dynamically below
)

# Prefix-based allowlist: any var starting with these prefixes is external
_EXTERNAL_PREFIXES = ("--bs-",)


def test_all_css_variables_are_defined():
    """Every var(--name) in any CSS file must have a --name: definition somewhere."""
    css_files = _collect_css_files()
    assert css_files, f"No CSS files found under {FRONTEND_DIR}"

    usages = _extract_var_usages(css_files)
    definitions = _extract_var_definitions(css_files)

    undefined = {
        var: locations
        for var, locations in sorted(usages.items())
        if var not in definitions
        and var not in CSS_BUILTINS
        and not any(var.startswith(p) for p in _EXTERNAL_PREFIXES)
    }

    if undefined:
        lines = ["Undefined CSS variables found (used but never defined):"]
        for var, locations in undefined.items():
            lines.append(f"  {var}  (used in: {', '.join(locations[:5])})")
        raise AssertionError("\n".join(lines))


def test_enhanced_components_variables_have_definitions():
    """Specifically guard enhanced-components.css — the usual offender."""
    ec_path = FRONTEND_DIR / "styles" / "enhanced-components.css"
    if not ec_path.exists():
        return  # File removed, test is N/A

    css_files = _collect_css_files()
    definitions = _extract_var_definitions(css_files)

    text = ec_path.read_text(encoding="utf-8")
    ec_usages: dict[str, list[int]] = {}
    for i, line in enumerate(text.splitlines(), 1):
        for match in VAR_USAGE_RE.finditer(line):
            ec_usages.setdefault(match.group(1), []).append(i)

    undefined = {
        var: line_nums
        for var, line_nums in sorted(ec_usages.items())
        if var not in definitions
        and var not in CSS_BUILTINS
        and not any(var.startswith(p) for p in _EXTERNAL_PREFIXES)
    }

    if undefined:
        lines = [
            "enhanced-components.css uses variables with no definition in any CSS file:"
        ]
        for var, line_nums in undefined.items():
            lines.append(f"  {var}  (lines: {line_nums})")
        raise AssertionError("\n".join(lines))


def test_theme_dropdown_menu_has_visible_background():
    """The theme dropdown must have a non-transparent background in both themes.

    Regression guard: component-enhancer adds .dropdown-enhanced to the theme
    dropdown.  If --glass-background is undefined, the dropdown becomes
    transparent and items are invisible.
    """
    globals_path = FRONTEND_DIR / "styles" / "globals.css"
    assert globals_path.exists(), "globals.css missing"

    text = globals_path.read_text(encoding="utf-8")

    # Must define --glass-background in :root
    assert "--glass-background:" in text, (
        "--glass-background not defined in globals.css — "
        "theme dropdown will be transparent"
    )

    # Must define --glass-background in [data-theme='fantasy']
    # Split on the fantasy block and check it contains the definition
    fantasy_match = re.search(
        r"\[data-theme=['\"]fantasy['\"]\]\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}",
        text,
        re.DOTALL,
    )
    assert fantasy_match, "Fantasy theme block not found in globals.css"
    assert "--glass-background:" in fantasy_match.group(1), (
        "--glass-background not defined in fantasy theme block — "
        "dropdown will be invisible in fantasy mode"
    )


def test_no_high_zindex_on_view_containers():
    """View containers must NOT have z-index that creates stacking contexts above the navbar.

    Regression guard: if #dashboard-view.active-view (or siblings) get
    position:relative + z-index >= 1000, the navbar dropdown menu becomes
    unclickable because the view's stacking context paints over it.
    """
    style_path = FRONTEND_DIR / "style.css"
    assert style_path.exists(), "style.css missing"

    text = style_path.read_text(encoding="utf-8")

    # Find all rule blocks that target view containers with .active-view
    view_pattern = re.compile(
        r"(#\w+-view\.active-view[^{]*\{[^}]+\})", re.DOTALL
    )
    zindex_pattern = re.compile(r"z-index\s*:\s*(\d+)")

    for match in view_pattern.finditer(text):
        block = match.group(1)
        zindex_match = zindex_pattern.search(block)
        if zindex_match:
            value = int(zindex_match.group(1))
            assert value < 1000, (
                f"View container has z-index: {value} which will cover the "
                f"navbar dropdown. Remove z-index from .active-view rules.\n"
                f"Block: {block.strip()[:200]}"
            )


def test_navbar_has_zindex_above_content():
    """Navbar must have z-index to paint above transform-created stacking contexts.

    Regression guard: animation-helpers.js sets transform:translateY(0) on
    active views during fade-in. Any non-none CSS transform creates a stacking
    context. Without an explicit z-index on the navbar, dashboard content
    (later in DOM order) paints over the navbar dropdown.
    """
    style_path = FRONTEND_DIR / "style.css"
    assert style_path.exists(), "style.css missing"

    text = style_path.read_text(encoding="utf-8")

    # The navbar must have a z-index rule
    navbar_zindex = re.search(
        r"\.navbar\s*\{[^}]*z-index\s*:\s*(\d+)", text, re.DOTALL
    )
    assert navbar_zindex, (
        "Navbar has no z-index in style.css — dropdown will be covered "
        "by view containers with CSS transforms"
    )
    value = int(navbar_zindex.group(1))
    assert value >= 1000, (
        f"Navbar z-index ({value}) is too low — must be >= 1000 to stay "
        f"above content with transform-created stacking contexts"
    )


if __name__ == "__main__":
    import sys

    failures = 0
    for test_fn in [
        test_all_css_variables_are_defined,
        test_enhanced_components_variables_have_definitions,
        test_theme_dropdown_menu_has_visible_background,
        test_no_high_zindex_on_view_containers,
        test_navbar_has_zindex_above_content,
    ]:
        try:
            test_fn()
            print(f"  PASS  {test_fn.__name__}")
        except AssertionError as e:
            print(f"  FAIL  {test_fn.__name__}:\n{e}")
            failures += 1

    sys.exit(1 if failures else 0)
