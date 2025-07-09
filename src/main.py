# src/main.py

import argparse
import time
from agents.loomx import run_loom
from agents.packr import PACKRAgent
from agents.obliv import OBLIVAgent

# ────── Agent Manifest ──────
AGENT_MANIFEST = {
    "VECTR": "Export scroll products (.txt/.md/.pdf)",
    "LOOMX": "Generate & package prompts via LLM",
    "PACKR": "Bundle products into ZIP archives",
    "OBLIV": "Inventory and manifest products"
}

def show_manifest():
    print("📜 Agent Manifest:")
    for name, desc in AGENT_MANIFEST.items():
        print(f" • {name}: {desc}")
    print()

# ────── Single Run ──────
def run_once(topic: str):
    print(f"\n🧪 Running pipeline for topic: {topic}\n")
    show_manifest()

    # 1) Generate + export scroll via LOOMX (which calls VECTR internally)
    run_loom(topic)

    # 2) Bundle everything in scroll_products/
    packr = PACKRAgent()
    bundle_path = packr.create_bundle(bundle_name=f"{topic.replace(' ','_')}_bundle")

    # 3) Update and display inventory
    obliv = OBLIVAgent()
    inventory_path = obliv.save_inventory()
    obliv.show_inventory()

    print(f"\n✅ Pipeline complete!\n  • Bundle: {bundle_path}\n  • Inventory: {inventory_path}\n")

# ────── Loop Mode ──────
def run_loop(topic: str, interval: int):
    print(f"♻️ Starting continuous mode for '{topic}' every {interval}s\n")
    try:
        while True:
            run_once(topic)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n🛑 Loop interrupted by user.")

# ────── CLI Entrypoint ──────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VORPALIS Digital Forge Orchestrator")
    parser.add_argument('--topic', '-t', default="wellness", help="Topic for scroll generation")
    parser.add_argument('--loop', '-l', action='store_true', help="Run continuously")
    parser.add_argument('--interval', '-i', type=int, default=600, help="Loop interval in seconds")
    args = parser.parse_args()

    if args.loop:
        run_loop(args.topic, args.interval)
    else:
        run_once(args.topic)

