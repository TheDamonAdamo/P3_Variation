"""
This module defines the TournamentManager class, responsible for managing
tournament data, including creation, loading, and saving tournaments
to JSON files, as per the project specifications.
It ensures data persistence and synchronization with in-memory objects.
"""

from typing import List, Optional, Any, Dict
from models.tournament import Tournament  # Assuming tournament.py is in the same 'models' package
from datetime import datetime
import json
import os

class TournamentManager:
    """
    Manages the creation, storage, and retrieval of Tournament objects.

    This manager handles reading from and writing to JSON files located in
    the 'data/tournaments' directory, ensuring data persistence for tournaments.
    It adheres to the single-responsibility principle by focusing solely on
    tournament data management.
    """

    def __init__(self, storage_directory: str = "data/tournaments"):
        """
        Initializes the TournamentManager.

        Args:
            storage_directory (str): The path to the directory where tournament
                                     JSON files are stored.
        """
        self.storage_directory = storage_directory
        self._ensure_storage_directory_exists()
        # Tournaments are loaded on demand or when getting all tournaments
        # to ensure the latest state from disk.

    def _ensure_storage_directory_exists(self):
        """Ensures the directory for tournament storage files exists."""
        if not os.path.exists(self.storage_directory):
            os.makedirs(self.storage_directory)

    def _get_tournament_file_path(self, tournament_name: str) -> str:
        """
        Generates the file path for a specific tournament's JSON data.

        Args:
            tournament_name (str): The name of the tournament.

        Returns:
            str: The full path to the tournament's JSON file.
        """
        # Sanitize the name to be filesystem-friendly
        # Replace spaces with underscores and remove non-alphanumeric characters
        safe_name = "".join(c for c in tournament_name if c.isalnum() or c in ('_', '-')).strip()
        safe_name = safe_name.replace(' ', '_')
        return os.path.join(self.storage_directory, f"{safe_name}.json")

    def _load_all_tournaments(self) -> List[Tournament]:
        """
        Loads all tournament data from JSON files in the storage directory.
        This method is called when `get_all_tournaments` or `get_tournament_by_name`
        is invoked to ensure the in-memory list is always synchronized with the files.

        Returns:
            List[Tournament]: A list of Tournament objects loaded from files.
        """
        loaded_tournaments = []
        if not os.path.exists(self.storage_directory):
            return loaded_tournaments

        for filename in os.listdir(self.storage_directory):
            if filename.endswith(".json"):
                filepath = os.path.join(self.storage_directory, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, dict):
                            loaded_tournaments.append(Tournament.from_dict(data))
                        # No need for 'elif isinstance(data, list)' as per project spec
                        # and single tournament per file assumption.
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode JSON from {filepath}. Skipping file.")
                except KeyError as e:
                    print(f"Warning: Missing key {e} in JSON from {filepath}. Skipping file.")
                except Exception as e:
                    print(f"An unexpected error occurred loading tournament from {filepath}: {e}")
        return loaded_tournaments

    def _save_tournament(self, tournament: Tournament):
        """
        Saves a single Tournament object to its corresponding JSON file.
        This method is called whenever a tournament's data is modified.

        Args:
            tournament (Tournament): The Tournament object to save.
        """
        filepath = self._get_tournament_file_path(tournament.name)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(tournament.to_dict(), f, indent=4)
        except Exception as e:
            print(f"Error saving tournament {tournament.name} to {filepath}: {e}")

    def create_tournament(self,
                          name: str,
                          venue: str,
                          start_date_str: str, # Expecting 'DD-MM-YYYY'
                          end_date_str: str,   # Expecting 'DD-MM-YYYY'
                          num_rounds: int,
                          description: str = "") -> Optional[Tournament]:
        """
        Creates a new tournament, adds it to the manager's list, and saves it to a JSON file.

        Args:
            name (str): The name of the tournament.
            venue (str): The venue of the tournament.
            start_date_str (str): The start date string (e.g., '21-12-2022').
            end_date_str (str): The end date string (e.g., '23-12-2022').
            num_rounds (int): The total number of rounds.
            description (str, optional): Tournament description. Defaults to "".

        Returns:
            Optional[Tournament]: The newly created Tournament object, or None if creation fails
                                  (e.g., tournament name already exists or invalid date format).
        """
        # Reload all tournaments to check for existing name
        existing_tournaments = self._load_all_tournaments()
        if any(t.name == name for t in existing_tournaments):
            print(f"Error: Tournament with name '{name}' already exists.")
            return None

        try:
            # Dates are now in DD-MM-YYYY format as per the sample JSON
            start_date = datetime.strptime(start_date_str, '%d-%m-%Y')
            end_date = datetime.strptime(end_date_str, '%d-%m-%Y')
        except ValueError as e:
            print(f"Error: Invalid date format. Please use 'DD-MM-YYYY'. Details: {e}")
            return None

        new_tournament = Tournament(
            name=name,
            venue=venue,
            start_date=start_date,
            end_date=end_date,
            num_rounds=num_rounds,
            current_round=0, # Tournament starts at round 0 (not started)
            completed=False,
            finished=False,
            players=[], # No players registered initially
            rounds=[], # No rounds generated initially
            description=description
        )
        self._save_tournament(new_tournament) # Save the new tournament immediately
        print(f"Tournament '{name}' created and saved.")
        return new_tournament

    def get_all_tournaments(self) -> List[Tournament]:
        """
        Returns a list of all managed tournaments, sorted by descending starting date.
        This method reloads all tournaments from disk to ensure the most current data.
        """
        self.tournaments = self._load_all_tournaments()
        # Sort by start_date in descending order (most recent first)
        return sorted(self.tournaments, key=lambda t: t.start_date, reverse=True)

    def get_tournament_by_name(self, name: str) -> Optional[Tournament]:
        """
        Finds and returns a tournament by its name.
        This method reloads all tournaments to ensure it reflects the latest file system state.

        Args:
            name (str): The name of the tournament to find.

        Returns:
            Optional[Tournament]: The Tournament object if found, None otherwise.
        """
        self.tournaments = self._load_all_tournaments() # Ensure in-memory is synced
        for tournament in self.tournaments:
            if tournament.name == name:
                return tournament
        return None

    def update_tournament(self, tournament: Tournament) -> bool:
        """
        Updates an existing tournament's data and saves changes to its JSON file.
        This method assumes the tournament object passed has been modified and
        needs to be persisted. It uses the tournament's name to identify the file.

        Args:
            tournament (Tournament): The Tournament object with updated data.
                                     It must have a 'name' that matches an existing tournament.

        Returns:
            bool: True if the tournament was updated and saved, False otherwise.
        """
        # Directly save the provided tournament object.
        # It's assumed that the calling code retrieved this object via get_tournament_by_name
        # or created it, and is now passing it back after modifications.
        filepath = self._get_tournament_file_path(tournament.name)
        if os.path.exists(filepath):
            self._save_tournament(tournament)
            print(f"Tournament '{tournament.name}' updated and saved.")
            return True
        else:
            print(f"Warning: Tournament '{tournament.name}' file not found for update. "
                  "Perhaps it was deleted or the name changed unexpectedly.")
            return False

    def delete_tournament(self, tournament_name: str) -> bool:
        """
        Deletes a tournament by its name and removes its corresponding JSON file.

        Args:
            tournament_name (str): The name of the tournament to delete.

        Returns:
            bool: True if the tournament was deleted, False otherwise.
        """
        filepath = self._get_tournament_file_path(tournament_name)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                print(f"Tournament '{tournament_name}' and its file deleted successfully.")
                return True
            except OSError as e:
                print(f"Error deleting file for tournament '{tournament_name}': {e}")
                return False
        else:
            print(f"Tournament '{tournament_name}' file not found. Nothing to delete.")
            return False

