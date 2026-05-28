import time
import requests
from logger import get_logger
from constants import MAX_RETRY_ATTEMPTS, RETRY_BACKOFF_SECONDS, REQUEST_TIMEOUT_SECONDS
from exceptions import APIError

log = get_logger(__name__)


class APIClient:
    def __init__(self, base_url: str, headers: dict = None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)

    def get(self, path: str, params: dict = None, use_cache: bool = False) -> dict:
        url = f"{self.base_url}/{path.lstrip('/')}"
        if use_cache:
            from data_cache import get_cached, set_cached
            cached = get_cached(url, params)
            if cached is not None:
                log.debug("Cache hit for %s", url)
                return cached
        for attempt in range(1, MAX_RETRY_ATTEMPTS + 1):
            try:
                resp = self.session.get(url, params=params, timeout=REQUEST_TIMEOUT_SECONDS)
                if resp.status_code == 429:
                    wait = RETRY_BACKOFF_SECONDS * attempt
                    log.warning("Rate limited — waiting %ds (attempt %d/%d)", wait, attempt, MAX_RETRY_ATTEMPTS)
                    time.sleep(wait)
                    continue
                if not resp.ok:
                    raise APIError(f"HTTP {resp.status_code} for {url}", status_code=resp.status_code)
                result = resp.json()
                if use_cache:
                    from data_cache import set_cached
                    set_cached(url, result, params)
                return result
            except requests.RequestException as exc:
                if attempt == MAX_RETRY_ATTEMPTS:
                    raise APIError(str(exc)) from exc
                time.sleep(RETRY_BACKOFF_SECONDS * attempt)
        raise APIError(f"All {MAX_RETRY_ATTEMPTS} attempts failed for {url}")