# screens/tournament_screens/advance_round_screen.py
"""
Screen for displaying matches of the current round when advancing.
"""
from screens.base_screen import BaseScreen
from models.round import Round

class AdvanceRoundScreen(BaseScreen):
    """
    Handles the user interface for displaying round information and matches.
    """
    def __init__(self):
        super().__init__()

    @staticmethod
    def display_round_matches(current_round: Round):
        """Displays details and matches for the given round."""
        print(f"\n--- {current_round.name} Matches ({current_round.start_time}) ---")
        if not current_round.matches:
            print("No matches generated for this round yet.")
            return

        for i, match in enumerate(current_round.matches):
            p1_name = f"{match.player1.first_name} {match.player1.last_name}"
            p2_name = f"{match.player2.first_name} {match.player2.last_name}"
            result_str = f"Result: {match.result[0]} - {match.result[1]}" if match.result else "Result: Pending"
            print(f"{i + 1}. {p1_name} vs {p2_name} - {result_str}")
        print("-" * 30)

    @staticmethod
    def confirm_advance_round():
        """Asks for user confirmation before advancing."""
        return BaseScreen.get_user_input("Advance to the next round? (yes/no): ").lower() == 'yes'