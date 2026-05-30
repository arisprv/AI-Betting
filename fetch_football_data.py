import pandas as pd
from api_client import APIClient
from config import CONFIG
from constants import FOOTBALL_API_BASE, STATUS_FINISHED, STATUS_SCHEDULED
from logger import get_logger

log = get_logger(__name__)


class FootballDataClient:
    def __init__(self, token: str = None):
        token = token or CONFIG.football_api_token
        self.client = APIClient(FOOTBALL_API_BASE, headers={"X-Auth-Token": token})

    def fetch_matches(self, league_code: str, season: int, status: str,
                      use_cache: bool = False) -> list[dict]:
        log.info("Fetching %s matches for %s season %d", status, league_code, season)
        data = self.client.get(
            f"competitions/{league_code}/matches",
            params={"season": season, "status": status},
            use_cache=use_cache,
        )
        return data.get("matches", [])

    def fetch_standings(self, league_code: str, season: int) -> list[dict]:
        log.info("Fetching standings for %s season %d", league_code, season)
        data = self.client.get(f"competitions/{league_code}/standings", params={"season": season})
        standings = []
        for table in data.get("standings", []):
            if table.get("type") == "TOTAL":
                for entry in table.get("table", []):
                    standings.append({
                        "league": league_code,
                        "season": season,
                        "position": entry["position"],
                        "team": entry["team"]["name"],
                        "played": entry["playedGames"],
                        "won": entry["won"],
                        "draw": entry["draw"],
                        "lost": entry["lost"],
                        "goals_for": entry["goalsFor"],
                        "goals_against": entry["goalsAgainst"],
                        "points": entry["points"],
                    })
        return standings

    def fetch_historical(self, league_code: str, season: int) -> list[dict]:
        matches = self.fetch_matches(league_code, season, STATUS_FINISHED)
        records = []
        for match in matches:
            records.append({
                "league": league_code,
                "date": match["utcDate"],
                "homeTeam": match["homeTeam"]["name"],
                "awayTeam": match["awayTeam"]["name"],
                "homeScore": match["score"]["fullTime"]["home"],
                "awayScore": match["score"]["fullTime"]["away"],
            })
        return records

    def fetch_upcoming(self, league_code: str, season: int) -> list[dict]:
        matches = self.fetch_matches(league_code, season, STATUS_SCHEDULED)
        records = []
        for match in matches:
            records.append({
                "league": league_code,
                "utcDate": match["utcDate"],
                "homeTeam": match["homeTeam"]["name"],
                "awayTeam": match["awayTeam"]["name"],
            })
        return records

    def fetch_multi_season(self, league_code: str, seasons: list[int]) -> pd.DataFrame:
        all_records = []
        for season in seasons:
            try:
                all_records.extend(self.fetch_historical(league_code, season))
            except Exception as exc:
                log.warning("Failed to fetch %s season %d: %s", league_code, season, exc)
        return pd.DataFrame(all_records)

    def fetch_all_leagues(self, leagues: dict = None, season: int = None) -> tuple[pd.DataFrame, pd.DataFrame]:
        leagues = leagues or CONFIG.leagues
        season = season or CONFIG.season
        all_historical = []
        all_upcoming = []

        for code, name in leagues.items():
            log.info("Processing %s (%s)", name, code)
            try:
                all_historical.extend(self.fetch_historical(code, season))
                all_upcoming.extend(self.fetch_upcoming(code, season))
            except Exception as exc:
                log.warning("Failed to fetch %s: %s", name, exc)

        hist_df = pd.DataFrame(all_historical)
        upcoming_df = pd.DataFrame(all_upcoming)

        if not hist_df.empty:
            hist_df["date"] = pd.to_datetime(hist_df["date"])
            hist_df = hist_df.sort_values(["league", "date"])

        if not upcoming_df.empty:
            upcoming_df["utcDate"] = pd.to_datetime(upcoming_df["utcDate"])
            upcoming_df = upcoming_df.sort_values(["league", "utcDate"])

        return hist_df, upcoming_df


if __name__ == "__main__":
    client = FootballDataClient()
    hist_df, upcoming_df = client.fetch_all_leagues()
    hist_df.to_csv(CONFIG.historical_file, index=False)
    upcoming_df.to_csv(CONFIG.upcoming_file, index=False)
    log.info("Saved %d historical and %d upcoming matches", len(hist_df), len(upcoming_df))
