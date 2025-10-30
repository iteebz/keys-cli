from pathlib import Path

import pytest

from keys.config import Config


@pytest.fixture
def tmp_config_dir(tmp_path):
    """Create a temporary config directory."""
    config_dir = tmp_path / ".keys"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


@pytest.fixture
def prompts_dir(tmp_path):
    """Create a temporary prompts directory."""
    prompts_dir = tmp_path / ".keys" / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    return prompts_dir


def test_config_creates_default_on_first_run(tmp_config_dir):
    """Config should create default file on first run."""
    config_path = tmp_config_dir / "config.yaml"
    config = Config(config_path)

    assert config_path.exists()
    assert config.prompts_dir == Path.home() / ".keys" / "prompts"
    assert config.hotkeys == {}


def test_config_loads_existing_file(tmp_config_dir):
    """Config should load existing config file."""
    config_path = tmp_config_dir / "config.yaml"
    config_path.write_text("""
prompts_dir: /tmp/prompts
hotkeys:
  ctrl+shift+f: fix
  ctrl+shift+c: commit
""")

    config = Config(config_path)
    assert config.prompts_dir == Path("/tmp/prompts")
    assert config.hotkeys == {"ctrl+shift+f": "fix", "ctrl+shift+c": "commit"}


def test_set_prompts_dir(tmp_config_dir, prompts_dir):
    """Config should save prompts directory."""
    config_path = tmp_config_dir / "config.yaml"
    config = Config(config_path)

    config.set_prompts_dir(prompts_dir)
    assert config.prompts_dir == prompts_dir

    reloaded = Config(config_path)
    assert reloaded.prompts_dir == prompts_dir


def test_add_hotkey(tmp_config_dir, prompts_dir):
    """Config should add hotkey binding."""
    config_path = tmp_config_dir / "config.yaml"
    (prompts_dir / "fix").write_text("Fix code")

    config = Config(config_path)
    config.set_prompts_dir(prompts_dir)
    config.add_hotkey("ctrl+shift+f", "fix")

    assert config.hotkeys["ctrl+shift+f"] == "fix"

    reloaded = Config(config_path)
    reloaded.set_prompts_dir(prompts_dir)
    assert reloaded.hotkeys["ctrl+shift+f"] == "fix"


def test_remove_hotkey(tmp_config_dir, prompts_dir):
    """Config should remove hotkey binding."""
    config_path = tmp_config_dir / "config.yaml"
    (prompts_dir / "fix").write_text("Fix code")

    config = Config(config_path)
    config.set_prompts_dir(prompts_dir)
    config.add_hotkey("ctrl+shift+f", "fix")
    config.remove_hotkey("ctrl+shift+f")

    assert "ctrl+shift+f" not in config.hotkeys


def test_load_prompt(tmp_config_dir, prompts_dir):
    """Config should load prompt from file."""
    config_path = tmp_config_dir / "config.yaml"
    prompt_file = prompts_dir / "fix"
    prompt_file.write_text("Fix syntax errors in this code:")

    config = Config(config_path)
    config.set_prompts_dir(prompts_dir)

    content = config.load_prompt("fix")
    assert content == "Fix syntax errors in this code:"


def test_load_prompt_not_found(tmp_config_dir, prompts_dir):
    """Config should raise error for missing prompt."""
    config_path = tmp_config_dir / "config.yaml"
    config = Config(config_path)
    config.set_prompts_dir(prompts_dir)

    with pytest.raises(FileNotFoundError, match="Prompt not found"):
        config.load_prompt("nonexistent")


def test_get_hotkey(tmp_config_dir, prompts_dir):
    """Config should get hotkey binding."""
    config_path = tmp_config_dir / "config.yaml"
    (prompts_dir / "fix").write_text("Fix code")

    config = Config(config_path)
    config.set_prompts_dir(prompts_dir)
    config.add_hotkey("ctrl+shift+f", "fix")

    assert config.get_hotkey("ctrl+shift+f") == "fix"
    assert config.get_hotkey("nonexistent") is None
