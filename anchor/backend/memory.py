"""Memory module — JSON-backed keyword retrieval + conversation logging.

Includes Concept 12 (BrowseBack-lite): logs profile gaps when the system
doesn't know something, so Priya can fill them in later.
"""

import json
from datetime import datetime
from pathlib import Path

PROFILE_PATH = Path("backend/patient_profile.json")
LOG_PATH = Path("data/conversation_log.json")
PROFILE_GAPS_PATH = Path("data/profile_update_suggestions.json")


def get_relevant_memories(query: str, k: int = 6) -> list[str]:
    """Naive keyword retrieval over the profile — good enough for a demo."""
    with open(PROFILE_PATH) as f:
        profile = json.load(f)

    # Flatten profile into a list of facts
    facts: list[str] = []
    facts.append(
        f"Margaret is {profile['identity']['age']}, "
        f"lives in {profile['identity']['location']}"
    )
    for fam in profile["family"]:
        facts.append(
            f"{fam['name']} is Margaret's {fam['relation']}. "
            f"{fam.get('notes', '')}"
        )
    for event in profile["scheduled_events"]:
        facts.append(f"Scheduled: {event['when']} — {event['what']}")
    for event in profile["recent_events"]:
        facts.append(f"Recent: {event['when']} — {event['what']}")
    for pref_key, pref_val in profile["preferences"].items():
        facts.append(f"Preference ({pref_key}): {pref_val}")
    for mem in profile["history"].get("meaningful_memories", []):
        facts.append(f"Memory: {mem}")
    for note in profile.get("care_notes", []):
        facts.append(f"Care note: {note}")

    # Routine facts
    for key, val in profile["routine"].items():
        if isinstance(val, dict):
            facts.append(f"Routine ({key}): {val}")
        else:
            facts.append(f"Routine ({key}): {val}")

    # Simple keyword match score
    query_words = set(query.lower().split())
    scored: list[tuple[int, str]] = []
    for fact in facts:
        fact_words = set(fact.lower().split())
        overlap = len(query_words & fact_words)
        scored.append((overlap, fact))

    scored.sort(reverse=True, key=lambda x: x[0])
    # Always return at least the top-k, even if overlap is 0
    return [fact for _, fact in scored[:k]]


def log_interaction(
    user_input: str, response: str, escalation: bool, rejected_by: str | None = None
):
    """Log a conversation turn to the conversation log."""
    log: list[dict] = []
    if LOG_PATH.exists():
        try:
            log = json.loads(LOG_PATH.read_text())
        except json.JSONDecodeError:
            log = []

    entry: dict = {
        "time": datetime.now().isoformat(),
        "margaret": user_input,
        "anchor": response,
        "escalation": escalation,
    }
    if rejected_by:
        entry["rejected_by"] = rejected_by

    log.append(entry)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text(json.dumps(log, indent=2))


def get_recent_conversation(n: int = 3) -> str:
    """Return the last n conversation turns as a formatted string."""
    if not LOG_PATH.exists():
        return "(No prior conversation)"
    try:
        log = json.loads(LOG_PATH.read_text())
    except json.JSONDecodeError:
        return "(No prior conversation)"
    recent = log[-n:]
    return "\n".join(
        f"Margaret: {t['margaret']}\nAnchor: {t['anchor']}" for t in recent
    )


def get_last_medication_log() -> str:
    """Return info about the last medication from the profile."""
    try:
        with open(PROFILE_PATH) as f:
            profile = json.load(f)
        med = profile["routine"].get("medication_morning", {})
        return (
            f"{med.get('drug', 'Unknown')} {med.get('dose', '')} "
            f"at {med.get('time', 'unknown')} ({med.get('notes', 'no notes')})"
        )
    except Exception:
        return "(Medication info not available)"


def log_profile_gap(user_input: str, response: str):
    """Concept 12 (BrowseBack-lite): log when Anchor doesn't know something.

    These gaps are shown to Priya so she can update the profile.
    """
    gaps: list[dict] = []
    if PROFILE_GAPS_PATH.exists():
        try:
            gaps = json.loads(PROFILE_GAPS_PATH.read_text())
        except json.JSONDecodeError:
            gaps = []

    gaps.append(
        {
            "time": datetime.now().isoformat(),
            "margaret_asked": user_input,
            "anchor_said": response,
            "suggestion": "Needs profile update — fact not in memory",
        }
    )
    PROFILE_GAPS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROFILE_GAPS_PATH.write_text(json.dumps(gaps, indent=2))