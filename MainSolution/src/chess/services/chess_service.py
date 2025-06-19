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

    @staticmethod
    def print_last_30_day_rating_for_top_player():
        """
        Prints the rating history of the last 30 days of the top player in classical chess.
        """
        top_player = LichessRepository.get_top_classical_players(count=1)
        if not top_player:
            print("Could not get top player.")
            return

        top_player = top_player[0] 
        rating_history = LichessRepository.get_player_rating_history(top_player)
        if not rating_history:
            print(f"Unable to retrieve rating history for {top_player}.")
            return

        today = datetime.today()
        last_30_days_ratings = {}

        for record in rating_history:
            year, month, day, rating = record
            date = datetime(year, month + 1, day)  # Adjustment in the month index
            if today - timedelta(days=30) <= date <= today:
                last_30_days_ratings[date.strftime('%Y-%m-%d')] = rating

        print(f"{top_player}, {last_30_days_ratings}")