import csv
import os
from datetime import datetime, timedelta
from balldontlie import BalldontlieAPI

# Initialize API
api = BalldontlieAPI(api_key="dd71137e-30a5-42da-87ba-9c424bfb8d00")

# Get yesterday's date
yesterday = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')

# Fetch games from yesterday
games = api.nba.games.list(start_date=yesterday, end_date=yesterday)
games_data = games.data

# Define CSV file
csv_filename = "nba_team_history.csv"

# Check if file exists and is empty
file_exists = os.path.exists(csv_filename)
is_empty = not file_exists or os.stat(csv_filename).st_size == 0

# Open CSV in append mode
with open(csv_filename, mode="a", newline="") as file:
    writer = csv.writer(file)

    # Write header only if the file is empty
    if is_empty:
        writer.writerow(["date", "team", "opponent", "points_scored", "points_allowed", "win_loss"])

    # Write each game twice (once for home team, once for visitor)
    for game in games_data:
        writer.writerow([
            game.date,
            game.home_team.full_name,
            game.visitor_team.full_name,
            game.home_team_score,
            game.visitor_team_score,
            "Win" if game.home_team_score > game.visitor_team_score else "Loss"
        ])

        writer.writerow([
            game.date,
            game.visitor_team.full_name,
            game.home_team.full_name,
            game.visitor_team_score,
            game.home_team_score,
            "Win" if game.visitor_team_score > game.home_team_score else "Loss"
        ])

print(f"✅ Data saved to {csv_filename}")
