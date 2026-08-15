import requests
import json
import time
from datetime import datetime, timezone


def fetch_github_products(query="artificial intelligence", max_results=300, per_page=100):
    all_products = []
    base_url = "https://api.github.com/search/repositories"
    headers = {"Accept": "application/vnd.github+json"}

    pages_needed = (max_results // per_page) + 1

    for page in range(1, pages_needed + 1):
        params = {
            "q": f"{query} in:name,description,readme",
            "sort": "stars",
            "order": "desc",
            "per_page": per_page,
            "page": page
        }
        print(f"Fetching page {page}...")

        try:
            response = requests.get(base_url, headers=headers, params=params, timeout=30)
            if response.status_code == 403:
                print("GitHub rate limit hit. Waiting 60 seconds before retrying...")
                time.sleep(60)
                response = requests.get(base_url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            continue

        data = response.json()
        items = data.get("items", [])

        if not items:
            print("No more results — stopping early.")
            break

        for repo in items:
            product = {
                "schemaVersion": "1.0",
                "recordType": "PRODUCT",
                "source": {
                    "name": "GitHub",
                    "url": repo.get("html_url")
                },
                "content": {
                    "startupName": repo.get("owner", {}).get("login"),
                    "pricingModel": "FREE"
                },
                "collectedAt": datetime.now(timezone.utc).isoformat()
            }
            all_products.append(product)

        time.sleep(6)

    return all_products


if __name__ == "__main__":
    products = fetch_github_products(query="artificial intelligence", max_results=300)
    print(f"\nTotal products collected: {len(products)}")

    with open("products_raw.json", "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    print("Saved to products_raw.json")