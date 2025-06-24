import re

def parse_duration_to_minutes(duration: str) -> int:
    """
    Converts a string (e.g., "1h10", "12 min", "1 h") to minutes.
    Input:
        duration (str): The duration to convert, formatted like "1h10", "12 min", "1 h", etc.
    Output:
        int: The duration in minutes.
    """
    duration = duration.lower().replace(" ", "")
    hours = 0
    minutes = 0

    # Search for hours (e.g., 1h, 2h, 1h30)
    match_hours = re.search(r'(\d+)h', duration)
    if match_hours:
        hours = int(match_hours.group(1))

    # Search for minutes (e.g., 10min, 45)
    match_minutes = re.search(r'(\d+)(?:min)?$', duration)
    if match_minutes:
        minutes = int(match_minutes.group(1))

    return hours * 60 + minutes


if __name__ == "__main__":
    try:
        assert parse_duration_to_minutes("1h10") == 70
        assert parse_duration_to_minutes("12 min") == 12
        assert parse_duration_to_minutes("1 h") == 60
        assert parse_duration_to_minutes("2h 30") == 150
        assert parse_duration_to_minutes("45") == 45
        assert parse_duration_to_minutes("3h") == 180
    except AssertionError:
        print("Tests : ❌")
    else:
        print("Tests : ✅")
