"""Expected goals (xG) derived features for teams."""
import pandas as pd
from logger import get_logger

log = get_logger(__name__)


def compute_xg_ratio(avg_goals_scored: float, avg_goals_conceded: float,
                      league_avg: float = 1.35) -> dict[str, float]:
    """Return attack and defence strength ratios relative to league average."""
    if league_avg == 0:
        return {"attack_strength": 1.0, "defence_strength": 1.0}
    return {
        "attack_strength": avg_goals_scored / league_avg,
        "defence_strength": avg_goals_conceded / league_avg,
    }


def expected_goals_conceded(opponent_attack: float, team_defence: float,
                              league_avg: float = 1.35) -> float:
    """Dixon-Coles style xGC estimate."""
    return opponent_attack * team_defence * league_avg


def add_xg_features(features: pd.DataFrame, league_avg_goals: float = 1.35) -> pd.DataFrame:
    """Enrich features DataFrame with attack/defence strength and xG estimates."""
    df = features.copy()
    df["attack_strength"] = df["avg_goals_5"] / league_avg_goals
    df["defence_strength"] = df["avg_goals_against_5"] / league_avg_goals
    df["xg_ratio"] = df["attack_strength"] / df["defence_strength"].replace(0, 1)
    return df
