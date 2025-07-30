"""
This module defines the Tournament class, representing a single chess tournament.
It includes attributes such as name, venue, start date, end date,
number of rounds, a list of participating players, and detailed round/match data.
"""

from datetime import datetime
from typing import List, Dict, Optional, Any

class Tournament:
    """
    Represents a chess tournament, including its state and match results.

    Attributes:
        name (str): The name of the tournament.
        venue (str): The venue where the tournament is held.
        start_date (datetime): The start date and time of the tournament.
        end_date (datetime): The end date and time of the tournament.
        num_rounds (int): The total number of rounds in the tournament.
        current_round (Optional[int]): The current round number being played (1-indexed).
                                        None if the tournament has not started or is completed.
        completed (bool): True if all planned rounds have been played.
        finished (bool): True if the tournament is officially closed/reported.
        players (list): A list of player IDs (e.g., Chess Identifiers)
                        participating in the tournament.
        rounds (List[List[Dict[str, Any]]]): A list of rounds, where each round is a list of matches.
                                             Each match is a dictionary with:
                                             - "players": List[str] (two player IDs)
                                             - "completed": bool
                                             - "winner": Optional[str] (player ID or None for tie)
        description (str): A general description or notes about the tournament.
    """

    def __init__(self,
                 name: str,
                 venue: str,
                 start_date: datetime,
                 end_date: datetime,
                 num_rounds: int,
                 players: List[str] = None,
                 current_round: Optional[int] = 0, # 0 could mean not started, None could mean finished
                 completed: bool = False,
                 finished: bool = False,
                 rounds: List[List[Dict[str, Any]]] = None,
                 description: str = ""):
        """
        Initializes a new Tournament instance.

        Args:
            name (str): The name of the tournament.
            venue (str): The venue of the tournament.
            start_date (datetime): The start date and time.
            end_date (datetime): The end date and time.
            num_rounds (int): The total number of rounds.
            players (List[str], optional): List of player IDs. Defaults to empty list.
            current_round (Optional[int], optional): The current round number. Defaults to 0.
            completed (bool, optional): Whether all rounds are played. Defaults to False.
            finished (bool, optional): Whether the tournament is officially finished. Defaults to False.
            rounds (List[List[Dict[str, Any]]], optional): List of round data. Defaults to empty list.
            description (str, optional): Tournament description. Defaults to "".
        """
        self.name = name
        self.venue = venue
        self.start_date = start_date
        self.end_date = end_date
        self.num_rounds = num_rounds
        self.players = players if players is not None else []
        self.current_round = current_round
        self.completed = completed
        self.finished = finished
        self.rounds = rounds if rounds is not None else []
        self.description = description

    def __str__(self):
        """
        Returns a string representation of the Tournament object.
        """
        status = "Completed" if self.completed else f"Round {self.current_round}/{self.num_rounds}"
        return (f"Tournament: {self.name} at {self.venue} "
                f"({self.start_date.strftime('%d-%m-%Y')} to {self.end_date.strftime('%d-%m-%Y')}) "
                f"Status: {status}")

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Tournament object to a dictionary for JSON serialization,
        matching the specified format.
        """
        return {
            "name": self.name,
            "dates": {
                "from": self.start_date.strftime('%d-%m-%Y'),
                "to": self.end_date.strftime('%d-%m-%Y')
            },
            "venue": self.venue,
            "number_of_rounds": self.num_rounds,
            "current_round": self.current_round, # Will be null if set to None
            "completed": self.completed,
            "finished": self.finished,
            "players": self.players,
            "rounds": self.rounds
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Creates a Tournament object from a dictionary, parsing dates and
        other attributes from the specified JSON format.
        """
        start_date_str = data["dates"]["from"]
        end_date_str = data["dates"]["to"]

        return cls(
            name=data["name"],
            venue=data["venue"],
            start_date=datetime.strptime(start_date_str, '%d-%m-%Y'),
            end_date=datetime.strptime(end_date_str, '%d-%m-%Y'),
            num_rounds=data["number_of_rounds"],
            players=data.get("players", []),
            current_round=data.get("current_round"), # Will load None if null in JSON
            completed=data.get("completed", False),
            finished=data.get("finished", False),
            rounds=data.get("rounds", []),
            description=data.get("description", "") # Assuming description might not always be in JSON
        )

