import pandas as pd
from datetime import datetime
from analytics import compute_roi, compute_win_rate, by_league, by_prediction, monthly_summary
from logger import get_logger

log = get_logger(__name__)


def generate_text_report(bets: pd.DataFrame, title: str = "Performance Report") -> str:
    lines = [
        f"{'=' * 60}",
        f" {title}",
        f" Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"{'=' * 60}",
        "",
        "## Summary",
        f"  Total bets:     {len(bets)}",
        f"  Total P&L:      {bets['pnl'].sum():.2f}" if 'pnl' in bets else "  Total P&L:      N/A",
        f"  ROI:            {(compute_roi(bets) or 0) * 100:.1f}%",
        f"  Win rate:       {(compute_win_rate(bets) or 0) * 100:.1f}%",
        "",
    ]

    league_breakdown = by_league(bets)
    if not league_breakdown.empty:
        lines.append("## By League")
        lines.append(f"  {'League':<20} {'Bets':>6} {'P&L':>10} {'ROI':>8} {'Win%':>8}")
        lines.append(f"  {'-'*56}")
        for idx, row in league_breakdown.iterrows():
            lines.append(f"  {str(idx):<20} {int(row['bets_count']):>6} {row['total_pnl']:>10.2f} {row['roi']*100:>7.1f}% {row['win_rate']*100:>7.1f}%")
        lines.append("")

    pred_breakdown = by_prediction(bets)
    if not pred_breakdown.empty:
        lines.append("## By Prediction Type")
        lines.append(f"  {'Prediction':<15} {'Bets':>6} {'P&L':>10} {'ROI':>8} {'Win%':>8}")
        lines.append(f"  {'-'*51}")
        for idx, row in pred_breakdown.iterrows():
            lines.append(f"  {str(idx):<15} {int(row['bets_count']):>6} {row['total_pnl']:>10.2f} {row['roi']*100:>7.1f}% {row['win_rate']*100:>7.1f}%")
        lines.append("")

    return "\n".join(lines)


def save_report(bets: pd.DataFrame, output_file: str = "performance_report.txt") -> None:
    report = generate_text_report(bets)
    with open(output_file, "w") as f:
        f.write(report)
    log.info("Report saved to %s", output_file)
