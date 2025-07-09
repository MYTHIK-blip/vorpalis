import os
import yaml
import glob
from datetime import datetime

class LOOMXAgent:
    def __init__(self):
        self.name = "LOOMX"
        self.description = "Local memory and scroll context scanner"
        self.memory_path = "memory/"
        self.output_path = "logs/loomx.echo.md"

    def gather_scroll_data(self):
        print(f"[{self.name}] Gathering local scrolls from {self.memory_path}")
        entries = []
        for file in glob.glob(f"{self.memory_path}/*.yaml"):
            with open(file, "r") as f:
                content = yaml.safe_load(f)
                entries.append({file: content})
        self.log(entries)
        return entries

    def log(self, data):
        ts = datetime.utcnow().isoformat()
        with open(self.output_path, "a") as log:
            log.write(f"# [{ts}] {self.description}\n")
            for entry in data:
                log.write(yaml.dump(entry, allow_unicode=True) + "\n")

if __name__ == "__main__":
    agent = LOOMXAgent()
    agent.gather_scroll_data()

