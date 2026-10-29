import sys
import os
from unittest.mock import patch, MagicMock

import pytest

from idcard_generator.utils import get_base_path, open_url, get_show_len, get_show_txt

def test_get_base_path_not_frozen():
    with patch.object(sys, 'frozen', False, create=True):
        assert get_base_path() == os.path.abspath(".")

def test_get_base_path_frozen():
    with patch.object(sys, 'frozen', True, create=True), \
         patch.object(sys, '_MEIPASS', '/mock/meipass', create=True):
        assert get_base_path() == '/mock/meipass'

def test_open_url():
    with patch('idcard_generator.utils.webbrowser.open') as mock_open:
        event_mock = MagicMock()
        open_url(event_mock)
        mock_open.assert_called_once_with("https://github.com/bzsome", new=0)

def test_get_show_len():
    assert get_show_len("abc") == 3
    assert get_show_len("中文") == 4
    assert get_show_len("a中b文c") == 7
    assert get_show_len("") == 0

def test_get_show_txt():
    txt = "abc中文def" # a(1) b(1) c(1) 中(2) 文(2) d(1) e(1) f(1)
    # len = 8, display len = 10
    # get_show_index logic:
    # index 0: 'a', len 1. if > i_len, return 0.

    # Let's trace get_show_txt("abc中文def", 0, 5)
    # i_start = get_show_index(txt, 0):
    #   index 0: 'a', len 1. 1 > 0 -> return 0.
    # i_end = get_show_index(txt, 5):
    #   index 0: 'a', len 1. 1 > 5 (F)
    #   index 1: 'ab', len 2. 2 > 5 (F)
    #   index 2: 'abc', len 3. 3 > 5 (F)
    #   index 3: 'abc中', len 5. 5 > 5 (F)
    #   index 4: 'abc中文', len 7. 7 > 5 -> return 4.
    # txt[0:4] -> "abc中"

    assert get_show_txt(txt, 0, 5) == "abc中"
    assert get_show_txt(txt, 3, 7) == "中文" # i_start(3)->3, i_end(7)->5. txt[3:5]="中文"

    # edge cases
    assert get_show_txt(txt, 0, 100) == "abc中文def"

    # When i_len is exactly the total length or more, loop finishes without returning, returns get_show_len(txt) = 10
    # txt[0:10] -> "abc中文def" (slice handles out of bounds)
    assert get_show_txt("abc", 0, 3) == "abc" # i_end(3) returns 3, txt[0:3] = "abc"
    assert get_show_txt("abc", 0, 10) == "abc"
