import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from logger import get_logger

log = get_logger(__name__)

RF_PARAM_GRID = {
    "n_estimators": [100, 200, 300],
    "max_depth": [None, 5, 10, 20],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
}

GB_PARAM_GRID = {
    "n_estimators": [100, 200],
    "learning_rate": [0.05, 0.1, 0.2],
    "max_depth": [3, 4, 5],
    "subsample": [0.8, 1.0],
}


def tune_random_forest(X: pd.DataFrame, y: pd.Series, cv: int = 5, n_iter: int = 20, random_state: int = 42):
    """Run randomized search for RandomForest hyperparameters."""
    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=random_state)
    search = RandomizedSearchCV(
        RandomForestClassifier(random_state=random_state, n_jobs=-1),
        RF_PARAM_GRID,
        n_iter=n_iter,
        cv=skf,
        scoring="accuracy",
        random_state=random_state,
        verbose=1,
    )
    search.fit(X, y)
    log.info("Best RF params: %s  (cv acc %.3f)", search.best_params_, search.best_score_)
    return search.best_estimator_, search.best_params_


def tune_gradient_boosting(X: pd.DataFrame, y: pd.Series, cv: int = 5, random_state: int = 42):
    """Run grid search for GradientBoosting hyperparameters."""
    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=random_state)
    search = GridSearchCV(
        GradientBoostingClassifier(random_state=random_state),
        GB_PARAM_GRID,
        cv=skf,
        scoring="accuracy",
        verbose=1,
    )
    search.fit(X, y)
    log.info("Best GB params: %s  (cv acc %.3f)", search.best_params_, search.best_score_)
    return search.best_estimator_, search.best_params_
