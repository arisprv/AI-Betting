import numpy as np
import pandas as pd
import pytest
from unittest.mock import MagicMock
from feature_importance_reporter import extract_importances, top_features


def make_mock_model(n_features: int = 6):
    model = MagicMock()
    model.feature_importances_ = np.random.dirichlet(np.ones(n_features))
    del model.estimators_
    return model


FEATURE_NAMES = ["home_goals", "home_conceded", "home_wins", "away_goals", "away_conceded", "away_wins"]


def test_extract_importances_shape():
    model = make_mock_model(6)
    df = extract_importances(model, FEATURE_NAMES)
    assert len(df) == 6


def test_extract_importances_sorted():
    model = make_mock_model(6)
    df = extract_importances(model, FEATURE_NAMES)
    imps = df["importance"].tolist()
    assert imps == sorted(imps, reverse=True)


def test_extract_importances_columns():
    model = make_mock_model(6)
    df = extract_importances(model, FEATURE_NAMES)
    assert "feature" in df.columns and "importance" in df.columns


def test_top_features_count():
    model = make_mock_model(6)
    top = top_features(model, FEATURE_NAMES, n=3)
    assert len(top) == 3


def test_no_feature_importances():
    model = MagicMock(spec=[])
    df = extract_importances(model, FEATURE_NAMES)
    assert df.empty
