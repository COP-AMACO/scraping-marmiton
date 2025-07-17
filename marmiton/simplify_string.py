import unicodedata

REPLACEMENTS = {
    "œ": "oe",
    "æ": "ae",
    " ": "-",
    "'": "-",
}


def simplify_string(text):
    """Simplifies a string by removing accents, ligatures, apostrophes and converting to
    lowercase.

    Args:
        text (str): The string to simplify.

    Returns:
        str: The simplified string or empty if input is empty.
    """
    # Convert text to lowercase
    text = text.lower()

    # Replace certain characters with their simplified versions
    for old_char, new_char in REPLACEMENTS.items():
        text = text.replace(old_char, new_char)

    # Decompose accented characters into base + accent: é becomes e + ́
    normalized_text = unicodedata.normalize("NFKD", text)
    # Filter and keep only non-accented characters
    simplified_text = "".join(
        c for c in normalized_text if not unicodedata.combining(c)
    )

    return simplified_text
