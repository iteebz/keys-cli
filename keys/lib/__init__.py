"""Library utilities for system integration."""

from .clipboard import get_clipboard, paste, set_clipboard
from .renderer import PromptRenderer

# Daemon is imported lazily to avoid pynput X display issues in testing
__all__ = ["get_clipboard", "set_clipboard", "paste", "Daemon", "PromptRenderer"]


def __getattr__(name):
    """Lazy import for Daemon to avoid X display requirements during testing."""
    if name == "Daemon":
        from .daemon import Daemon

        return Daemon
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
