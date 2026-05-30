"""Analyse referee tendencies — cards per game, home bias, foul rates."""
import pandas as pd
from logger import get_logger

log = get_logger(__name__)


def cards_per_game(matches: pd.DataFrame, referee_col: str = "referee") -> pd.Series:
    """Return average cards per match per referee (if card columns exist)."""
    if referee_col not in matches.columns:
        log.warning("No '%s' column in matches DataFrame", referee_col)
        return pd.Series(dtype=float)
    card_cols = [c for c in ["homeYellow", "awayYellow", "homeRed", "awayRed"] if c in matches.columns]
    if not card_cols:
        return pd.Series(dtype=float)
    matches = matches.copy()
    matches["total_cards"] = matches[card_cols].sum(axis=1)
    return matches.groupby(referee_col)["total_cards"].mean()


def home_bias_score(matches: pd.DataFrame, referee_col: str = "referee") -> pd.Series:
    """Return per-referee home win rate as a proxy for home bias."""
    if referee_col not in matches.columns:
        return pd.Series(dtype=float)
    matches = matches.copy()
    matches["home_win"] = (matches["homeScore"] > matches["awayScore"]).astype(int)
    return matches.groupby(referee_col)["home_win"].mean()


def top_card_referees(matches: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Return top-n referees by average cards issued per game."""
    cpg = cards_per_game(matches)
    if cpg.empty:
        return pd.DataFrame()
    return cpg.nlargest(n).reset_index().rename(columns={0: "avg_cards"})
