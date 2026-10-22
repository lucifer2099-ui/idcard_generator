import unittest
import calendar

from idcard_generator.id_card_utils import random_day

class TestRandomDay(unittest.TestCase):
    def test_random_day_standard_month_31_days(self):
        """Test a month with 31 days (January)."""
        # We run it multiple times to ensure it's always in range.
        for _ in range(100):
            day = random_day(year=2023, month=1)
            self.assertTrue(1 <= day <= 31)

    def test_random_day_standard_month_30_days(self):
        """Test a month with 30 days (April)."""
        for _ in range(100):
            day = random_day(year=2023, month=4)
            self.assertTrue(1 <= day <= 30)

    def test_random_day_leap_year_february(self):
        """Test February in a leap year."""
        for _ in range(100):
            day = random_day(year=2020, month=2)
            self.assertTrue(1 <= day <= 29)

    def test_random_day_non_leap_year_february(self):
        """Test February in a non-leap year."""
        for _ in range(100):
            day = random_day(year=2023, month=2)
            self.assertTrue(1 <= day <= 28)

    def test_random_day_invalid_month(self):
        """Test that invalid months raise calendar.IllegalMonthError."""
        with self.assertRaises(calendar.IllegalMonthError):
            random_day(year=2023, month=13)

        with self.assertRaises(calendar.IllegalMonthError):
            random_day(year=2023, month=0)

    def test_random_day_default_args(self):
        """Test default arguments (year=2020, month=2)."""
        for _ in range(100):
            day = random_day()
            # 2020 is a leap year, so max days in Feb is 29
            self.assertTrue(1 <= day <= 29)

if __name__ == '__main__':
    unittest.main()
