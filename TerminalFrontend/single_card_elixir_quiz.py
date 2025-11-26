import random
import sys, tty, termios
from Data.data_utils import load_card_data
import re

# LOAD DATA
card_data = load_card_data()
# uncomment following 2 lines to use small sample dataset:
# from Data.data_utils import load_card_data_sample
# card_data = load_card_data_sample()

# VARIABLES
game_is_on = True
correctly_answered = []
incorrect_guess_counter = 0

# FUNCTIONS
def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)  # one character, instantly
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def get_elixir_input():
    while True:
        key = get_key()

        # Check if key is a digit 1–9
        pattern = r'^[1-9]$'
        if re.fullmatch(pattern, key):
            value = int(key)
            if 1 <= value <= 9:
                print(value)
                return value
            
        if key == "q":
            return key
        
        # If invalid:
        print("Indicate a number from 1 to 9 for the elixir cost or press 'q' to leave")


# LETS GO
while game_is_on:

    cards = [key for key in card_data.keys() if not key.startswith("_") and key not in correctly_answered]
    # print("cards:", cards)
    # print("correctly:", correctly_answered)
    # print(card_data.keys())

    if not cards: 
        guess_keyword = "guess" if incorrect_guess_counter == 1 else "guesses"
        print(f"You've correctly answered all the cards, with {incorrect_guess_counter} incorrect {guess_keyword}.")
        break

    # Pick random card
    random_card = random.choice(cards)
    random_card_elixir = card_data[random_card]["elixir"]

    print(random_card, "| (press 'q' to quit)")   # newline for readability
    print("Your guess: ")
    guess = get_elixir_input()

    if guess == "q":
        print("Goodbye!")
        break

    if guess == random_card_elixir: 
        print("Correct!\n")
        correctly_answered.append(random_card)
    else: 
        print(f"Wrong! {random_card_elixir} elixir is correct\n")
        incorrect_guess_counter += 1
        

