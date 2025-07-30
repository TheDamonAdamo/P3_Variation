# screens/tournament_screens/enter_results_screen.py
"""
Screen for entering match results for the current round.
"""
from screens.base_screen import BaseScreen
from models.round import Round
from typing import Dict


class EnterResultsScreen(BaseScreen):
    """
    Handles the user interface for entering match results.
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_match_results(matches: list[any]) -> Dict[str, str]:
        """
        Prompts the user to enter results for each match in a list.
        Returns a dictionary mapping match_id to winner_id (or "draw").
        """
        results = {}
        print("\n--- Enter Match Results ---")

        for match in matches:
            if match.result is not None:
                print(
                    f"Match: {match.player1.first_name} vs {match.player2.first_name} (Already {match.result[0]} - {match.result[1]})")
                continue  # Skip if already has a result

            while True:
                print(
                    f"\nMatch: {match.player1.first_name} {match.player1.last_name} (Player 1) vs {match.player2.first_name} {match.player2.last_name} (Player 2)")
                result_input = input(
                    f"Enter winner (1 for {match.player1.first_name}, 2 for {match.player2.first_name}, d for draw): ").strip().lower()

                if result_input == '1':
                    results[match.match_id] = match.player1.player_id
                    break
                elif result_input == '2':
                    results[match.match_id] = match.player2.player_id
                    break
                elif result_input == 'd':
                    results[match.match_id] = "draw"
                    break
                else:
                    print("Invalid input. Please enter '1', '2', or 'd'.")
        return results