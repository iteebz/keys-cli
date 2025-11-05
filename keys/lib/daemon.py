"""Hotkey daemon for system-wide key bindings."""

import os
import signal
import sys
import time

from pynput import keyboard

from ..config import Config
from .clipboard import get_clipboard, paste, set_clipboard
from .renderer import PromptRenderer


class Daemon:
    def __init__(self):
        self.config = Config()
        self.pid_file_path = self.config.pid_file_path
        self.listener = keyboard.GlobalHotKeys(self._build_hotkey_map())
        self._running = False

    def _build_hotkey_map(self):
        """Convert config hotkeys to pynput format.

        Supports: ctrl, shift, alt, cmd (macOS), win (Windows).
        Example: ctrl+shift+f, cmd+option+j, win+alt+x
        """
        mapping = {}
        for hotkey_key, prompt_name in self.config.hotkeys.items():
            pynput_hotkey = (
                hotkey_key.replace("ctrl", "<ctrl>")
                .replace("shift", "<shift>")
                .replace("alt", "<alt>")
                .replace("option", "<alt>")
                .replace("cmd", "<cmd>")
                .replace("win", "<cmd>")
            )
            mapping[pynput_hotkey] = lambda pn=prompt_name: self._handle_hotkey(pn)
        return mapping

    def _handle_hotkey(self, prompt_name):
        """Execute hotkey action: render prompt and paste into active window."""
        try:
            # Save current clipboard
            original_clipboard = get_clipboard()

            # Load and render prompt template
            template = self.config.load_prompt(prompt_name)
            renderer = PromptRenderer()
            rendered = renderer.render(template, clipboard=original_clipboard)

            # Set clipboard to rendered prompt
            set_clipboard(rendered)

            # Small delay to ensure clipboard is set
            time.sleep(0.05)

            # Paste into active window
            paste()

            # Small delay before restoring
            time.sleep(0.05)

            # Restore original clipboard
            set_clipboard(original_clipboard)

        except Exception as e:
            print(f"Error in hotkey handler: {e}", file=sys.stderr)

    def _handle_signal(self, signum, frame):
        """Handle termination signals."""
        print(f"Received signal {signum}. Shutting down daemon...", file=sys.stderr)
        self.stop()

    def run(self):
        """Start listening for hotkeys."""
        if self.pid_file_path.exists():
            print(
                f"Error: Daemon already running. PID file exists at {self.pid_file_path}",
                file=sys.stderr,
            )
            sys.exit(1)

        self.pid_file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.pid_file_path, "w") as f:
            f.write(str(os.getpid()))

        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)

        print(f"Keys daemon started (PID: {os.getpid()}). Listening for hotkeys...")
        self._running = True
        try:
            self.listener.start()
            self.listener.join()
        except Exception as e:
            print(f"Daemon listener error: {e}", file=sys.stderr)
        finally:
            self.stop()

    def stop(self):
        """Stop the hotkey listener and clean up."""
        if self._running:
            print("Stopping hotkey listener...", file=sys.stderr)
            self.listener.stop()
            self._running = False

        if self.pid_file_path.exists():
            self.pid_file_path.unlink()
            print(f"Removed PID file: {self.pid_file_path}", file=sys.stderr)
