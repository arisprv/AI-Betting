"""Compare multiple models on the same dataset and pick the best."""
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, log_loss
from sklearn.model_selection import StratifiedKFold, cross_val_score
from logger import get_logger

log = get_logger(__name__)


def compare_models(models: dict, X: pd.DataFrame, y: pd.Series,
                    cv: int = 5, random_state: int = 42) -> pd.DataFrame:
    """
    Cross-validate each model and return a comparison DataFrame.
    models: dict of name -> sklearn estimator
    """
    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=random_state)
    results = []
    for name, model in models.items():
        acc_scores = cross_val_score(model, X, y, cv=skf, scoring="accuracy")
        f1_scores = cross_val_score(model, X, y, cv=skf, scoring="f1_weighted")
        results.append({
            "model": name,
            "cv_accuracy_mean": round(acc_scores.mean(), 4),
            "cv_accuracy_std": round(acc_scores.std(), 4),
            "cv_f1_mean": round(f1_scores.mean(), 4),
            "cv_f1_std": round(f1_scores.std(), 4),
        })
        log.info("[%s] accuracy=%.3f±%.3f  f1=%.3f±%.3f",
                 name, acc_scores.mean(), acc_scores.std(), f1_scores.mean(), f1_scores.std())

    df = pd.DataFrame(results).sort_values("cv_accuracy_mean", ascending=False).reset_index(drop=True)
    return df


def best_model(comparison_df: pd.DataFrame, models: dict):
    """Return the name and estimator of the highest-accuracy model."""
    best_name = comparison_df.iloc[0]["model"]
    return best_name, models[best_name]
