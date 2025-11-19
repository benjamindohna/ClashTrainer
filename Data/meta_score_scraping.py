from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time 
from collections import Counter
from datetime import datetime
from .data_utils import load_card_data, save_card_data

# --- Configuration ---
# 1. Define the list of URLs here. Add or remove URLs as needed.
URLS = [
    "https://royaleapi.com/decks/popular?time=1d&sort=rating&size=30&players=PvP&min_ranked_trophies=0&max_ranked_trophies=4400&min_elixir=1&max_elixir=9&evo=None&min_cycle_elixir=4&max_cycle_elixir=28&mode=detail&type=TopRanked&&&global_exclude=false",
    "https://royaleapi.com/decks/popular?time=1d&sort=rating&size=30&players=PvP&min_trophies=0&max_trophies=20000&min_elixir=1&max_elixir=9&evo=None&min_cycle_elixir=4&max_cycle_elixir=28&mode=detail&type=Ladder&&&global_exclude=false"
]

# --- Selenium Setup ---
print("--- Starting Scraping Process ---")
print(f"URLs to process: {len(URLS)}")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

final_cards_list: list[str] = []
driver = None

try:
    # Initialize the WebDriver once
    driver = webdriver.Chrome(options=chrome_options) 
    
    # --- Loop Through All URLs ---
    for i, url in enumerate(URLS):
        driver.get(url)
        # Wait for the JavaScript content to load
        time.sleep(5) 
        
        # Get the final, fully rendered HTML source
        html_content = driver.page_source
        
        # --- Parse HTML and Extract Card Names ---
        soup = BeautifulSoup(html_content, 'html.parser')

        # Use CSS Selector to find all <img> tags inside ALL 'deck_card__four_wide' divs
        card_images = soup.select('div.deck_card__four_wide img')
        
        # Extract card names and extend the master list
        cards_scraped = 0
        for card_img in card_images:
            card_name = card_img.get('alt')
            if card_name:
                final_cards_list.append(card_name)
                cards_scraped += 1
        
        print(f"Status: Successfully scraped {cards_scraped} cards.")
            
except Exception as e:
    print(f"\n--- CRITICAL ERROR --- \nAn error occurred during processing: {e}")
    
finally:
    # Ensure the browser is closed
    if driver:
        driver.quit() 
        
# ----------------------------------------------------------------------
## 📊 Meta Score Calculation and Data update
# ----------------------------------------------------------------------

total_cards_scraped = len(final_cards_list)
card_counts = Counter(final_cards_list)
unique_cards = set(final_cards_list)

print("\n--- Summary of Scraped Data ---")
print(f"Total cards scraped from all URLs: {total_cards_scraped}")
print(f"Total number of distinct card individuals: {len(unique_cards)}")

# Calculate Meta Scores
meta_scores: dict[str, float] = {}
if card_counts:
    # Find the most frequent card (the score 100 benchmark)
    highest_frequency = card_counts.most_common(1)[0][1] 
    
    # Assign scores using a linear distribution (0-100 scale)
    for card_name, frequency in card_counts.items():
        score = round((frequency / highest_frequency) * 100, 2)
        meta_scores[card_name] = score


# PRINT SCORES IF YOU WANT TO
print("\n--- Card Meta Scores (0-100 Scale) ---")
# Print the top 15 scoring cards, sorted by score
sorted_meta_scores = sorted(meta_scores.items(), key=lambda item: item[1], reverse=True)

for card, score in sorted_meta_scores[:16]:
    print(f"🌟 {card:<20}: {score}")

print("\n(Note: Any card not listed above has an implicit Meta Score of 0 based on this data.)")



print("\n--- Updating cards.json ---")

# 1. LOAD existing data using the robust function
card_data = load_card_data() 

if card_data is None:
    print("🚨 Aborting update: Could not load existing card data.")
    # Exit the script gracefully if the load fails
    # You might consider creating the file here if it's missing, but aborting is safer.
    exit() 

# Get current timestamp
timestamp = datetime.now().strftime("%d %b %Y, %H:%M:%S")
cards_updated_count = 0

# 2. UPDATE the data structure (Merging meta_scores)
for card_name in card_data.keys():
    if card_name.startswith('_'):
        continue
        
    # Get the score (0 if not found)
    score = meta_scores.get(card_name, 0)
    card_data[card_name]['meta_score'] = score
    cards_updated_count += 1
    
# 3. Update the metadata fields
card_data["_last_updated_meta_scores"] = timestamp

# 4. SAVE the updated dictionary using the robust function
if save_card_data(card_data):
    print(f"Success! Updated {cards_updated_count} cards with new meta scores.")
    print(f"File saved with timestamp: {timestamp}")
else:
    print("🚨 Update failed during save process.")
