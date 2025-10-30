import subprocess
from unittest.mock import patch

import pytest

from keys.lib.clipboard import get_selection, set_clipboard


@pytest.fixture(autouse=True)
def mock_platform_system():
    """Fixture to mock platform.system() for consistent testing."""
    with patch("platform.system", return_value="Darwin") as mock_system:
        yield mock_system


class TestClipboard:
    @patch("subprocess.run")
    @patch("subprocess.check_output")
    @patch("time.sleep", return_value=None)  # Mock time.sleep to speed up tests
    def test_get_selection_macos(
        self, mock_sleep, mock_check_output, mock_run, mock_platform_system
    ):
        mock_platform_system.return_value = "Darwin"
        mock_check_output.return_value = "selected text from macos"

        result = get_selection()

        mock_run.assert_called_once_with(
            [
                "osascript",
                "-e",
                'tell application "System Events" to keystroke "c" using command down',
            ],
            check=True,
        )
        mock_check_output.assert_called_once_with(["pbpaste"], text=True)
        assert result == "selected text from macos"

    @patch("subprocess.run")
    def test_set_clipboard_macos(self, mock_run, mock_platform_system):
        mock_platform_system.return_value = "Darwin"
        text_to_copy = "text to copy to macos clipboard"

        set_clipboard(text_to_copy)

        mock_run.assert_called_once_with(["pbcopy"], input=text_to_copy, text=True, check=True)

    @patch("subprocess.run")
    @patch("subprocess.check_output")
    def test_get_selection_linux_primary(self, mock_check_output, mock_run, mock_platform_system):
        mock_platform_system.return_value = "Linux"
        mock_check_output.return_value = "selected text from linux primary"

        result = get_selection()

        mock_check_output.assert_called_once_with(
            ["xclip", "-o", "-selection", "primary"], text=True
        )
        assert result == "selected text from linux primary"

    @patch("subprocess.run")
    @patch(
        "subprocess.check_output",
        side_effect=[
            subprocess.CalledProcessError(1, "xclip"),
            "selected text from linux clipboard",
        ],
    )
    def test_get_selection_linux_clipboard_fallback(
        self, mock_check_output, mock_run, mock_platform_system
    ):
        mock_platform_system.return_value = "Linux"

        result = get_selection()

        assert mock_check_output.call_count == 2
        mock_check_output.assert_any_call(["xclip", "-o", "-selection", "primary"], text=True)
        mock_check_output.assert_any_call(["xclip", "-o", "-selection", "clipboard"], text=True)
        assert result == "selected text from linux clipboard"

    @patch("subprocess.run")
    def test_set_clipboard_linux(self, mock_run, mock_platform_system):
        mock_platform_system.return_value = "Linux"
        text_to_copy = "text to copy to linux clipboard"

        set_clipboard(text_to_copy)

        mock_run.assert_called_once_with(
            ["xclip", "-selection", "clipboard"], input=text_to_copy, text=True, check=True
        )

    def test_get_selection_unsupported_platform(self, mock_platform_system):
        mock_platform_system.return_value = "Windows"
        with pytest.raises(
            NotImplementedError, match="Platform not supported for getting selection: Windows"
        ):
            get_selection()

    def test_set_clipboard_unsupported_platform(self, mock_platform_system):
        mock_platform_system.return_value = "Windows"
        with pytest.raises(
            NotImplementedError, match="Platform not supported for setting clipboard: Windows"
        ):
            set_clipboard("some text")
