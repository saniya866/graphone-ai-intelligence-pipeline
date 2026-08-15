import json
import csv

# Seed list of ~50 known AI startups (canonical names)
CANONICAL_STARTUPS = {
    "openai": "OpenAI", "open ai": "OpenAI", "openai inc": "OpenAI",
    "anthropic": "Anthropic", "anthropic pbc": "Anthropic",
    "google deepmind": "Google DeepMind", "deepmind": "Google DeepMind",
    "microsoft": "Microsoft", "meta": "Meta", "meta ai": "Meta",
    "nvidia": "NVIDIA", "hashicorp": "HashiCorp", "aws": "Amazon Web Services",
    "amazon": "Amazon", "apache": "Apache Software Foundation",
    "hugging face": "Hugging Face", "huggingface": "Hugging Face",
    "allenai": "Allen Institute for AI", "allen ai": "Allen Institute for AI",
    "deepseek-ai": "DeepSeek", "deepseek": "DeepSeek",
    "qwenlm": "Alibaba Qwen", "moonshotai": "Moonshot AI",
    "zai-org": "Zhipu AI", "google": "Google", "google-deepmind": "Google DeepMind",
    "pytorch": "PyTorch (Meta)", "tensorflow": "TensorFlow (Google)",
    "sakanaai": "Sakana AI", "prefecthq": "Prefect", "qdrant": "Qdrant",
    "jina-ai": "Jina AI", "cleanlab": "Cleanlab", "interpretml": "InterpretML",
}


def canonicalize(raw_name):
    if not raw_name:
        return None
    key = raw_name.strip().lower()
    return CANONICAL_STARTUPS.get(key, raw_name)  # fallback: keep original if unknown


def build_mapping_log():
    log_rows = []
    with open("products_raw.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    seen = set()
    for p in products:
        raw = p["content"]["startupName"]
        if not raw or raw in seen:
            continue
        seen.add(raw)
        canonical = canonicalize(raw)
        log_rows.append({
            "raw_name": raw,
            "canonical_name": canonical,
            "matched": "YES" if canonical != raw else "NO (kept as-is, not in seed list)"
        })

    with open("entity_mapping_log.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["raw_name", "canonical_name", "matched"])
        writer.writeheader()
        writer.writerows(log_rows)

    print(f"Saved {len(log_rows)} entity mapping rows to entity_mapping_log.csv")


if __name__ == "__main__":
    build_mapping_log()