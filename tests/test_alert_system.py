import pytest
from alert_system import AlertSystem


def test_info_alert():
    alerts = AlertSystem()
    alerts.info("Test info message")
    assert len(alerts.alerts) == 1
    assert alerts.alerts[0].level == "INFO"


def test_warning_alert():
    alerts = AlertSystem()
    alerts.warning("Test warning")
    assert alerts.alerts[0].level == "WARNING"


def test_critical_alert():
    alerts = AlertSystem()
    alerts.critical("Test critical")
    assert alerts.alerts[0].level == "CRITICAL"


def test_check_bankroll_triggers_critical():
    alerts = AlertSystem()
    alerts.check_bankroll(current=700.0, initial=1000.0, drawdown_threshold=0.2)
    assert any(a.level == "CRITICAL" for a in alerts.alerts)


def test_check_bankroll_no_alert():
    alerts = AlertSystem()
    alerts.check_bankroll(current=950.0, initial=1000.0, drawdown_threshold=0.2)
    assert len(alerts.alerts) == 0


def test_custom_handler():
    captured = []
    alerts = AlertSystem()
    alerts.add_handler(lambda level, msg: captured.append((level, msg)))
    alerts.warning("Custom handler test")
    assert any("Custom handler test" in m for _, m in captured)
