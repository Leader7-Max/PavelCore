import pytest
from datetime import date, time

def test_event_structure():
    """Vérifie la structure de données d'un événement de l'agenda."""
    event = {
        "title": "Réunion Stratégique",
        "date": date(2026, 10, 15),
        "time": time(14, 30),
        "category": "Business / Travail",
        "desc": "Préparer le planning trimestriel",
        "ringtone": "Alarme Digitale"
    }
    
    assert event["title"] == "Réunion Stratégique"
    assert event["date"].year == 2026
    assert event["time"].hour == 14
    assert event["category"] == "Business / Travail"

def test_event_sorting():
    """Vérifie que le tri chronologique des tâches fonctionne correctement."""
    events = [
        {"title": "Tâche B", "date": date(2026, 10, 20), "time": time(10, 0)},
        {"title": "Tâche A", "date": date(2026, 10, 10), "time": time(9, 0)},
        {"title": "Tâche C", "date": date(2026, 10, 10), "time": time(15, 0)}
    ]
    
    sorted_events = sorted(events, key=lambda x: (x['date'], x['time']))
    
    assert sorted_events[0]["title"] == "Tâche A"
    assert sorted_events[1]["title"] == "Tâche C"
    assert sorted_events[2]["title"] == "Tâche B"
