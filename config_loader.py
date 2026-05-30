"""Load configuration from YAML or JSON files with env-var overrides."""
import json
import os
from pathlib import Path
from logger import get_logger

log = get_logger(__name__)


def load_json_config(path: str) -> dict:
    """Load a JSON config file."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    data = json.loads(p.read_text())
    log.info("Loaded JSON config from %s", path)
    return data


def load_yaml_config(path: str) -> dict:
    """Load a YAML config file (requires PyYAML)."""
    try:
        import yaml
    except ImportError:
        raise ImportError("PyYAML not installed — run: pip install pyyaml")
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(p) as f:
        data = yaml.safe_load(f)
    log.info("Loaded YAML config from %s", path)
    return data or {}


def apply_env_overrides(config: dict, prefix: str = "FP_") -> dict:
    """Override config values from environment variables with given prefix."""
    config = config.copy()
    for key, val in os.environ.items():
        if key.startswith(prefix):
            config_key = key[len(prefix):].lower()
            config[config_key] = val
            log.debug("Config override from env: %s = %s", config_key, val)
    return config


def load_config(path: str, env_prefix: str = "FP_") -> dict:
    """Load config from JSON or YAML and apply env-var overrides."""
    ext = Path(path).suffix.lower()
    if ext == ".json":
        data = load_json_config(path)
    elif ext in (".yaml", ".yml"):
        data = load_yaml_config(path)
    else:
        raise ValueError(f"Unsupported config format: {ext}")
    return apply_env_overrides(data, env_prefix)
