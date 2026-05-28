import pandas as pd
from logger import get_logger

log = get_logger(__name__)


def get_h2h_stats(matches: pd.DataFrame, home: str, away: str, n: int = 5) -> dict:
    """Return head-to-head stats between two teams from the last n encounters."""
    h2h = matches[
        ((matches["homeTeam"] == home) & (matches["awayTeam"] == away)) |
        ((matches["homeTeam"] == away) & (matches["awayTeam"] == home))
    ].sort_values("date").tail(n)

    if h2h.empty:
        return {"h2h_count": 0, "h2h_home_wins": 0.0, "h2h_draws": 0.0, "h2h_away_wins": 0.0, "h2h_avg_goals": 0.0}

    home_wins = draws = away_wins = 0
    for _, match in h2h.iterrows():
        hs, as_ = match["homeScore"], match["awayScore"]
        actual_home = match["homeTeam"] == home
        if hs > as_:
            if actual_home:
                home_wins += 1
            else:
                away_wins += 1
        elif hs == as_:
            draws += 1
        else:
            if actual_home:
                away_wins += 1
            else:
                home_wins += 1

    n_matches = len(h2h)
    return {
        "h2h_count": n_matches,
        "h2h_home_wins": home_wins / n_matches,
        "h2h_draws": draws / n_matches,
        "h2h_away_wins": away_wins / n_matches,
        "h2h_avg_goals": (h2h["homeScore"] + h2h["awayScore"]).mean(),
    }


def enrich_with_h2h(upcoming: pd.DataFrame, matches: pd.DataFrame) -> pd.DataFrame:
    """Add H2H columns to each upcoming match row."""
    h2h_rows = []
    for _, row in upcoming.iterrows():
        stats = get_h2h_stats(matches, row["homeTeam"], row["awayTeam"])
        h2h_rows.append(stats)
    return pd.concat([upcoming.reset_index(drop=True), pd.DataFrame(h2h_rows)], axis=1)
