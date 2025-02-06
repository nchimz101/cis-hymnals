from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import json
import os

# Initialize FastAPI app
app = FastAPI()

# Get the project directory
directory = os.getcwd()

# Load config.json
config_path = os.path.join(directory, "config.json")
with open(config_path, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

# Map keys to language titles
language_map = {item["key"]: item["title"] for item in config}

def load_hymnals():
    hymnals = {}
    for filename in os.listdir(directory):
        if filename.endswith(".json") and filename != "config.json":
            language = filename.split(".")[0]
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                hymnals[language] = json.load(file)
    return hymnals

hymnals = load_hymnals()

class Hymnal(BaseModel):
    title: str
    number: int
    content: str

@app.get("/languages", response_model=List[str])
def get_languages():
    """Returns a list of available hymnals."""
    return list(language_map.keys())

@app.get("/hymnals/{language}", response_model=List[Hymnal])
def get_hymnals(language: str):
    """Fetch all hymns of a specific language."""
    if language not in hymnals:
        raise HTTPException(status_code=404, detail="Language not found")
    return hymnals[language]

@app.get("/hymnals/{language}/{number}", response_model=Hymnal)
def get_hymn(language: str, number: int):
    """Retrieve a specific hymn by its number."""
    if language not in hymnals:
        raise HTTPException(status_code=404, detail="Language not found")
    hymn = next((hymn for hymn in hymnals[language] if hymn["number"] == number), None)
    if not hymn:
        raise HTTPException(status_code=404, detail="Hymn not found")
    return hymn

# Deployment Instructions:
# 1. Install dependencies: pip install fastapi uvicorn
# 2. Run the API: uvicorn filename:app --host 0.0.0.0 --port 8000 --reload
