"""Command-line interface for keys."""

import sys
from pathlib import Path

import typer

from . import api

app = typer.Typer(help="System-wide hotkey CLI for LLM integration.")


@app.command()
def prompts(
    path: str = typer.Argument(..., help="Path to prompts directory"),
    config: Path | None = typer.Option(None, "--config", "-c", help="Config file path"),
) -> None:
    """Set the prompts directory."""
    try:
        message = api.set_prompts_dir(Path(path), config)
        typer.echo(f"✓ {message}")
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from e


@app.command()
def add(
    key: str = typer.Argument(
        ...,
        help="Key combination. Supports: ctrl, shift, alt, cmd (macOS), win/option (Windows). Example: ctrl+shift+f, cmd+shift+j, win+alt+x",
    ),
    prompt_name: str = typer.Argument(..., help="Prompt file name (without extension)"),
    config: Path | None = typer.Option(None, "--config", "-c", help="Config file path"),
) -> None:
    """Register a key binding to a prompt."""
    try:
        message = api.add_key(key, prompt_name, config)
        typer.echo(f"✓ {message}")
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from e


@app.command()
def list(
    config: Path | None = typer.Option(None, "--config", "-c", help="Config file path"),
) -> None:
    """List all key bindings."""
    keys = api.list_keys(config)

    if not keys:
        typer.echo("No keys configured.")
        return

    for key, prompt_name in keys:
        typer.echo(f"{key:20} → {prompt_name}")


@app.command()
def remove(
    key: str = typer.Argument(..., help="Key combination to remove"),
    config: Path | None = typer.Option(None, "--config", "-c", help="Config file path"),
) -> None:
    """Remove a key binding."""
    try:
        message = api.remove_key(key, config)
        typer.echo(f"✓ {message}")
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from e


@app.command()
def show(
    prompt_name: str = typer.Argument(..., help="Prompt file name (without extension)"),
    input_text: str | None = typer.Option(None, "--input", "-i", help="Input text"),
    config: Path | None = typer.Option(None, "--config", "-c", help="Config file path"),
) -> None:
    """Show prompt content or run as CLI passthrough."""
    try:
        prompt_content = api.get_prompt(prompt_name, config)
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from e

    if input_text is None:
        if sys.stdin.isatty():
            typer.echo(prompt_content)
            return
        input_text = sys.stdin.read().strip()
        if not input_text:
            typer.echo(prompt_content)
            return

    full_prompt = f"{prompt_content}\n\n{input_text}"
    typer.echo(f"Sending to claude: {full_prompt}", err=True)


@app.command()
def start(
    config: Path | None = typer.Option(None, "--config", "-c", help="Config file path"),
) -> None:
    """Start the hotkey daemon."""
    typer.echo("Starting keys daemon...")
    api.start_daemon(config)


@app.command()
def stop(
    config: Path | None = typer.Option(None, "--config", "-c", help="Config file path"),
) -> None:
    """Stop the hotkey daemon."""
    try:
        message = api.stop_daemon(config)
        typer.echo(message)
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from e


if __name__ == "__main__":
    app()
