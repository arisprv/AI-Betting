import pytest
from sharp_money import reverse_line_movement


def test_reverse_line_movement_detected():
    # Public on home (60%+), but odds lengthened → sharp fade
    assert reverse_line_movement(public_pct=0.70, odds_move=-0.10) is True


def test_reverse_line_movement_not_detected_low_public():
    assert reverse_line_movement(public_pct=0.45, odds_move=-0.10) is False


def test_reverse_line_movement_not_detected_small_move():
    assert reverse_line_movement(public_pct=0.70, odds_move=-0.02) is False


def test_reverse_line_movement_positive_move():
    # Odds shortened with public support — normal movement
    assert reverse_line_movement(public_pct=0.70, odds_move=0.10) is False
