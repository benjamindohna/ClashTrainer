# function attributes: two lists, first containing player cards played, second containing opponets cards played
# function then iterates over each of the lists isolatedly, fetching the elixir values of each card and computing 
# the sum of each list
# then it computes and outputs the difference of the two sums 

from Data.data_utils import load_card_data

# LOAD DATA

card_data = load_card_data()

# attributes for testing
cards_player = ["Knight", "Archers"]
cards_opponent = ["Mega Knight", "Balloon"]

def get_trade_balance(cards_player: list, cards_opponent: list) -> int:
    
    
    # Calculate the total elixir cost for the opponent's cards
    elixir_spent_opponent = sum(
        int(card_data[card]['elixir']) 
        for card in cards_opponent
    )

    # Calculate the total elixir cost for the player's cards
    elixir_spent_player = sum(
        int(card_data[card]['elixir']) 
        for card in cards_player
    )

    # Determine the trade balance
    trade_balance = elixir_spent_opponent - elixir_spent_player

    return trade_balance

def explain_trade_balance(cards_player: list, cards_opponent: list):
    """
    Prints a detailed explanation of the trade balance between player and opponent cards.

    Parameters:
        cards_player (list): List of player's card names.
        cards_opponent (list): List of opponent's card names.
        card_data (dict): Dictionary containing card info, must include 'elixir' for each card.
    """
    
    # Opponent cards explanation
    elixir_spent_opponent = sum(int(card_data[card]['elixir']) for card in cards_opponent)
    for card in cards_opponent:
        print(f"{card} costs {card_data[card]['elixir']} elixir")
    print(f"Total spent opponent: {elixir_spent_opponent} elixir\n")
    
    # Player cards explanation
    elixir_spent_player = sum(int(card_data[card]['elixir']) for card in cards_player)
    for card in cards_player:
        print(f"{card} costs {card_data[card]['elixir']} elixir")
    print(f"Total spent player: {elixir_spent_player} elixir\n")
    
    # Trade balance explanation
    trade_balance = elixir_spent_opponent - elixir_spent_player
    print(f"{elixir_spent_opponent} - {elixir_spent_player} = {trade_balance}")
    
    return trade_balance
    

def get_trade_balance_sign(trade_balance: int) -> str: 
    if trade_balance > 0:
        return "positive"
    if trade_balance < 0: 
        return "negative"
    return "neutral"

