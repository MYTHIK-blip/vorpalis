import time
import os
import requests
from datetime import datetime

# CONFIG
OUTPUT_DIR = "scroll_products"
SCRAPE_INTERVAL = 10  # seconds
HF_SEARCH_URL = "https://huggingface.co/api/models?sort=downloads&limit=5"
GH_SEARCH_URL = "https://api.github.com/search/repositories?q=docker+stack&sort=stars&order=desc&per_page=5"

HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "vorpalis-agent"
}

# Ensure output dir exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def fetch_hf_models():
    try:
        r = requests.get(HF_SEARCH_URL)
        data = r.json()
        return [f"{m['modelId']} - {m.get('tags',[])}" for m in data]
    except Exception as e:
        return [f"HuggingFace fetch error: {e}"]

def fetch_github_stacks():
    try:
        r = requests.get(GH_SEARCH_URL, headers=HEADERS)
        data = r.json()
        items = data.get("items", [])
        return [f"{item['full_name']} - ⭐ {item['stargazers_count']}" for item in items]
    except Exception as e:
        return [f"GitHub fetch error: {e}"]

def generate_prompt():
    timestamp = get_timestamp()
    hf_models = fetch_hf_models()
    gh_repos = fetch_github_stacks()

    prompt = f"""📦 VORPALIS PRODUCT DROP [{timestamp}]

🔥 HuggingFace Models:
{chr(10).join(['- ' + m for m in hf_models])}

🚀 GitHub Stacks:
{chr(10).join(['- ' + r for r in gh_repos])}

🌀 Prompt Idea:
> How can we remix these into passive-income agents or scroll kits for resale?

🧪 Your move, scrollsmith.
"""
    return prompt

def save_prompt(text):
    fname = f"{OUTPUT_DIR}/drop_{get_timestamp()}.txt"
    with open(fname, "w") as f:
        f.write(text)
    print(f"[✓] Saved → {fname}")

def run_loop():
    while True:
        prompt = generate_prompt()
        save_prompt(prompt)
        time.sleep(SCRAPE_INTERVAL)

if __name__ == "__main__":
    run_loop()

