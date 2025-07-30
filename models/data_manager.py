# commands/models/data_manager.py
"""
Manages persistence operations (loading and saving) for tournament-related data (Tournaments, Players, etc.).
This acts as the utility for data management.
"""
import json
import os
from .tournament import Tournament
from .player import Player # Assuming Player model might also be saved/loaded independently

class DataManager:
    """Handles reading from and writing to JSON files for tournament data."""

    def __init__(self, tournaments_dir="data/tournaments", clubs_dir="data/clubs"):
        self.tournaments_dir = tournaments_dir
        self.clubs_dir = clubs_dir
        os.makedirs(self.tournaments_dir, exist_ok=True)
        os.makedirs(self.clubs_dir, exist_ok=True) # Ensure clubs dir exists for loading players

    def save_tournament(self, tournament: Tournament):
        """Saves a Tournament object to a JSON file."""
        file_name = f"{tournament.name.lower().replace(' ', '_')}.json"
        file_path = os.path.join(self.tournaments_dir, file_name)
        with open(file_path, 'w') as f:
            json.dump(tournament.to_dict(), f, indent=4)
        print(f"Tournament '{tournament.name}' saved successfully.")

    def load_tournament(self, name: str) -> Tournament | None:
        """Loads a Tournament object from a JSON file."""
        file_name = f"{name.lower().replace(' ', '_')}.json"
        file_path = os.path.join(self.tournaments_dir, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
            return Tournament.from_dict(data)
        return None

    def load_all_tournaments(self) -> list[Tournament]:
        """Loads all tournament objects from the tournaments directory."""
        tournaments = []
        for filename in os.listdir(self.tournaments_dir):
            if filename.endswith(".json"):
                tournament_name = os.path.splitext(filename)[0].replace('_', ' ').title()
                tournament = self.load_tournament(tournament_name)
                if tournament:
                    tournaments.append(tournament)
        return tournaments

    def load_all_players_from_clubs(self) -> list[dict]:
        """
        Loads all player data from existing club JSON files.
        Returns a flat list of player dictionaries.
        """
        all_players = []
        for filename in os.listdir(self.clubs_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(self.clubs_dir, filename)
                try:
                    with open(file_path, 'r') as f:
                        club_data = json.load(f)
                        if 'players' in club_data and isinstance(club_data['players'], list):
                            all_players.extend(club_data['players'])
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from {filename}")
                except Exception as e:
                    print(f"An error occurred loading {filename}: {e}")
        return all_players

    # Potentially add methods for saving/loading individual Player objects if needed outside of tournament context