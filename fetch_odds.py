import requests
import pandas as pd

API_KEY = "ad6045f62362a96a24924113faa405eb"  # Replace with your key
SPORT = "soccer_epl"           # English Premier League
REGIONS = "uk"                 # Bookmaker regions
MARKETS = "h2h"                # Head-to-head odds (win/draw/win)
ODDS_API_URL = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds/"

params = {
    "apiKey": API_KEY,
    "regions": REGIONS,
    "markets": MARKETS
}

response = requests.get(ODDS_API_URL, params=params)
data = response.json()

# Convert to DataFrame for easier handling
matches = []
for match in data:
    home_team = match["home_team"]
    away_team = match["away_team"]
    for bookmaker in match["bookmakers"]:
        odds = bookmaker["markets"][0]["outcomes"]
        odds_dict = {o["name"]: o["price"] for o in odds}
        matches.append({
            "home_team": home_team,
            "away_team": away_team,
            "bookmaker": bookmaker["title"],
            "home_odds": odds_dict.get(home_team),
            "draw_odds": odds_dict.get("Draw"),
            "away_odds": odds_dict.get(away_team)
        })

df_odds = pd.DataFrame(matches)
print(df_odds.head())

# Save to CSV
df_odds.to_csv("live_odds.csv", index=False)
