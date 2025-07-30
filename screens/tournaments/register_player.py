# screens/tournament_screens/register_player_screen.py
"""
Screen for registering players to a tournament.
"""
from screens.base_screen import BaseScreen
from typing import List


class RegisterPlayerScreen(BaseScreen):
    """
    Handles the user interface for registering players to a tournament.
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_players_for_registration(available_players: List[dict], tournament_players: List[any]) -> List[str]:
        """
        Displays available players and prompts user to select players to register.
        Returns a list of selected player IDs.
        """
        registered_ids = {p.player_id for p in tournament_players}
        unregistered_players = [p for p in available_players if p['player_id'] not in registered_ids]

        if not unregistered_players:
            print("\nAll available players are already registered for this tournament.")
            return []

        print("\n--- Register Players to Tournament ---")
        print("Available Players (from clubs):")
        for i, player_data in enumerate(unregistered_players):
            print(
                f"{i + 1}. {player_data.get('first_name')} {player_data.get('last_name')} (ELO: {player_data.get('elo_rating')})")

        print("\nEnter numbers of players to register (comma-separated), or 'd' when done.")
        selected_player_ids = []
        while True:
            user_input = input("Selection: ").strip().lower()
            if user_input == 'd':
                break

            try:
                indices = [int(x.strip()) - 1 for x in user_input.split(',')]
                for index in indices:
                    if 0 <= index < len(unregistered_players):
                        player_id = unregistered_players[index]['player_id']
                        if player_id not in selected_player_ids:  # Avoid duplicates
                            selected_player_ids.append(player_id)
                    else:
                        print(f"Warning: Invalid number {index + 1} skipped.")
            except ValueError:
                print("Invalid input. Please enter numbers separated by commas, or 'd'.")

        return selected_player_ids