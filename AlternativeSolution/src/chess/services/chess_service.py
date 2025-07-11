from typing import List, Dict
from src.chess.repositories.lichess_repository import LichessRepository
from src.chess.models import Player, RatingHistory
from datetime import datetime, timedelta
import csv
import os

class ChessService:

    @staticmethod
    def get_top_50_classical_players() -> List[Player]:
        """
        Returns the list of usernames of the top 50 classical chess players.
        """
        return LichessRepository.get_top_classical_players()

    @staticmethod
    def print_last_30_day_rating_for_top_player() -> Dict:
        """
        Returns the rating history for the last 30 days for the top 1 player.
        """
        top_player = LichessRepository.get_top_classical_players(count=1)
        if not top_player:
            return "Top player not found"
        return top_player[0],ChessService.get_last_30_days_ratings(top_player[0])

    @staticmethod
    def get_last_30_days_ratings(username, last_30_days) -> Dict:
            """
            Returns a dictionary with date -> rating for the last 30 calendar days.
            Fills missing days using the last known rating (backfilling).
            """
            rating_history = LichessRepository.get_player_rating_history(username)
            if not rating_history:
                return {}

            today = datetime.today()
            last_30_days_set = set(last_30_days)
            rating_map = {}

            # Convert points into {date: rating}
            for year, month, day, rating in rating_history:
                date = datetime(year, month + 1, day)
                date_str = date.strftime('%Y-%m-%d')
                if date_str in last_30_days_set:
                    rating_map[date_str] = rating

            # Backfill using a stack
            filled_ratings = {}
            stack = []
            for date_str in last_30_days:
                if date_str in rating_map:
                    stack.append(rating_map[date_str])
                filled_ratings[date_str] = stack[-1] if stack else ""

            return filled_ratings

    @staticmethod
    def generate_rating_csv_for_top_50_classical_players(filename="top_50_classical_players_ratings.csv"):
        """
        Generates a CSV file containing the rating history of the last 30 days of the top 50 players.
        """
        top_players = LichessRepository.get_top_classical_players()
        if not top_players:
            return "Unable to retrieve top 50 players list."

        today = datetime.today()
        last_30_days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]

        csv_data = [['username'] + last_30_days]

        for player in top_players:
            player_ratings_the_last_30_days = ChessService.get_last_30_days_ratings(player, last_30_days)
            row = [player] + [player_ratings_the_last_30_days.get(date, "") for date in last_30_days]
            csv_data.append(row)

        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_filepath = os.path.join(output_dir, filename)
        with open(output_filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(csv_data)
