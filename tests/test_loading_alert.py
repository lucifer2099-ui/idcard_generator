import pytest
from unittest.mock import MagicMock, call
import tkinter as tk
from idcard_generator.loading_alert import format_form, LoadingBar

def test_format_form():
    mock_form = MagicMock()
    mock_form.winfo_screenwidth.return_value = 1920
    mock_form.winfo_screenheight.return_value = 1080

    format_form(mock_form, 400, 300)

    # Calculate expected width_adjust and height_adjust
    # width_adjust = (1920 - 400) / 2 = 760
    # height_adjust = (1080 - 300) / 2 = 390
    mock_form.geometry.assert_called_once_with("400x300+760+390")

def test_loading_bar_init():
    bar = LoadingBar(title="Test", content="Testing...", width=300, height=200)

    assert bar._LoadingBar__title == "Test"
    assert bar._LoadingBar__content == "Testing..."
    assert bar._LoadingBar__width == 300
    assert bar._LoadingBar__height == 200
    assert bar._LoadingBar__showFlag is False
    assert bar._LoadingBar__dialog is None

def test_loading_bar_show(mocker):
    # Mocking tkinter components
    mock_toplevel = mocker.patch("idcard_generator.loading_alert.tk.Toplevel")
    mock_label = mocker.patch("idcard_generator.loading_alert.tk.Label")
    mock_progressbar = mocker.patch("idcard_generator.loading_alert.ttk.Progressbar")
    mock_format_form = mocker.patch("idcard_generator.loading_alert.format_form")

    mock_dialog = MagicMock()
    mock_toplevel.return_value = mock_dialog

    mock_parent = MagicMock()

    bar = LoadingBar()
    bar.show(parent=mock_parent, speed=15, sleep=2)

    assert bar._LoadingBar__showFlag is True
    assert bar._LoadingBar__parent == mock_parent
    assert bar._LoadingBar__sleep == 2

    mock_toplevel.assert_called_once_with(mock_parent)
    mock_dialog.title.assert_called_once_with("提示")
    mock_format_form.assert_called_once_with(mock_dialog, 200, 100)
    mock_dialog.wm_attributes.assert_called_once_with("-topmost", True)
    mock_dialog.resizable.assert_called_once_with(0, 0)
    mock_dialog.protocol.assert_called_once()

    mock_label.assert_called_once_with(mock_dialog, text="正在处理...")
    mock_label.return_value.pack.assert_called_once_with(side=tk.TOP)

    mock_parent.grab_set.assert_called_once()

    mock_progressbar.assert_called_once_with(mock_dialog, length=200, mode="indeterminate", orient=tk.HORIZONTAL)
    mock_progressbar.return_value.pack.assert_called_once_with(expand=True)
    mock_progressbar.return_value.start.assert_called_once_with(15)

    mock_dialog.after.assert_called_once_with(250, bar.wait_close)

def test_loading_bar_show_already_shown():
    bar = LoadingBar()
    # Mock __dialog to be not None
    bar._LoadingBar__dialog = MagicMock()

    # show shouldn't do anything if __dialog is already set
    bar.show()
    assert bar._LoadingBar__showFlag is False

def test_loading_bar_wait_close_while_showing():
    bar = LoadingBar()
    bar._LoadingBar__showFlag = True

    mock_dialog = MagicMock()
    bar._LoadingBar__dialog = mock_dialog

    bar.wait_close()

    mock_dialog.after.assert_called_once_with(250, bar.wait_close)
    mock_dialog.destroy.assert_not_called()

def test_loading_bar_wait_close_when_closed():
    bar = LoadingBar()
    bar._LoadingBar__showFlag = False

    mock_dialog = MagicMock()
    bar._LoadingBar__dialog = mock_dialog

    mock_parent = MagicMock()
    bar._LoadingBar__parent = mock_parent

    bar.wait_close()

    mock_dialog.after.assert_not_called()
    mock_dialog.destroy.assert_called_once()
    mock_parent.grab_release.assert_called_once()
    assert bar._LoadingBar__dialog is None

def test_loading_bar_close():
    bar = LoadingBar()
    bar._LoadingBar__showFlag = True

    bar.close()

    assert bar._LoadingBar__showFlag is False
