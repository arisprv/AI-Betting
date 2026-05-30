import json
import os
import pytest
from config_loader import load_json_config, apply_env_overrides


@pytest.fixture
def json_config_file(tmp_path):
    config = {"season": 2025, "rolling_window": 5, "model": "rf"}
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config))
    return str(path)


def test_load_json_config(json_config_file):
    config = load_json_config(json_config_file)
    assert config["season"] == 2025
    assert config["rolling_window"] == 5


def test_load_json_not_found():
    with pytest.raises(FileNotFoundError):
        load_json_config("/nonexistent/path/config.json")


def test_apply_env_overrides():
    base = {"season": 2025, "model": "rf"}
    os.environ["FP_MODEL"] = "xgb"
    result = apply_env_overrides(base, prefix="FP_")
    del os.environ["FP_MODEL"]
    assert result["model"] == "xgb"


def test_env_overrides_preserves_other_keys():
    base = {"season": 2025, "model": "rf"}
    result = apply_env_overrides(base, prefix="NONEXISTENT_PREFIX_")
    assert result["season"] == 2025
