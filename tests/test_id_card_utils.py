import unittest
from unittest.mock import patch
from idcard_generator.id_card_utils import random_day

class TestIdCardUtils(unittest.TestCase):

    def test_random_day_leap_year_february(self):
        # 2020 is a leap year, February has 29 days
        for _ in range(100):
            day = random_day(2020, 2)
            self.assertGreaterEqual(day, 1)
            self.assertLessEqual(day, 29)

    def test_random_day_non_leap_year_february(self):
        # 2021 is not a leap year, February has 28 days
        for _ in range(100):
            day = random_day(2021, 2)
            self.assertGreaterEqual(day, 1)
            self.assertLessEqual(day, 28)

    def test_random_day_31_day_month(self):
        # January has 31 days
        for _ in range(100):
            day = random_day(2021, 1)
            self.assertGreaterEqual(day, 1)
            self.assertLessEqual(day, 31)

    def test_random_day_30_day_month(self):
        # April has 30 days
        for _ in range(100):
            day = random_day(2021, 4)
            self.assertGreaterEqual(day, 1)
            self.assertLessEqual(day, 30)

    def test_random_day_default_args(self):
        # Default args are 2020, 2 (leap year February)
        for _ in range(100):
            day = random_day()
            self.assertGreaterEqual(day, 1)
            self.assertLessEqual(day, 29)

    @patch('idcard_generator.id_card_utils.random.randint')
    def test_random_day_randint_called_with_correct_range(self, mock_randint):
        mock_randint.return_value = 15

        # Test leap year February
        random_day(2020, 2)
        mock_randint.assert_called_with(1, 29)

        # Test non-leap year February
        random_day(2021, 2)
        mock_randint.assert_called_with(1, 28)

        # Test 31-day month
        random_day(2021, 1)
        mock_randint.assert_called_with(1, 31)

        # Test 30-day month
        random_day(2021, 4)
        mock_randint.assert_called_with(1, 30)

if __name__ == '__main__':
    unittest.main()
