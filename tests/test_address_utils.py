import unittest
from unittest.mock import patch, mock_open
import json
import os
import sys

from idcard_generator.address_utils import get_random_address, create_default_config_file

class TestAddressUtils(unittest.TestCase):
    @patch('idcard_generator.address_utils.os.path.exists')
    @patch('idcard_generator.address_utils.utils.get_base_path')
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({"addresses": ["Address 1", "Address 2"]}))
    def test_get_random_address_normal_env(self, mock_file, mock_base_path, mock_exists):
        mock_base_path.return_value = '/base/path'
        mock_exists.return_value = True

        with patch('idcard_generator.address_utils.sys') as mock_sys:
            # Setting frozen to False to ensure normal env
            mock_sys.frozen = False
            address = get_random_address()
            self.assertIn(address, ["Address 1", "Address 2"])
            mock_file.assert_called_with(os.path.join('/base/path', 'idcard_generator', 'address_config.json'), 'r', encoding='utf-8')

    @patch('idcard_generator.address_utils.os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({"addresses": ["Address 3"]}))
    def test_get_random_address_frozen_env(self, mock_file, mock_exists):
        mock_exists.return_value = True

        with patch('idcard_generator.address_utils.sys') as mock_sys:
            mock_sys.frozen = True
            mock_sys.executable = os.path.join('/exe', 'dir', 'my_app.exe')
            address = get_random_address()
            self.assertEqual(address, "Address 3")
            mock_file.assert_called_with(os.path.join('/exe', 'dir', 'address_config.json'), 'r', encoding='utf-8')

    @patch('idcard_generator.address_utils.os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({"addresses": []}))
    def test_get_random_address_empty_addresses(self, mock_file, mock_exists):
        mock_exists.return_value = True
        with patch('idcard_generator.address_utils.sys') as mock_sys:
            mock_sys.frozen = False
            address = get_random_address()
            self.assertEqual(address, "江苏省南京市鼓楼区中山路1号")

    @patch('idcard_generator.address_utils.os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data="invalid json")
    def test_get_random_address_json_decode_error(self, mock_file, mock_exists):
        mock_exists.return_value = True
        with patch('idcard_generator.address_utils.sys') as mock_sys:
            mock_sys.frozen = False
            address = get_random_address()
            self.assertEqual(address, "江苏省南京市鼓楼区中山路1号")

    @patch('idcard_generator.address_utils.os.path.exists')
    @patch('idcard_generator.address_utils.create_default_config_file')
    @patch('builtins.open')
    def test_get_random_address_file_not_found(self, mock_file, mock_create, mock_exists):
        mock_exists.return_value = False
        mock_file.side_effect = FileNotFoundError
        with patch('idcard_generator.address_utils.sys') as mock_sys:
            mock_sys.frozen = False
            address = get_random_address()
            self.assertEqual(address, "江苏省南京市鼓楼区中山路1号")
            mock_create.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    @patch('idcard_generator.address_utils.json.dump')
    def test_create_default_config_file_success(self, mock_json_dump, mock_file):
        config_path = '/dummy/path/config.json'
        create_default_config_file(config_path)

        mock_file.assert_called_once_with(config_path, 'w', encoding='utf-8')
        mock_json_dump.assert_called_once()
        args, kwargs = mock_json_dump.call_args
        self.assertIn("addresses", args[0])
        self.assertEqual(kwargs['ensure_ascii'], False)
        self.assertEqual(kwargs['indent'], 2)

    @patch('builtins.open', new_callable=mock_open)
    def test_create_default_config_file_exception(self, mock_file):
        mock_file.side_effect = Exception("Test Exception")
        config_path = '/dummy/path/config.json'

        try:
            create_default_config_file(config_path)
        except Exception:
            self.fail("create_default_config_file() raised Exception unexpectedly!")

if __name__ == '__main__':
    unittest.main()
