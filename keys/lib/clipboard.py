# keys/clipboard.py
import platform
import subprocess
import time


def get_selection() -> str:
    """Get selected text from system."""
    system = platform.system()

    if system == "Darwin":  # macOS
        # Simulate copy, then read clipboard
        # This requires 'osascript' and 'pbpaste'
        subprocess.run(
            [
                "osascript",
                "-e",
                'tell application "System Events" to keystroke "c" using command down',
            ],
            check=True,
        )
        time.sleep(0.1)  # Give clipboard time to update
        return subprocess.check_output(["pbpaste"], text=True).strip()

    if system == "Linux":
        # This requires 'xclip' or 'xsel'
        # Try primary selection first, fall back to clipboard
        try:
            return subprocess.check_output(
                ["xclip", "-o", "-selection", "primary"], text=True
            ).strip()
        except subprocess.CalledProcessError:
            return subprocess.check_output(
                ["xclip", "-o", "-selection", "clipboard"], text=True
            ).strip()

    raise NotImplementedError(f"Platform not supported for getting selection: {system}")


def set_clipboard(text: str):
    """Copy text to clipboard."""
    system = platform.system()

    if system == "Darwin":
        # This requires 'pbcopy'
        subprocess.run(["pbcopy"], input=text, text=True, check=True)
    elif system == "Linux":
        # This requires 'xclip' or 'xsel'
        subprocess.run(["xclip", "-selection", "clipboard"], input=text, text=True, check=True)
    else:
        raise NotImplementedError(f"Platform not supported for setting clipboard: {system}")
