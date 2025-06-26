import re


def parse_duration_to_minutes(duration: str) -> int:
    """Converts a string (e.g., "1h10", "12 min", "1 h") to minutes.

    Input:
        duration (str): The duration to convert formatted like "1h10", "12 min", "1 h"
    Output:
        int: The duration in minutes.
    """
    duration = duration.lower().replace(" ", "")
    hours = 0
    minutes = 0

    # Search for hours (e.g., 1h, 2h, 1h30)
    match_hours = re.search(r"(\d+)h", duration)
    if match_hours:
        hours = int(match_hours.group(1))

    # Search for minutes (e.g., 10min, 45)
    match_minutes = re.search(r"(\d+)(?:min)?$", duration)
    if match_minutes:
        minutes = int(match_minutes.group(1))

    return hours * 60 + minutes
