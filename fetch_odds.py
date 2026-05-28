import pandas as pd
from api_client import APIClient
from config import CONFIG
from constants import ODDS_API_BASE
from logger import get_logger

log = get_logger(__name__)


class OddsClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or CONFIG.odds_api_key
        self.client = APIClient(ODDS_API_BASE)

    def fetch_sport_odds(self, sport: str, regions: str = None, markets: str = None) -> list[dict]:
        params = {
            "apiKey": self.api_key,
            "regions": regions or CONFIG.odds_regions,
            "markets": markets or CONFIG.odds_markets,
        }
        log.info("Fetching odds for %s", sport)
        return self.client.get(f"sports/{sport}/odds/", params=params)

    def parse_odds(self, data: list[dict], league: str) -> list[dict]:
        records = []
        for match in data:
            home = match.get("home_team", "")
            away = match.get("away_team", "")
            for bookmaker in match.get("bookmakers", []):
                markets = bookmaker.get("markets", [])
                if not markets:
                    continue
                outcomes = {o["name"]: o["price"] for o in markets[0].get("outcomes", [])}
                records.append({
                    "league": league,
                    "home_team": home,
                    "away_team": away,
                    "bookmaker": bookmaker.get("title", ""),
                    "home_odds": outcomes.get(home),
                    "draw_odds": outcomes.get("Draw"),
                    "away_odds": outcomes.get(away),
                })
        return records


def fetch_all_odds(leagues: dict = None) -> pd.DataFrame:
    leagues = leagues or CONFIG.odds_leagues
    client = OddsClient()
    all_records = []
    for sport, league_name in leagues.items():
        try:
            data = client.fetch_sport_odds(sport)
            records = client.parse_odds(data, league_name)
            all_records.extend(records)
            log.info("Fetched %d odds rows for %s", len(records), league_name)
        except Exception as exc:
            log.warning("Failed to fetch odds for %s: %s", league_name, exc)
    return pd.DataFrame(all_records)


if __name__ == "__main__":
    odds_df = fetch_all_odds()
    odds_df.to_csv("live_odds.csv", index=False)
    log.info("Saved %d odds rows to live_odds.csv", len(odds_df))
