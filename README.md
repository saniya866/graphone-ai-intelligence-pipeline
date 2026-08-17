# graphone-ai-intelligence-pipeline
.
# GraphOne AI Intelligence Graph — Data Pipeline (Trial Task)

## Overview
This repository contains a working data pipeline that scrapes, structures, and canonicalizes AI ecosystem data (research papers, products, startups, jobs, and news) as part of the GraphOne/FrontierAtlas AI Engineer trial task.

**Scope note**: Given the 3-day trial window, this submission prioritizes real, sourced, non-hallucinated data over hitting the full 1000+ target on every vertical. Every record traces to a live, verifiable source URL. See `architecture.pdf` for the full design of how this scales to 500k+ records in production.

## What's implemented
- **Research Papers**: 500 real papers from the Arxiv API, including GitHub repo detection + live star-count lookup via GitHub's API.
- **Products**: 400 real GitHub repositories (AI-tagged), used as a proxy for "products" given the trial's time constraints — documented tradeoff.
- **Startups**: 1,000 real companies from Y Combinator's public company dataset — meeting the full 1000+ target.
- **Jobs**: Real scraper against RemoteOK's API with a strict 24-hour freshness filter.
- **News**: Real scraper against 5 RSS feeds (TechCrunch, VentureBeat, MIT Tech Review, The Verge, Wired) with a strict 24-hour freshness filter.
- **Entity Resolution**: Deduplication/canonicalization engine matching raw names against a 30+ company seed list (e.g., "microsoft" → "Microsoft").
- **LLM Extraction**: Working integration with Google's Gemini API, extracting structured fields (topic category, one-line summary) from raw paper titles, with retry logic and rate-limit handling for free-tier quotas. Demonstrated on a live sample of 20 papers.
- **Asynchronous Scraping**: A working `asyncio` + `aiohttp` implementation demonstrating concurrent data collection — 200 papers fetched in ~17 seconds, proving the concurrency pattern required by the task.
- **Error handling**: All network calls wrapped in try/except with graceful degradation — network and rate-limit failures during testing were logged and retried, not crashed.

## What's NOT implemented (and why)
- **Multi-tier LLM fallback (Gemini → Groq → DeepSeek)**: Only the Gemini tier was implemented in code; the full fallback chain design is documented in `architecture.pdf`.
- **Anti-bot / Cloudflare bypass**: Not needed for the sources used (Arxiv, GitHub, YC, RemoteOK, RSS feeds all have open, unprotected access); strategy for harder sources is documented in `architecture.pdf`.

## Setup
```bash
pip install requests feedparser google-genai python-dotenv aiohttp --break-system-packages
python arxiv_scraper.py
python github_products_scraper.py
python startups_scraper.py
python jobs_news_scraper.py
python convert_to_csv.py
python entity_resolution.py
python llm_extraction.py
python async_arxiv_demo.py
```

## Repo structure
arxiv_scraper.py # Research papers + GitHub star tracking
github_products_scraper.py # Products (GitHub repos as proxy)
startups_scraper.py # Startups (YC dataset)
jobs_news_scraper.py # Jobs (RemoteOK) + News (RSS feeds), 24hr freshness filter
convert_to_csv.py # JSON -> CSV for Google Sheets
entity_resolution.py # Canonicalization engine
llm_extraction.py # Gemini LLM structured extraction
async_arxiv_demo.py # Async/concurrent scraping demo (asyncio + aiohttp)
architecture.pdf # Full system design for production scale

## Data Output
Google Sheet (public link): https://docs.google.com/spreadsheets/d/11B9vRabT1xzGOoxJLS6NQ3FxJbhvGMZijce8BF3vBpY/edit?usp=sharing

## Author
Syeda Saniya Kouser — AI Engineer Intern Trial Submission
