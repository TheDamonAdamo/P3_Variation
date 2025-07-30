# commands/tournaments.py
"""
This module contains the core application logic (controller) for managing tournaments.
It orchestrates interactions between screens (UI) and models (data structures and persistence).
"""

from ..screens.tournaments.create_tournament import CreateTournamentScreen
from ..screens.tournaments.manage_tournament import ManageTournamentScreen
from ..screens.tournaments.register_player import RegisterPlayerScreen
from ..screens.tournaments.advance_round import AdvanceRoundScreen
from ..screens.tournaments.enter_results import EnterResultsScreen
from ..screens.tournaments.tournament_report import TournamentReportScreen
from ..screens.main_menu import MainMenuScreen
from ..models.tournament import Tournament
from ..models.player import Player
from ..models.data_manager import DataManager

class TournamentController:
    """Manages the overall tournament application flow."""

    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.current_tournament = None # Stores the tournament currently being managed

    def run(self):
        """Main loop for tournament management."""
        while True:
            choice = MainMenuScreen.display_tournament_menu() # Assume MainMenuScreen has this method
            if choice == "1":
                self.create_new_tournament()
            elif choice == "2":
                self.load_and_manage_tournament()
            elif choice == "3":
                # Back to main application menu, handled by main.py
                break
            else:
                print("Invalid choice. Please try again.")

    def create_new_tournament(self):
        """Handles the creation of a new tournament."""
        tournament_data = CreateTournamentScreen.get_tournament_details()
        if tournament_data:
            new_tournament = Tournament(**tournament_data)
            self.data_manager.save_tournament(new_tournament)
            print(f"Tournament '{new_tournament.name}' created successfully!")
            self.current_tournament = new_tournament
            self.manage_current_tournament()

    def load_and_manage_tournament(self):
        """Loads an existing tournament and enters its management interface."""
        tournament_list = self.data_manager.load_all_tournaments()
        if not tournament_list:
            print("No tournaments found to manage.")
            return

        selected_tournament_name = ManageTournamentScreen.select_tournament(tournament_list)
        if selected_tournament_name:
            self.current_tournament = next(
                (t for t in tournament_list if t.name == selected_tournament_name), None
            )
            if self.current_tournament:
                self.manage_current_tournament()
            else:
                print("Selected tournament not found.")

    def manage_current_tournament(self):
        """Enters the specific management interface for the current tournament."""
        if not self.current_tournament:
            print("No tournament selected to manage.")
            return

        while True:
            choice = ManageTournamentScreen.display_management_menu(self.current_tournament.name)
            if choice == "1":
                self._register_players_to_tournament()
            elif choice == "2":
                self._start_or_advance_round()
            elif choice == "3":
                self._enter_match_results()
            elif choice == "4":
                self._view_tournament_report()
            elif choice == "5":
                print(f"Exiting management for '{self.current_tournament.name}'.")
                break
            else:
                print("Invalid choice. Please try again.")

    def _register_players_to_tournament(self):
        """Handles player registration for the current tournament."""
        # This would involve loading players from club data and letting user select
        available_players = self.data_manager.load_all_players_from_clubs() # Need to implement this in DataManager
        selected_player_ids = RegisterPlayerScreen.get_players_for_registration(
            available_players, self.current_tournament.players
        )

        for player_id in selected_player_ids:
            # Find the full player data and create a Tournament Player object
            player_data = next((p for p in available_players if p['player_id'] == player_id), None)
            if player_data:
                tournament_player = Player(
                    player_data['player_id'],
                    player_data['first_name'],
                    player_data['last_name'],
                    player_data['date_of_birth'],
                    player_data['elo_rating']
                )
                self.current_tournament.add_player(tournament_player)
        self.data_manager.save_tournament(self.current_tournament)
        print(f"Players registered. Current players: {len(self.current_tournament.players)}")


    def _start_or_advance_round(self):
        """Starts a new round or advances the current one."""
        if not self.current_tournament.players or len(self.current_tournament.players) % 2 != 0:
            print("Not enough or odd number of players to start a round.")
            return

        if self.current_tournament.current_round == 0:
            print("Starting Round 1...")
            self.current_tournament.start_first_round()
        else:
            print(f"Advancing to Round {self.current_tournament.current_round + 1}...")
            self.current_tournament.advance_round()

        if self.current_tournament.rounds:
            AdvanceRoundScreen.display_round_matches(self.current_tournament.rounds[-1])
        self.data_manager.save_tournament(self.current_tournament)


    def _enter_match_results(self):
        """Enters results for matches in the current round."""
        if not self.current_tournament.rounds:
            print("No rounds have been started yet.")
            return

        current_round = self.current_tournament.rounds[-1]
        results = EnterResultsScreen.get_match_results(current_round.matches)

        for match_id, winner_id in results.items():
            for match in current_round.matches:
                if match.match_id == match_id:
                    match.set_winner(winner_id)
                    # Update player scores in tournament (handled by tournament.py logic)
                    if winner_id == match.player1.player_id:
                        match.player1.tournament_points += 1 # Or 0.5 for draw
                    elif winner_id == match.player2.player_id:
                        match.player2.tournament_points += 1
                    break
        self.data_manager.save_tournament(self.current_tournament)
        print("Match results updated.")
        self.current_tournament.update_player_elos_based_on_results() # Hypothetical method

    def _view_tournament_report(self):
        """Displays the tournament report."""
        TournamentReportScreen.display_report(self.current_tournament)
