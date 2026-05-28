import pytest
import tempfile
import os
from unittest.mock import patch
from pathlib import Path
import data_cache


@pytest.fixture(autouse=True)
def tmp_cache(tmp_path):
    original = data_cache.CACHE_DIR
    data_cache.CACHE_DIR = str(tmp_path / "cache")
    yield
    data_cache.CACHE_DIR = original


def test_miss_on_empty():
    result = data_cache.get_cached("http://example.com", {})
    assert result is None


def test_set_and_get():
    payload = {"key": "value", "count": 42}
    data_cache.set_cached("http://example.com", payload, {})
    result = data_cache.get_cached("http://example.com", {})
    assert result == payload


def test_different_params_are_separate():
    data_cache.set_cached("http://example.com", {"a": 1}, {"q": "1"})
    data_cache.set_cached("http://example.com", {"b": 2}, {"q": "2"})
    r1 = data_cache.get_cached("http://example.com", {"q": "1"})
    r2 = data_cache.get_cached("http://example.com", {"q": "2"})
    assert r1 == {"a": 1}
    assert r2 == {"b": 2}


def test_clear_cache():
    data_cache.set_cached("http://example.com", {"x": 1}, {})
    deleted = data_cache.clear_cache()
    assert deleted >= 1
    assert data_cache.get_cached("http://example.com", {}) is None
