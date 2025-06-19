from datetime import datetime, timedelta
import csv
import os
from chess.repositories.lichess_repository import LichessRepository

class ChessService:
    @staticmethod
    def print_top_50_classical_players():
        """
        Prints the usernames of the top 50 classical chess players.
        """
        top_players = LichessRepository.get_top_classical_players()
        for username in top_players:
            print(username)