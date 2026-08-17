import json
import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_INSTRUCTION = """You are a data extraction engine. Given a research paper's raw title and metadata,
output ONLY a valid JSON object matching this exact schema, nothing else, no markdown fences:
{
  "entityName": "<canonical startup/lab name if identifiable from authors' affiliation, else null>",
  "topic_category": "<one of: NLP, Computer Vision, Robotics, RL, Multimodal, Infrastructure, Safety, Other>",
  "one_line_summary": "<a single plain-English sentence under 20 words summarizing the paper's contribution>"
}"""


def extract_structured_data(paper_title, retries=3):
    prompt = f"{SYSTEM_INSTRUCTION}\n\nPaper title: {paper_title}"

    for attempt in range(retries):
        try:
            response = client.models.generate_content(
    model="gemini-flash-lite-latest",
    contents=prompt
)
            text = response.text.strip()
            text = text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except Exception as e:
            wait = (2 ** attempt) + 1
            print(f"LLM call failed (attempt {attempt+1}/{retries}): {e}. Waiting {wait}s...")
            time.sleep(wait)

    return {"entityName": None, "topic_category": "Other", "one_line_summary": None}


if __name__ == "__main__":
    with open("papers_raw.json", "r", encoding="utf-8") as f:
        papers = json.load(f)

    sample = papers[:20]
    enriched = []

    for i, paper in enumerate(sample):
        title = paper["content"]["title"]
        print(f"[{i+1}/{len(sample)}] Extracting: {title[:60]}...")
        structured = extract_structured_data(title)
        paper["content"]["llm_extracted"] = structured
        enriched.append(paper)
        time.sleep(5)

    with open("papers_llm_enriched.json", "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=2, ensure_ascii=False)

    print(f"\nDone. Enriched {len(enriched)} papers saved to papers_llm_enriched.json")