import pandas as pd
from pathlib import Path
from datetime import datetime
from logger import get_logger

log = get_logger(__name__)


class FeatureStore:
    """Simple file-backed feature store with versioning support."""

    def __init__(self, store_dir: str = "feature_store"):
        self.store_dir = Path(store_dir)
        self.store_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, name: str, version: str) -> Path:
        return self.store_dir / f"{name}_v{version}.csv"

    def save(self, df: pd.DataFrame, name: str, version: str = None) -> str:
        if version is None:
            version = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = self._path(name, version)
        df.to_csv(path, index=False)
        log.info("Saved feature set '%s' version '%s' (%d rows) to %s", name, version, len(df), path)
        return version

    def load(self, name: str, version: str) -> pd.DataFrame:
        path = self._path(name, version)
        if not path.exists():
            raise FileNotFoundError(f"Feature set '{name}' version '{version}' not found at {path}")
        return pd.read_csv(path)

    def list_versions(self, name: str) -> list[str]:
        return sorted(p.stem.replace(f"{name}_v", "") for p in self.store_dir.glob(f"{name}_v*.csv"))

    def latest(self, name: str) -> pd.DataFrame:
        versions = self.list_versions(name)
        if not versions:
            raise FileNotFoundError(f"No versions found for feature set '{name}'")
        return self.load(name, versions[-1])
