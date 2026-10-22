import datetime
import unittest
from unittest.mock import patch

from idcard_generator.id_card_utils import IdentityCard, generate_validity_period


class TestIdentityCardCheck(unittest.TestCase):

    def test_check_valid_length(self):
        # 17 characters string should return True
        valid_code = "12345678901234567"
        self.assertTrue(IdentityCard.check(valid_code))

    def test_check_invalid_length_short(self):
        # Less than 17 characters should return False
        short_code = "1234567890123456"
        self.assertFalse(IdentityCard.check(short_code))

    def test_check_invalid_length_long(self):
        # More than 17 characters should return False
        long_code = "123456789012345678"
        self.assertFalse(IdentityCard.check(long_code))

    def test_check_empty_string(self):
        # Empty string should return False
        empty_code = ""
        self.assertFalse(IdentityCard.check(empty_code))


def test_generate_validity_period_format_and_gap():
    """Test the general format and the strict 20-year gap rule."""
    start_str, end_str = generate_validity_period()

    # Check format length (YYYY.MM.DD)
    assert len(start_str) == 10
    assert len(end_str) == 10

    # Parse dates
    start_date = datetime.datetime.strptime(start_str, "%Y.%m.%d")
    end_date = datetime.datetime.strptime(end_str, "%Y.%m.%d")

    # Check strict 20-year difference and matching month/day
    assert end_date.year - start_date.year == 20
    assert start_date.month == end_date.month
    assert start_date.day == end_date.day

    # Check it ends strictly after or exactly on 2030 (based on implementation logic start_year >= 2010 -> end_year >= 2030)
    assert end_date.year >= 2030


def test_generate_validity_period_clamping_to_2010():
    """Test that if the random start year would be < 2010, it is clamped to 2010."""
    # Mock datetime.now() to a year where current_year - 5 < 2010 (e.g. 2014)
    # The range is (current_year - 15, current_year - 5)
    # So range will be (1999, 2009). Maximum start year will be 2009.
    # Therefore, it MUST clamp to 2010.

    class MockDatetime(datetime.datetime):
        @classmethod
        def now(cls):
            return cls(2014, 1, 1)

    with patch('idcard_generator.id_card_utils.datetime.datetime', MockDatetime):
        start_str, end_str = generate_validity_period()
        start_date = datetime.datetime.strptime(start_str, "%Y.%m.%d")
        end_date = datetime.datetime.strptime(end_str, "%Y.%m.%d")

        assert start_date.year == 2010
        assert end_date.year == 2030
        assert end_date.year - start_date.year == 20
        assert start_date.month == end_date.month
        assert start_date.day == end_date.day


def test_generate_validity_period_no_clamping():
    """Test that if the random start year is >= 2010, it is NOT clamped to 2010."""
    # Mock datetime.now() to a year where current_year - 15 >= 2010 (e.g. 2026)
    # Range is (2011, 2021). All years are >= 2010, so it should not clamp to 2010.

    class MockDatetime(datetime.datetime):
        @classmethod
        def now(cls):
            return cls(2026, 1, 1)

    with patch('idcard_generator.id_card_utils.datetime.datetime', MockDatetime):
        start_str, end_str = generate_validity_period()
        start_date = datetime.datetime.strptime(start_str, "%Y.%m.%d")

        assert start_date.year >= 2011
        assert start_date.year <= 2021
        assert start_date.year != 2010  # Because range starts at 2011


def test_generate_validity_period_randomness():
    """Test that multiple calls generate different validity periods (non-deterministic parts)."""
    results = set()
    for _ in range(10):
        results.add(generate_validity_period())

    # Very unlikely to generate exactly the same start and end 10 times in a row
    assert len(results) > 1


if __name__ == '__main__':
    unittest.main()
