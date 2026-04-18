"""Escalation module — carer notification logic.

Includes Concept 10 (SOAN-Lite): enhanced urgency classification with
gentle check-ins for unknown facts/people, not just distress alerts.
"""

import json
from datetime import datetime
from pathlib import Path

NOTIF_PATH = Path("data/carer_notifications.json")


def fire_escalation(reason: str, patient_said: str, anchor_replied: str):
    """Write a carer notification to the notifications file."""
    notifs: list[dict] = []
    if NOTIF_PATH.exists():
        try:
            notifs = json.loads(NOTIF_PATH.read_text())
        except json.JSONDecodeError:
            notifs = []

    notifs.append(
        {
            "time": datetime.now().isoformat(),
            "reason": reason,
            "patient_said": patient_said,
            "anchor_replied": anchor_replied,
            "urgency": classify_urgency(reason),
            "seen": False,
        }
    )
    NOTIF_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTIF_PATH.write_text(json.dumps(notifs, indent=2))


def classify_urgency(reason: str) -> str:
    """Concept 10 (SOAN-Lite): classify escalation urgency.

    High urgency: safety, fall, injury, medication, wandering.
    Gentle: anxiety, unknown person/fact, memory gap.
    Default: gentle (non-alarming).
    """
    high = ["safety", "fall", "injury", "medication", "wandering"]
    gentle = ["anxiety", "unknown_person", "unknown_fact", "memory_gap"]

    reason_lower = reason.lower()
    if any(k in reason_lower for k in high):
        return "high"
    if any(k in reason_lower for k in gentle):
        return "gentle"
    return "gentle"  # default to non-alarming


def read_notifications() -> list[dict]:
    """Read all carer notifications (polled by carer.html)."""
    if not NOTIF_PATH.exists():
        return []
    try:
        return json.loads(NOTIF_PATH.read_text())  # type: ignore[no-any-return]
    except json.JSONDecodeError:
        return []