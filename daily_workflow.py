"""Automated daily workflow: fetch fresh data, generate predictions, check value bets."""
from datetime import datetime
from config import CONFIG
from logger import get_logger
from fetch_odds import fetch_all_odds
from predict_daily import load_resources, build_feature_row, predict_match
from odds_analyzer import best_odds, expected_value
from alert_system import AlertSystem
from constants import MIN_CONFIDENCE_THRESHOLD, MIN_VALUE_THRESHOLD
import pandas as pd

log = get_logger(__name__)
alerts = AlertSystem()


def run_daily():
    log.info("=== Daily workflow started: %s ===", datetime.now().strftime("%Y-%m-%d %H:%M"))

    try:
        model, features_df, upcoming = load_resources()
    except Exception as exc:
        alerts.critical(f"Failed to load resources: {exc}")
        return

    try:
        odds_df = fetch_all_odds()
        log.info("Fetched %d odds rows", len(odds_df))
    except Exception as exc:
        alerts.warning(f"Odds fetch failed: {exc}")
        odds_df = pd.DataFrame()

    value_bets = []
    today_matches = upcoming[upcoming["utcDate"].dt.date == datetime.today().date()]
    log.info("Processing %d matches for today", len(today_matches))

    for _, match in today_matches.iterrows():
        home, away, date = match["homeTeam"], match["awayTeam"], match["utcDate"]
        row = build_feature_row(home, away, date, features_df)
        if row is None:
            continue

        label, prob, _ = predict_match(model, row)
        if prob < MIN_CONFIDENCE_THRESHOLD:
            continue

        odds = best_odds(odds_df, home, away, label) if not odds_df.empty else None
        if odds is None:
            continue

        ev = expected_value(prob, odds)
        if ev >= MIN_VALUE_THRESHOLD:
            value_bets.append({"match": f"{home} vs {away}", "prediction": label, "ev": ev})
            log.info("Value bet: %s vs %s → %s (EV: %.3f)", home, away, label, ev)

    if not value_bets:
        log.info("No value bets found today")
    else:
        log.info("Found %d value bet(s) for today", len(value_bets))

    log.info("=== Daily workflow complete ===")
    return value_bets


if __name__ == "__main__":
    run_daily()
