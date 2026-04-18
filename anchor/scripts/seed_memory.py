"""Seed memory script — ensures all data files exist with empty arrays."""

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
        fpath = data_dir / fname
        if not fpath.exists():
            fpath.write_text("[]")
            print(f"Created {fpath}")
        else:
            print(f"Already exists: {fpath}")


if __name__ == "__main__":
    run()