import pandas as pd
import numpy as np
import pytest
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from model_comparison import compare_models, best_model


@pytest.fixture
def sample_data():
    np.random.seed(42)
    X = pd.DataFrame(np.random.randn(100, 4), columns=["f1", "f2", "f3", "f4"])
    y = pd.Series(np.random.choice([0, 1, -1], size=100))
    return X, y


def test_compare_models_returns_df(sample_data):
    X, y = sample_data
    models = {
        "rf": RandomForestClassifier(n_estimators=10, random_state=42),
        "lr": LogisticRegression(max_iter=200, random_state=42),
    }
    result = compare_models(models, X, y, cv=3)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2


def test_compare_models_columns(sample_data):
    X, y = sample_data
    models = {"rf": RandomForestClassifier(n_estimators=10, random_state=42)}
    result = compare_models(models, X, y, cv=3)
    assert "cv_accuracy_mean" in result.columns
    assert "model" in result.columns


def test_best_model_returns_name(sample_data):
    X, y = sample_data
    models = {
        "rf": RandomForestClassifier(n_estimators=10, random_state=42),
        "lr": LogisticRegression(max_iter=200, random_state=42),
    }
    df = compare_models(models, X, y, cv=3)
    name, est = best_model(df, models)
    assert name in models
