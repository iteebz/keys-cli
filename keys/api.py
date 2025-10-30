"""Business logic for keys management - pure functions."""

import os
import signal
from pathlib import Path

from .config import Config
from .lib import Daemon


def set_prompts_dir(path: Path, config_path: Path | None = None) -> str:
    """Set the prompts directory."""
    path = Path(path).expanduser()
    if not path.exists():
        raise ValueError(f"Directory does not exist: {path}")
    config = Config(config_path)
    config.set_prompts_dir(path)
    return f"Prompts directory set to {path}"


def add_key(key: str, prompt_name: str, config_path: Path | None = None) -> str:
    """Register a key binding to a prompt."""
    config = Config(config_path)
    try:
        config.load_prompt(prompt_name)
    except FileNotFoundError as e:
        raise ValueError(str(e)) from e

    config.add_hotkey(key, prompt_name)
    return f"Registered {key} → {prompt_name}"


def list_keys(config_path: Path | None = None) -> list[tuple[str, str]]:
    """Get all key bindings."""
    config = Config(config_path)
    hotkeys = config.hotkeys
    return sorted(hotkeys.items())


def remove_key(key: str, config_path: Path | None = None) -> str:
    """Remove a key binding."""
    config = Config(config_path)
    if config.get_hotkey(key) is None:
        raise ValueError(f"Key not found: {key}")

    config.remove_hotkey(key)
    return f"Removed {key}"


def get_prompt(prompt_name: str, config_path: Path | None = None) -> str:
    """Load prompt content."""
    config = Config(config_path)
    return config.load_prompt(prompt_name)


def start_daemon(config_path: Path | None = None) -> None:
    """Start the hotkey daemon."""
    daemon = Daemon()
    daemon.run()


def stop_daemon(config_path: Path | None = None) -> str:
    """Stop the hotkey daemon."""
    config = Config(config_path)
    pid_file = config.pid_file_path

    if not pid_file.exists():
        raise ValueError("Daemon not running (PID file not found).")

    try:
        with open(pid_file) as f:
            pid = int(f.read().strip())
    except (OSError, ValueError) as e:
        raise ValueError(f"Error reading PID file {pid_file}: {e}") from e

    try:
        os.kill(pid, signal.SIGTERM)
        return f"Sent SIGTERM to daemon (PID: {pid})."
    except ProcessLookupError as e:
        pid_file.unlink(missing_ok=True)
        raise ValueError("Daemon not running.") from e
    except Exception as e:
        raise ValueError(f"Error stopping daemon (PID: {pid}): {e}") from e
