import sys
import os

# Allow Python to find the 'agents' directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.vorpalis_agent import run_agent

if __name__ == "__main__":
    print("🧠 VORPALIS AGENT BOOTING...")
    run_agent()

