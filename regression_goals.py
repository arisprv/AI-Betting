"""Linear regression model for predicting expected goals scored/conceded."""
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from logger import get_logger

log = get_logger(__name__)


def build_goals_features(features: pd.DataFrame) -> pd.DataFrame:
    """Select numeric features suitable for goal regression."""
    cols = ["avg_goals_5", "avg_goals_against_5", "win_rate_5", "form_score_5",
            "goal_diff_avg_5", "clean_sheet_rate_5"]
    available = [c for c in cols if c in features.columns]
    return features[available].fillna(0)


def train_goals_model(matches: pd.DataFrame, features: pd.DataFrame,
                       alpha: float = 1.0) -> tuple:
    """
    Train Ridge regression models for home and away goals.
    Returns (home_model, away_model, home_mae, away_mae).
    """
    X_home, y_home, X_away, y_away = [], [], [], []

    for _, match in matches.iterrows():
        home, away, date = match["homeTeam"], match["awayTeam"], match["utcDate"]
        home_f = features[(features["team"] == home) & (features["utcDate"] < date)].sort_values("utcDate").tail(1)
        away_f = features[(features["team"] == away) & (features["utcDate"] < date)].sort_values("utcDate").tail(1)
        if home_f.empty or away_f.empty:
            continue
        row = build_goals_features(home_f).values[0].tolist()
        X_home.append(row)
        y_home.append(match["homeScore"])
        row_a = build_goals_features(away_f).values[0].tolist()
        X_away.append(row_a)
        y_away.append(match["awayScore"])

    X_h, y_h = np.array(X_home), np.array(y_home, dtype=float)
    X_a, y_a = np.array(X_away), np.array(y_away, dtype=float)

    Xh_tr, Xh_te, yh_tr, yh_te = train_test_split(X_h, y_h, test_size=0.2, random_state=42)
    Xa_tr, Xa_te, ya_tr, ya_te = train_test_split(X_a, y_a, test_size=0.2, random_state=42)

    home_model = Ridge(alpha=alpha)
    away_model = Ridge(alpha=alpha)
    home_model.fit(Xh_tr, yh_tr)
    away_model.fit(Xa_tr, ya_tr)

    home_mae = mean_absolute_error(yh_te, home_model.predict(Xh_te))
    away_mae = mean_absolute_error(ya_te, away_model.predict(Xa_te))
    log.info("Goals regression — Home MAE: %.3f | Away MAE: %.3f", home_mae, away_mae)

    return home_model, away_model, home_mae, away_mae
