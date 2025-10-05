import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# === CONFIG ===
FEATURES_FILE = "team_features_PL_2025_v5.csv"
MATCHES_FILE = "matches_PL_2025.csv"
MODEL_FILE = "football_model_v5.pkl"

# Load historical matches
matches = pd.read_csv(MATCHES_FILE)
matches = matches[matches["status"] == "FINISHED"].copy()
matches["utcDate"] = pd.to_datetime(matches["utcDate"])
matches["result"] = matches.apply(lambda r: 1 if r["homeScore"] > r["awayScore"]
                                 else (-1 if r["homeScore"] < r["awayScore"] else 0), axis=1)

# Load features
features = pd.read_csv(FEATURES_FILE)
features["utcDate"] = pd.to_datetime(features["utcDate"])

X_list = []
y_list = []

for _, match in matches.iterrows():
    home = match["homeTeam"]
    away = match["awayTeam"]
    date = match["utcDate"]

    home_stats = features[(features["team"]==home) & (features["utcDate"] < date) & (features["is_home"]==True)].sort_values("utcDate").tail(1)
    away_stats = features[(features["team"]==away) & (features["utcDate"] < date) & (features["is_home"]==False)].sort_values("utcDate").tail(1)

    if home_stats.empty or away_stats.empty:
        continue

    X_list.append([
        home_stats["avg_goals_for_5"].values[0],
        home_stats["avg_goals_against_5"].values[0],
        home_stats["win_rate_5"].values[0],
        away_stats["avg_goals_for_5"].values[0],
        away_stats["avg_goals_against_5"].values[0],
        away_stats["win_rate_5"].values[0]
    ])
    y_list.append(match["result"])

X = pd.DataFrame(X_list, columns=[
    "home_avg_goals_for_5","home_avg_goals_against_5","home_win_rate_5",
    "away_avg_goals_for_5","away_avg_goals_against_5","away_win_rate_5"
])
y = pd.Series(y_list)

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("✅ Model accuracy:", round(accuracy_score(y_test, y_pred), 3))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save model
joblib.dump(model, MODEL_FILE)
print(f"💾 Model saved as {MODEL_FILE}")
