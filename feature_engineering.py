import pandas as pd
from logger import get_logger

log = get_logger(__name__)

HISTORICAL_FILE = "matches_2025.csv"
FEATURES_FILE = "team_features_2025.csv"
ROLLING_WINDOW = 5


def _goals_for(match: pd.Series, team: str) -> int:
    return match["homeScore"] if match["homeTeam"] == team else match["awayScore"]


def _goals_against(match: pd.Series, team: str) -> int:
    return match["awayScore"] if match["homeTeam"] == team else match["homeScore"]


def _result(gf: int, ga: int) -> int:
    return 1 if gf > ga else 0 if gf == ga else -1


def compute_team_features(league_df: pd.DataFrame, team: str, window: int) -> list[dict]:
    records = []
    team_matches = league_df[
        (league_df["homeTeam"] == team) | (league_df["awayTeam"] == team)
    ].sort_values("date")

    for idx, match in team_matches.iterrows():
        is_home = match["homeTeam"] == team
        gf = _goals_for(match, team)
        ga = _goals_against(match, team)

        prev = team_matches[team_matches["date"] < match["date"]].tail(window)
        prev_home = prev[prev["homeTeam"] == team]
        prev_away = prev[prev["awayTeam"] == team]
        if prev.empty:
            avg_goals = avg_goals_against = win_rate = 0.0
            home_win_rate = away_win_rate = 0.0
        else:
            prev_gf = [_goals_for(m, team) for _, m in prev.iterrows()]
            prev_ga = [_goals_against(m, team) for _, m in prev.iterrows()]
            results = [_result(f, a) for f, a in zip(prev_gf, prev_ga)]
            avg_goals = sum(prev_gf) / len(prev_gf)
            avg_goals_against = sum(prev_ga) / len(prev_ga)
            win_rate = results.count(1) / len(results)
            home_results = [_result(_goals_for(m, team), _goals_against(m, team)) for _, m in prev_home.iterrows()]
            away_results = [_result(_goals_for(m, team), _goals_against(m, team)) for _, m in prev_away.iterrows()]
            home_win_rate = home_results.count(1) / len(home_results) if home_results else 0.0
            away_win_rate = away_results.count(1) / len(away_results) if away_results else 0.0

        draw_rate = results.count(0) / len(results) if not prev.empty else 0.0
        loss_rate = results.count(-1) / len(results) if not prev.empty else 0.0
        goal_diff_avg = (avg_goals - avg_goals_against) if not prev.empty else 0.0
        clean_sheets = sum(1 for g in (prev_ga if not prev.empty else []) if g == 0)
        clean_sheet_rate = clean_sheets / len(prev) if not prev.empty else 0.0

        records.append({
            "league": match["league"],
            "utcDate": match["date"],
            "team": team,
            "is_home": is_home,
            "goals_for": gf,
            "goals_against": ga,
            "avg_goals_5": avg_goals,
            "avg_goals_against_5": avg_goals_against,
            "win_rate_5": win_rate,
            "draw_rate_5": draw_rate,
            "loss_rate_5": loss_rate,
            "goal_diff_avg_5": goal_diff_avg,
            "clean_sheet_rate_5": clean_sheet_rate,
            "home_win_rate_5": home_win_rate,
            "away_win_rate_5": away_win_rate,
        })

    return records


def build_features(historical_file: str = HISTORICAL_FILE, window: int = ROLLING_WINDOW) -> pd.DataFrame:
    df = pd.read_csv(historical_file)
    df["date"] = pd.to_datetime(df["date"])
    all_records = []

    for league in df["league"].unique():
        league_df = df[df["league"] == league]
        teams = pd.unique(league_df[["homeTeam", "awayTeam"]].values.ravel())
        log.info("Processing league %s (%d teams)", league, len(teams))
        for team in teams:
            all_records.extend(compute_team_features(league_df, team, window))

    return pd.DataFrame(all_records).sort_values(["league", "team", "utcDate"])


if __name__ == "__main__":
    features_df = build_features()
    features_df.to_csv(FEATURES_FILE, index=False)
    log.info("Saved features for all teams to %s", FEATURES_FILE)
