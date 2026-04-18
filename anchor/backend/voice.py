"""Voice module — ElevenLabs TTS with hash-based caching.

Returns a URL path to generated audio. Falls back to None (triggers
browser SpeechSynthesis on the frontend) if ElevenLabs is unavailable.
"""

import os
import hashlib
from pathlib import Path

import requests

AUDIO_DIR = Path("frontend/assets/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

ELEVENLABS_VOICE_ID = "warm-older-british-female-voice-id"  # pick one from ElevenLabs library


def synthesize_speech(text: str) -> str | None:
    """Returns a URL path to the generated audio file, or None for browser fallback."""
    # Cache by hash so repeated sentences are free
    h = hashlib.md5(text.encode()).hexdigest()[:12]
    fname = f"{h}.mp3"
    fpath = AUDIO_DIR / fname

    if not fpath.exists():
        api_key = os.environ.get("ELEVENLABS_API_KEY")
        if not api_key:
            return None  # Frontend will fall back to browser SpeechSynthesis

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
        response = requests.post(
            url,
            headers={"xi-api-key": api_key, "Content-Type": "application/json"},
            json={
                "text": text,
                "model_id": "eleven_turbo_v2_5",  # fastest model
                "voice_settings": {
                    "stability": 0.6,
                    "similarity_boost": 0.8,
                },
            },
            timeout=10,
        )
        if response.status_code == 200:
            fpath.write_bytes(response.content)
        else:
            return None

    return f"/static/assets/audio/{fname}"