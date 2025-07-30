# main.py
"""
Main entry point for the Chess Tournament Management Application.
This script orchestrates the main menu and dispatches to various modules
for club, player, and tournament management.
"""
from models.data_manager import DataManager
from commands.tournaments import TournamentController
from screens.main_menu import MainMenuScreen


# Import existing club and player command modules (if they exist and are to be used)
# from commands.clubs import ClubsManager # Example, adjust based on actual structure
# from commands.players import PlayersManager # Example, adjust based on actual structure

def run_application():
    """Main function to run the application."""
    data_manager = DataManager()
    tournament_controller = TournamentController(data_manager)

    # Initialize managers for existing club/player functionality if needed
    # clubs_manager = ClubsManager(...)
    # players_manager = PlayersManager(...)

    main_menu = MainMenuScreen()

    while True:
        choice = main_menu.display()

        if choice == "1":
            print("\n--- Navigating to Club Management (Existing Functionality) ---")
            # This would call into the existing club management logic, e.g.:
            # commands.clubs.run_club_management(data_manager) # or similar
            # For now, a placeholder
            print("Club management not yet integrated with new main menu.")
            input("Press Enter to continue...")
        elif choice == "2":
            print("\n--- Navigating to Player Management (Existing Functionality) ---")
            # This would call into the existing player management logic, e.g.:
            # commands.players.run_player_management(data_manager) # or similar
            # For now, a placeholder
            print("Player management not yet integrated with new main menu.")
            input("Press Enter to continue...")
        elif choice == "3":
            tournament_controller.run()
        elif choice == "4":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    run_application()