"""
rayban-sheet-music — FastAPI backend
Parses MusicXML files and streams score data to Meta Ray-Ban glasses via the Display API.
"""
from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .parser.musicxml import parse_musicxml
from .display.rayban_client import RayBanDisplayClient

app = FastAPI(
    title="rayban-sheet-music",
    description="Stream sheet music to Meta Ray-Ban glasses",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_display_client: RayBanDisplayClient | None = None


@app.on_event("startup")
async def startup() -> None:
    global _display_client
    api_key = os.environ.get("RAYBAN_DISPLAY_API_KEY", "")
    _display_client = RayBanDisplayClient(api_key=api_key)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/upload")
async def upload_score(file: UploadFile = File(...)) -> dict:
    """Accept a MusicXML file, parse it, and prepare it for display."""
    if not file.filename or not file.filename.endswith(".xml"):
        raise HTTPException(status_code=400, detail="Only .xml (MusicXML) files are accepted")

    contents = await file.read()
    try:
        score = parse_musicxml(contents)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Failed to parse score: {exc}") from exc

    return {
        "filename": file.filename,
        "measures": len(score.measures),
        "title": score.title,
    }


@app.post("/display/show")
async def show_measure(measure_index: int = 0) -> dict[str, str]:
    """Send a specific measure to the Ray-Ban glasses display."""
    if _display_client is None:
        raise HTTPException(status_code=503, detail="Display client not initialized")

    await _display_client.show_measure(measure_index)
    return {"status": "sent", "measure": measure_index}


@app.post("/display/next")
async def next_measure() -> dict[str, str]:
    """Advance to the next measure on the glasses display."""
    if _display_client is None:
        raise HTTPException(status_code=503, detail="Display client not initialized")

    await _display_client.next_measure()
    return {"status": "advanced"}
