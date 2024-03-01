import unittest
from unittest import mock
import os
import json
import logging
import sys
sys.path.insert(1, 'D:\ModpackChangelogger\src')
from config_handler import create_config
from constants import DEFAULT_CONFIG

class TestCreateConfig(unittest.TestCase):
    @mock.patch('builtins.open', new_callable=mock.mock_open)
    @mock.patch('os.getcwd', return_value='/some/path')
    @mock.patch('json.dump')
    @mock.patch('logging.debug')
    def test_create_config_success(self, mock_debug, mock_dump, mock_getcwd, mock_open):
        create_config()
        mock_open.assert_called_once_with('config.json', 'w', encoding='utf-8')
        mock_dump.assert_called_once_with(DEFAULT_CONFIG, mock_open(), indent=4)
        mock_debug.assert_called_once_with('Created config.json')

    @mock.patch('builtins.open', side_effect=PermissionError)
    @mock.patch('os.getcwd', return_value='/some/path')
    @mock.patch('logging.error')
    @mock.patch('sys.exit')
    def test_create_config_permission_error(self, mock_exit, mock_error, mock_getcwd, mock_open):
        create_config()
        mock_open.assert_called_once_with('config.json', 'w', encoding='utf-8')
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()