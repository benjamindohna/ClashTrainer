from flask import Blueprint, session, jsonify, request
import random
from Data.data_utils import load_card_data, load_card_data_sample

card_bp = Blueprint("card_bp", __name__)

CARDS = load_card_data_sample()

def init_game():
    session["pool"] = [card for card in CARDS.keys() if not card.startswith("_")]
    random.shuffle(session["pool"])
    session["incorrect_guess_counter"] = 0
    session["current_card"] = None


@card_bp.route("/")
def ajax_game_page():
    # Render HTML file only, JS will handle everything else
    from flask import render_template
    return render_template("elixir_quiz.html")


@card_bp.route("/api/next_card")
def next_card():
    if (
        "pool" not in session
        or not session["pool"]
        or any(card not in CARDS for card in session["pool"])
    ):
        init_game()


    pool = session["pool"]

    if not pool:
        return jsonify({"finished": True})

    # pick card
    card = random.choice(pool)
    session["current_card"] = card

    return jsonify({
        "finished": False,
        "card": card,
        "image": CARDS[card].get("image", None),  # optional
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

    correct_elixir = CARDS[current_card]["elixir"]

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
        "finished": len(pool) == 0
    })
