import unittest
import os
import json
import tempfile
import sys

# Ensure idcard_generator is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from idcard_generator.address_utils import create_default_config_file

class TestAddressUtils(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.test_dir.name, 'test_address_config.json')

    def tearDown(self):
        # Cleanup the temporary directory
        self.test_dir.cleanup()

    def test_create_default_config_file_success(self):
        """Test that the default config file is created successfully."""
        # Ensure file does not exist before test
        self.assertFalse(os.path.exists(self.config_path))

        create_default_config_file(self.config_path)

        # Verify the file was created
        self.assertTrue(os.path.exists(self.config_path))

        # Read the file and verify content
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        self.assertIn('addresses', config)
        self.assertIsInstance(config['addresses'], list)
        self.assertTrue(len(config['addresses']) > 0)
        self.assertEqual(config['addresses'][0], "江苏省徐州市云龙区汉山路滨湖花园小区5栋1203室")

    def test_create_default_config_file_invalid_path(self):
        """Test that exceptions are handled silently for invalid paths."""
        # Use a path that is known to be invalid/unwritable to trigger exception
        invalid_path = os.path.join(self.test_dir.name, 'nonexistent_dir', 'test_address_config.json')

        # Should not raise any exception
        try:
            create_default_config_file(invalid_path)
        except Exception as e:
            self.fail(f"create_default_config_file raised Exception unexpectedly: {e}")

        # Ensure file wasn't magically created in a non-existent dir
        self.assertFalse(os.path.exists(invalid_path))

if __name__ == '__main__':
    unittest.main()
