import os
import glob
import yaml
from datetime import datetime

class LOOMXAgent:
    """
    LOOMX: Local memory & scroll context scanner.
    """

    def __init__(self,
                 memory_dir="memory",
                 output_log="logs/loomx.echo.md"):
        self.name = "LOOMX"
        self.memory_dir = memory_dir
        self.output_log = output_log
        os.makedirs(self.memory_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.output_log), exist_ok=True)

    def run(self, topic: str = None) -> list[dict]:
        """
        Scan all YAML memory entries and return as list of dicts.
        """
        print(f"[{self.name}] Scanning memory from {self.memory_dir} …")
        entries = []
        for path in glob.glob(f"{self.memory_dir}/*.yaml"):
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            entries.append({"file": path, "content": data})
        self._log(entries)
        return entries

    def _log(self, entries: list[dict]):
        ts = datetime.utcnow().isoformat()
        with open(self.output_log, "a", encoding="utf-8") as log:
            log.write(f"# [{ts}] {self.name} scan\n")
            for entry in entries:
                log.write(yaml.dump(entry, allow_unicode=True))
                log.write("\n")
        print(f"[{self.name}] Logged {len(entries)} entries → {self.output_log}")

if __name__ == "__main__":
    agent = LOOMXAgent()
    agent.run()

