from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Config:
    football_api_token: str = "55232aed707e498c914f70d4cf2f40c3"
    odds_api_key: str = "ad6045f62362a96a24924113faa405eb"
    season: int = 2025
    rolling_window: int = 5
    test_size: float = 0.25
    random_state: int = 42
    model_file: str = "football_model_v5.pkl"
    historical_file: str = "matches_2025.csv"
    upcoming_file: str = "upcoming_matches_2025.csv"
    features_file: str = "team_features_2025.csv"
    predictions_file: str = "predictions_multileague_2025.csv"
    value_bets_file: str = "value_bets_multileague_2025.csv"
    odds_regions: str = "uk"
    odds_markets: str = "h2h"
    leagues: Dict[str, str] = field(default_factory=lambda: {
        "PL": "Premier League",
        "PD": "La Liga",
        "SA": "Serie A",
        "BL1": "Bundesliga",
        "FL1": "Ligue 1",
    })
    odds_leagues: Dict[str, str] = field(default_factory=lambda: {
        "soccer_epl": "Premier League",
        "soccer_spain_la_liga": "La Liga",
        "soccer_italy_serie_a": "Serie A",
        "soccer_germany_bundesliga": "Bundesliga",
        "soccer_france_ligue_one": "Ligue 1",
    })


CONFIG = Config()