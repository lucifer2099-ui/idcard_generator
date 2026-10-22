import datetime
import unittest
from unittest.mock import patch
import pytest

from idcard_generator.id_card_utils import (
    IdentityCard,
    random_card_no,
    generate_validity_period,
    XUZHOU_AREA_CODES,
)


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


def test_random_card_no_default():
    """Test the default generation of ID card numbers."""
    code = random_card_no()

    # Check length
    assert len(code) == 18

    # Check valid prefix (should default to one of XUZHOU_AREA_CODES if not specified)
    assert code[:6] in XUZHOU_AREA_CODES

    # Check parity bit
    assert IdentityCard.check(code[:17])
    expected_vi_code = IdentityCard.calculate(code[:17])
    assert code[-1] == expected_vi_code


def test_random_card_no_specific_prefix():
    """Test generating ID card with a specific prefix."""
    prefix = '110105'
    code = random_card_no(prefix=prefix)

    assert code[:6] == prefix
    assert len(code) == 18


def test_random_card_no_specific_year_month_day():
    """Test generating ID card with specific year, month, and day."""
    year = '1990'
    month = '5'
    day = '9'

    code = random_card_no(year=year, month=month, day=day)

    assert code[6:10] == '1990'
    assert code[10:12] == '05'
    assert code[12:14] == '09'


def test_random_card_no_year_before_1980():
    """Test generating ID card with a year before 1980."""
    year = '1970'

    code = random_card_no(year=year)

    assert code[6:10] == '1980'


def test_random_card_no_sex_female():
    """Test generating ID card for a female."""
    code = random_card_no(sex=0)

    seq_last = int(code[16])
    assert seq_last % 2 == 0


def test_random_card_no_sex_male():
    """Test generating ID card for a male."""
    code = random_card_no(sex=1)

    seq_last = int(code[16])
    assert seq_last % 2 != 0


def test_random_card_no_all_parameters():
    """Test generating ID card with all specific parameters."""
    prefix = '110101'
    year = '2000'
    month = '12'
    day = '31'
    sex = 1

    code = random_card_no(prefix=prefix, year=year, month=month, day=day, sex=sex)

    assert code[:6] == prefix
    assert code[6:10] == year
    assert code[10:12] == month
    assert code[12:14] == day

    seq_last = int(code[16])
    assert seq_last % 2 != 0

    # Parity bit check
    expected_vi_code = IdentityCard.calculate(code[:17])
    assert code[-1] == expected_vi_code


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
    class MockDatetime(datetime.datetime):
        @classmethod
        def now(cls):
            return cls(2026, 1, 1)

    with patch('idcard_generator.id_card_utils.datetime.datetime', MockDatetime):
        start_str, end_str = generate_validity_period()
        start_date = datetime.datetime.strptime(start_str, "%Y.%m.%d")

        assert start_date.year >= 2011
        assert start_date.year <= 2021
        assert start_date.year != 2010


def test_generate_validity_period_randomness():
    """Test that multiple calls generate different validity periods (non-deterministic parts)."""
    results = set()
    for _ in range(10):
        results.add(generate_validity_period())

    assert len(results) > 1


if __name__ == '__main__':
    unittest.main()
