from flask import Blueprint, render_template
from Data.data_utils import load_card_data

card_bp = Blueprint("card_bp", __name__)

@card_bp.route("/", methods=["GET"])
def start():
    # We will temporarily render a simple text response instead of redirecting or loading data
    data = load_card_data()
    return list(data.keys())

@card_bp.route("/test", methods=["GET"])
def test_route():
    # A second simple route to confirm routing works
    return "This is a Test Page."