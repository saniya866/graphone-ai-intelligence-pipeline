import requests
import feedparser
import json
import time
import re
from datetime import datetime, timezone

def extract_github_url(text):
    """Finds the first GitHub repo link mentioned in a paper's abstract."""
    match = re.search(r"https?://github\.com/[\w\-]+/[\w\-\.]+", text)
    if match:
        return match.group(0).rstrip(".,)")
    return None


def get_github_stars(github_url):
    """Calls GitHub's public API to fetch live star count for a repo."""
    try:
        parts = github_url.replace("https://github.com/", "").split("/")
        owner, repo = parts[0], parts[1]
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            return response.json().get("stargazers_count")
        elif response.status_code == 403:
            print("GitHub rate limit hit — skipping star lookup for this repo.")
            return None
        else:
            return None
    except Exception as e:
        print(f"Error fetching GitHub stars for {github_url}: {e}")
        return None

def fetch_arxiv_papers(query="artificial intelligence", max_results=500, batch_size=100):
    """
    Fetches papers from Arxiv's public API in batches (Arxiv limits ~100 per request).
    Returns a list of dicts matching our RESEARCH_PAPER schema (minus GitHub data for now).
    """
    all_papers = []
    base_url = "http://export.arxiv.org/api/query"

    for start in range(0, max_results, batch_size):
        params = {
            "search_query": f"all:{query}",
            "start": start,
            "max_results": batch_size,
            "sortBy": "submittedDate",
            "sortOrder": "descending"
        }
        print(f"Fetching records {start} to {start + batch_size}...")

        try:
            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching batch starting at {start}: {e}")
            continue

        feed = feedparser.parse(response.text)

        if not feed.entries:
            print("No more entries returned — stopping early.")
            break

        for entry in feed.entries:
            github_url = extract_github_url(entry.summary if hasattr(entry, "summary") else "")
            github_stars = get_github_stars(github_url) if github_url else None

            paper = {
                "schemaVersion": "1.0",
                "recordType": "RESEARCH_PAPER",
                "source": {
                    "name": "Arxiv",
                    "url": entry.link
                },
                "content": {
                    "title": entry.title.replace("\n", " ").strip(),
                    "authors": [author.name for author in entry.authors] if hasattr(entry, "authors") else [],
                    "paper_url": entry.link,
                    "github_url": github_url,
                    "github_stars": github_stars,
                    "published_date": entry.published
                },
                "collectedAt": datetime.now(timezone.utc).isoformat()
            }
            all_papers.append(paper)

        # Be polite to Arxiv's servers — required by their API terms
        time.sleep(3)

    return all_papers


if __name__ == "__main__":
    papers = fetch_arxiv_papers(query="artificial intelligence", max_results=500)
    print(f"\nTotal papers collected: {len(papers)}")

    with open("papers_raw.json", "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)

    print("Saved to papers_raw.json")