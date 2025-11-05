import subprocess
from unittest.mock import patch

import pytest

from keys.lib.clipboard import get_clipboard, paste, set_clipboard


@pytest.fixture(autouse=True)
def mock_platform_system():
    """Fixture to mock platform.system() for consistent testing."""
    with patch("platform.system", return_value="Darwin") as mock_system:
        yield mock_system


class TestClipboard:
    @patch("subprocess.check_output")
    def test_get_clipboard_macos(self, mock_check_output, mock_platform_system):
        mock_platform_system.return_value = "Darwin"
        mock_check_output.return_value = "clipboard content from macos"

        result = get_clipboard()

        mock_check_output.assert_called_once_with(["pbpaste"], text=True)
        assert result == "clipboard content from macos"

    @patch("subprocess.run")
    def test_set_clipboard_macos(self, mock_run, mock_platform_system):
        mock_platform_system.return_value = "Darwin"
        text_to_copy = "text to copy to macos clipboard"

        set_clipboard(text_to_copy)

        mock_run.assert_called_once_with(["pbcopy"], input=text_to_copy, text=True, check=True)

    @patch("subprocess.check_output")
    def test_get_clipboard_linux(self, mock_check_output, mock_platform_system):
        mock_platform_system.return_value = "Linux"
        mock_check_output.return_value = "clipboard content from linux"

        result = get_clipboard()

        mock_check_output.assert_called_once_with(
            ["xclip", "-o", "-selection", "clipboard"], text=True
        )
        assert result == "clipboard content from linux"

    @patch("subprocess.check_output", side_effect=subprocess.CalledProcessError(1, "xclip"))
    def test_get_clipboard_linux_empty_on_error(self, mock_check_output, mock_platform_system):
        mock_platform_system.return_value = "Linux"

        result = get_clipboard()

        assert result == ""

    @patch("subprocess.run")
    def test_set_clipboard_linux(self, mock_run, mock_platform_system):
        mock_platform_system.return_value = "Linux"
        text_to_copy = "text to copy to linux clipboard"

        set_clipboard(text_to_copy)

        mock_run.assert_called_once_with(
            ["xclip", "-selection", "clipboard"], input=text_to_copy, text=True, check=True
        )

    @patch("subprocess.run")
    def test_paste_macos(self, mock_run, mock_platform_system):
        mock_platform_system.return_value = "Darwin"

        paste()

        mock_run.assert_called_once_with(
            [
                "osascript",
                "-e",
                'tell application "System Events" to keystroke "v" using command down',
            ],
            check=True,
        )

    @patch("subprocess.run")
    def test_paste_linux(self, mock_run, mock_platform_system):
        mock_platform_system.return_value = "Linux"

        paste()

        mock_run.assert_called_once_with(["xdotool", "key", "ctrl+v"], check=True)

    def test_get_clipboard_unsupported_platform(self, mock_platform_system):
        mock_platform_system.return_value = "Windows"
        with pytest.raises(NotImplementedError, match="Platform not supported: Windows"):
            get_clipboard()

    def test_set_clipboard_unsupported_platform(self, mock_platform_system):
        mock_platform_system.return_value = "Windows"
        with pytest.raises(NotImplementedError, match="Platform not supported: Windows"):
            set_clipboard("some text")

    def test_paste_unsupported_platform(self, mock_platform_system):
        mock_platform_system.return_value = "Windows"
        with pytest.raises(NotImplementedError, match="Platform not supported: Windows"):
            paste()
