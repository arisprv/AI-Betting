import argparse
import joblib
import pandas as pd
from config import CONFIG
from feature_engineering import build_features
from fetch_football_data import FootballDataClient
from train_model import train, FEATURE_COLS
from logger import get_logger

log = get_logger(__name__)


def run_fetch(args):
    client = FootballDataClient()
    hist_df, upcoming_df = client.fetch_all_leagues()
    hist_df.to_csv(CONFIG.historical_file, index=False)
    upcoming_df.to_csv(CONFIG.upcoming_file, index=False)
    log.info("Fetched %d historical, %d upcoming matches", len(hist_df), len(upcoming_df))


def run_features(args):
    features_df = build_features(CONFIG.historical_file)
    features_df.to_csv(CONFIG.features_file, index=False)
    log.info("Built features: %d rows saved to %s", len(features_df), CONFIG.features_file)


def run_train(args):
    train(CONFIG.historical_file, CONFIG.features_file, CONFIG.model_file)


def run_predict(args):
    from predict_daily import run_predictions
    run_predictions()


def run_full(args):
    run_fetch(args)
    run_features(args)
    run_train(args)
    run_predict(args)


def main():
    parser = argparse.ArgumentParser(description="Football prediction pipeline")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("fetch", help="Fetch match data from API")
    sub.add_parser("features", help="Build feature set")
    sub.add_parser("train", help="Train prediction model")
    sub.add_parser("predict", help="Generate predictions")
    sub.add_parser("full", help="Run full pipeline")

    args = parser.parse_args()
    commands = {
        "fetch": run_fetch,
        "features": run_features,
        "train": run_train,
        "predict": run_predict,
        "full": run_full,
    }

    handler = commands.get(args.command)
    if handler is None:
        parser.print_help()
    else:
        handler(args)


if __name__ == "__main__":
    main()
