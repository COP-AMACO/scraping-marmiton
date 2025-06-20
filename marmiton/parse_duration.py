import re

def parse_duration_to_minutes(duration: str) -> int:
    """
    Convertit une chaîne de texte (ex: "1h10", "12 min", "1 h") en minutes.
    Entrée :
        duration (str): La durée à convertir, formatée comme "1h10", "12 min", "1 h", etc.
    Sortie :
        int: La durée en minutes.
    """
    duration = duration.lower().replace(" ", "")  # Nettoyage
    hours = 0
    minutes = 0

    # Cherche les heures (ex: 1h, 2h, 1h30)
    match_hours = re.search(r'(\d+)h', duration)
    if match_hours:
        hours = int(match_hours.group(1))

    # Cherche les minutes (ex: 10min, 45)
    match_minutes = re.search(r'(\d+)(?:min)?$', duration)
    if match_minutes:
        minutes = int(match_minutes.group(1))

    return hours * 60 + minutes


if __name__ == "__main__":
    assert parse_duration_to_minutes("1h10") == 70
    assert parse_duration_to_minutes("12 min") == 12
    assert parse_duration_to_minutes("1 h") == 60
    assert parse_duration_to_minutes("2h 30") == 150
    assert parse_duration_to_minutes("45") == 45
    assert parse_duration_to_minutes("3h") == 180
    print("Tests : ✅")
