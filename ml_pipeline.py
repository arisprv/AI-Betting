"""End-to-end ML pipeline: clean → feature engineer → select → train → evaluate."""
import pandas as pd
from data_cleaner import clean_matches
from feature_engineering import build_features
from feature_selector import select_features
from train_model import build_training_set, evaluate_model, cross_validate_model, FEATURE_COLS
from model_comparison import compare_models, best_model
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.calibration import CalibratedClassifierCV
from config import CONFIG
from logger import get_logger

log = get_logger(__name__)


def run_ml_pipeline(matches_file: str = None, features_file: str = None) -> tuple:
    """
    Run the full ML pipeline from raw match CSV to a trained, calibrated model.
    Returns (model, selected_features, metrics).
    """
    matches_file = matches_file or CONFIG.historical_file
    features_file = features_file or CONFIG.features_file

    log.info("=== ML Pipeline Started ===")

    # Step 1: Load and clean
    raw_matches = pd.read_csv(matches_file)
    matches = clean_matches(raw_matches)
    log.info("Cleaned %d/%d matches", len(matches), len(raw_matches))

    # Step 2: Features
    features = pd.read_csv(features_file)
    features["utcDate"] = pd.to_datetime(features["utcDate"])

    # Step 3: Build training set
    X, y = build_training_set(matches, features)
    if X.empty:
        raise ValueError("Training set is empty — check input data")
    log.info("Training set: %d samples, %d features", len(X), X.shape[1])

    # Step 4: Feature selection
    selected = select_features(X, y)
    X = X[selected]
    log.info("Selected %d features: %s", len(selected), selected)

    # Step 5: Model comparison
    models = {
        "rf": RandomForestClassifier(n_estimators=200, random_state=CONFIG.random_state, n_jobs=-1),
        "gb": GradientBoostingClassifier(n_estimators=200, random_state=CONFIG.random_state),
    }
    comparison = compare_models(models, X, y)
    best_name, base_model = best_model(comparison, models)
    log.info("Best model: %s", best_name)

    # Step 6: Calibrate and return
    final_model = CalibratedClassifierCV(base_model, cv=3)
    final_model.fit(X, y)

    metrics = {
        "best_model": best_name,
        "n_samples": len(X),
        "n_features": len(selected),
        "comparison": comparison.to_dict(orient="records"),
    }
    log.info("=== ML Pipeline Complete ===")
    return final_model, selected, metrics
