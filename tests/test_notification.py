import pytest
from notification import ConsoleNotifier, NotificationManager


def test_console_notifier_sends():
    notifier = ConsoleNotifier()
    result = notifier.send("Test message", "INFO")
    assert result is True


def test_notification_manager_notify(capsys):
    mgr = NotificationManager()
    mgr.notify("Hello", level="INFO")
    captured = capsys.readouterr()
    assert "Hello" in captured.out


def test_notification_manager_value_bet(capsys):
    mgr = NotificationManager()
    mgr.value_bet_found("Arsenal vs Chelsea", "Home Win", ev=0.12)
    captured = capsys.readouterr()
    assert "Value bet" in captured.out


def test_notification_manager_drawdown_alert(capsys):
    mgr = NotificationManager()
    mgr.drawdown_alert(25.0)
    captured = capsys.readouterr()
    assert "drawdown" in captured.out.lower()


def test_custom_handler():
    received = []
    mgr = NotificationManager()
    mgr.add_handler(lambda level, msg: received.append(msg))
    mgr.notify("Custom message")
    assert "Custom message" in received
