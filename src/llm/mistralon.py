# src/llm/mistralon.py

import subprocess

def query_mistral(prompt: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral", prompt],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            raise Exception(f"Ollama Error: {result.stderr}")
        return result.stdout.strip()
    except Exception as e:
        return f"💥 Mistralon error: {str(e)}"

