"""Configuration management."""

from pathlib import Path
from typing import Any

import yaml


class Config:
    """Load and parse keys configuration."""

    def __init__(self, path: Path | None = None):
        self.path = path or Path.home() / ".keys" / "config.yaml"
        self._data = self._load()

    def _load(self) -> dict[str, Any]:
        """Load YAML config file, create if missing."""
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            default_data = {
                "prompts_dir": str(Path.home() / ".keys" / "prompts"),
                "hotkeys": {},
            }
            with open(self.path, "w") as f:
                yaml.safe_dump(default_data, f)
            return default_data

        with open(self.path) as f:
            data = yaml.safe_load(f)
            return data or {}

    def save(self) -> None:
        """Write config back to file."""
        with open(self.path, "w") as f:
            yaml.safe_dump(self._data, f)

    @property
    def prompts_dir(self) -> Path:
        """Get prompts directory."""
        path_str = self._data.get("prompts_dir", str(Path.home() / ".keys" / "prompts"))
        return Path(path_str).expanduser()

    def set_prompts_dir(self, path: Path) -> None:
        """Set prompts directory."""
        self._data["prompts_dir"] = str(path.expanduser())
        self.save()

    @property
    def hotkeys(self) -> dict[str, str]:
        """Get hotkeys configuration (key -> prompt_name mapping)."""
        return self._data.get("hotkeys", {})

    def get_hotkey(self, key: str) -> str | None:
        """Get prompt name for a hotkey."""
        return self.hotkeys.get(key)

    def add_hotkey(self, key: str, prompt_name: str) -> None:
        """Add a hotkey binding."""
        self._data.setdefault("hotkeys", {})[key] = prompt_name
        self.save()

    def remove_hotkey(self, key: str) -> None:
        """Remove a hotkey binding."""
        if "hotkeys" in self._data and key in self._data["hotkeys"]:
            del self._data["hotkeys"][key]
            self.save()

    def load_prompt(self, name: str) -> str:
        """Load prompt content from file."""
        prompt_path = self.prompts_dir / name
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt not found: {prompt_path}")
        return prompt_path.read_text().strip()

    @property
    def pid_file_path(self) -> Path:
        """Get the path for the daemon PID file."""
        return self.path.parent / "keys_daemon.pid"
