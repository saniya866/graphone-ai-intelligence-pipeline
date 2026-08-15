import json
import csv

def json_to_csv(json_file, csv_file, fieldnames, row_mapper):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(row_mapper(item))

    print(f"Saved {len(data)} rows to {csv_file}")


# Papers
json_to_csv(
    "papers_raw.json", "papers.csv",
    ["title", "authors", "paper_url", "github_url", "github_stars", "published_date", "source_url"],
    lambda p: {
        "title": p["content"]["title"],
        "authors": " | ".join(p["content"]["authors"]),
        "paper_url": p["content"]["paper_url"],
        "github_url": p["content"]["github_url"] or "",
        "github_stars": p["content"]["github_stars"] or "",
        "published_date": p["content"]["published_date"],
        "source_url": p["source"]["url"]
    }
)

# Products
json_to_csv(
    "products_raw.json", "products.csv",
    ["startupName", "pricingModel", "source_url", "collectedAt"],
    lambda p: {
        "startupName": p["content"]["startupName"],
        "pricingModel": p["content"]["pricingModel"],
        "source_url": p["source"]["url"],
        "collectedAt": p["collectedAt"]
    }
)

# Startups
json_to_csv(
    "startups_raw.json", "startups.csv",
    ["entityName", "employeeCount", "source_url", "collectedAt"],
    lambda s: {
        "entityName": s["content"]["entityName"],
        "employeeCount": s["content"]["data"]["employeeCount"] or "",
        "source_url": s["source"]["url"],
        "collectedAt": s["collectedAt"]
    }
)

print("\nAll CSVs generated.")