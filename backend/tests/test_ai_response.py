from app.ai.llm import sanitize_response


def test_sanitize_response_keeps_bold_heading_and_cleans_emoji():
    raw = """Here is the summary.
### Overview
**Key finding**: this repo is mostly Python and React.
✨ This is a nice result.
"""

    cleaned = sanitize_response(raw)

    assert "**Key finding**" in cleaned
    assert "### Overview" in cleaned
    assert "✨" not in cleaned
    assert "Key finding" in cleaned
