# src/main.py

import argparse
import time
from datetime import datetime
from agents.vectr import export_scroll
from src.llm.mistralon import query_mistral

# Optional: future modules
# from agents.loomx import loom_trigger
# from scrollsync.glyphx import route_output
# from memory.arkive import log_context

def generate_prompt_pack():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"Generate 5 startup tools using AI for mental resilience. Time: {now}"

def run_once():
    prompt = generate_prompt_pack()
    print(f"\n🧠 Prompt: {prompt}\n")

    response = query_mistral(prompt)

    scroll_title = "Mistral Prompt Pack"
    export_scroll(scroll_title, response)

def run_loop(interval_seconds=600):
    print(f"♻️ Looping every {interval_seconds} seconds...")
    try:
        while True:
            run_once()
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\n🛑 Scrollloop interrupted.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run VORPALIS")
    parser.add_argument('--loop', action='store_true', help="Run in scrollloop mode")
    parser.add_argument('--interval', type=int, default=600, help="Loop interval in seconds")
    args = parser.parse_args()

    if args.loop:
        run_loop(args.interval)
    else:
        run_once()

