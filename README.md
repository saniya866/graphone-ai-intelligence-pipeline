# graphone-ai-intelligence-pipeline
.
# GraphOne AI Intelligence Graph — Data Pipeline (Trial Task)

## Overview
This repository contains a working data pipeline that scrapes, structures, and canonicalizes AI ecosystem data (research papers, products, startups) as part of the GraphOne/FrontierAtlas AI Engineer trial task.

**Scope note:** Given the 3-day trial window, this submission prioritizes real, sourced, non-hallucinated data over hitting the full 1000+ target on every vertical. Every record traces to a live, verifiable source URL. See `architecture.pdf` for the full design of how this scales to 500k+ records in production.

## What's implemented
- **Research Papers**: 500 real papers from the Arxiv API, including GitHub repo detection + live star-count lookup via GitHub's API.
- **Products**: 400 real GitHub repositories (AI-tagged), used as a proxy for "products" given the trial's time constraints — documented tradeoff.
- **Startups**: 1000 real companies from Y Combinator's public company dataset.
- **Entity Resolution**: Deduplication/canonicalization engine matching raw names against a 30+ company seed list (e.g., "microsoft" → "Microsoft").
- **Error handling**: All network calls wrapped in try/except with graceful degradation — network failures during testing were logged, not crashed (see terminal logs in `/logs` if included).

## What's NOT implemented (and why)
- **Jobs / News (24hr freshness)**: Not built in this trial due to time constraints. Full design for freshness tracking, relative-date parsing, and dedup across distributed nodes is documented in `architecture.pdf`.
- **Multi-tier LLM fallback (Gemini → Groq → DeepSeek)**: Not implemented in code; design documented in `architecture.pdf`.
- **Anti-bot / Cloudflare bypass**: Not needed for the sources used (Arxiv, GitHub, YC all have open APIs); strategy for harder sources documented in `architecture.pdf`.

## Setup
```bash
pip install requests feedparser google-generativeai python-dotenv --break-system-packages
python arxiv_scraper.py
python github_products_scraper.py
python startups_scraper.py
python convert_to_csv.py
python entity_resolution.py
```

## Repo structure

src/
arxiv_scraper.py # Research papers + GitHub star tracking
github_products_scraper.py # Products (GitHub repos as proxy)
startups_scraper.py # Startups (YC dataset)
convert_to_csv.py # JSON -> CSV for Google Sheets
entity_resolution.py # Canonicalization engine
architecture.pdf # Full system design for production scale

## Data Output
Google Sheet (public link): https://docs.google.com/spreadsheets/d/11B9vRabT1xzGOoxJLS6NQ3FxJbhvGMZijce8BF3vBpY/edit?usp=sharing

## Author
SYEDA SANIYA KOUSER — AI Engineer Intern Trial Submission
