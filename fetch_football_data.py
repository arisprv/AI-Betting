import requests
import pandas as pd
from datetime import datetime

# ================= CONFIG =================
API_TOKEN = "55232aed707e498c914f70d4cf2f40c3"  # Replace with your football-data.org API key
LEAGUES = {
    "PL": "Premier League",
    "PD": "La Liga",
    "SA": "Serie A",
    "BL1": "Bundesliga",
    "FL1": "Ligue 1"
}
SEASON = 2025
HISTORICAL_FILE = "matches_2025.csv"
UPCOMING_FILE = "upcoming_matches_2025.csv"
# ==========================================

headers = {"X-Auth-Token": API_TOKEN}

all_historical_matches = []
all_upcoming_matches = []

for league_code, league_name in LEAGUES.items():
    print(f"Fetching matches for {league_name} ({league_code})...")

    # 1️⃣ Historical matches
    hist_url = f"https://api.football-data.org/v4/competitions/{league_code}/matches"
    hist_params = {"season": SEASON, "status": "FINISHED"}
    hist_resp = requests.get(hist_url, headers=headers, params=hist_params)

    if hist_resp.status_code == 200:
        hist_data = hist_resp.json()
        for match in hist_data.get("matches", []):
            all_historical_matches.append({
                "league": league_code,
                "date": match["utcDate"],
                "homeTeam": match["homeTeam"]["name"],
                "awayTeam": match["awayTeam"]["name"],
                "homeScore": match["score"]["fullTime"]["home"],
                "awayScore": match["score"]["fullTime"]["away"]
            })
    else:
        print(f"⚠️ Failed to fetch historical matches for {league_name}: {hist_resp.status_code}")

    # 2️⃣ Upcoming matches
    upcoming_url = f"https://api.football-data.org/v4/competitions/{league_code}/matches"
    upcoming_params = {"season": SEASON, "status": "SCHEDULED"}
    upcoming_resp = requests.get(upcoming_url, headers=headers, params=upcoming_params)

    if upcoming_resp.status_code == 200:
        upcoming_data = upcoming_resp.json()
        for match in upcoming_data.get("matches", []):
            all_upcoming_matches.append({
                "league": league_code,
                "utcDate": match["utcDate"],
                "homeTeam": match["homeTeam"]["name"],
                "awayTeam": match["awayTeam"]["name"]
            })
    else:
        print(f"⚠️ Failed to fetch upcoming matches for {league_name}: {upcoming_resp.status_code}")

# Save historical matches
hist_df = pd.DataFrame(all_historical_matches)
hist_df["date"] = pd.to_datetime(hist_df["date"])
hist_df = hist_df.sort_values(["league", "date"])
hist_df.to_csv(HISTORICAL_FILE, index=False)
print(f"✅ Saved {len(hist_df)} historical matches to {HISTORICAL_FILE}")

# Save upcoming matches
upcoming_df = pd.DataFrame(all_upcoming_matches)
upcoming_df["utcDate"] = pd.to_datetime(upcoming_df["utcDate"])
upcoming_df = upcoming_df.sort_values(["league", "utcDate"])
upcoming_df.to_csv(UPCOMING_FILE, index=False)
print(f"✅ Saved {len(upcoming_df)} upcoming matches to {UPCOMING_FILE}")
