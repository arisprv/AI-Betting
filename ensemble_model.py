"""Ensemble voting classifier that combines RF, GBM, and Poisson-based probabilities."""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.calibration import CalibratedClassifierCV
from logger import get_logger

log = get_logger(__name__)


def build_ensemble(random_state: int = 42) -> VotingClassifier:
    """Create a soft-voting ensemble of RF and GBM classifiers."""
    rf = CalibratedClassifierCV(
        RandomForestClassifier(n_estimators=200, random_state=random_state, n_jobs=-1),
        cv=3,
    )
    gb = CalibratedClassifierCV(
        GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, max_depth=4, random_state=random_state),
        cv=3,
    )
    ensemble = VotingClassifier(
        estimators=[("rf", rf), ("gb", gb)],
        voting="soft",
    )
    return ensemble


def train_ensemble(X: pd.DataFrame, y: pd.Series, random_state: int = 42) -> VotingClassifier:
    ensemble = build_ensemble(random_state)
    ensemble.fit(X, y)
    log.info("Ensemble trained on %d samples", len(X))
    return ensemble


def ensemble_predict_proba(ensemble: VotingClassifier, X: pd.DataFrame) -> np.ndarray:
    return ensemble.predict_proba(X)


def top_prediction(proba: np.ndarray, classes: np.ndarray) -> tuple[int, float]:
    idx = int(np.argmax(proba))
    return int(classes[idx]), float(proba[idx])
