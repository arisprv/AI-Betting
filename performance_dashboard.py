"""Aggregate all performance metrics into a unified dashboard dict."""
import pandas as pd
from analytics import compute_roi, compute_win_rate, by_league, by_prediction
from risk_metrics import sharpe_ratio, max_drawdown
from closing_line_value import average_clv, clv_from_bets
from logger import get_logger

log = get_logger(__name__)


def build_dashboard(bets: pd.DataFrame) -> dict:
    """Return a comprehensive performance dashboard dictionary."""
    if bets.empty:
        return {}

    returns = (bets["pnl"] / bets["stake"].replace(0, 1)).tolist() if "pnl" in bets and "stake" in bets else []
    balances = bets["balance"].tolist() if "balance" in bets else []
    clv_vals = clv_from_bets(bets.to_dict("records"))

    roi = compute_roi(bets)
    wr = compute_win_rate(bets)
    sr = sharpe_ratio(returns)
    md = max_drawdown(balances)
    avg_clv = average_clv(clv_vals)

    league_breakdown = by_league(bets).to_dict("index") if "league" in bets else {}
    pred_breakdown = by_prediction(bets).to_dict("index") if "prediction" in bets else {}

    dashboard = {
        "total_bets": len(bets),
        "total_pnl": round(bets["pnl"].sum(), 2) if "pnl" in bets else 0,
        "roi_pct": round((roi or 0) * 100, 2),
        "win_rate_pct": round((wr or 0) * 100, 2),
        "sharpe_ratio": round(sr, 4) if sr is not None else None,
        "max_drawdown_pct": round(md * 100, 2),
        "avg_clv": round(avg_clv, 4),
        "by_league": league_breakdown,
        "by_prediction": pred_breakdown,
    }
    log.info("Dashboard: %d bets | ROI: %.1f%% | WR: %.1f%% | Sharpe: %s",
             dashboard["total_bets"], dashboard["roi_pct"], dashboard["win_rate_pct"],
             f"{sr:.3f}" if sr else "N/A")
    return dashboard
