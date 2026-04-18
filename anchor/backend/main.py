# HACKATHON PROTOTYPE — NOT FOR USE WITH REAL PATIENT DATA

"""Anchor — main FastAPI application.

Serves the patient interface, carer notification view, and API routes
for the core conversation loop, carer notifications, and demo reset.
"""

import sys
import json
from pathlib import Path
from contextlib import asynccontextmanager

# Ensure backend modules can import each other when running via uvicorn
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Load .env before importing modules that use env vars
load_dotenv()

from agent import respond_to_margaret  # noqa: E402
from voice import synthesize_speech  # noqa: E402
from escalation import read_notifications  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ensure data directories and files exist on startup."""
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)
    for fname in ["carer_notifications.json", "conversation_log.json", "profile_update_suggestions.json"]:
        fpath = data_dir / fname
        if not fpath.exists():
            fpath.write_text("[]")
    yield


app = FastAPI(title="Anchor", lifespan=lifespan)

# Serve the frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")


class PatientInput(BaseModel):
    text: str


@app.get("/")
def patient_interface():
    """Serve the main patient interface."""
    return FileResponse("frontend/index.html")


@app.get("/carer")
def carer_interface():
    """Serve the carer notification view (second screen)."""
    return FileResponse("frontend/carer.html")


@app.post("/api/speak")
async def speak(input: PatientInput):
    """Core loop: take patient utterance, return Anchor response + audio URL."""
    result = respond_to_margaret(input.text)
    audio_url = synthesize_speech(result["response"])
    return {
        "response_text": result["response"],
        "audio_url": audio_url,
        "escalation": result.get("escalation_fired", False),
    }


@app.get("/api/carer/notifications")
def carer_notifications():
    """Return all carer notifications (polled by carer.html every 2s)."""
    return read_notifications()


@app.post("/api/reset")
def reset():
    """Reset all data files for a clean demo."""
    data_dir = Path("data")
    for fname in ["carer_notifications.json", "conversation_log.json", "profile_update_suggestions.json"]:
        fpath = data_dir / fname
        fpath.write_text("[]")
    return {"ok": True}