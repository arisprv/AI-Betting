import json
from datetime import date
from pathlib import Path
from typing import Any
from logger import get_logger

log = get_logger(__name__)

TRACKER_FILE = "performance_tracker.json"


def _load(file: str) -> dict:
    p = Path(file)
    if not p.exists():
        return {"entries": [], "created": date.today().isoformat()}
    return json.loads(p.read_text())


def _save(data: dict, file: str) -> None:
    Path(file).write_text(json.dumps(data, indent=2, default=str))


def record_prediction_outcome(match: str, prediction: str, actual: str, confidence: float,
                               file: str = TRACKER_FILE) -> None:
    """Append a settled prediction outcome to the tracker file."""
    data = _load(file)
    data["entries"].append({
        "date": date.today().isoformat(),
        "match": match,
        "prediction": prediction,
        "actual": actual,
        "confidence": confidence,
        "correct": prediction == actual,
    })
    _save(data, file)


def get_accuracy(file: str = TRACKER_FILE) -> float | None:
    data = _load(file)
    entries = data.get("entries", [])
    if not entries:
        return None
    return sum(1 for e in entries if e.get("correct")) / len(entries)


def get_accuracy_by_confidence(file: str = TRACKER_FILE, bins: int = 5) -> dict:
    import numpy as np
    data = _load(file)
    entries = data.get("entries", [])
    if not entries:
        return {}
    thresholds = np.linspace(0.5, 1.0, bins + 1)
    result = {}
    for lo, hi in zip(thresholds[:-1], thresholds[1:]):
        bucket = [e for e in entries if lo <= e.get("confidence", 0) < hi]
        key = f"{lo:.2f}-{hi:.2f}"
        result[key] = sum(1 for e in bucket if e.get("correct")) / len(bucket) if bucket else None
    return result
