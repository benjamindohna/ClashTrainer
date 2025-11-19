from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time 
from collections import Counter
from datetime import datetime
from .data_utils import load_card_data, save_card_data

# this is where you list your urls
# you can add or remove urls here.
URLS = [
    "https://royaleapi.com/decks/popular?time=1d&sort=rating&size=30&players=PvP&min_ranked_trophies=0&max_ranked_trophies=4400&min_elixir=1&max_elixir=9&evo=None&min_cycle_elixir=4&max_cycle_elixir=28&mode=detail&type=TopRanked&&&global_exclude=false",
    "https://royaleapi.com/decks/popular?time=1d&sort=rating&size=30&players=PvP&min_trophies=0&max_trophies=20000&min_elixir=1&max_elixir=9&evo=None&min_cycle_elixir=4&max_cycle_elixir=28&mode=detail&type=Ladder&&&global_exclude=false"
]

# setting up selenium
print("starting scraping process")
print(f"urls to process: {len(URLS)}")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

final_cards_list: list[str] = []
driver = None

try:
    # init the webdriver
    driver = webdriver.Chrome(options=chrome_options) 
    
    # loop through all urls
    for i, url in enumerate(URLS):
        driver.get(url)
        # wait a bit for the page to load
        time.sleep(5) 
        
        # get the html
        html_content = driver.page_source
        
        # parse html to get card names
        soup = BeautifulSoup(html_content, 'html.parser')

        # use css selector to find the card images
        card_images = soup.select('div.deck_card__four_wide img')
        
        # extract card names
        cards_scraped = 0
        for card_img in card_images:
            card_name = card_img.get('alt')
            if card_name:
                final_cards_list.append(card_name)
                cards_scraped += 1
        
        print(f"status: successfully scraped {cards_scraped} cards.")
            
except Exception as e:
    print(f"\ncritical error\nan error occurred during processing: {e}")
    
finally:
    # close the browser
    if driver:
        driver.quit() 
        
# calculations and data update

total_cards_scraped = len(final_cards_list)
card_counts = Counter(final_cards_list)
unique_cards = set(final_cards_list)

print("\nsummary of scraped data")
print(f"total cards scraped from all urls: {total_cards_scraped}")
print(f"total number of distinct card individuals: {len(unique_cards)}")

# calculate meta scores
meta_scores: dict[str, float] = {}
if card_counts:
    # find the most frequent card (the score 100 benchmark)
    highest_frequency = card_counts.most_common(1)[0][1] 
    
    # assign scores using a linear distribution (0-100 scale)
    for card_name, frequency in card_counts.items():
        score = round((frequency / highest_frequency) * 100, 2)
        meta_scores[card_name] = score


# print scores if you want to
print("\ncard meta scores (0-100 scale)")
# print the top 15 scoring cards, sorted by score
sorted_meta_scores = sorted(meta_scores.items(), key=lambda item: item[1], reverse=True)

for card, score in sorted_meta_scores[:16]:
    # removed the star emoji
    print(f"{card:<20}: {score}")

print("\n(note: any card not listed above has an implicit meta score of 0 based on this data.)")


print("\nupdating cards.json")

# load existing data using the robust function
card_data = load_card_data() 

if card_data is None:
    print("aborting update: could not load existing card data.")
    # exit the script gracefully if the load fails
    exit() 

# get current timestamp
timestamp = datetime.now().strftime("%d %b %Y, %H:%M:%S")
cards_updated_count = 0

# update the data structure (merging meta_scores)
for card_name in card_data.keys():
    if card_name.startswith('_'):
        continue
        
    # get score (0 if not found)
    score = meta_scores.get(card_name, 0)
    card_data[card_name]['meta_score'] = score
    cards_updated_count += 1
    
# update  metadata fields
card_data["_last_updated_meta_scores"] = timestamp

# save  updated dictionary using the robust function
if save_card_data(card_data):
    print(f"success! updated {cards_updated_count} cards with new meta scores.")
    print(f"file saved with timestamp: {timestamp}")
else:
    print("update failed during save process.")