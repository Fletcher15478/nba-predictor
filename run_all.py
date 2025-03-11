import os
import time

print("🔄 Fetching today's NBA games...")
os.system("python fetch_nba_data.py")

print("🔄 Fetching tomorrow's NBA games...")
os.system("python fetch_upcoming_games.py")

print("🔄 Generating predictions...")
os.system("python predict_games.py")

print("🔄 Restarting the web server...")
os.system("pkill -f server.py")  # Kills old server (if running)
time.sleep(2)  # Small delay before restarting
os.system("python server.py &")  # Runs in background

print("✅ All tasks completed successfully!")
