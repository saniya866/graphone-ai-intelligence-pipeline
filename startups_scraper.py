import requests
import json
import time
from datetime import datetime, timezone


def fetch_yc_startups(max_results=1000):
    """
    Fetches real startup data from YCombinator's public Algolia-backed API.
    No authentication required.
    """
    all_startups = []
    base_url = "https://yc-oss.github.io/api/companies/all.json"

    print("Fetching YC company dataset...")
    try:
        response = requests.get(base_url, timeout=30)
        response.raise_for_status()
        companies = response.json()
    except Exception as e:
        print(f"Error fetching YC data: {e}")
        return []

    print(f"Total companies in source: {len(companies)}")

    for company in companies[:max_results]:
        startup = {
            "schemaVersion": "1.0",
            "recordType": "STARTUP",
            "source": {
                "name": "Y Combinator",
                "url": company.get("url") or f"https://www.ycombinator.com/companies/{company.get('slug', '')}"
            },
            "content": {
                "entityName": company.get("name"),
                "data": {
                    "employeeCount": company.get("team_size")
                }
            },
            "collectedAt": datetime.now(timezone.utc).isoformat()
        }
        all_startups.append(startup)

    return all_startups


if __name__ == "__main__":
    startups = fetch_yc_startups(max_results=1000)
    print(f"\nTotal startups collected: {len(startups)}")

    with open("startups_raw.json", "w", encoding="utf-8") as f:
        json.dump(startups, f, indent=2, ensure_ascii=False)

    print("Saved to startups_raw.json")