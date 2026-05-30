from dataclasses import dataclass, field
from typing import Optional
from constants import KELLY_FRACTION


@dataclass
class BankrollManager:
    initial_capital: float = 1000.0
    current_capital: float = field(init=False)
    kelly_fraction: float = KELLY_FRACTION
    history: list[dict] = field(default_factory=list)

    def __post_init__(self):
        self.current_capital = self.initial_capital

    def kelly_stake(self, prob: float, odds: float) -> float:
        """Return a stake sized by fractional Kelly criterion, capped at 10% of capital."""
        edge = prob * odds - 1
        if edge <= 0 or odds <= 1:
            return 0.0
        full_kelly = edge / (odds - 1)
        stake = full_kelly * self.kelly_fraction * self.current_capital
        return round(min(stake, self.current_capital * 0.1), 2)

    def record_bet(self, match: str, prediction: str, stake: float, odds: float, won: bool) -> float:
        """Record a settled bet, update capital, and return the P&L."""
        pnl = stake * (odds - 1) if won else -stake
        self.current_capital += pnl
        self.history.append({
            "match": match,
            "prediction": prediction,
            "stake": stake,
            "odds": odds,
            "won": won,
            "pnl": pnl,
            "balance": self.current_capital,
        })
        return pnl

    @property
    def roi(self) -> Optional[float]:
        total_staked = sum(b["stake"] for b in self.history)
        if total_staked == 0:
            return None
        total_pnl = sum(b["pnl"] for b in self.history)
        return total_pnl / total_staked

    @property
    def win_rate(self) -> Optional[float]:
        if not self.history:
            return None
        return sum(1 for b in self.history if b["won"]) / len(self.history)

    @property
    def max_drawdown(self) -> float:
        """Maximum peak-to-trough drawdown fraction of bankroll."""
        if not self.history:
            return 0.0
        balances = [b["balance"] for b in self.history]
        peak = self.initial_capital
        max_dd = 0.0
        for b in balances:
            peak = max(peak, b)
            dd = (peak - b) / peak if peak > 0 else 0.0
            max_dd = max(max_dd, dd)
        return round(max_dd, 4)

    @property
    def profit(self) -> float:
        return round(self.current_capital - self.initial_capital, 2)

    def summary(self) -> dict:
        """Return a summary dict of bankroll performance."""
        return {
            "initial": self.initial_capital,
            "current": round(self.current_capital, 2),
            "profit": self.profit,
            "bets": len(self.history),
            "roi": round(self.roi or 0, 4),
            "win_rate": round(self.win_rate or 0, 4),
            "max_drawdown": self.max_drawdown,
        }
