import json
import pandas as pd
import pytest
from pathlib import Path
from data_exporter import export_to_csv, export_to_json


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "team": ["Arsenal", "Chelsea"],
        "goals": [2.1, 1.4],
    })


def test_export_to_csv(tmp_path, sample_df):
    path = str(tmp_path / "out.csv")
    export_to_csv(sample_df, path)
    assert Path(path).exists()
    loaded = pd.read_csv(path)
    assert len(loaded) == 2


def test_export_to_json(tmp_path, sample_df):
    path = str(tmp_path / "out.json")
    export_to_json(sample_df, path)
    assert Path(path).exists()
    data = json.loads(Path(path).read_text())
    assert isinstance(data, list)
    assert len(data) == 2


def test_export_json_preserves_columns(tmp_path, sample_df):
    path = str(tmp_path / "out.json")
    export_to_json(sample_df, path)
    data = json.loads(Path(path).read_text())
    assert "team" in data[0]
    assert "goals" in data[0]
