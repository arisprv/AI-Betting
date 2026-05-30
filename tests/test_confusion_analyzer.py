import numpy as np
import pytest
from confusion_analyzer import confusion_df, most_confused_pair, error_analysis


def test_confusion_df_shape():
    y_true = [1, 0, -1, 1, 0]
    y_pred = [1, 1, -1, 0, 0]
    df = confusion_df(y_true, y_pred)
    assert df.shape == (3, 3)


def test_confusion_df_diagonal_correct():
    y_true = [1, 1, 0, 0]
    y_pred = [1, 1, 0, 0]
    df = confusion_df(y_true, y_pred)
    assert df.values.diagonal().sum() == 4


def test_error_analysis_returns_only_mistakes():
    y_true = [1, 0, -1, 1]
    y_pred = [1, 1, -1, 0]
    df = error_analysis(y_true, y_pred)
    assert len(df) == 2


def test_error_analysis_empty_when_perfect():
    y_true = [1, 0, -1]
    y_pred = [1, 0, -1]
    df = error_analysis(y_true, y_pred)
    assert df.empty


def test_most_confused_pair():
    y_true = [1, 1, 1, 0]
    y_pred = [0, 0, 0, 0]
    actual, predicted = most_confused_pair(y_true, y_pred)
    assert actual == "Home Win"
    assert predicted == "Draw"
