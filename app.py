from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict
import json
import os

app = FastAPI(
    title="Multilingual Hymnal API",
    description="API for accessing hymnal collections",
    version="1.0.0"
)

# Load configuration
directory = os.getcwd()
config_path = os.path.join(directory, "config.json")
with open(config_path, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)


class LanguageConfig(BaseModel):
    key: str
    title: str
    language: str


class HymnDetails(BaseModel):
    number: int
    title: str
    content: str


def load_hymnals():
    hymnals = {}

    for filename in os.listdir(directory):
        if filename.endswith(".json") and filename != "config.json":
            language_key = filename.split(".")[0]
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                hymnals[language_key] = json.load(file)

    return hymnals


hymnals = load_hymnals()


@app.get("/languages", response_model=List[LanguageConfig])
def get_languages():
    """Returns available hymnal languages from config."""
    return config


@app.get("/hymnals/{language_key}", response_model=List[HymnDetails])
def get_hymnals(
        language_key: str,
        min_number: Optional[int] = Query(None),
        max_number: Optional[int] = Query(None)
):
    """Retrieve hymns for a specific language."""
    if language_key not in hymnals:
        raise HTTPException(status_code=404, detail="Language not found")

    filtered_hymnals = hymnals[language_key]

    if min_number is not None:
        filtered_hymnals = [h for h in filtered_hymnals if h['number'] >= min_number]

    if max_number is not None:
        filtered_hymnals = [h for h in filtered_hymnals if h['number'] <= max_number]

    return filtered_hymnals


@app.get("/hymnals/{language_key}/{number}", response_model=HymnDetails)
def get_hymn(language_key: str, number: int):
    """Retrieve a specific hymn by language and number."""
    if language_key not in hymnals:
        raise HTTPException(status_code=404, detail="Language not found")

    hymn = next((h for h in hymnals[language_key] if h['number'] == number), None)

    if not hymn:
        raise HTTPException(status_code=404, detail="Hymn not found")

    return hymn

# Deployment Instructions:
# 1. Install dependencies: pip install fastapi uvicorn
# 2. Run the API: uvicorn filename:app --host 0.0.0.0 --port 8000 --reload
