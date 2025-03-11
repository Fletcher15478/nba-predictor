import csv
import os
from datetime import datetime
from balldontlie import BalldontlieAPI

# Initialize API
api = BalldontlieAPI(api_key="dd71137e-30a5-42da-87ba-9c424bfb8d00")

# Get today's date
today = datetime.utcnow().strftime('%Y-%m-%d')

# Fetch today's games
games = api.nba.games.list(start_date=today, end_date=today)
games_data = games.data

# Define CSV file
csv_filename = "upcoming_nba_games.csv"

# Open CSV in write mode (overwrite old data)
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    
    # Write header
    writer.writerow(["date", "home_team", "visitor_team"])

    # Write games
    for game in games_data:
        writer.writerow([game.date, game.home_team.full_name, game.visitor_team.full_name])

print(f"✅ Upcoming games saved to {csv_filename}")
