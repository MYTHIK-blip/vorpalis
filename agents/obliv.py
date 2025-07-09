# agents/obliv.py

import os
import json
from datetime import datetime

class OBLIVAgent:
    """
    OBLIV: scans the scroll_products directory,
    records file metadata, and writes an inventory.
    """

    def __init__(self,
                 product_dir="scroll_products",
                 inventory_file="memory/inventory.json"):
        self.name = "OBLIV"
        self.product_dir = product_dir
        self.inventory_file = inventory_file

    def scan_inventory(self) -> list[dict]:
        items = []
        for root, _, files in os.walk(self.product_dir):
            for fn in files:
                path = os.path.join(root, fn)
                st = os.stat(path)
                items.append({
                    "path": path,
                    "size_bytes": st.st_size,
                    "modified": datetime.fromtimestamp(st.st_mtime).isoformat()
                })
        return items

    def save_inventory(self) -> str:
        inv = self.scan_inventory()
        os.makedirs(os.path.dirname(self.inventory_file), exist_ok=True)
        with open(self.inventory_file, "w", encoding="utf-8") as f:
            json.dump(inv, f, indent=2)
        print(f"[{self.name}] Saved inventory → {self.inventory_file}")
        return self.inventory_file

    def show_inventory(self) -> None:
        inv = self.scan_inventory()
        print(f"[{self.name}] Current Inventory:")
        for item in inv:
            print(f" — {item['path']} ({item['size_bytes']} B, modified {item['modified']})")

if __name__ == "__main__":
    agent = OBLIVAgent()
    agent.save_inventory()
    agent.show_inventory()

