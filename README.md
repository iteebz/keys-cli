# Keys: Hotkey-Driven Prompt Snippets

`keys` is a system-wide hotkey manager for prompt templates. Press a hotkey anywhere, and it pastes your prompt into the active window—perfect for working with AI assistants, chat interfaces, or any text input.

Think **Alfred** or **TextExpander** for AI prompts.

## Quick Start

```bash
# Point to any folder with markdown files
keys prompts ./prompts

# Bind hotkeys to your prompts
keys add ctrl+shift+e explain.md
keys add ctrl+shift+f fix.md

# Start the daemon
keys start

# Now press your hotkeys anywhere!
```

## How It Works

1. **Press hotkey** → Reads your clipboard
2. **Loads prompt template** → Replaces `{clipboard}` with your content
3. **Pastes into active window** → Works in browser, terminal, IDE, anywhere
4. **Restores clipboard** → Your original clipboard is preserved

No LLM execution. No API calls. Just templates + hotkeys + paste.

## Installation

```bash
pip install keys-cli
```

Or with poetry:
```bash
poetry add keys-cli
```

## Setup

### 1. Create Prompt Templates

Any markdown file becomes a prompt:

**prompts/explain.md:**
```markdown
Explain this code step by step:

{clipboard}
```

**prompts/fix.md:**
```markdown
Fix any issues in this code:

{clipboard}
```

**prompts/commit.md:**
```markdown
Write a clear, concise commit message for these changes:

{clipboard}
```

### 2. Point Keys at Your Prompts

```bash
# Use prompts from any project
cd ~/my-project
keys prompts ./prompts

# Or use a global prompts directory
keys prompts ~/my-prompts
```

### 3. Bind Hotkeys

```bash
keys add ctrl+shift+e explain.md
keys add ctrl+shift+f fix.md
keys add ctrl+shift+c commit.md
keys list
```

### 4. Start the Daemon

```bash
keys start
```

### 5. Use Anywhere

Copy code → Press hotkey → Prompt appears in active window → Submit to your AI assistant

## Commands

```bash
keys prompts <path>              # Point to a prompts directory
keys add <key> <prompt>          # Bind a hotkey to a prompt
keys list                        # Show all bindings
keys remove <key>                # Remove a binding
keys show <prompt>               # View a prompt's content
keys start                       # Start the daemon
keys stop                        # Stop the daemon
```

## Template Variables

Prompts support simple variable substitution:

- `{clipboard}` - Current clipboard contents
- `{date}` - Current date (YYYY-MM-DD)
- `{time}` - Current time (HH:MM:SS)

**Example:**
```markdown
Review this code written on {date}:

{clipboard}
```

## Key Combinations

Supported modifiers: `ctrl`, `shift`, `alt`, `cmd` (macOS), `win` (Windows), `option` (macOS alias for alt)

Examples:
- `ctrl+shift+f` - Cross-platform
- `cmd+shift+j` - macOS
- `win+alt+x` - Windows
- `option+shift+k` - macOS

## Configuration

Config file: `~/.keys/config.yaml`

```yaml
prompts_dir: ~/my-project/prompts

hotkeys:
  ctrl+shift+e: explain.md
  ctrl+shift+f: fix.md
  cmd+shift+c: commit.md
```

## Use Cases

### AI Coding Assistants
Copy code → Hotkey → Prompt appears in Claude, ChatGPT, Cursor, etc.

### Project-Specific Prompts
Each project gets its own `prompts/` folder with relevant templates. Point `keys` at it and bind your hotkeys.

### Shared Prompt Libraries
Share prompts via git. Clone → `keys prompts ./shared-prompts` → Done.

### Markdown-Driven Workflows
Already using markdown for context injection? Now add hotkeys to those files.

## Requirements

- **Python 3.10+**
- **macOS**: `osascript`, `pbcopy`, `pbpaste` (built-in)
- **Linux**: `xclip` and `xdotool`
- **Windows**: Not yet implemented

Install Linux dependencies:
```bash
# Debian/Ubuntu
sudo apt install xclip xdotool

# Arch
sudo pacman -S xclip xdotool
```

## Why Keys?

- **No vendor lock-in** - Works with any AI interface (web, CLI, IDE)
- **No LLM execution** - Just templates and hotkeys
- **Portable prompts** - Markdown files you can version control
- **Project-aware** - Point at different prompt folders per project
- **Zero magic** - Simple, transparent, reference-grade code

## Example Workflow

```bash
# Clone a repo with prompts
cd ~/my-app

# Point keys at the prompts folder
keys prompts ./prompts

# Bind some hotkeys
keys add ctrl+shift+e explain.md
keys add ctrl+shift+r refactor.md
keys add ctrl+shift+t test.md

# Start the daemon
keys start

# Now you can:
# 1. Copy code in your editor
# 2. Switch to ChatGPT/Claude web interface
# 3. Press ctrl+shift+e
# 4. Prompt appears with your code ready to submit
```

## License

MIT
