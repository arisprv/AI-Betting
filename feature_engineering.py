import pandas as pd

# ================= CONFIG =================
HISTORICAL_FILE = "matches_2025.csv"
FEATURES_FILE = "team_features_2025.csv"
ROLLING_WINDOW = 5
# ==========================================

# Load historical matches
df = pd.read_csv(HISTORICAL_FILE)
df["date"] = pd.to_datetime(df["date"])

# Initialize list for features
features = []

# Get unique leagues and teams
leagues = df["league"].unique()

for league in leagues:
    league_df = df[df["league"] == league]
    teams = pd.unique(league_df[["homeTeam", "awayTeam"]].values.ravel())

    for team in teams:
        # Get all matches for this team
        team_matches = league_df[(league_df["homeTeam"]==team) | (league_df["awayTeam"]==team)].sort_values("date")

        for idx, match in team_matches.iterrows():
            is_home = match["homeTeam"] == team
            goals_for = match["homeScore"] if is_home else match["awayScore"]
            goals_against = match["awayScore"] if is_home else match["homeScore"]
            result = 1 if goals_for > goals_against else 0 if goals_for == goals_against else -1

            # Get last ROLLING_WINDOW matches
            prev_matches = team_matches[team_matches["date"] < match["date"]].tail(ROLLING_WINDOW)
            if len(prev_matches) == 0:
                avg_goals = 0
                avg_goals_against = 0
                win_rate = 0
            else:
                prev_goals_for = [
                    m["homeScore"] if m["homeTeam"]==team else m["awayScore"]
                    for _, m in prev_matches.iterrows()
                ]
                prev_goals_against = [
                    m["awayScore"] if m["homeTeam"]==team else m["homeScore"]
                    for _, m in prev_matches.iterrows()
                ]
                prev_results = [
                    1 if gf > ga else 0 if gf==ga else -1
                    for gf, ga in zip(prev_goals_for, prev_goals_against)
                ]
                avg_goals = sum(prev_goals_for)/len(prev_goals_for)
                avg_goals_against = sum(prev_goals_against)/len(prev_goals_against)
                win_rate = prev_results.count(1)/len(prev_results)

            features.append({
                "league": league,
                "utcDate": match["date"],
                "team": team,
                "is_home": is_home,
                "goals_for": goals_for,
                "goals_against": goals_against,
                "avg_goals_5": avg_goals,
                "avg_goals_against_5": avg_goals_against,
                "win_rate_5": win_rate
            })

# Save features
features_df = pd.DataFrame(features)
features_df = features_df.sort_values(["league","team","utcDate"])
features_df.to_csv(FEATURES_FILE, index=False)
print(f"✅ Saved features for all teams to {FEATURES_FILE}")
