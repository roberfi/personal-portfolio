from __future__ import annotations

import markdown
from bs4 import BeautifulSoup


def markdown_to_plaintext(text: str) -> str:
    """Convert markdown to plain text.

    Args:
        text: The markdown text to convert.

    Returns:
        The plain text representation of the markdown.
    """
    soup = BeautifulSoup(markdown.markdown(text), "html.parser")
    return soup.get_text(separator=" ", strip=True)
