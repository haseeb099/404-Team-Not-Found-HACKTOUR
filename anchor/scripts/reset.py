"""Reset script — wipes memory, notifications, and logs for a clean demo."""

import json
from pathlib import Path


def run():
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)

    for fname in [
        "carer_notifications.json",
        "conversation_log.json",
        "profile_update_suggestions.json",
    ]:
        (data_dir / fname).write_text("[]")

    # Clear cached audio
    audio_dir = Path("frontend/assets/audio")
    if audio_dir.exists():
        for f in audio_dir.glob("*.mp3"):
            f.unlink()

    print("Reset complete — all data cleared.")


if __name__ == "__main__":
    run()