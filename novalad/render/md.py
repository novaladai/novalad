import markdown
from IPython.display import display, Markdown

def render_markdown(md_text: str | dict) -> None:
    """
    Renders a Markdown string in a Jupyter Notebook or prints the HTML in the console as a fallback.

    Args:
        md_text (str | dict): Markdown content as a string, or a dictionary in the form:
            {
                "data": {
                    "markdown": "<markdown_text>"
                }
            }

    Returns:
        None

    Notes:
        - Uses IPython display for rich Markdown rendering in Jupyter.
        - Falls back to plain HTML rendering via `markdown` library if display fails (e.g., non-notebook environments).
    """
    try:
        # Extract markdown text if a dict is passed
        if isinstance(md_text, dict):
            md_text = md_text.get("data", {}).get("markdown", "")

        if not isinstance(md_text, str):
            raise ValueError("Input must be a markdown string or a valid dictionary structure.")

        display(Markdown(md_text))  # Rich rendering in Jupyter Notebook
    except Exception as e:
        print(markdown.markdown(md_text))  # Console-safe HTML rendering
