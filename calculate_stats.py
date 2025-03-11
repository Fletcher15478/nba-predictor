import pandas as pd

# Load historical game data
csv_filename = "nba_team_history.csv"
df = pd.read_csv(csv_filename)

# Convert date column to datetime for sorting
df["date"] = pd.to_datetime(df["date"])

# Sort data by date (oldest first)
df = df.sort_values(by="date")

# Function to calculate last 5 game win percentage
def get_last_5_win_percentage(team, current_date):
    recent_games = df[
        (df["team"] == team) & (df["date"] < current_date)
    ].tail(5)  # Get last 5 games
    return recent_games["win_loss"].value_counts(normalize=True).get("Win", 0.0)  # % of Wins

# Function to get head-to-head record
def get_head_to_head_record(team, opponent):
    matchups = df[
        ((df["team"] == team) & (df["opponent"] == opponent))
        | ((df["team"] == opponent) & (df["opponent"] == team))
    ]
    return matchups["win_loss"].value_counts(normalize=True).get("Win", 0.0)

# Create new prediction dataset
predictions = []
for _, row in df.iterrows():
    team = row["team"]
    opponent = row["opponent"]
    date = row["date"]

    predictions.append({
        "date": date,
        "team": team,
        "opponent": opponent,
        "win_percentage_last_5": get_last_5_win_percentage(team, date),
        "head_to_head_win_percentage": get_head_to_head_record(team, opponent),
        "actual_result": row["win_loss"]  # For validation
    })

# Save to CSV
predictions_df = pd.DataFrame(predictions)
predictions_df.to_csv("nba_team_predictions.csv", index=False)

print("✅ Predictions dataset created: nba_team_predictions.csv")
