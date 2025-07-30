# commands/models/player.py
"""
Defines the Player class, representing a chess player within the context of a tournament.
"""
from dataclasses import dataclass, field
import uuid

@dataclass
class Player:
    player_id: str
    first_name: str
    last_name: str
    date_of_birth: str # YYYY-MM-DD format
    elo_rating: int
    tournament_points: float = 0.0
    played_opponents: list[str] = field(default_factory=list) # List of player_ids

    def __post_init__(self):
        # Ensure player_id is unique if not provided (e.g., for new players)
        if not self.player_id:
            self.player_id = str(uuid.uuid4())

    def to_dict(self):
        """Converts the Player object to a dictionary for JSON serialization."""
        return {
            "player_id": self.player_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "elo_rating": self.elo_rating,
            "tournament_points": self.tournament_points,
            "played_opponents": self.played_opponents
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Player object from a dictionary."""
        return cls(
            player_id=data['player_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=data['date_of_birth'],
            elo_rating=data['elo_rating'],
            tournament_points=data.get('tournament_points', 0.0),
            played_opponents=data.get('played_opponents', [])
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Elo: {self.elo_rating}, Points: {self.tournament_points})"

    def __repr__(self):
        return f"Player(id='{self.player_id}', name='{self.first_name} {self.last_name}')"

    def __eq__(self, other):
        if not isinstance(other, Player):
            return NotImplemented
        return self.player_id == other.player_id

    def __hash__(self):
        return hash(self.player_id)