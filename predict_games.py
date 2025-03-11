import pandas as pd

# Load team history
history_file = "nba_team_history.csv"
df = pd.read_csv(history_file)

# Ensure necessary columns exist
required_columns = {"date", "team", "opponent", "win_loss"}
if not required_columns.issubset(df.columns):
    raise ValueError(f"Missing columns in {history_file}. Expected: {required_columns}, Found: {df.columns}")

# Function to calculate win percentage from last 5 games
def get_last_5_win_pct(team_name):
    team_games = df[df["team"] == team_name].sort_values("date", ascending=False).head(5)
    if team_games.empty:
        return 0.5  # Default to 50% if no data
    wins = (team_games["win_loss"] == "Win").sum()
    return wins / len(team_games)

# Function to compute head-to-head win percentage
def get_head_to_head_pct(team1, team2):
    matchups = df[((df["team"] == team1) & (df["opponent"] == team2)) |
                  ((df["team"] == team2) & (df["opponent"] == team1))]
    if matchups.empty:
        return 0.5  # Default to 50% if no previous matchups
    team1_wins = ((matchups["team"] == team1) & (matchups["win_loss"] == "Win")).sum()
    return team1_wins / len(matchups)

# Load upcoming games
upcoming_games_file = "upcoming_nba_games.csv"
upcoming_games = pd.read_csv(upcoming_games_file)

# Ensure correct column names in upcoming games file
expected_columns = {"date", "home_team", "visitor_team"}  # Ensure visitor_team is used
if not expected_columns.issubset(upcoming_games.columns):
    raise ValueError(f"Missing columns in {upcoming_games_file}. Expected: {expected_columns}, Found: {upcoming_games.columns}")

# Generate predictions
predictions = []
for _, row in upcoming_games.iterrows():
    home_team = row["home_team"]
    visitor_team = row["visitor_team"]

    # Get team performance data
    home_win_pct = get_last_5_win_pct(home_team)
    visitor_win_pct = get_last_5_win_pct(visitor_team)
    head_to_head = get_head_to_head_pct(home_team, visitor_team)

    # Calculate win probability (simple average of factors)
    home_team_chance = (home_win_pct + (1 - visitor_win_pct) + head_to_head) / 3
    visitor_team_chance = 1 - home_team_chance

    # Determine favored team
    if home_team_chance > visitor_team_chance:
        favored_team = f"{home_team} is favored by {home_team_chance:.2%}"
    else:
        favored_team = f"{visitor_team} is favored by {visitor_team_chance:.2%}"

    predictions.append([home_team, visitor_team, f"{home_team_chance:.2%}", f"{visitor_team_chance:.2%}", favored_team])

# Save predictions
predictions_df = pd.DataFrame(predictions, columns=["Home Team", "Visitor Team", "Home Win %", "Visitor Win %", "Favored Team"])
predictions_df.to_csv("nba_predictions.csv", index=False)

print("✅ Predictions saved to nba_predictions.csv")
