import unittest
from idcard_generator.id_card_utils import IdentityCard

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

if __name__ == '__main__':
    unittest.main()
