"""Generate feature importance reports from trained models."""
import pandas as pd
import numpy as np
from logger import get_logger

log = get_logger(__name__)


def extract_importances(model, feature_names: list[str]) -> pd.DataFrame:
    """Extract feature importances from a sklearn-compatible model."""
    if hasattr(model, "feature_importances_"):
        imps = model.feature_importances_
    elif hasattr(model, "estimators_"):
        # VotingClassifier — average over estimators
        all_imps = []
        for est_name, est in model.estimators:
            if hasattr(est, "feature_importances_"):
                all_imps.append(est.feature_importances_)
        imps = np.mean(all_imps, axis=0) if all_imps else np.zeros(len(feature_names))
    else:
        log.warning("Model has no feature_importances_ attribute")
        return pd.DataFrame()

    df = pd.DataFrame({"feature": feature_names, "importance": imps})
    return df.sort_values("importance", ascending=False).reset_index(drop=True)


def print_importance_report(model, feature_names: list[str]) -> None:
    df = extract_importances(model, feature_names)
    if df.empty:
        return
    log.info("=== Feature Importance Report ===")
    for _, row in df.iterrows():
        bar = "█" * int(row["importance"] * 40)
        log.info("  %-35s %.4f %s", row["feature"], row["importance"], bar)


def top_features(model, feature_names: list[str], n: int = 5) -> list[str]:
    """Return top-n feature names by importance."""
    df = extract_importances(model, feature_names)
    return df["feature"].head(n).tolist()
