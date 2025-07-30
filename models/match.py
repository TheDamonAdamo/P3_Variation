# commands/models/match.py
"""
Defines the Match class, representing a single chess match within a round.
"""
from dataclasses import dataclass
import uuid
from .player import Player # Import Player for type hinting if needed

@dataclass
class Match:
    match_id: str
    player1: Player
    player2: Player
    result: tuple[float, float] | None = None # (player1_score, player2_score) e.g., (1.0, 0.0), (0.5, 0.5)
    winner_id: str | None = None # ID of the winning player, or None for draw/not played

    def __post_init__(self):
        if not self.match_id:
            self.match_id = str(uuid.uuid4())

    def set_winner(self, winner_player_id: str):
        """Sets the winner of the match and updates scores."""
        if winner_player_id == self.player1.player_id:
            self.result = (1.0, 0.0)
            self.winner_id = self.player1.player_id
        elif winner_player_id == self.player2.player_id:
            self.result = (0.0, 1.0)
            self.winner_id = self.player2.player_id
        elif winner_player_id == "draw": # Special value for a draw
            self.result = (0.5, 0.5)
            self.winner_id = None
        else:
            raise ValueError("Invalid winner_player_id. Must be player1_id, player2_id, or 'draw'.")

    def to_dict(self):
        """Converts the Match object to a dictionary for JSON serialization."""
        return {
            "match_id": self.match_id,
            "player1_id": self.player1.player_id, # Store only ID to avoid circular refs
            "player2_id": self.player2.player_id,
            "result": self.result,
            "winner_id": self.winner_id
        }

    @classmethod
    def from_dict(cls, data: dict, all_players_in_tournament: dict[str, Player]):
        """
        Creates a Match object from a dictionary.
        Requires a dictionary of all players in the tournament for proper object reconstruction.
        """
        player1 = all_players_in_tournament.get(data['player1_id'])
        player2 = all_players_in_tournament.get(data['player2_id'])
        if not player1 or not player2:
            raise ValueError(f"Player(s) not found for match: {data['player1_id']}, {data['player2_id']}")

        return cls(
            match_id=data['match_id'],
            player1=player1,
            player2=player2,
            result=tuple(data['result']) if data['result'] else None,
            winner_id=data.get('winner_id')
        )

    def __str__(self):
        return f"Match {self.player1.first_name} vs {self.player2.first_name} - Result: {self.result}"