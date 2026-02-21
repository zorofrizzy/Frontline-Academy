from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

APP_ROOT = Path(__file__).resolve().parents[1]
PROMPT_PATH = APP_ROOT / "prompt.md"

# ---- App ----
app = FastAPI(title="Frontline Quiz", redirect_slashes=False)

# Dev CORS (tighten for prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: set to your UI host(s) for production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Gemini client ----
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    # Fail fast so you don't "think" it's working in prod
    raise RuntimeError("Missing GEMINI_API_KEY env var")

client = genai.Client(api_key=GEMINI_API_KEY)

# Choose a model (swap as you prefer)
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def load_system_prompt() -> str:
    if not PROMPT_PATH.exists():
        raise RuntimeError(f"prompt.md not found at: {PROMPT_PATH}")
    return PROMPT_PATH.read_text(encoding="utf-8")


def build_user_prompt(difficulty: str, number_of_questions: int, user_prompt: str, has_files: bool) -> str:
    base = (
        f"Create an MCQ quiz.\n"
        f"I want {number_of_questions} questions.\n"
        f"The difficulty should be {difficulty}.\n"
    )

    if user_prompt and user_prompt.strip():
        base += "\nAdditional instructions from user:\n" + user_prompt.strip() + "\n"

    if has_files:
        base += "\nUse ONLY the provided file content as the source.\n"
    else:
        base += "\nUse ONLY the user prompt text as the source.\n"

    return base


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate-quiz/")
async def generate_quiz(
    difficulty: str = Form("Medium"),
    number_of_questions: int = Form(10),
    user_prompt: str = Form(""),
    files: Optional[List[UploadFile]] = File(None),
):
    files = files or []
    has_files = len(files) > 0

    if (not has_files) and (not user_prompt.strip()):
        raise HTTPException(status_code=400, detail="Provide a file OR a prompt.")

    system_prompt = load_system_prompt()
    user_text = build_user_prompt(difficulty, number_of_questions, user_prompt, has_files)

    # Build contents: first text instruction, then optional files as bytes
    contents = [user_text]

    for f in files:
        data = await f.read()
        if not data:
            continue
        mime = f.content_type or "application/octet-stream"
        contents.append(types.Part.from_bytes(data=data, mime_type=mime))

    # Ask Gemini for strict JSON
    resp = await client.aio.models.generate_content(
        model=DEFAULT_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            temperature=0.2,
        ),
    )

    # resp.text should be JSON; parse and return dict
    try:
        quiz_obj = json.loads(resp.text)
    except Exception:
        # If model returns something unexpected, still return raw text for debugging
        raise HTTPException(status_code=502, detail={"error": "Model did not return valid JSON", "raw": resp.text})

    return {"quiz": quiz_obj.get("quiz", []), "raw": quiz_obj}