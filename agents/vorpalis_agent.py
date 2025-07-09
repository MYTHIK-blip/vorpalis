#!/usr/bin/env python3

import yaml
import subprocess
import os
import time
import argparse
from datetime import datetime

CONFIG_PATH = os.path.join("config", "settings.yaml")
OUTPUT_DIR = os.path.expanduser("~/Documents/scroll_products/loop_prompts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def query_llm(prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", "mistral:instruct", prompt],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip()

def log_prompt(content: str):
    today = datetime.now().strftime("%Y-%m-%d")
    log_path = os.path.join(OUTPUT_DIR, f"{today}_prompts.md")
    timestamp = datetime.now().isoformat()
    numbered = f"## [{timestamp}]\n{content}\n\n"
    with open(log_path, "a") as log:
        log.write(numbered)

def run_once():
    prompt_instruction = "Write one powerful, sellable prompt for a product in wellness, AI, or civic resilience."
    prompt = query_llm(prompt_instruction)
    print(f"📦 Prompt:\n{prompt}\n")
    log_prompt(prompt)

def run_loop(interval=10):
    print("♻️ VORPALIS SCROLLLOOP ACTIVE — Generating every", interval, "seconds")
    try:
        while True:
            run_once()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n🛑 Loop interrupted by user.")

def run_agent():
    parser = argparse.ArgumentParser()
    parser.add_argument('--loop', action='store_true', help='Run VORPALIS in timed scrollloop mode')
    parser.add_argument('--interval', type=int, default=10, help='Loop interval in seconds')
    args = parser.parse_args()

    print("🧠 VORPALIS AGENT BOOTING...")

    with open(CONFIG_PATH, "r") as f:
        settings = yaml.safe_load(f)

    name = settings['agent']['name']
    role = settings['agent']['role']
    mood = settings['agent']['mood']
    version = settings['agent']['version']

    print(f"🔮 {name} [{role}] ONLINE — Mood: {mood} | v{version}")

    if args.loop:
        run_loop(args.interval)
    else:
        run_once()

if __name__ == "__main__":
    run_agent()

