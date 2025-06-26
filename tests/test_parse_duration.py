import unittest

from marmiton.parse_duration import parse_duration_to_minutes


class TestParseDurationToMinutes(unittest.TestCase):
    """Unit tests for the parse_duration_to_minutes function."""

    def test_hours_and_minutes(self):
        """Test with durations containing hours and minutes."""
        self.assertEqual(parse_duration_to_minutes("1h10"), 70)
        self.assertEqual(parse_duration_to_minutes("2h30"), 150)
        self.assertEqual(parse_duration_to_minutes("3h45"), 225)
        self.assertEqual(parse_duration_to_minutes("1h05"), 65)

    def test_hours_and_minutes_with_spaces(self):
        """Test with durations containing spaces."""
        self.assertEqual(parse_duration_to_minutes("1 h 10"), 70)
        self.assertEqual(parse_duration_to_minutes("2 h 30"), 150)
        self.assertEqual(parse_duration_to_minutes("1 h 5"), 65)

    def test_only_minutes(self):
        """Test with durations in minutes only."""
        self.assertEqual(parse_duration_to_minutes("12 min"), 12)
        self.assertEqual(parse_duration_to_minutes("45 min"), 45)
        self.assertEqual(parse_duration_to_minutes("30min"), 30)
        self.assertEqual(parse_duration_to_minutes("5min"), 5)

    def test_only_minutes_without_unit(self):
        """Test with durations in minutes without unit."""
        self.assertEqual(parse_duration_to_minutes("45"), 45)
        self.assertEqual(parse_duration_to_minutes("30"), 30)
        self.assertEqual(parse_duration_to_minutes("15"), 15)
        self.assertEqual(parse_duration_to_minutes("5"), 5)

    def test_only_hours(self):
        """Test with durations in hours only."""
        self.assertEqual(parse_duration_to_minutes("1 h"), 60)
        self.assertEqual(parse_duration_to_minutes("2h"), 120)
        self.assertEqual(parse_duration_to_minutes("3 h"), 180)
        self.assertEqual(parse_duration_to_minutes("4h"), 240)

    def test_zero_values(self):
        """Test with zero values."""
        self.assertEqual(parse_duration_to_minutes("0h"), 0)
        self.assertEqual(parse_duration_to_minutes("0 min"), 0)
        self.assertEqual(parse_duration_to_minutes("0"), 0)
        self.assertEqual(parse_duration_to_minutes("0h0"), 0)

    def test_large_values(self):
        """Test with large values."""
        self.assertEqual(parse_duration_to_minutes("10h30"), 630)
        self.assertEqual(parse_duration_to_minutes("24h"), 1440)
        self.assertEqual(parse_duration_to_minutes("120 min"), 120)
        self.assertEqual(parse_duration_to_minutes("500"), 500)

    def test_case_insensitive(self):
        """Test that the function is case insensitive."""
        self.assertEqual(parse_duration_to_minutes("1H30"), 90)
        self.assertEqual(parse_duration_to_minutes("2H"), 120)
        self.assertEqual(parse_duration_to_minutes("45 MIN"), 45)
        self.assertEqual(parse_duration_to_minutes("1h30MIN"), 90)

    def test_mixed_formats(self):
        """Test with mixed formats."""
        self.assertEqual(parse_duration_to_minutes("2h 30"), 150)
        self.assertEqual(parse_duration_to_minutes("1h 0"), 60)
        self.assertEqual(parse_duration_to_minutes("0h 45"), 45)

    def test_edge_cases(self):
        """Test edge cases."""
        # Test with single digit numbers
        self.assertEqual(parse_duration_to_minutes("1h1"), 61)
        self.assertEqual(parse_duration_to_minutes("9h9"), 549)

        # Test with multi-digit numbers
        self.assertEqual(parse_duration_to_minutes("12h15"), 735)
        self.assertEqual(parse_duration_to_minutes("100h59"), 6059)

    def test_string_with_extra_whitespace(self):
        """Test with extra whitespace."""
        self.assertEqual(parse_duration_to_minutes("  1h30  "), 90)
        self.assertEqual(parse_duration_to_minutes(" 45 min "), 45)
        self.assertEqual(parse_duration_to_minutes("   2 h   "), 120)

    def test_various_minute_formats(self):
        """Test with various minute formats."""
        # Minutes with explicit 'min'
        self.assertEqual(parse_duration_to_minutes("30min"), 30)
        self.assertEqual(parse_duration_to_minutes("15 min"), 15)

        # Minutes without 'min' (number only)
        self.assertEqual(parse_duration_to_minutes("25"), 25)
        self.assertEqual(parse_duration_to_minutes("60"), 60)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
