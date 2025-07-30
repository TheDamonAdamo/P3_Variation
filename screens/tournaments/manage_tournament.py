# screens/tournaments/manage_tournament.py
"""
Screen for managing an existing tournament (register players, advance rounds, enter results, view reports).
"""
from screens.base_screen import BaseScreen
from typing import List, Dict

class ManageTournamentScreen(BaseScreen):
    """
    Handles the user interface for managing an existing tournament.
    """
    def __init__(self):
        super().__init__()

    @staticmethod
    def select_tournament(tournaments: List[any]) -> str | None:
        """
        Displays a list of tournaments and prompts the user to select one by name.
        """
        if not tournaments:
            print("\nNo tournaments available.")
            return None

        print("\n--- Select Tournament to Manage ---")
        for i, tournament in enumerate(tournaments):
            print(f"{i + 1}. {tournament.name} ({tournament.venue}) - Completed: {tournament.completed}")

        while True:
            choice = input("Enter the number of the tournament, or 'b' to go back: ").strip().lower()
            if choice == 'b':
                return None
            try:
                index = int(choice) - 1
                if 0 <= index < len(tournaments):
                    return tournaments[index].name
                else:
                    print("Invalid number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number or 'b'.")

    @staticmethod
    def display_management_menu(tournament_name: str):
        """Displays options for managing a specific tournament."""
        print(f"\n--- Managing Tournament: {tournament_name} ---")
        print("1. Register Players")
        print("2. Start/Advance Round")
        print("3. Enter Match Results")
        print("4. View Tournament Report")
        print("5. Back to Tournament Menu")
        return BaseScreen.get_user_input("Enter your choice: ")