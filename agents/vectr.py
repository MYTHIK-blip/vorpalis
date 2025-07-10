import os
from datetime import datetime
from llm.mistralon import query_model  # ensure this function returns a string

class VECTRAgent:
    """
    VECTR: Uses an LLM to generate product/marketing scrolls
    and saves them into scroll_products/.
    """

    def __init__(self,
                 output_dir="scroll_products"):
        self.name = "VECTR"
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def run(self, topic: str = "default") -> str:
        """
        Send a prompt to the LLM, save the response as a markdown scroll.
        Returns the path to the saved file.
        """
        prompt = f"Generate 10 product ideas and marketing prompts for: {topic}"
        print(f"[{self.name}] Prompting LLM → {prompt}")
        response = query_model(prompt)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe = topic.replace(" ", "_")
        filename = f"{safe}_{ts}.md"
        path = os.path.join(self.output_dir, filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(response)
        print(f"[{self.name}] Saved scroll → {path}")
        return path

if __name__ == "__main__":
    import sys
    topic = sys.argv[1] if len(sys.argv) > 1 else "default"
    agent = VECTRAgent()
    agent.run(topic)

