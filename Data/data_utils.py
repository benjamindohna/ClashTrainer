import json
from pathlib import Path


# FUNCTIONS
# --- Private Helper Function ---
def __load_json_data(filename: str) -> dict | None:
    """
    Private helper function to perform the core logic:
    1. Determine the path relative to this file.
    2. Handle file opening and error management (try/except).
    """
    DATA_PATH = Path(__file__).resolve().parent / filename
    
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            card_data = json.load(f)
        return card_data
    except FileNotFoundError:
        print(f"Error: Data file not found at {DATA_PATH}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {DATA_PATH}")
        return None
    

# --- Public Functions ---
def load_card_data():
    """
    Loads and returns all card data from cards.json.
    """
    return __load_json_data("cards.json")
    
def load_card_data_sample():
    """
    Loads and returns sample card data from cards_sample.json.
    """
    return __load_json_data("cards_sample.json")

def save_card_data(data_to_save: dict):
    """
    Saves the complete card data dictionary to cards.json.
    Uses robust path management and clean JSON formatting.
    """
    filename = "cards.json"
    # Replicate the robust path finding from __load_json_data
    DATA_PATH = Path(__file__).resolve().parent / filename
    
    try:
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            # Use indent=4 for clean, readable JSON formatting
            json.dump(data_to_save, f, indent=4)
        return True
    except Exception as e:
        print(f"Error: Failed to save JSON data to {DATA_PATH}: {e}")
        return False

# count amount of cards in dataset
def print_amount_of_cards():
    # Count only entries that do NOT start with "_" (those are metadata, NOT cards)
    data = load_card_data()
    card_count = sum(1 for key in data.keys() if not key.startswith("_"))

    print("Number of cards:", card_count)
