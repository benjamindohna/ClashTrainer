import random
import re
import sys, tty, termios
from Data.data_utils import load_card_data
from Backend.trade_calculations import get_trade_balance, get_trade_balance_sign, explain_trade_balance

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
def get_key_n(n):
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        buffer = ""
        
        while len(buffer) < n:
            ch = sys.stdin.read(1)

            if ch == 'q':
                return 'q'
            buffer += ch

        return buffer
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def get_elixir_input(digit_length):
    while True:
        key = get_key_n(digit_length)

        if key == 'q':
            return 'q'
        
        pattern = r'^\d+$'
        if re.fullmatch(pattern, key):
                return int(key)
        
        print("Indicate digits or press 'q' to leave")


# LETS GO
while game_is_on:
    print()
    cards = [key for key in card_data.keys() if not key.startswith("_")]
    # print("cards:", cards)
    # print("correctly:", correctly_answered)
    # print(card_data.keys())

    attacking_cards = random.sample(cards, 1)
    defending_cards = random.sample(cards, 1)

    print(f"Opponent: {', '.join(attacking_cards)}")
    print(f"You: {', '.join(defending_cards)}")
    print("What is the trade balance (positive numbers for negative or positive)? (press 'q' to quit)")   # newline for readability

    correct_answer = get_trade_balance(defending_cards, attacking_cards)
    correct_answer_sign = get_trade_balance_sign(correct_answer)

    guess = get_elixir_input(len(str(correct_answer)))

    if guess == "q":
        print("Goodbye!")
        break

    print()
    print("----------------------")

    if guess == abs(correct_answer): 
        print(f"{guess} is correct!\n")
    else: 
        print(f"{guess} is wrong! It was a {correct_answer} elixir trade\n")
        incorrect_guess_counter += 1
    
    
    explain_trade_balance(defending_cards, attacking_cards)
        

