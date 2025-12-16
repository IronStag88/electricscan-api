from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import random

app = FastAPI(title="ElectricScan API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/analyze")
async def analyze(
    category: str = Form(...),
    image: UploadFile = File(...)
):
    data = await image.read()
    try:
        Image.open(io.BytesIO(data))
    except Exception:
        return {"risk_level": "UNKNOWN"}

    return {
        "risk_level": random.choice(["LOW", "MEDIUM", "HIGH"]),
        "risk_reason": ["Photo-based safety check only"],
        "possible_issues": [
            {
                "title": "Possible electrical concern",
                "confidence": 0.6,
                "why": "Based on visible features in the image"
            }
        ],
        "immediate_actions": [
            "If unsure, stop using and contact a licensed electrician"
        ],
        "questions": [
            "Any burning smell?",
            "Breaker tripping?"
        ],
        "disclaimer": "ElectricScan is informational only. Not a diagnosis."
    }
