"""
Disk-based cache for API responses to avoid redundant requests.
Cache entries expire after DEFAULT_TTL_HOURS and are stored as JSON files.
"""
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from logger import get_logger

log = get_logger(__name__)

CACHE_DIR = ".api_cache"
DEFAULT_TTL_HOURS = 6


def _cache_key(url: str, params: dict) -> str:
    raw = url + json.dumps(params or {}, sort_keys=True)
    return hashlib.md5(raw.encode()).hexdigest()


def _cache_path(key: str) -> Path:
    return Path(CACHE_DIR) / f"{key}.json"


def cache_stats() -> dict:
    """Return count and total size of cached files."""
    cache_dir = Path(CACHE_DIR)
    if not cache_dir.exists():
        return {"count": 0, "size_bytes": 0}
    files = list(cache_dir.glob("*.json"))
    total_size = sum(f.stat().st_size for f in files)
    return {"count": len(files), "size_bytes": total_size}


def get_cached(url: str, params: dict = None, ttl_hours: int = DEFAULT_TTL_HOURS):
    """Return cached response dict or None if missing/expired."""
    path = _cache_path(_cache_key(url, params))
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    cached_at = datetime.fromisoformat(data["_cached_at"])
    if datetime.now() - cached_at > timedelta(hours=ttl_hours):
        log.debug("Cache expired for %s", url)
        return None
    return data["payload"]


def set_cached(url: str, payload, params: dict = None) -> None:
    """Write response to disk cache."""
    Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)
    path = _cache_path(_cache_key(url, params))
    path.write_text(json.dumps({"_cached_at": datetime.now().isoformat(), "payload": payload}, default=str))
    log.debug("Cached response for %s", url)


def clear_cache() -> int:
    """Delete all cache files. Returns count of deleted files."""
    cache_dir = Path(CACHE_DIR)
    if not cache_dir.exists():
        return 0
    files = list(cache_dir.glob("*.json"))
    for f in files:
        f.unlink()
    log.info("Cleared %d cache files", len(files))
    return len(files)
