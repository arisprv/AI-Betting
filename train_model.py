import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.calibration import CalibratedClassifierCV
from config import CONFIG
from constants import RESULT_HOME_WIN, RESULT_DRAW, RESULT_AWAY_WIN
from logger import get_logger

log = get_logger(__name__)

FEATURES_FILE = CONFIG.features_file
MATCHES_FILE = CONFIG.historical_file
MODEL_FILE = CONFIG.model_file

FEATURE_COLS = [
    "home_avg_goals_for_5", "home_avg_goals_against_5", "home_win_rate_5",
    "away_avg_goals_for_5", "away_avg_goals_against_5", "away_win_rate_5",
]


def load_data(matches_file: str, features_file: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load finished matches and feature CSV files, adding a result column."""
    matches = pd.read_csv(matches_file)
    matches = matches[matches["status"] == "FINISHED"].copy()
    matches["utcDate"] = pd.to_datetime(matches["utcDate"])
    matches["result"] = matches.apply(
        lambda r: RESULT_HOME_WIN if r["homeScore"] > r["awayScore"]
        else (RESULT_AWAY_WIN if r["homeScore"] < r["awayScore"] else RESULT_DRAW),
        axis=1,
    )
    features = pd.read_csv(features_file)
    features["utcDate"] = pd.to_datetime(features["utcDate"])
    return matches, features


def build_training_set(matches: pd.DataFrame, features: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Join matches with pre-match team features to form (X, y) training pairs."""
    X_rows, y_rows = [], []
    for _, match in matches.iterrows():
        home, away, date = match["homeTeam"], match["awayTeam"], match["utcDate"]
        home_s = features[(features["team"] == home) & (features["utcDate"] < date) & features["is_home"]].sort_values("utcDate").tail(1)
        away_s = features[(features["team"] == away) & (features["utcDate"] < date) & ~features["is_home"]].sort_values("utcDate").tail(1)
        if home_s.empty or away_s.empty:
            continue
        X_rows.append([
            home_s["avg_goals_5"].values[0], home_s["avg_goals_against_5"].values[0], home_s["win_rate_5"].values[0],
            away_s["avg_goals_5"].values[0], away_s["avg_goals_against_5"].values[0], away_s["win_rate_5"].values[0],
        ])
        y_rows.append(match["result"])
    return pd.DataFrame(X_rows, columns=FEATURE_COLS), pd.Series(y_rows)


def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series) -> float:
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    log.info("Accuracy: %.3f", acc)
    log.info("Classification report:\n%s", classification_report(y_test, y_pred))
    return acc


def cross_validate_model(model, X: pd.DataFrame, y: pd.Series, cv: int = 5) -> np.ndarray:
    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=CONFIG.random_state)
    scores = cross_val_score(model, X, y, cv=skf, scoring="accuracy")
    log.info("CV accuracy: %.3f ± %.3f", scores.mean(), scores.std())
    return scores


def train(matches_file: str = MATCHES_FILE, features_file: str = FEATURES_FILE, model_file: str = MODEL_FILE):
    matches, features = load_data(matches_file, features_file)
    X, y = build_training_set(matches, features)
    log.info("Training set: %d samples, %d features", len(X), X.shape[1])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=CONFIG.test_size, random_state=CONFIG.random_state, stratify=y
    )

    rf = RandomForestClassifier(n_estimators=200, random_state=CONFIG.random_state, n_jobs=-1)
    gb = GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, max_depth=4, random_state=CONFIG.random_state)

    importances = dict(zip(FEATURE_COLS, rf.feature_importances_))
    for feat, imp in sorted(importances.items(), key=lambda x: -x[1]):
        log.info("Feature importance: %-35s %.4f", feat, imp)

    for name, clf in [("RandomForest", rf), ("GradientBoosting", gb)]:
        clf.fit(X_train, y_train)
        acc = evaluate_model(clf, X_test, y_test)
        log.info("%s test accuracy: %.3f", name, acc)

    cv_scores = cross_validate_model(rf, X, y)

    model = CalibratedClassifierCV(rf, cv=3, method="isotonic")
    model.fit(X_train, y_train)

    joblib.dump(model, model_file)
    log.info("Model saved to %s", model_file)
    return model


if __name__ == "__main__":
    train()
