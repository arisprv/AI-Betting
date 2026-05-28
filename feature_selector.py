"""Feature selection utilities to remove low-importance and correlated features."""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from logger import get_logger

log = get_logger(__name__)


def importance_based_selection(X: pd.DataFrame, y: pd.Series,
                                threshold: float = 0.01,
                                random_state: int = 42) -> list[str]:
    """Return feature names with importance >= threshold."""
    rf = RandomForestClassifier(n_estimators=100, random_state=random_state, n_jobs=-1)
    rf.fit(X, y)
    importances = dict(zip(X.columns, rf.feature_importances_))
    selected = [f for f, imp in importances.items() if imp >= threshold]
    dropped = [f for f in X.columns if f not in selected]
    log.info("Selected %d features, dropped %d (threshold=%.3f)", len(selected), len(dropped), threshold)
    if dropped:
        log.debug("Dropped features: %s", dropped)
    return selected


def correlation_filter(X: pd.DataFrame, threshold: float = 0.95) -> list[str]:
    """Remove one of each pair of features with correlation > threshold."""
    corr = X.corr().abs()
    upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
    to_drop = [col for col in upper.columns if (upper[col] > threshold).any()]
    selected = [c for c in X.columns if c not in to_drop]
    if to_drop:
        log.info("Correlation filter dropped %d features: %s", len(to_drop), to_drop)
    return selected


def select_features(X: pd.DataFrame, y: pd.Series,
                    importance_threshold: float = 0.01,
                    correlation_threshold: float = 0.95) -> list[str]:
    """Apply importance-based then correlation-based feature selection."""
    candidates = importance_based_selection(X, y, importance_threshold)
    return correlation_filter(X[candidates], correlation_threshold)
