from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = "your-secret-key"

    from .routes.routes import card_bp
    app.register_blueprint(card_bp)

    from .routes.routes import trade_bp
    app.register_blueprint(trade_bp)

    app.config["TESTING"] = False 

    return app
