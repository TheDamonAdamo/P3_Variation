# commands/models/round.py
"""
Defines the Round class, representing a round in a chess tournament.
"""
from dataclasses import dataclass, field
from datetime import datetime
import uuid
from .match import Match

@dataclass
class Round:
    round_id: str
    name: str
    start_time: str
    end_time: str | None
    matches: list[Match] = field(default_factory=list)

    def __post_init__(self):
        if not self.round_id:
            self.round_id = str(uuid.uuid4())

    def to_dict(self):
        """Converts the Round object to a dictionary for JSON serialization."""
        return {
            "round_id": self.round_id,
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "matches": [match.to_dict() for match in self.matches]
        }

    @classmethod
    def from_dict(cls, data: dict, all_players_in_tournament: dict[str, any]):
        """
        Creates a Round object from a dictionary.
        Requires a dictionary of all players in the tournament for match reconstruction.
        """
        matches = [
            Match.from_dict(m_data, all_players_in_tournament)
            for m_data in data.get('matches', [])
        ]
        return cls(
            round_id=data['round_id'],
            name=data['name'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            matches=matches
        )

    def is_finished(self) -> bool:
        """Checks if all matches in the round have results."""
        return all(match.result is not None for match in self.matches)

    def __str__(self):
        return f"Round {self.name} ({len(self.matches)} matches)"