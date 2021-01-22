"""collection of functions for news-sentiment"""


def validate_url(text):
    """checks whether url is valid"""

    # see if there's between 1 or 2 dots
    dot_position = text.count(".")
    if not 0 < dot_position < 3:
        return False

    return True