"""Notification system — webhook and console-based alerting."""
import json
import urllib.request
from dataclasses import dataclass, field
from logger import get_logger

log = get_logger(__name__)


@dataclass
class WebhookNotifier:
    url: str
    headers: dict = field(default_factory=lambda: {"Content-Type": "application/json"})

    def send(self, message: str, level: str = "INFO") -> bool:
        payload = json.dumps({"text": f"[{level}] {message}"}).encode()
        req = urllib.request.Request(self.url, data=payload, headers=self.headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status == 200
        except Exception as exc:
            log.warning("Webhook notification failed: %s", exc)
            return False


class ConsoleNotifier:
    """Fallback notifier that logs to stdout."""
    def send(self, message: str, level: str = "INFO") -> bool:
        print(f"[NOTIFICATION] [{level}] {message}")
        return True


class NotificationManager:
    def __init__(self):
        self._notifiers: list = [ConsoleNotifier()]

    def add_webhook(self, url: str) -> None:
        self._notifiers.append(WebhookNotifier(url))

    def notify(self, message: str, level: str = "INFO") -> None:
        for notifier in self._notifiers:
            try:
                notifier.send(message, level)
            except Exception as exc:
                log.error("Notifier %s error: %s", type(notifier).__name__, exc)

    def value_bet_found(self, match: str, prediction: str, ev: float) -> None:
        self.notify(f"Value bet: {match} → {prediction} (EV: {ev:+.3f})", level="INFO")

    def drawdown_alert(self, drawdown_pct: float) -> None:
        self.notify(f"Bankroll drawdown alert: {drawdown_pct:.1f}%", level="WARNING")
