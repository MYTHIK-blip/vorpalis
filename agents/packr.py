import os
import zipfile
import yaml
from datetime import datetime

class PACKRAgent:
    """
    PACKR: bundles all scroll outputs into timestamped ZIP archives
          and emits a metadata manifest for each bundle.
    """
    def __init__(self, source_dir="scroll_products", bundle_dir="scroll_products/bundles"):
        self.name       = "PACKR"
        self.source_dir = source_dir
        self.bundle_dir = bundle_dir
        os.makedirs(self.bundle_dir, exist_ok=True)

    def create_bundle(self, bundle_name: str = None) -> str:
        ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
        base     = bundle_name or f"bundle_{ts}"
        zip_path = os.path.join(self.bundle_dir, f"{base}.zip")

        # Build the ZIP
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(self.source_dir):
                for fn in files:
                    full = os.path.join(root, fn)
                    # skip nested bundles and manifests
                    if full.startswith(self.bundle_dir):
                        continue
                    arcname = os.path.relpath(full, self.source_dir)
                    zf.write(full, arcname)
        print(f"[{self.name}] Created bundle → {zip_path}")

        # Emit a sidecar manifest.yaml
        manifest = {
            "product_name": base,
            "filename":     os.path.basename(zip_path),
            "created":      datetime.now().isoformat(),
            "description":  f"Prompt pack for '{base}'",
            "keywords":     [base],
            "price":        "5.00",
            "license":      "MIT"
        }
        mf_path = zip_path.replace(".zip", ".yaml")
        with open(mf_path, "w") as mf:
            yaml.safe_dump(manifest, mf, sort_keys=False)
        print(f"[{self.name}] Wrote manifest → {mf_path}")

        return zip_path

    def list_bundles(self) -> list[str]:
        bundles = [f for f in os.listdir(self.bundle_dir) if f.endswith(".zip")]
        print(f"[{self.name}] Available bundles:")
        for b in bundles:
            print(f"  • {b}")
        return bundles

if __name__ == "__main__":
    agent = PACKRAgent()
    zipf  = agent.create_bundle()
    agent.list_bundles()

