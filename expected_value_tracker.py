"""Track expected value accuracy over time to evaluate model calibration."""
import json
from datetime import date
from pathlib import Path
from logger import get_logger

log = get_logger(__name__)

EV_TRACKER_FILE = "ev_tracker.json"


def _load(file: str) -> dict:
    p = Path(file)
    return json.loads(p.read_text()) if p.exists() else {"entries": []}


def _save(data: dict, file: str) -> None:
    Path(file).write_text(json.dumps(data, indent=2, default=str))


def record_ev_bet(match: str, predicted_ev: float, actual_won: bool,
                   odds: float, stake: float, file: str = EV_TRACKER_FILE) -> None:
    """Record a bet with its predicted EV and actual outcome."""
    data = _load(file)
    actual_return = stake * (odds - 1) if actual_won else -stake
    data["entries"].append({
        "date": date.today().isoformat(),
        "match": match,
        "predicted_ev": predicted_ev,
        "actual_return": actual_return,
        "stake": stake,
        "won": actual_won,
    })
    _save(data, file)


def ev_accuracy(file: str = EV_TRACKER_FILE) -> dict:
    """Return correlation-style analysis of predicted EV vs actual returns."""
    data = _load(file)
    entries = data.get("entries", [])
    if not entries:
        return {}
    predicted = [e["predicted_ev"] for e in entries]
    actual = [e["actual_return"] / e["stake"] if e["stake"] else 0 for e in entries]
    mean_pred = sum(predicted) / len(predicted)
    mean_actual = sum(actual) / len(actual)
    return {
        "count": len(entries),
        "mean_predicted_ev": round(mean_pred, 4),
        "mean_actual_return": round(mean_actual, 4),
        "ev_accuracy": round(1 - abs(mean_pred - mean_actual), 4),
    }
