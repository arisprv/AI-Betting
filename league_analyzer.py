import pandas as pd
from logger import get_logger

log = get_logger(__name__)


def home_advantage(matches: pd.DataFrame) -> pd.Series:
    finished = matches.copy()
    finished["result"] = finished.apply(
        lambda r: "home" if r["homeScore"] > r["awayScore"]
        else ("draw" if r["homeScore"] == r["awayScore"] else "away"),
        axis=1,
    )
    rates = finished.groupby("league")["result"].value_counts(normalize=True).unstack(fill_value=0)
    return rates.get("home", pd.Series(dtype=float))


def avg_goals_per_match(matches: pd.DataFrame) -> pd.Series:
    matches = matches.copy()
    matches["total_goals"] = matches["homeScore"] + matches["awayScore"]
    return matches.groupby("league")["total_goals"].mean()


def btts_rate_by_league(matches: pd.DataFrame) -> pd.Series:
    def btts(r):
        return r["homeScore"] > 0 and r["awayScore"] > 0
    matches = matches.copy()
    matches["btts"] = matches.apply(btts, axis=1)
    return matches.groupby("league")["btts"].mean()


def over_under_rate(matches: pd.DataFrame, threshold: float = 2.5) -> pd.Series:
    matches = matches.copy()
    matches["over"] = (matches["homeScore"] + matches["awayScore"]) > threshold
    return matches.groupby("league")["over"].mean()


def league_summary(matches: pd.DataFrame) -> pd.DataFrame:
    ha = home_advantage(matches).rename("home_win_rate")
    avg_g = avg_goals_per_match(matches).rename("avg_goals")
    btts = btts_rate_by_league(matches).rename("btts_rate")
    ou = over_under_rate(matches).rename("over_2_5_rate")
    return pd.concat([ha, avg_g, btts, ou], axis=1)
