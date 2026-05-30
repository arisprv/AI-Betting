"""Analyse where the model makes mistakes using confusion matrix breakdown."""
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
from constants import RESULT_HOME_WIN, RESULT_DRAW, RESULT_AWAY_WIN, RESULT_LABELS
from logger import get_logger

log = get_logger(__name__)

CLASSES = [RESULT_AWAY_WIN, RESULT_DRAW, RESULT_HOME_WIN]
CLASS_LABELS = [RESULT_LABELS[c] for c in CLASSES]


def confusion_df(y_true, y_pred) -> pd.DataFrame:
    """Return confusion matrix as a labelled DataFrame."""
    cm = confusion_matrix(y_true, y_pred, labels=CLASSES)
    return pd.DataFrame(cm, index=CLASS_LABELS, columns=[f"Pred {l}" for l in CLASS_LABELS])


def most_confused_pair(y_true, y_pred) -> tuple[str, str]:
    """Return the most commonly confused (actual, predicted) pair."""
    df = confusion_df(y_true, y_pred)
    np.fill_diagonal(df.values, 0)
    idx = np.unravel_index(df.values.argmax(), df.shape)
    return CLASS_LABELS[idx[0]], df.columns[idx[1]].replace("Pred ", "")


def print_classification_report(y_true, y_pred) -> None:
    report = classification_report(y_true, y_pred, labels=CLASSES,
                                    target_names=CLASS_LABELS, zero_division=0)
    log.info("Classification Report:\n%s", report)


def error_analysis(y_true, y_pred, match_labels: list[str] = None) -> pd.DataFrame:
    """Return a DataFrame of misclassified predictions for further analysis."""
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    mask = y_true != y_pred
    rows = []
    for i, wrong in enumerate(mask):
        if wrong:
            rows.append({
                "index": i,
                "match": match_labels[i] if match_labels else i,
                "actual": RESULT_LABELS.get(y_true[i], str(y_true[i])),
                "predicted": RESULT_LABELS.get(y_pred[i], str(y_pred[i])),
            })
    return pd.DataFrame(rows)
