import os
import sys
import shutil

# ─ Ensure repo root on path for `import agents` ───────────────────
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from agents.loomx import LOOMXAgent
from agents.vectr import VECTRAgent
from agents.obliv import OBLIVAgent
from agents.packr import PACKRAgent

def main(topic="civic tech"):
    print(f"[MAIN] Starting pipeline for topic: {topic}\n")

    # 1) Scan local scroll memory
    loomx      = LOOMXAgent()
    entries    = loomx.run(topic)

    # 2) Generate new scroll via LLM
    vectr      = VECTRAgent()
    scroll_md  = vectr.run(topic)

    # 3) Inventory current scroll products
    obliv      = OBLIVAgent()
    inventory  = obliv.run(topic)

    # 4) Bundle all scroll products + manifest
    packr      = PACKRAgent()
    bundle_zip = packr.create_bundle(topic)

    # 5) Export ready-to-sell package
    out_dir = os.path.abspath("products_ready")
    os.makedirs(out_dir, exist_ok=True)

    # copy the main bundle + its manifest
    manifest  = bundle_zip.replace(".zip", ".yaml")
    for f in (bundle_zip, manifest, scroll_md):
        dest = os.path.join(out_dir, os.path.basename(f))
        shutil.copy(f, dest)
    print(f"\n[MAIN] Published to → {out_dir}")

    # Summary
    print("\n[MAIN] Pipeline complete:")
    print(f"  • Memory entries: {len(entries)}")
    print(f"  • Scroll output:  {scroll_md}")
    print(f"  • Inventory:      {inventory}")
    print(f"  • Bundle ZIP:     {bundle_zip}")
    print(f"  • Manifest YAML:  {manifest}")

if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "civic tech"
    main(topic)

