"""Multiple staking strategies for bankroll management."""
from logger import get_logger

log = get_logger(__name__)


def flat_stake(bankroll: float, unit_size: float = 10.0) -> float:
    """Fixed flat stake per bet."""
    return min(unit_size, bankroll)


def percentage_stake(bankroll: float, pct: float = 0.02) -> float:
    """Stake a fixed percentage of current bankroll."""
    return round(bankroll * pct, 2)


def kelly_stake(bankroll: float, prob: float, odds: float, fraction: float = 0.25) -> float:
    """Fractional Kelly criterion stake."""
    edge = prob * odds - 1
    if edge <= 0 or odds <= 1:
        return 0.0
    full_kelly = edge / (odds - 1)
    return round(min(full_kelly * fraction * bankroll, bankroll * 0.10), 2)


def fibonacci_stake(bankroll: float, loss_streak: int, base_unit: float = 10.0) -> float:
    """Fibonacci staking: escalate stake size on loss streaks."""
    fib = [1, 1]
    for _ in range(loss_streak):
        fib.append(fib[-1] + fib[-2])
    return min(base_unit * fib[min(loss_streak, len(fib) - 1)], bankroll * 0.25)


def d_alembert_stake(bankroll: float, wins: int, losses: int, base_unit: float = 10.0) -> float:
    """D'Alembert: increase after loss, decrease after win."""
    net_losses = max(losses - wins, 0)
    return min(base_unit * (1 + net_losses), bankroll * 0.20)


def proportional_kelly(bankroll: float, prob: float, odds: float, kelly_pct: float = 0.5) -> float:
    """Half-Kelly criterion for reduced variance."""
    return kelly_stake(bankroll, prob, odds, fraction=kelly_pct * 0.25)


STRATEGIES = {
    "flat": flat_stake,
    "percentage": percentage_stake,
    "kelly": kelly_stake,
    "fibonacci": fibonacci_stake,
    "d_alembert": d_alembert_stake,
}
