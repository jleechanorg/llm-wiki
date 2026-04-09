import unittest
import math

from mvp_site.utils import normalize_status_code, add_safe


class TestNormalizeStatusCode(unittest.TestCase):
    """Tests for normalize_status_code utility function."""

    def test_valid_int_passthrough(self):
        """Valid integer codes are returned unchanged."""
        assert normalize_status_code(200) == 200
        assert normalize_status_code(404) == 404
        assert normalize_status_code(500) == 500

    def test_string_numeric_converted(self):
        """Numeric strings are coerced to int."""
        assert normalize_status_code("200") == 200
        assert normalize_status_code("404") == 404

    def test_none_returns_default(self):
        """None returns the default value."""
        assert normalize_status_code(None) == 200
        assert normalize_status_code(None, default=500) == 500

    def test_invalid_value_returns_default(self):
        """Non-numeric input returns default."""
        assert normalize_status_code("ok") == 200
        assert normalize_status_code([]) == 200
        assert normalize_status_code({}) == 200

    def test_out_of_range_returns_default(self):
        """Status codes outside 100-599 return default."""
        assert normalize_status_code(99) == 200
        assert normalize_status_code(600) == 200
        assert normalize_status_code(0) == 200

    def test_boundary_values(self):
        """Boundary values 100 and 599 are valid."""
        assert normalize_status_code(100) == 100
        assert normalize_status_code(599) == 599

    def test_custom_default(self):
        """Custom default is used on failure."""
        assert normalize_status_code("bad", default=503) == 503


class TestAddSafe(unittest.TestCase):
    """
    Tests for add_safe arithmetic helper.

    File Protocol
    - GOAL: Provide a tiny arithmetic helper for safe addition with basic coercion
      and graceful handling of invalid inputs.
    - MODIFICATION: Add tests here (integration-first) and later implement
      `add_safe` in `mvp_site/utils.py`.
    - NECESSITY: Several modules work with numeric-like values (ints, floats,
      numeric strings). A centralized, defensive adder reduces duplication and
      edge-case bugs (None, bad strings) similar to existing normalization
      helpers.
    - INTEGRATION PROOF: Tests live in existing `test_utils.py`, using the
      existing import style from `mvp_site.utils`. The new function will be
      added to that module to maintain code locality and discoverability.
    """

    def test_add_integers(self):
        assert add_safe(2, 3) == 5
        assert isinstance(add_safe(2, 3), int)

    def test_add_floats(self):
        result = add_safe(2.5, 0.5)
        assert math.isclose(result, 3.0, rel_tol=1e-9, abs_tol=1e-12)
        assert isinstance(result, float)

    def test_add_numeric_strings(self):
        assert add_safe("2", "3") == 5
        assert math.isclose(add_safe("2.5", "0.5"), 3.0, rel_tol=1e-9, abs_tol=1e-12)

    def test_add_mixed_types(self):
        assert math.isclose(add_safe("2", 3.5), 5.5, rel_tol=1e-9, abs_tol=1e-12)

    def test_none_or_invalid_returns_default(self):
        assert add_safe(None, 2) == 0
        assert add_safe(1, None) == 0
        assert add_safe("bad", 1) == 0
        assert add_safe(1, "bad") == 0

    def test_custom_default_on_error(self):
        assert add_safe("oops", "nah", default=999) == 999

    def test_float_precision_guard(self):
        # Typical floating-point precision case: ensure close to 0.3
        assert math.isclose(add_safe(0.1, 0.2), 0.3, rel_tol=1e-9, abs_tol=1e-12)


if __name__ == "__main__":
    unittest.main()
