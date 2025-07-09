import os
import requests
import json
from datetime import datetime
from src.feedloop import generate_feed_summary
from config import settings
from memory import context_store

class VECTRAgent:
    def __init__(self):
        self.name = "VECTR"
        self.description = "Market scanner and prompt packager"
        self.scan_endpoint = "https://huggingface.co/api/models?sort=downloads"

    def scan_online_assets(self, limit=10):
        print(f"[{self.name}] Scanning Hugging Face for top {limit} models...")
        try:
            response = requests.get(self.scan_endpoint)
            data = response.json()[:limit]
            entries = [{"name": d["modelId"], "downloads": d["downloads"]} for d in data]
            self.log(entries)
            return entries
        except Exception as e:
            print(f"[{self.name}] Error: {e}")
            return []

    def package_prompts(self, model_name):
        prompt = f"Generate 20 useful prompts for model: {model_name}"
        result = generate_feed_summary(prompt)
        filename = f"scroll_products/{model_name}_prompts.txt"
        with open(filename, "w") as f:
            f.write(result)
        print(f"[{self.name}] Prompt scroll saved → {filename}")
        return filename

    def log(self, data):
        ts = datetime.utcnow().isoformat()
        path = "logs/vectr.echo.md"
        with open(path, "a") as log:
            log.write(f"## [{ts}] {self.description}\n")
            log.write(json.dumps(data, indent=2) + "\n\n")

if __name__ == "__main__":
    agent = VECTRAgent()
    top_models = agent.scan_online_assets()
    if top_models:
        agent.package_prompts(top_models[0]["name"])

