import pytest
from unittest.mock import MagicMock
from model_registry import ModelRegistry


@pytest.fixture
def registry(tmp_path):
    return ModelRegistry(
        models_dir=str(tmp_path / "models"),
        registry_file=str(tmp_path / "registry.json"),
    )


def test_register_model(registry):
    model = MagicMock()
    version = registry.register(model, "test_model", metrics={"accuracy": 0.75})
    assert version is not None


def test_list_models(registry):
    model = MagicMock()
    registry.register(model, "test_model")
    models = registry.list_models("test_model")
    assert len(models) == 1
    assert models[0]["name"] == "test_model"


def test_get_latest_raises_on_missing(registry):
    with pytest.raises(KeyError):
        registry.get_latest("nonexistent_model")


def test_metadata_stored(registry):
    model = MagicMock()
    registry.register(model, "my_model", metrics={"acc": 0.8}, tags={"env": "test"})
    entries = registry.list_models("my_model")
    assert entries[0]["metrics"]["acc"] == 0.8
    assert entries[0]["tags"]["env"] == "test"
