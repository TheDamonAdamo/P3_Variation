# screens/tournament_screens/tournament_report_screen.py
"""
Screen for displaying detailed tournament reports.
"""
from ..base import BaseScreen
from ..models.tournament import Tournament


class TournamentReportScreen(BaseScreen):
    """
    Handles the user interface for displaying various tournament reports.
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def display_report(tournament: Tournament):
        """Displays a detailed report for the given tournament."""
        print(f"\n--- Tournament Report: {tournament.name} ({tournament.location}) ---")
        print(f"Status: {tournament.status}")
        print(f"Dates: {tournament.start_date} to {tournament.end_date}")
        print(f"Rounds Played: {tournament.current_round_num}/{tournament.num_rounds}")
        print(f"Description: {tournament.description if tournament.description else 'N/A'}")

        print("\n--- Players (Ranked by Points) ---")
        ranked_players = tournament.get_ranked_players()
        if not ranked_players:
            print("No players registered yet.")
        else:
            for i, player in enumerate(ranked_players):
                print(
                    f"{i + 1}. {player.first_name} {player.last_name} (ELO: {player.elo_rating}, Points: {player.tournament_points})")

        print("\n--- Rounds and Matches ---")
        if not tournament.rounds:
            print("No rounds have been played yet.")
        else:
            for round_obj in tournament.rounds:
                print(
                    f"\n--- {round_obj.name} (Started: {round_obj.start_time}, Ended: {round_obj.end_time or 'N/A'}) ---")
                if not round_obj.matches:
                    print("No matches in this round.")
                else:
                    for i, match in enumerate(round_obj.matches):
                        p1_name = f"{match.player1.first_name} {match.player1.last_name}"
                        p2_name = f"{match.player2.first_name} {match.player2.last_name}"
                        result_str = "Pending"
                        if match.result:
                            result_str = f"{match.result[0]} - {match.result[1]}"
                            if match.winner_id:
                                winner = match.player1 if match.player1.player_id == match.winner_id else match.player2
                                result_str += f" (Winner: {winner.first_name})"
                            elif match.result == (0.5, 0.5):
                                result_str += " (Draw)"

                        print(f"  Match {i + 1}: {p1_name} vs {p2_name} | {result_str}")
        print("\n--- End of Report ---")