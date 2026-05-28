"""Alert system for notable predictions and bankroll events."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable
from logger import get_logger

log = get_logger(__name__)

AlertHandler = Callable[[str, str], None]


@dataclass
class Alert:
    level: str
    message: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class AlertSystem:
    def __init__(self):
        self.alerts: list[Alert] = []
        self._handlers: list[AlertHandler] = [self._log_handler]

    def add_handler(self, handler: AlertHandler) -> None:
        self._handlers.append(handler)

    def _log_handler(self, level: str, message: str) -> None:
        getattr(log, level.lower(), log.info)(message)

    def _emit(self, level: str, message: str) -> None:
        alert = Alert(level=level, message=message)
        self.alerts.append(alert)
        for handler in self._handlers:
            try:
                handler(level, message)
            except Exception as exc:
                log.error("Alert handler error: %s", exc)

    def info(self, message: str) -> None:
        self._emit("INFO", message)

    def warning(self, message: str) -> None:
        self._emit("WARNING", message)

    def critical(self, message: str) -> None:
        self._emit("CRITICAL", message)

    def check_bankroll(self, current: float, initial: float, drawdown_threshold: float = 0.2) -> None:
        drawdown = (initial - current) / initial
        if drawdown >= drawdown_threshold:
            self.critical(f"Bankroll drawdown {drawdown:.1%} exceeds threshold ({drawdown_threshold:.1%})")

    def check_win_rate(self, recent_win_rate: float, expected_win_rate: float = 0.45) -> None:
        if recent_win_rate < expected_win_rate * 0.7:
            self.warning(f"Win rate {recent_win_rate:.1%} significantly below expected {expected_win_rate:.1%}")
