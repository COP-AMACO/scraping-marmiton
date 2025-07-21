import re


def extract_id_from_url(image_url):
    """Extracts the numeric ingredient ID from the image URL.

    Args:
        image_url (str): The ingredient image URL

    Returns:
        str|None: Numeric ID extracted from URL or None if extraction is impossible
    """
    if not image_url:
        return None

    # Convert URL to lowercase to avoid case sensitivity issues
    image_url = image_url.lower()
    # Check if the ingredient image is a placeholder
    if "ingredient_default_w300h300.webp" in image_url:
        return None

    # Pattern to extract ID from URL
    # URLs' format are :
    #  - https://assets.afcdn.com/recipe/<RECIPE_ID>/<INGREDIENT_ID>_w300h300.webp
    #  - https://assets.afcdn.com/recipe/<RECIPE_ID>/<INGREDIENT_ID>_w300h300.png
    pattern = r"/(\d+)_w300h300\.(webp|png)$"
    match = re.search(pattern, image_url)
    if match:
        return match.group(1)  # Return the numeric ID
    return None
