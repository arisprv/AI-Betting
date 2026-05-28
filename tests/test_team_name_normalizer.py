import pytest
from team_name_normalizer import normalize, names_match, find_best_match


def test_normalize_strips_fc():
    assert normalize("Manchester FC") == "manchester"


def test_normalize_strips_afc():
    assert normalize("Arsenal AFC") == "arsenal"


def test_normalize_lowercases():
    assert normalize("LIVERPOOL") == "liverpool"


def test_normalize_handles_non_string():
    assert normalize(None) == ""
    assert normalize(123) == ""


def test_names_match_exact():
    assert names_match("Chelsea FC", "Chelsea") is True


def test_names_match_different():
    assert names_match("Arsenal", "Tottenham") is False


def test_find_best_match_exact():
    candidates = ["Arsenal FC", "Chelsea", "Liverpool"]
    assert find_best_match("Chelsea FC", candidates) == "Chelsea"


def test_find_best_match_none():
    candidates = ["Arsenal", "Chelsea"]
    assert find_best_match("Tottenham", candidates) is None
