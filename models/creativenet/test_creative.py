# test_creative.py
from generate import generate_creative_associations

while True:
    prompt = input("🎨 Enter a concept (or 'exit'): ")
    if prompt.lower() == "exit":
        break

    results = generate_creative_associations(prompt)
    for r in results:
        print("  🌀", r)
