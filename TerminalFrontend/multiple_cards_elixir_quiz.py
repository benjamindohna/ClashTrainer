import random
import sys, tty, termios
from Data.data_utils import load_card_data
from Backend.trade_calculations import get_trade_balance, get_trade_balance_sign

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
        if key.isdigit():
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

    cards = [key for key in card_data.keys() if not key.startswith("_")]
    # print("cards:", cards)
    # print("correctly:", correctly_answered)
    # print(card_data.keys())

    attacking_cards = random.sample(cards, 2)
    defending_cards = random.sample(cards, 1)

    print(f"Opponent: {', '.join(attacking_cards)}")
    print(f"You: {', '.join(defending_cards)}")
    print("What is the trade balance (positive numbers for negative or positive)? (press 'q' to quit)")   # newline for readability
    guess = get_elixir_input()

    if guess == "q":
        print("Goodbye!")
        break

    correct_answer = get_trade_balance(defending_cards, attacking_cards)
    correct_answer_sign = get_trade_balance_sign(correct_answer)

    if guess == abs(correct_answer): 
        print("Correct!\n")
    else: 
        print(f"Wrong! It was a {correct_answer} trade\n")
        incorrect_guess_counter += 1
        

