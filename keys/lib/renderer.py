"""Template rendering for prompt files."""

from datetime import datetime


class PromptRenderer:
    """Renders prompt templates with variable substitution."""

    def render(self, template: str, clipboard: str = "") -> str:
        """Render a prompt template with available variables.

        Variables:
            {clipboard} - Current clipboard contents
            {date} - Current date (YYYY-MM-DD)
            {time} - Current time (HH:MM:SS)

        Args:
            template: The prompt template string
            clipboard: Clipboard contents for substitution

        Returns:
            Rendered prompt with variables substituted
        """
        now = datetime.now()
        variables = {
            "clipboard": clipboard,
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
        }

        result = template
        for key, value in variables.items():
            result = result.replace(f"{{{key}}}", value)

        return result
