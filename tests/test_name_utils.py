import unittest
from idcard_generator.name_utils import random_name

class TestNameUtils(unittest.TestCase):
    def test_random_name_structure(self):
        """Test the structure and types of the dictionary returned by random_name."""
        result = random_name()

        # Check return type
        self.assertIsInstance(result, dict)

        # Check keys
        expected_keys = {"name_full", "name_xing", "name_ming", "sex", "sex_text"}
        self.assertEqual(set(result.keys()), expected_keys)

        # Check value types
        self.assertIsInstance(result["name_full"], str)
        self.assertIsInstance(result["name_xing"], str)
        self.assertIsInstance(result["name_ming"], str)
        self.assertIsInstance(result["sex"], int)
        self.assertIsInstance(result["sex_text"], str)

    def test_random_name_values(self):
        """Test the values and logic correctness of random_name."""
        result = random_name()

        # Check sex and sex_text correspondence
        self.assertIn(result["sex"], [0, 1])
        if result["sex"] == 0:
            self.assertEqual(result["sex_text"], "女")
        else:
            self.assertEqual(result["sex_text"], "男")

        # Check full name concatenation
        self.assertEqual(result["name_full"], result["name_xing"] + result["name_ming"])

    def test_random_name_multiple_calls(self):
        """Test multiple calls to ensure consistency and randomness."""
        results = [random_name() for _ in range(100)]

        for result in results:
            # Check basic constraints on all calls
            self.assertIn(result["sex"], [0, 1])
            self.assertIn(result["sex_text"], ["男", "女"])
            self.assertEqual(result["name_full"], result["name_xing"] + result["name_ming"])

        # Check that it actually generates different names
        # (It's statistically nearly impossible to generate the same name 100 times)
        unique_names = set(r["name_full"] for r in results)
        self.assertTrue(len(unique_names) > 1, "random_name should generate different names")

if __name__ == '__main__':
    unittest.main()
