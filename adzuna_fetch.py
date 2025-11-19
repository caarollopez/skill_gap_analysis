import requests
from textwrap import shorten
from dotenv import load_dotenv
import os

load_dotenv()
APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")

url = "https://api.adzuna.com/v1/api/jobs/es/search/1"

params = {
    "app_id": APP_ID,
    "app_key": APP_KEY,
    "what": "data analyst",
    "results_per_page": 1,
    "content-type": "application/json"
}

response = requests.get(url, params=params)
response.raise_for_status()

data = response.json()

def pretty_print_job(job):
    title       = job.get("title", "N/A")
    company     = job.get("company", {}).get("display_name", "N/A")
    location    = job.get("location", {}).get("display_name", "N/A")
    contract    = job.get("contract_type", "N/A")
    salary_min  = job.get("salary_min", "N/A")
    salary_max  = job.get("salary_max", "N/A")
    redirect    = job.get("redirect_url", "N/A")

    description = job.get("description", "N/A")
    description = shorten(description, width=350, placeholder="...")

    print("\n" + "="*60)
    print(f"JOB TITLE:      {title}")
    print("="*60)
    print(f"Company:        {company}")
    print(f"Location:       {location}")
    print(f"Contract Type:  {contract}")
    print(f"Salary Range:   {salary_min} - {salary_max}")
    print(f"Apply Link:     {redirect}")
    print("\nDescription:\n")
    print(description)
    print("="*60 + "\n")

# Show one example job
if data.get("results"):
    pretty_print_job(data["results"][0])
else:
    print("No jobs found.")
