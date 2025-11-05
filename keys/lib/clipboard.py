"""Cross-platform clipboard operations."""

import platform
import subprocess


def get_clipboard() -> str:
    """Read current clipboard contents without modification."""
    system = platform.system()

    if system == "Darwin":
        return subprocess.check_output(["pbpaste"], text=True)

    if system == "Linux":
        try:
            return subprocess.check_output(["xclip", "-o", "-selection", "clipboard"], text=True)
        except subprocess.CalledProcessError:
            return ""

    raise NotImplementedError(f"Platform not supported: {system}")


def set_clipboard(text: str) -> None:
    """Write text to clipboard."""
    system = platform.system()

    if system == "Darwin":
        subprocess.run(["pbcopy"], input=text, text=True, check=True)
    elif system == "Linux":
        subprocess.run(["xclip", "-selection", "clipboard"], input=text, text=True, check=True)
    else:
        raise NotImplementedError(f"Platform not supported: {system}")


def paste() -> None:
    """Simulate paste keystroke in active window."""
    system = platform.system()

    if system == "Darwin":
        subprocess.run(
            [
                "osascript",
                "-e",
                'tell application "System Events" to keystroke "v" using command down',
            ],
            check=True,
        )
    elif system == "Linux":
        subprocess.run(
            ["xdotool", "key", "ctrl+v"],
            check=True,
        )
    else:
        raise NotImplementedError(f"Platform not supported: {system}")
