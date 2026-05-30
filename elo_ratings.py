"""
Simple Elo rating system for football teams.
Based on the classic Elo formulation with a home advantage adjustment.
"""
import math
from collections import defaultdict
from typing import Optional
from logger import get_logger

log = get_logger(__name__)

DEFAULT_RATING = 1500.0
K_FACTOR = 32
HOME_ADVANTAGE = 100


def expected_score(rating_a: float, rating_b: float) -> float:
    """Return the expected score (win probability) for team A vs team B."""
    return 1 / (1 + math.pow(10, (rating_b - rating_a) / 400))


def update_ratings(rating_home: float, rating_away: float, home_score: int, away_score: int
                   ) -> tuple[float, float]:
    """Update Elo ratings after a match result."""
    if home_score > away_score:
        actual_home, actual_away = 1.0, 0.0
    elif home_score == away_score:
        actual_home, actual_away = 0.5, 0.5
    else:
        actual_home, actual_away = 0.0, 1.0

    expected_home = expected_score(rating_home + HOME_ADVANTAGE, rating_away)
    expected_away = 1 - expected_home

    new_home = rating_home + K_FACTOR * (actual_home - expected_home)
    new_away = rating_away + K_FACTOR * (actual_away - expected_away)
    return new_home, new_away


def rating_diff_to_prob(home_rating: float, away_rating: float) -> float:
    """Convert Elo rating difference to win probability for the home team."""
    return expected_score(home_rating + HOME_ADVANTAGE, away_rating)


def build_elo_ratings(matches, default_rating: float = DEFAULT_RATING) -> dict[str, float]:
    """Compute final Elo ratings from a sorted sequence of match rows."""
    ratings: dict[str, float] = defaultdict(lambda: default_rating)
    for _, match in matches.sort_values("date").iterrows():
        home, away = match["homeTeam"], match["awayTeam"]
        new_h, new_a = update_ratings(ratings[home], ratings[away], match["homeScore"], match["awayScore"])
        ratings[home] = new_h
        ratings[away] = new_a
    return dict(ratings)
