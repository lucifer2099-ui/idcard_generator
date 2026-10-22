import unittest
from idcard_generator.id_card_utils import random_card_no, IdentityCard, XUZHOU_AREA_CODES

class TestRandomCardNo(unittest.TestCase):

    def test_default_generation(self):
        """Test default arguments return a valid 18 character ID card string."""
        card_no = random_card_no()
        self.assertEqual(len(card_no), 18)

        # Verify prefix is from Xuzhou
        self.assertIn(card_no[0:6], XUZHOU_AREA_CODES)

        # Verify parity bit is correct
        card_17 = card_no[:17]
        expected_parity = IdentityCard.calculate(card_17)
        self.assertEqual(card_no[17], expected_parity)

    def test_prefix(self):
        """Test that provided prefix works correctly."""
        # Providing a prefix > 6 chars should truncate
        card_no = random_card_no(prefix="12345678")
        self.assertEqual(card_no[:6], "123456")

        # Providing a prefix < 6 chars should fall back to XUZHOU_AREA_CODES
        card_no_short = random_card_no(prefix="123")
        self.assertIn(card_no_short[0:6], XUZHOU_AREA_CODES)

    def test_year(self):
        """Test that year argument is used correctly and clamped if before 1980."""
        # Normal year
        card_no = random_card_no(year="2005")
        self.assertEqual(card_no[6:10], "2005")

        # Year < 1980 should clamp to 1980
        card_no_old = random_card_no(year="1975")
        self.assertEqual(card_no_old[6:10], "1980")

    def test_month_day(self):
        """Test that month and day arguments are correctly padded."""
        # Month < 10, Day < 10
        card_no = random_card_no(month="5", day="9")
        self.assertEqual(card_no[10:12], "05")
        self.assertEqual(card_no[12:14], "09")

        # Month >= 10, Day >= 10
        card_no2 = random_card_no(month="11", day="25")
        self.assertEqual(card_no2[10:12], "11")
        self.assertEqual(card_no2[12:14], "25")

    def test_sex(self):
        """Test that sex argument correctly determines 17th digit."""
        # sex=1 (Male) should be odd
        for _ in range(10):
            card_no = random_card_no(sex=1)
            self.assertTrue(int(card_no[16]) % 2 != 0)

        # sex=0 (Female) should be even
        for _ in range(10):
            card_no = random_card_no(sex=0)
            self.assertTrue(int(card_no[16]) % 2 == 0)

        # Invalid/None sex should just be a digit 0-9
        for _ in range(10):
            card_no = random_card_no(sex="invalid")
            self.assertTrue(card_no[16].isdigit())

        for _ in range(10):
            card_no = random_card_no(sex=None)
            self.assertTrue(card_no[16].isdigit())

    def test_all_parity(self):
        """Verify parity bit for all generated cards."""
        for _ in range(50):
            card_no = random_card_no(prefix="110105", year="1990", month="01", day="01", sex=1)
            expected_parity = IdentityCard.calculate(card_no[:17])
            self.assertEqual(card_no[17], expected_parity)

if __name__ == '__main__':
    unittest.main()
