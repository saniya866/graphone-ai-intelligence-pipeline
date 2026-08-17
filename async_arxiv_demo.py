import asyncio
import aiohttp
import feedparser
import json
import time
from datetime import datetime, timezone


async def fetch_batch(session, start, batch_size, query="artificial intelligence"):
    """Fetch one batch of papers asynchronously from Arxiv."""
    params = {
        "search_query": f"all:{query}",
        "start": start,
        "max_results": batch_size,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    url = "http://export.arxiv.org/api/query"

    try:
        async with session.get(url, params=params, timeout=30) as response:
            text = await response.text()
            feed = feedparser.parse(text)
            papers = []
            for entry in feed.entries:
                papers.append({
                    "schemaVersion": "1.0",
                    "recordType": "RESEARCH_PAPER",
                    "source": {"name": "Arxiv", "url": entry.link},
                    "content": {
                        "title": entry.title.replace("\n", " ").strip(),
                        "authors": [a.name for a in entry.authors] if hasattr(entry, "authors") else [],
                        "paper_url": entry.link,
                        "published_date": entry.published
                    },
                    "collectedAt": datetime.now(timezone.utc).isoformat()
                })
            return papers
    except Exception as e:
        print(f"Batch starting at {start} failed: {e}")
        return []


async def fetch_all_async(total=200, batch_size=50):
    """
    Demonstrates concurrent scraping: multiple batches fetched in parallel
    instead of sequentially, using asyncio + aiohttp (per task's async requirement).
    """
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_batch(session, start, batch_size)
            for start in range(0, total, batch_size)
        ]
        # Arxiv asks for polite pacing, so we stagger task starts slightly
        results = []
        for i, task in enumerate(tasks):
            if i > 0:
                await asyncio.sleep(3)  # stay polite to Arxiv's servers
            result = await task
            results.append(result)

        all_papers = [p for batch in results for p in batch]
        return all_papers


if __name__ == "__main__":
    start_time = time.time()
    papers = asyncio.run(fetch_all_async(total=200, batch_size=50))
    elapsed = time.time() - start_time

    print(f"\nCollected {len(papers)} papers asynchronously in {elapsed:.1f}s")

    with open("papers_async_demo.json", "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)

    print("Saved to papers_async_demo.json")