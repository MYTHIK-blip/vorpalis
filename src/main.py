from feedloop import generate_prompt, save_prompt

if __name__ == "__main__":
    print("🧠 VORPALIS Manual Boot: Generating one drop...")
    prompt = generate_prompt()
    save_prompt(prompt)
    print("✅ Drop complete.")

