import pandas as pd
import requests
import joblib

# ================= CONFIG =================
MODEL_FILE = "football_model_v5.pkl"
TEAM_FEATURES_FILE = "team_features_2025.csv"
UPCOMING_FILE = "upcoming_matches_2025.csv"
API_KEY = "ad6045f62362a96a24924113faa405eb"  # The Odds API key
LEAGUES = {
    "soccer_epl": "Premier League",
    "soccer_spain_la_liga": "La Liga",
    "soccer_italy_serie_a": "Serie A",
    "soccer_germany_bundesliga": "Bundesliga",
    "soccer_france_ligue_one": "Ligue 1"
}
REGIONS = "uk"
MARKETS = "h2h"
# ==========================================

# Load model and features
model = joblib.load(MODEL_FILE)
features_df = pd.read_csv(TEAM_FEATURES_FILE)
features_df["utcDate"] = pd.to_datetime(features_df["utcDate"])

# Load upcoming matches
upcoming = pd.read_csv(UPCOMING_FILE)
upcoming["utcDate"] = pd.to_datetime(upcoming["utcDate"])

# ---------------- FETCH ODDS ----------------
all_odds = []

for SPORT in LEAGUES.keys():
    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds/"
    params = {"apiKey": API_KEY, "regions": REGIONS, "markets": MARKETS}
    resp = requests.get(url, params=params)
    try:
        data = resp.json()
        print(data)
    except Exception as e:
        print(f"⚠️ Error fetching odds for {SPORT}: {e}")
        continue

    for match in data:
        home_team = match["home_team"]  # use the exact column name from your CSV
        away_team = match["away_team"]
        for bookmaker in match.get("bookmakers", []):
            if not bookmaker.get("markets"):
                continue
            outcomes = bookmaker["markets"][0]["outcomes"]
            odds_dict = {o["name"]: o["price"] for o in outcomes}
            all_odds.append({
                "league": SPORT,
                "home_team": home_team,
                "away_team": away_team,
                "bookmaker": bookmaker["title"],
                "home_odds": odds_dict.get(home_team),
                "draw_odds": odds_dict.get("Draw"),
                "away_odds": odds_dict.get(away_team)
            })

odds_df = pd.DataFrame(all_odds)


# ----------- HELPER FUNCTIONS -------------
def find_odds_row(odds_df, home, away):
    """Safe lookup for odds, ignoring FC/AFC"""

    def clean(name):
        if not isinstance(name, str):
            return ""
        return name.replace("FC", "").replace("AFC", "").strip()

    row = odds_df[(odds_df["home_team"] == home) & (odds_df["away_team"] == away)]
    if not row.empty:
        return row.iloc[0]
    # Try partial match
    row = odds_df[(odds_df["home_team"].apply(clean) == clean(home)) &
                  (odds_df["away_team"].apply(clean) == clean(away))]
    if not row.empty:
        return row.iloc[0]
    return None


# ----------- PREDICTIONS & VALUE BETS -------------
predictions = []
value_bets = []

for _, match in upcoming.iterrows():
    home = match["homeTeam"]
    away = match["awayTeam"]
    match_date = match["utcDate"]

    # Skip if team stats missing
    home_stats = features_df[
        (features_df["team"] == home) & (features_df["utcDate"] < match_date) & (features_df["is_home"] == True)]
    away_stats = features_df[
        (features_df["team"] == away) & (features_df["utcDate"] < match_date) & (features_df["is_home"] == False)]
    if home_stats.empty or away_stats.empty:
        print(f"⚠️ Skipping {home} vs {away} (missing team stats)")
        continue

    # Take latest stats
    home_latest = home_stats.sort_values("utcDate").iloc[-1]
    away_latest = away_stats.sort_values("utcDate").iloc[-1]

    # Prepare features for model
    feature_row = pd.DataFrame([[
        home_latest["avg_goals_5"],
        home_latest["avg_goals_against_5"],
        home_latest["win_rate_5"],
        away_latest["avg_goals_5"],
        away_latest["avg_goals_against_5"],
        away_latest["win_rate_5"]
    ]], columns=[
        "home_avg_goals_for_5", "home_avg_goals_against_5", "home_win_rate_5",
        "away_avg_goals_for_5", "away_avg_goals_against_5", "away_win_rate_5"
    ])

    # Predict outcome
    pred_class = model.predict(feature_row)[0]
    pred_prob = max(model.predict_proba(feature_row)[0])
    label_map = {1: "Home Win", 0: "Draw", -1: "Away Win"}
    pred_label = label_map[pred_class]

    predictions.append({
        "match": f"{home} vs {away}",
        "prediction": pred_label,
        "confidence": round(pred_prob, 2)
    })

    # Find odds
    odds_row = find_odds_row(odds_df, home, away)
    if odds_row is None:
        # print(f"⚠️ Odds not found for {home} vs {away}")
        continue

    # Calculate implied probabilities
    implied_probs = {
        "Home Win": 1 / odds_row["home_odds"] if odds_row["home_odds"] else 0,
        "Draw": 1 / odds_row["draw_odds"] if odds_row["draw_odds"] else 0,
        "Away Win": 1 / odds_row["away_odds"] if odds_row["away_odds"] else 0
    }
    total = sum(implied_probs.values())
    for k in implied_probs:
        implied_probs[k] /= total if total > 0 else 1

    # Check for value bet
    if pred_prob > implied_probs[pred_label]:
        value_bets.append({
            "match": f"{home} vs {away}",
            "prediction": pred_label,
            "model_prob": pred_prob,
            "implied_prob": implied_probs[pred_label],
            "bookmaker": odds_row["bookmaker"]
        })

# ----------- OUTPUT -------------
print("\n🏆 Predictions for Upcoming Matches:\n")
for p in predictions:
    print(f"{p['match']:40} → {p['prediction']:10} ({p['confidence'] * 100:.1f}% confidence)")

print("\n💰 Value Bets:\n")
for vb in value_bets:
    print(
        f"{vb['match']:40} → {vb['prediction']:10} | Model: {vb['model_prob'] * 100:.1f}% > Odds: {vb['implied_prob'] * 100:.1f}% ({vb['bookmaker']})")

# Save CSVs
pd.DataFrame(predictions).to_csv("predictions_multileague_2025.csv", index=False)
pd.DataFrame(value_bets).to_csv("value_bets_multileague_2025.csv", index=False)
