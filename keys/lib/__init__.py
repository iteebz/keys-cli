"""Library utilities for system integration."""

from .clipboard import get_selection, set_clipboard
from .daemon import Daemon

__all__ = ["get_selection", "set_clipboard", "Daemon"]
