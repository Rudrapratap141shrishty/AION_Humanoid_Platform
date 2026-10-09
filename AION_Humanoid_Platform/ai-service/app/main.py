import os
import tempfile
import socket
from urllib.parse import urlparse
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
import speech_recognition as sr
from .automation import open_allowed_url, selenium_title

app = FastAPI(title="AION AI & Automation Gateway", version="0.1.0")

class CommandRequest(BaseModel):
    text: str = Field(min_length=1, max_length=500)

class BrowserRequest(BaseModel):
    url: str

@app.get("/health")
def health():
    return {"status": "UP", "service": "aion-ai"}

@app.post("/command")
def command(body: CommandRequest):
    text = body.text.strip()
    normalized = text.lower()

    if any(word in normalized for word in ["robot status", "show robot status", "status"]):
        return {
            "intent": "robot_status",
            "message": "Robot status panel selected. This demo does not actuate hardware.",
            "safe_to_execute": True
        }
    if "visualization" in normalized or "show scene" in normalized:
        return {
            "intent": "open_visualization",
            "url": os.getenv("VISER_URL", "http://localhost:8082"),
            "message": "Open the Viser visualization URL in your browser."
        }
    if normalized.startswith("open "):
        candidate = text[5:].strip()
        try:
            result = open_allowed_url(candidate, open_browser=False)
            return {"intent": "open_url", "result": result}
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
    return {
        "intent": "unknown",
        "message": "Try: 'show robot status', 'show visualization', or 'open https://example.com'.",
        "received": text
    }

@app.post("/browser/open")
def browser_open(body: BrowserRequest):
    try:
        return open_allowed_url(body.url, open_browser=False)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.post("/browser/title")
def browser_title(body: BrowserRequest):
    try:
        return {"title": selenium_title(body.url)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Browser automation failed: {type(exc).__name__}")

@app.post("/voice/transcribe")
async def transcribe(file: UploadFile = File(...)):
    # Accept audio files only; SpeechRecognition's Google recognizer requires internet.
    if not (file.content_type or "").startswith("audio/"):
        raise HTTPException(status_code=415, detail="Upload an audio file with an audio/* content type.")
    suffix = os.path.splitext(file.filename or "audio.wav")[1] or ".wav"
    content = await file.read()
    if len(content) > 15 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Audio file limit is 15 MB.")
    recognizer = sr.Recognizer()
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=True) as tmp:
            tmp.write(content)
            tmp.flush()
            with sr.AudioFile(tmp.name) as source:
                audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        return {"text": text, "language": "auto", "provider": "google-speech"}
    except sr.UnknownValueError:
        raise HTTPException(status_code=422, detail="Speech could not be understood.")
    except sr.RequestError:
        raise HTTPException(status_code=502, detail="Speech recognition provider is unavailable.")
    except ValueError:
        raise HTTPException(status_code=415, detail="Use a supported WAV/AIFF/FLAC audio file.")
