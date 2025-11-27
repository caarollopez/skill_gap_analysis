import os
import json
import requests
from pathlib import Path

from dotenv import load_dotenv
from .config import DATA_DIR, MAX_NUM_PAGES

load_dotenv()
API_KEY_JSEARCH = os.getenv("API_KEY_JSEARCH")

if not API_KEY_JSEARCH:
    raise RuntimeError("API_KEY_JSEARCH missing in .env")

def sanitize(value):
    return "".join(c.lower() if c.isalnum() else "_" for c in value)

def get_cache_paths(role, location):
    role_t = sanitize(role)
    loc_t = sanitize(location)
    raw = DATA_DIR / f"raw_jobs_{role_t}_{loc_t}.json"
    return raw

def fetch_from_api(query, country="es", **params):
    url = "https://api.openwebninja.com/jsearch/search"
    headers = {"x-api-key": API_KEY_JSEARCH}

    full_params = {
        "query": query,
        "country": country,
        "page": 1,
        "num_pages": MAX_NUM_PAGES,
        **params,
    }

    r = requests.get(url, params=full_params, headers=headers, timeout=20)
    r.raise_for_status()
    return r.json()

def load_or_fetch_jobs(role, location, country="es", **filters):
    raw_path = get_cache_paths(role, location)

    if raw_path.exists():
        with raw_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    query = f"{role} jobs in {location}"
    data = fetch_from_api(query, country, **filters)

    with raw_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return data
