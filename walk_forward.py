"""Walk-forward cross-validation for time-series aware model evaluation."""
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from logger import get_logger

log = get_logger(__name__)


def walk_forward_splits(df: pd.DataFrame, date_col: str = "utcDate",
                         n_splits: int = 5, min_train_size: int = 100):
    """
    Generate (train_idx, test_idx) pairs using expanding window.
    Each fold tests on the next chronological chunk after training.
    """
    df = df.sort_values(date_col).reset_index(drop=True)
    n = len(df)
    step = (n - min_train_size) // n_splits

    for i in range(n_splits):
        train_end = min_train_size + i * step
        test_end = min(train_end + step, n)
        if train_end >= n:
            break
        yield list(range(train_end)), list(range(train_end, test_end))


def walk_forward_evaluate(model_factory, X: pd.DataFrame, y: pd.Series,
                           dates: pd.Series, n_splits: int = 5) -> dict:
    """
    Train and evaluate model using walk-forward expanding window.
    Returns per-fold and overall accuracy scores.
    """
    combined = X.copy()
    combined["_date"] = dates.values
    combined["_y"] = y.values
    combined = combined.sort_values("_date").reset_index(drop=True)

    X_sorted = combined.drop(columns=["_date", "_y"])
    y_sorted = combined["_y"]
    dates_sorted = combined["_date"]

    dummy_df = pd.DataFrame({"utcDate": dates_sorted})
    splits = list(walk_forward_splits(dummy_df, date_col="utcDate", n_splits=n_splits))

    fold_scores = []
    for fold, (train_idx, test_idx) in enumerate(splits, 1):
        if not test_idx:
            continue
        X_train, X_test = X_sorted.iloc[train_idx], X_sorted.iloc[test_idx]
        y_train, y_test = y_sorted.iloc[train_idx], y_sorted.iloc[test_idx]

        model = model_factory()
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        fold_scores.append(acc)
        log.info("Walk-forward fold %d: accuracy=%.3f (train=%d, test=%d)",
                 fold, acc, len(train_idx), len(test_idx))

    return {
        "fold_scores": fold_scores,
        "mean_accuracy": float(np.mean(fold_scores)) if fold_scores else 0.0,
        "std_accuracy": float(np.std(fold_scores)) if fold_scores else 0.0,
    }
