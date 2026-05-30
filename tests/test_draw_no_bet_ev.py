import pytest
from draw_no_bet import dnb_ev


def test_dnb_ev_positive_edge():
    ev = dnb_ev(model_prob=0.6, market_odds=2.0, draw_prob=0.25)
    assert ev > 0


def test_dnb_ev_negative_edge():
    ev = dnb_ev(model_prob=0.3, market_odds=2.0, draw_prob=0.25)
    assert ev < 0


def test_dnb_ev_high_draw_reduces_value():
    ev_low_draw = dnb_ev(0.55, 2.0, draw_prob=0.1)
    ev_high_draw = dnb_ev(0.55, 2.0, draw_prob=0.4)
    assert ev_low_draw > ev_high_draw
