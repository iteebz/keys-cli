# Keys: Prompt Hotkey CLI

`keys` is a lightweight CLI tool that binds system-wide hotkeys to prompts and dispatches them to LLM CLIs or other tools. Perfect for rapid text transformation workflows.

## Quick Start

```bash
# Set your prompts directory (e.g., markdown files with prompts)
keys prompts ~/my-prompts

# Register a hotkey
keys add ctrl+shift+f fix.md

# List your keys
keys list

# Show a prompt or pipe text through it
keys show fix.md
echo "bad code" | keys show fix.md
```

## Installation

```bash
pip install keys-cli
```

Or with poetry:
```bash
poetry add keys-cli
```

## Setup

1. **Create a prompts directory** with markdown files:
   ```
   ~/my-prompts/
   ├── fix.md
   ├── commit.md
   └── refactor.md
   ```

2. **Set the prompts directory:**
   ```bash
   keys prompts ~/my-prompts
   ```

3. **Register hotkeys:**
   ```bash
   keys add ctrl+shift+f fix.md
   keys add cmd+shift+j commit.md        # macOS
   keys add win+alt+r refactor.md        # Windows
   ```

4. **Start the daemon:**
   ```bash
   keys start
   ```

5. **Use your hotkeys** - select text anywhere and press your key combination. The text gets piped to your prompt and the result goes to clipboard.

## Commands

```bash
keys prompts <path>              # Set prompts directory
keys add <key> <prompt_name>     # Register a hotkey
keys list                        # Show all hotkeys
keys remove <key>                # Unregister a hotkey
keys show <prompt_name>          # Display prompt content or pipe input
keys start                       # Start the hotkey daemon
keys stop                        # Stop the daemon
```

## Key Combinations

Supports: `ctrl`, `shift`, `alt`, `cmd` (macOS), `win` (Windows), `option` (macOS = alt)

Examples:
- `ctrl+shift+f` - All platforms
- `cmd+shift+j` - macOS
- `win+alt+x` - Windows
- `option+shift+k` - macOS (option = alt)

## Prompt Files

Create simple markdown files with your prompt templates:

**fix.md:**
```markdown
Fix the syntax errors in this code:
```

**commit.md:**
```markdown
Generate a conventional commit message for this code change:
```

The text you select or pipe will be appended to the prompt.

## How It Works

### Daemon Mode (Primary)
1. Run `keys start` in the background
2. Select text anywhere on your system
3. Press your registered hotkey
4. Selected text + prompt gets sent to `claude` CLI
5. Result copied to clipboard

### CLI Mode (Secondary)
Pipe text through prompts directly:
```bash
echo "def foo( ): return 1" | keys show fix.md
```

## Configuration

Config file: `~/.keys/config.yaml`

```yaml
prompts_dir: ~/my-prompts

hotkeys:
  ctrl+shift+f: fix.md
  cmd+shift+j: commit.md
```

That's it. No targets, no actions, no bloat.

## Requirements

- Python 3.10+
- For clipboard support on Linux: `xclip` or `xsel`
- A CLI tool that accepts piped input (e.g., `claude`, `gpt-cli`)

## Why Keys?

- **Simple** - Just prompts + hotkeys. No complex config.
- **Fast** - Pure functions, minimal overhead.
- **Flexible** - Works with any CLI tool, any text editor.
- **Cross-platform** - macOS, Linux, Windows support.

## License

MIT
