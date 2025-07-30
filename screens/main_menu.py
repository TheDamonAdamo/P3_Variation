# screens/main_menu_screen.py
"""
This module defines the main menu screen for the entire application,
allowing navigation to club management, player management, and tournament management.
"""
from .base_screen import BaseScreen # Assuming screens/base.py provides a BaseScreen

class MainMenu(BaseScreen):
    """
    Displays the main menu of the application and handles user navigation.
    """
    def __init__(self):
        super().__init__()

    def display(self):
        """Displays the main menu options."""
        print("\n--- Main Menu ---")
        print("1. Manage Clubs")
        print("2. Manage Players")
        print("3. Manage Tournaments")
        print("4. Exit")
        return self.get_user_input("Enter your choice: ")

    @staticmethod
    def display_tournament_menu():
        """Displays the tournament-specific menu options."""
        print("\n--- Tournament Management Menu ---")
        print("1. Create New Tournament")
        print("2. Load and Manage Existing Tournament")
        print("3. Back to Main Menu")
        return input("Enter your choice: ").strip()

    @staticmethod
    def display_club_menu():
        """Placeholder for club menu display (assuming clubs.py will use this)"""
        print("\n--- Club Management Menu ---")
        print("1. Create Club")
        print("2. List Clubs")
        print("3. Manage Club Players")
        print("4. Delete Club")
        print("5. View Club")
        print("6. Back to Main Menu")
        return input("Enter your choice: ").strip()

    @staticmethod
    def display_player_menu():
        """Placeholder for player menu display (assuming players.py will use this)"""
        print("\n--- Player Management Menu ---")
        print("1. Create Player")
        print("2. List Players")
        print("3. Update Player ELO") # Example
        print("4. Back to Main Menu")
        return input("Enter your choice: ").strip()