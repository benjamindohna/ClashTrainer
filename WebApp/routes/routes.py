from flask import Blueprint, session, jsonify, request, render_template
import random, requests, os
from dotenv import load_dotenv
from Data.data_utils import load_card_data, load_card_data_sample
from pathlib import Path
from google import genai

# -----------------------
# Blueprints
# -----------------------
card_bp = Blueprint("card_bp", __name__)
trade_bp = Blueprint("trade_bp", __name__)
ai_bp = Blueprint("ai_bp", __name__)

# -----------------------
# Card Data
# -----------------------
CARDS_ELIXIR_QUIZ = load_card_data_sample()  # sample
CARDS_TRADE_QUIZ = load_card_data()         # full

# -----------------------
# Home Route
# -----------------------
@card_bp.route("/")
def home():
    return render_template("home.html")

# -----------------------
# Elixir Quiz
# -----------------------

def init_game():
    session["pool"] = [card for card in CARDS_ELIXIR_QUIZ.keys() if not card.startswith("_")]
    random.shuffle(session["pool"])
    session["incorrect_guess_counter"] = 0
    session["current_card"] = None

@card_bp.route("/elixir_quiz")
def elixir_quiz_page():
    session.clear()
    init_game()
    return render_template("elixir_quiz.html")

@card_bp.route("/api/next_card")
def next_card():
    if "pool" not in session or not session["pool"]:
        init_game()

    pool = session["pool"]
    if not pool:
        return jsonify({"finished": True})

    card = random.choice(pool)
    session["current_card"] = card

    return jsonify({
        "finished": False,
        "card": card,
        "image": CARDS_ELIXIR_QUIZ[card].get("image", None),
    })


@card_bp.route("/api/submit_guess", methods=["POST"])
def submit_guess():
    data = request.get_json()
    guess = int(data["guess"])
    
    current_card = session.get("current_card")
    pool = session.get("pool", [])
    incorrect = session.get("incorrect_guess_counter", 0)

    if current_card is None:
        return jsonify({"error": "No active card"}), 400

    correct_elixir = CARDS_ELIXIR_QUIZ[current_card]["elixir"]

    if guess == correct_elixir:
        pool.remove(current_card)
        result = True
    else:
        incorrect += 1
        session["incorrect_guess_counter"] = incorrect
        result = False

    session["pool"] = pool
    session["current_card"] = None

    return jsonify({
        "correct": result,
        "correct_elixir": correct_elixir,
        "card": current_card,
        "user_guess": guess,
        "finished": len(pool) == 0,
        "incorrect_guesses": incorrect
    })


# -----------------------
# Trade Quiz
# -----------------------

def init_trade_game():
    session["trade_active"] = True
    session["opponent_card"] = None
    session["player_card"] = None

@trade_bp.route("/trade_quiz")
def trade_page():
    session.clear()
    init_trade_game()
    return render_template("trade_quiz.html")


@trade_bp.route("/api/trade/next")
def trade_next():
    if "trade_active" not in session:
        init_trade_game()

    cards = [c for c in CARDS_TRADE_QUIZ.keys() if not c.startswith("_")]
    opponent = random.choice(cards)
    player = random.choice(cards)
    while player == opponent:
        player = random.choice(cards)

    session["opponent_card"] = opponent
    session["player_card"] = player

    return jsonify({
        "opponent": opponent,
        "player": player,
        "image_opponent": CARDS_TRADE_QUIZ[opponent].get("image"),
        "image_player": CARDS_TRADE_QUIZ[player].get("image")
    })


@trade_bp.route("/api/trade/submit", methods=["POST"])
def trade_submit():
    data = request.get_json()
    guess = int(data["guess"])

    opp = session.get("opponent_card")
    ply = session.get("player_card")

    if opp is None or ply is None:
        return jsonify({"error": "No active trade"}), 400

    opp_cost = CARDS_TRADE_QUIZ[opp]["elixir"]
    ply_cost = CARDS_TRADE_QUIZ[ply]["elixir"]

    correct_value = opp_cost - ply_cost
    correct = (guess == correct_value)

    # reset state for next trade
    session["opponent_card"] = None
    session["player_card"] = None

    return jsonify({
        "correct": correct,
        "response_if_wrong": f"{guess} elixir is wrong! {opp_cost} elixir (the {opp}) - {ply_cost} elixir (the {ply}) = <b>{correct_value}</b> elixir.",
        "correct_value": correct_value
    })


client = genai.Client()

@ai_bp.route("/api/fart_ai")
def fart_ai():
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents="Tell me a fact that I GENUINELY would not want to know or be remined of. Like a fact that will ruin my day if I hear it. GENUINELY, not joking. Dont include any explanations or addresse to me, just the fact itself."
    )
    return jsonify({"fart_text": response.text})
