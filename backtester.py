"""Historical backtesting engine — simulates a betting strategy on past matches."""
import pandas as pd
import numpy as np
from bankroll import BankrollManager
from constants import RESULT_LABELS, MIN_CONFIDENCE_THRESHOLD
from logger import get_logger

log = get_logger(__name__)


def run_backtest(  # noqa: PLR0913
    matches: pd.DataFrame,
    features: pd.DataFrame,
    model,
    feature_cols: list[str],
    initial_capital: float = 1000.0,
    confidence_threshold: float = MIN_CONFIDENCE_THRESHOLD,
) -> tuple[BankrollManager, pd.DataFrame]:
    bankroll = BankrollManager(initial_capital=initial_capital)
    bet_records = []

    matches = matches.sort_values("utcDate")

    for _, match in matches.iterrows():
        home, away, date = match["homeTeam"], match["awayTeam"], match["utcDate"]
        actual_result = match["result"]

        home_s = features[(features["team"] == home) & (features["utcDate"] < date) & features["is_home"]].sort_values("utcDate").tail(1)
        away_s = features[(features["team"] == away) & (features["utcDate"] < date) & ~features["is_home"]].sort_values("utcDate").tail(1)

        if home_s.empty or away_s.empty:
            continue

        try:
            row_vals = [home_s[c].values[0] for c in feature_cols[:3]] + [away_s[c].values[0] for c in feature_cols[3:]]
        except KeyError:
            continue

        X = pd.DataFrame([row_vals], columns=feature_cols)
        proba = model.predict_proba(X)[0]
        classes = model.classes_
        pred_idx = int(np.argmax(proba))
        pred_class = classes[pred_idx]
        pred_prob = proba[pred_idx]

        if pred_prob < confidence_threshold:
            continue

        pred_label = RESULT_LABELS.get(pred_class, str(pred_class))
        implied_odds = 1 / pred_prob
        stake = bankroll.kelly_stake(pred_prob, implied_odds)
        won = pred_class == actual_result

        bankroll.record_bet(f"{home} vs {away}", pred_label, stake, implied_odds, won)
        bet_records.append({
            "date": date,
            "match": f"{home} vs {away}",
            "prediction": pred_label,
            "confidence": round(pred_prob, 3),
            "stake": stake,
            "won": won,
            "balance": bankroll.current_capital,
        })

    total_staked = sum(b["stake"] for b in bet_records)
    total_pnl = sum(b["pnl"] for b in bet_records if "pnl" in b)
    roi = total_pnl / total_staked if total_staked > 0 else 0.0
    log.info(
        "Backtest: %d bets | balance %.2f (start %.2f) | ROI %.1f%% | win rate %.1f%%",
        len(bet_records), bankroll.current_capital, initial_capital,
        roi * 100, (bankroll.win_rate or 0) * 100,
    )
    return bankroll, pd.DataFrame(bet_records)
