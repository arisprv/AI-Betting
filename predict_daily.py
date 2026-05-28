import pandas as pd
import numpy as np
import joblib
from config import CONFIG
from constants import RESULT_LABELS, MIN_CONFIDENCE_THRESHOLD, MIN_VALUE_THRESHOLD
from bankroll import BankrollManager
from odds_analyzer import best_odds, expected_value
from logger import get_logger

log = get_logger(__name__)

FEATURE_COLS = [
    "home_avg_goals_for_5", "home_avg_goals_against_5", "home_win_rate_5",
    "away_avg_goals_for_5", "away_avg_goals_against_5", "away_win_rate_5",
]


def load_resources():
    model = joblib.load(CONFIG.model_file)
    features_df = pd.read_csv(CONFIG.features_file)
    features_df["utcDate"] = pd.to_datetime(features_df["utcDate"])
    upcoming = pd.read_csv(CONFIG.upcoming_file)
    upcoming["utcDate"] = pd.to_datetime(upcoming["utcDate"])
    return model, features_df, upcoming


def fetch_odds_df() -> pd.DataFrame:
    from fetch_odds import fetch_all_odds
    return fetch_all_odds()


def build_feature_row(home: str, away: str, match_date, features_df: pd.DataFrame):
    home_s = features_df[
        (features_df["team"] == home) & (features_df["utcDate"] < match_date) & features_df["is_home"]
    ].sort_values("utcDate").tail(1)
    away_s = features_df[
        (features_df["team"] == away) & (features_df["utcDate"] < match_date) & ~features_df["is_home"]
    ].sort_values("utcDate").tail(1)

    if home_s.empty or away_s.empty:
        return None

    try:
        vals = [
            home_s["avg_goals_5"].values[0], home_s["avg_goals_against_5"].values[0], home_s["win_rate_5"].values[0],
            away_s["avg_goals_5"].values[0], away_s["avg_goals_against_5"].values[0], away_s["win_rate_5"].values[0],
        ]
    except KeyError:
        return None
    return pd.DataFrame([vals], columns=FEATURE_COLS)


def predict_match(model, feature_row: pd.DataFrame) -> tuple[str, float, np.ndarray]:
    proba = model.predict_proba(feature_row)[0]
    classes = model.classes_
    pred_idx = int(np.argmax(proba))
    pred_class = classes[pred_idx]
    pred_prob = float(proba[pred_idx])
    pred_label = RESULT_LABELS.get(pred_class, str(pred_class))
    return pred_label, pred_prob, proba


def run_predictions(odds_df: pd.DataFrame = None):
    model, features_df, upcoming = load_resources()
    if odds_df is None:
        try:
            odds_df = fetch_odds_df()
        except Exception as exc:
            log.warning("Could not fetch odds: %s", exc)
            odds_df = pd.DataFrame()

    bankroll = BankrollManager()
    predictions, value_bets = [], []

    for _, match in upcoming.iterrows():
        home, away, date = match["homeTeam"], match["awayTeam"], match["utcDate"]
        feature_row = build_feature_row(home, away, date, features_df)
        if feature_row is None:
            log.debug("Skipping %s vs %s — missing stats", home, away)
            continue

        pred_label, pred_prob, proba = predict_match(model, feature_row)
        predictions.append({"match": f"{home} vs {away}", "prediction": pred_label, "confidence": round(pred_prob, 3)})

        if pred_prob < MIN_CONFIDENCE_THRESHOLD:
            continue

        bet_odds = best_odds(odds_df, home, away, pred_label) if not odds_df.empty else None
        if bet_odds is None:
            continue

        ev = expected_value(pred_prob, bet_odds)
        if ev < MIN_VALUE_THRESHOLD:
            continue

        stake = bankroll.kelly_stake(pred_prob, bet_odds)
        value_bets.append({
            "match": f"{home} vs {away}",
            "prediction": pred_label,
            "model_prob": round(pred_prob, 3),
            "odds": bet_odds,
            "ev": round(ev, 3),
            "stake": stake,
        })

    _print_predictions(predictions)
    _print_value_bets(value_bets)

    pd.DataFrame(predictions).to_csv(CONFIG.predictions_file, index=False)
    pd.DataFrame(value_bets).to_csv(CONFIG.value_bets_file, index=False)
    log.info("Saved %d predictions and %d value bets", len(predictions), len(value_bets))


def _print_predictions(predictions: list[dict]) -> None:
    print("\n🏆 Predictions for Upcoming Matches:\n")
    for p in predictions:
        print(f"{p['match']:40} → {p['prediction']:10} ({p['confidence'] * 100:.1f}%)")


def _print_value_bets(value_bets: list[dict]) -> None:
    print("\n💰 Value Bets:\n")
    for vb in value_bets:
        print(f"{vb['match']:40} → {vb['prediction']:10} | EV: {vb['ev']:+.3f} | Odds: {vb['odds']:.2f} | Stake: £{vb['stake']:.2f}")


if __name__ == "__main__":
    run_predictions()
