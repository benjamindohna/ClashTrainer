import pytest
from WebApp import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess.clear()  # ensure fresh session
        yield client


def test_next_card_initializes_game(client):
    # First request — should initialize pool and return a card
    response = client.get("/api/next_card")
    data = response.get_json()

    assert response.status_code == 200
    assert "finished" in data
    assert data["finished"] is False
    assert "card" in data


def test_submit_guess_correct(client):
    # Fetch a card
    first = client.get("/api/next_card").get_json()
    card = first["card"]

    # Guess correctly
    correct_elixir =  load_card_data_sample()[card]["elixir"]
    response = client.post("/api/submit_guess", json={"guess": correct_elixir})
    data = response.get_json()

    assert data["correct"] is True
    assert "finished" in data


def test_submit_guess_wrong(client):
    # Fetch card
    first = client.get("/api/next_card").get_json()
    card = first["card"]

    # Intentionally wrong guess
    response = client.post("/api/submit_guess", json={"guess": 99})
    data = response.get_json()

    assert data["correct"] is False
    assert "finished" in data
