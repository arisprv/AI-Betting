import json
import joblib
from datetime import datetime
from pathlib import Path
from logger import get_logger

log = get_logger(__name__)

REGISTRY_FILE = "model_registry.json"


class ModelRegistry:
    """Lightweight local model registry tracking model versions and metadata."""

    def __init__(self, models_dir: str = "models", registry_file: str = REGISTRY_FILE):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.registry_path = Path(registry_file)
        self._data = self._load()

    def _load(self) -> dict:
        if self.registry_path.exists():
            return json.loads(self.registry_path.read_text())
        return {"models": []}

    def _save(self) -> None:
        self.registry_path.write_text(json.dumps(self._data, indent=2, default=str))

    def register(self, model, name: str, metrics: dict = None, tags: dict = None) -> str:
        version = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_path = self.models_dir / f"{name}_{version}.pkl"
        joblib.dump(model, model_path)
        entry = {
            "name": name,
            "version": version,
            "path": str(model_path),
            "metrics": metrics or {},
            "tags": tags or {},
            "registered_at": datetime.now().isoformat(),
        }
        self._data["models"].append(entry)
        self._save()
        log.info("Registered model '%s' version '%s' at %s", name, version, model_path)
        return version

    def get_latest(self, name: str):
        models = [m for m in self._data["models"] if m["name"] == name]
        if not models:
            raise KeyError(f"No model '{name}' found in registry")
        latest = sorted(models, key=lambda m: m["version"])[-1]
        return joblib.load(latest["path"]), latest

    def list_models(self, name: str = None) -> list[dict]:
        if name:
            return [m for m in self._data["models"] if m["name"] == name]
        return self._data["models"]
