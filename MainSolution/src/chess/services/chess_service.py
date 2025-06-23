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

        today = datetime.today()
        last_30_days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]

        last_30_days_ratings = ChessService.get_last_30_days_ratings(top_player, last_30_days)

        print(f"{top_player}, {last_30_days_ratings}")

    @staticmethod
    def generate_rating_csv_for_top_50_classical_players(filename="top_50_classical_players_ratings.csv"):
        """
        Generates a CSV file containing the rating history of the last 30 days of the top 50 players.
        """
        top_players = LichessRepository.get_top_classical_players()
        if not top_players:
            print("Unable to retrieve top 50 players list.")
            return

        today = datetime.today()
        last_30_days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]

        csv_data = [['username'] + last_30_days]

        for player in top_players:
            player_ratings_the_last_30_days = ChessService.get_last_30_days_ratings(player, last_30_days)
            row = [player] + [player_ratings_the_last_30_days.get(date, "") for date in last_30_days]
            csv_data.append(row)
        
        output_dir = "MainSolution\output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_filepath = os.path.join(output_dir, filename)
        with open(output_filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(csv_data)

    @staticmethod
    def get_last_30_days_ratings(username, last_30_days):
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