# data/make_tournament.py
"""
Script to generate dummy tournament data (JSON files) in the 'data/tournaments'
directory for testing and initial setup.
"""
import json
import os
import datetime

def generate_dummy_tournament(tournament_name, location, start_date, end_date, num_players=8):
    """Generates a single dummy tournament JSON."""
    tournament_data = {
        "name": tournament_name,
        "location": location,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "current_round": 0,
        "rounds": [],
        "players": [], # Players will be registered via the application normally
        "status": "created" # or 'in_progress', 'finished'
    }

    # Example for initial players (usually registered through app)
    for i in range(num_players):
        tournament_data["players"].append({
            "player_id": f"dummy_player_{i+1}",
            "first_name": f"Player{i+1}",
            "last_name": "Dummy",
            "date_of_birth": "2000-01-01",
            "elo_rating": 1500,
            "tournament_points": 0
        })

    return tournament_data

def main():
    tournaments_dir = "data/tournaments"
    os.makedirs(tournaments_dir, exist_ok=True)

    # Example 1
    t1_data = generate_dummy_tournament(
        "Summer Blitz", "Online",
        datetime.date(2025, 7, 10), datetime.date(2025, 7, 12), num_players=8
    )
    t1_path = os.path.join(tournaments_dir, "summer_blitz.json")
    with open(t1_path, 'w') as f:
        json.dump(t1_data, f, indent=4)
    print(f"Generated: {t1_path}")

    # Example 2
    t2_data = generate_dummy_tournament(
        "Winter Classic", "New York",
        datetime.date(2025, 12, 1), datetime.date(2025, 12, 5), num_players=16
    )
    t2_path = os.path.join(tournaments_dir, "winter_classic.json")
    with open(t2_path, 'w') as f:
        json.dump(t2_data, f, indent=4)
    print(f"Generated: {t2_path}")

if __name__ == "__main__":
    main()