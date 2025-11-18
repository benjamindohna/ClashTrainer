import json

with open("cards.json") as f:
    data = json.load(f)

# Count only entries that do NOT start with "_"
card_count = sum(1 for key in data.keys() if not key.startswith("_"))

print("Number of cards:", card_count)
