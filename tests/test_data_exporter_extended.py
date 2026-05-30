import json
import pandas as pd
import pytest
from pathlib import Path
from data_exporter import export_to_json


def test_json_export_empty_df(tmp_path):
    df = pd.DataFrame()
    path = str(tmp_path / "empty.json")
    export_to_json(df, path)
    data = json.loads(Path(path).read_text())
    assert data == []


def test_json_export_numeric_values(tmp_path):
    df = pd.DataFrame({"value": [1.5, 2.5, 3.5]})
    path = str(tmp_path / "numeric.json")
    export_to_json(df, path)
    data = json.loads(Path(path).read_text())
    assert data[0]["value"] == pytest.approx(1.5)
