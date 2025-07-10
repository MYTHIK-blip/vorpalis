import os
import json
from datetime import datetime

class OBLIVAgent:
    """
    OBLIV: Inventory scanner that catalogs every file in scroll_products/
    and writes a JSON manifest to memory/inventory.json.
    """

    def __init__(self,
                 source_dir="scroll_products",
                 inventory_file="memory/inventory.json"):
        self.name = "OBLIV"
        self.source_dir = source_dir
        self.inventory_file = inventory_file
        # Ensure output directory exists
        os.makedirs(os.path.dirname(self.inventory_file), exist_ok=True)

    def run(self, topic: str = None) -> str:
        """
        Scan source_dir, build list of file metadata, save to JSON.
        Returns path to the inventory file.
        """
        print(f"[{self.name}] Scanning {self.source_dir} …")
        items = []
        for root, _, files in os.walk(self.source_dir):
            for fn in files:
                path = os.path.join(root, fn)
                st = os.stat(path)
                items.append({
                    "path": path,
                    "size_bytes": st.st_size,
                    "modified": datetime.fromtimestamp(st.st_mtime).isoformat()
                })

        with open(self.inventory_file, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2)
        print(f"[{self.name}] Saved inventory → {self.inventory_file}")
        return self.inventory_file

if __name__ == "__main__":
    agent = OBLIVAgent()
    agent.run()

